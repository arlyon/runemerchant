from typing import List

from django.db import IntegrityError
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from merchapi.models import Item, Price, Favorite, Tag
from merchapi.serializers.item import ItemPriceSerializer, ItemPriceFavoriteSerializer, ItemFavoriteSerializer, \
    SingleItemPriceSerializer, SingleItemPriceFavoriteSerializer
from merchapi.serializers.base import ItemSerializer, PriceLogSerializer, TagSerializer
from merchapi.serializers.price import PriceItemSerializer


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
            queryset = queryset.with_favorited(self.request.user.merchant)

        # adds the price to the item
        if self.request.query_params.get('prices'):
            return queryset.with_prices()

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            if self.request.query_params.get('prices'):
                return ItemPriceFavoriteSerializer
            else:
                return ItemFavoriteSerializer
        else:
            if self.request.query_params.get('prices'):
                return ItemPriceSerializer
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
            Item.objects.with_favorited(self.request.user.merchant)
            if self.request.user.is_authenticated
            else Item.objects.all()
        )

    def get_serializer_class(self):
        return SingleItemPriceFavoriteSerializer if self.request.user.is_authenticated else SingleItemPriceSerializer


class ItemPrices(generics.ListAPIView):
    """
    Gets the prices for an item.
    todo add querystring for granularity and range
    """

    def get_queryset(self):
        try:
            return Item.objects.get(item_id=self.kwargs['item_id']).price_set
        except Item.DoesNotExist:
            raise Http404("Item does not exist.")

    serializer_class = PriceLogSerializer


class ItemTags(generics.ListAPIView):
    """

    """
    serializer_class = TagSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    lookup_field = 'item_id'

    def get_queryset(self):
        try:
            tags = Item.objects.get(item_id=self.kwargs[self.lookup_field]).tags
        except Item.DoesNotExist as err:
            raise Http404("Item does not exist.")
        else:
            unowned_tags = tags.filter(taggeditem__user=None)

            if self.request.user.is_authenticated:
                owned_tags = tags.filter(taggeditem__user=self.request.user.merchant)
                tags = (unowned_tags | owned_tags).distinct()
            else:
                tags = unowned_tags

            return tags


class PriceForItemList(generics.ListAPIView):
    """
    Gets the most recent price logs for each item.
    """
    queryset = Price.objects.most_recent_for_each_item()
    serializer_class = PriceItemSerializer


class FavoriteList(generics.ListAPIView):
    """
    Gets the favorited items for a user.
    """

    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.merchant.favorites.all()

    serializer_class = ItemSerializer


class FavoriteSingle(generics.GenericAPIView, mixins.DestroyModelMixin):
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
         # todo find out why foreign key is ignored
        """
        try:
            Favorite.objects.create(merchant=request.user.merchant, item=Item.objects.get(item_id=item_id))
        except IntegrityError as err:
            if 'unique' in err.args[0].lower():
                return Response({"detail": "Already exists."}, status.HTTP_409_CONFLICT)
            elif 'foreign key' in err.args[0].lower():
                return Response({"detail": "Item does not exist."}, status.HTTP_404_NOT_FOUND)
        except Item.DoesNotExist:
            raise Http404("Item does not exist.")
        else:
            return Response(None, status.HTTP_201_CREATED)

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
            return Response(True) if Item.objects.with_favorited(request.user.merchant).get(
                item_id=item_id).favorited else Response(False)
        except Item.DoesNotExist:
            raise Http404("Item does not exist.")


class TagList(generics.ListAPIView):
    """

    """
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagItems(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    serializer_class = ItemSerializer

    lookup_field = 'tag_name'

    def get_queryset(self):

        items = Item.objects.all()
        unowned_tagged = items.filter(taggeditem__user=None)

        if self.request.user.is_authenticated:
            owned_tagged = items.filter(tags__taggeditem__user=self.request.user.merchant)
            items = (unowned_tagged | owned_tagged).distinct()
        else:
            items = unowned_tagged

        return items.filter(tags__name=self.kwargs[self.lookup_field])
