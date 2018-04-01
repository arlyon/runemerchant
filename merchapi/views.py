from typing import List, Iterable, Dict

from django.db import IntegrityError
from rest_framework import generics, mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from merchapi.models import Item, PriceLog, Favorite, OuterRef, Max, Subquery
from merchapi.serializers.item import ItemPriceLogSerializer, ItemPriceLogFavoriteSerializer, ItemFavoriteSerializer, \
    SingleItemPriceLogSerializer, SingleItemPriceLogFavoriteSerializer
from merchapi.serializers.base import ItemSerializer, PriceLogSerializer
from merchapi.serializers.pricelog import PriceLogItemSerializer


def item_generator(items: Iterable[Item], price_logs: Dict[int, PriceLog]):
    for item in items:
        item.price_log = price_logs[item.item_id] if item.item_id in price_logs else None
        yield item


def include_pricelogs(queryset) -> Iterable[Item]:
    """
    Takes a queryset of Items and merges in price data.
    :param queryset:
    :return:
    """
    latest_prices = PriceLog.objects.filter(
        date=Subquery(
            PriceLog.objects
                .filter(item=OuterRef('item'))
                .values('item')
                .annotate(last_price=Max('date'))
                .values('last_price')[:1]
        )
    )

    return item_generator(
        queryset.order_by('item_id'),
        {price_log.item_id: price_log for price_log in latest_prices}
    )


class ItemList(generics.ListAPIView):
    """
    Gets all the items, with an optional search parameter
    to return all matching a given name.

    ### **Query Strings**
    This endpoint supports a set of querystring parameters:

    - **name:** *?name=[query]* - Filters the items list to names matching the one given.
    - **members:** *?members=[true|false]* - Gets all items that are either members or non-members.
    - **tag:** *?tag=[first]&tag=[second]* - Filters the items list by one or more tags.
    - **prices:** *?prices* - Additionally gets the prices for each item.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    def get_queryset(self):
        """
        Overrides the get queryset function to inject the querystring.
        """

        queryset = Item.objects.all()

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        members = self.request.query_params.get('members')
        if members in ['true', '1', 'y']:
            queryset = queryset.filter(members=True)
        elif members in ['false', '0', 'n']:
            queryset = queryset.filter(members=False)

        tags: List[str] = self.request.query_params.getlist('tag', [])
        for tag in tags:
            queryset = queryset.filter(tag__name=tag.lower())

        if self.request.user.is_authenticated:
            queryset = queryset.with_favorited(self.request.user)

        # adds the price to the item
        if self.request.query_params.get('prices'):
            return include_pricelogs(queryset)

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.query_params.get('prices'):
                return ItemPriceLogFavoriteSerializer
            else:
                return ItemFavoriteSerializer
        else:
            if self.request.query_params.get('prices'):
                return ItemPriceLogSerializer
            else:
                return ItemSerializer


class ItemSingle(generics.RetrieveAPIView):
    """
    Gets a single item from the database.
    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    lookup_field = 'item_id'

    def get_queryset(self):
        return (
            Item.objects.with_favorited(self.request.user)
            if self.request.user.is_authenticated
            else Item.objects.all()
        )

    def get_serializer_class(self):
        return SingleItemPriceLogFavoriteSerializer if self.request.user.is_authenticated else SingleItemPriceLogSerializer


class PriceLogPerItemList(generics.ListAPIView):
    """
    Gets the most recent price logs for each item.
    """
    queryset = PriceLog.objects.most_recent_for_each_item()
    serializer_class = PriceLogItemSerializer


class PriceLogsForItem(generics.ListAPIView):
    """
    Gets the prices for an item.
    todo add querystring for granularity and range
    """

    def get_queryset(self):
        return PriceLog.objects.filter(item__item_id=self.kwargs['item_id'])

    serializer_class = PriceLogSerializer


class UserFavoriteList(generics.ListAPIView):
    """
    Gets the favorited items for a user.
    """

    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.merchant.favorites.all()

    serializer_class = ItemSerializer


class FavoriteCreateDestroy(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    Manages the creation and deletion of favorites.
    """

    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    lookup_field = 'item_id'
    serializer_class = Serializer

    def get_queryset(self):
        return self.request.user.merchant.favorite_set.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, version, item_id):
        """
        Tries to add a favorited relation for a given item id
        and returns a 404 if the item does not exist.
        :param request: The request object.
        :param version: The api version.
        :param item_id: The item id.
        :return: 409 if the relation exists already
                 404 if the item does not exist
                 201 if the create was successful
        """
        try:
            Favorite.objects.create(user=request.user.merchant, item_id=item_id)
        except IntegrityError as err:
            if 'unique' in err.args[0].lower():
                return Response({"detail": "Already exists."}, 409)
            elif 'foreign key' in err.args[0].lower():
                return Response({"detail": "Not found."}, 404)
        else:
            return Response(None, 201)

    def get(self, request, version, item_id):
        """
        Gets the status of the favorited for a given item id.
        :param request: The request object.
        :param version: The api version.
        :param item_id: The item id.
        :return: True / False if the item is or isn't favorited
                 404 if the item does not exist.
        """
        try:
            return Response(True) if Item.objects.with_favorited(request.user).get(
                item_id=item_id).favorited else Response(False)
        except Item.DoesNotExist:
            return Response({"detail": "Not found."}, 404)
