from django.db.models import OuterRef, Subquery, Max

from merchapi.models import Item, PriceLog
from merchapi.serializers import ItemPriceLogSerializer, ItemSerializer, PriceLogItemSerializer, \
    PriceLogSerializer
from rest_framework import generics


class ItemList(generics.ListAPIView):
    """
    Gets all the items, with an optional search parameter
    to return all matching a given name.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        """
        Overrides the get queryset function to optionally
        restrict the returned items to match a given name.
        """
        queryset = Item.objects.all()
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__contains=search)
        return queryset


class ItemSingle(generics.RetrieveAPIView):
    """
    Gets a single item from the database.
    """

    queryset = Item.objects.all()
    lookup_field = 'item_id'
    serializer_class = ItemPriceLogSerializer


class PriceLogList(generics.ListAPIView):
    queryset = PriceLog.objects.filter(
        date=Subquery(
            PriceLog.objects
                .filter(item=OuterRef('item'))
                .values('item')
                .annotate(last_price=Max('date'))
                .values('last_price')[:1]
        )
    )
    serializer_class = PriceLogItemSerializer


class PriceLogsForItem(generics.ListAPIView):
    """
    Gets the prices for an item.
    """

    def get_queryset(self):
        return PriceLog.objects.filter(item__item_id = self.kwargs['item_id'])


    serializer_class = PriceLogSerializer
