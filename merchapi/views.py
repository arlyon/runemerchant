from django.db.models import OuterRef, Subquery, Max

from merchapi.models import Item, PriceLog
from merchapi.serializers import ItemPriceLogSerializer, ItemSerializer, PriceLogItemSerializer, \
    PriceLogSerializer
from rest_framework import generics


class ItemList(generics.ListAPIView):
    """
    Gets all the items, with an optional search parameter
    to return all matching a given name.

    ### **Query Strings**
    This endpoint supports a set of querystring parameters:

    - **name:** *?name=[first]&name=[second]* - Gets all the items with name matching the list of parameters.
    - **members:** *?members=[true|false]* - Gets all items that are either members or non-members.
    """

    def get_queryset(self):
        """
        Overrides the get queryset function to inject the querystring.
        """
        queryset = Item.objects.all()

        name = self.request.query_params.getlist('name', None) or []
        for string in name:
            queryset = queryset.filter(name__contains=string)

        members = self.request.query_params.get('members', None) or []
        if members in ['true', '1', 'y']:
            queryset = queryset.filter(members=True)
        elif members in ['false', '0', 'n']:
            queryset = queryset.filter(members=False)

        return queryset

    def get_serializer_class(self):
        return ItemSerializer if self.request.version == 1 else None


class ItemSingle(generics.RetrieveAPIView):
    """
    Gets a single item from the database.
    """

    queryset = Item.objects.all()
    lookup_field = 'item_id'

    def get_serializer_class(self):
        return ItemPriceLogSerializer if self.request.version == 1 else None


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
        return PriceLogItemSerializer if self.request.version == 1 else None


class PriceLogsForItem(generics.ListAPIView):
    """
    Gets the prices for an item.
    todo add querystring for granularity and range
    """

    def get_queryset(self):
        return PriceLog.objects.filter(item__item_id=self.kwargs['item_id'])

    def get_serializer_class(self):
        return PriceLogSerializer if self.request.version == 1 else None
