from typing import List

from django.db import IntegrityError
from django.db.models import OuterRef, Subquery, Max
from rest_framework import generics, mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from merchapi.models import Item, PriceLog, Favorite
from merchapi.serializers import ItemPriceLogSerializer, ItemSerializer, PriceLogItemSerializer, \
    PriceLogSerializer


class ItemList(generics.ListAPIView):
    """
    Gets all the items, with an optional search parameter
    to return all matching a given name.

    ### **Query Strings**
    This endpoint supports a set of querystring parameters:

    - **name:** *?name=[query]* - Filters the items list to names matching the one given.
    - **members:** *?members=[true|false]* - Gets all items that are either members or non-members.
    - **tag:** *?tag=[first]&tag=[second]* - Filters the items list by one or more tags.
    """

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

        return queryset

    def get_serializer_class(self):
        return ItemSerializer


class ItemSingle(generics.RetrieveAPIView):
    """
    Gets a single item from the database.
    """

    queryset = Item.objects.all()
    lookup_field = 'item_id'

    def get_serializer_class(self):
        return ItemPriceLogSerializer


class ItemPriceLogList(generics.ListAPIView):
    """
    Gets the most recent price logs for each item.
    """

    def get_queryset(self):
        return PriceLog.objects.filter(
            date=Subquery(
                PriceLog.objects
                    .filter(item=OuterRef('item'))
                    .values('item')
                    .annotate(last_price=Max('date'))
                    .values('last_price')[:1]
            )
        )

    def get_serializer_class(self):
        return PriceLogItemSerializer


class PriceLogsForItem(generics.ListAPIView):
    """
    Gets the prices for an item.
    todo add querystring for granularity and range
    """

    def get_queryset(self):
        return PriceLog.objects.filter(item__item_id=self.kwargs['item_id'])

    def get_serializer_class(self):
        return PriceLogSerializer


class UserFavoriteList(generics.ListAPIView):
    """
    Gets the favorite items for a user.
    """

    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.merchant.favorites.all()

    def get_serializer_class(self):
        return ItemSerializer


class FavoriteCreateDestroy(generics.GenericAPIView, mixins.DestroyModelMixin):
    """
    Creates and deletes favorites for a given item id and authentication.
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
        try:
            Favorite.objects.create(user=request.user.merchant, item_id=item_id)
        except IntegrityError as ignore:
            pass  # unique constraint failed, already added
        finally:
            return Response(None, 201)
