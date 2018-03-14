import math
from django.http import JsonResponse

from merchapi.models import Item
from merchapi.serializers import ItemSerializer
from rest_framework import generics


class ItemList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned items to match a given name.
        """
        queryset = Item.objects.all()
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__contains=search)
        return queryset


def item_get(request, item_id):
    if request.method == 'GET':
        items = Item.objects.filter(item_id=item_id).first()
        serializer = ItemSerializer(items)
        return JsonResponse(serializer.data, safe=False)


def item_search(request, name: str):
    if request.method == 'GET':
        items = Item.objects.filter(name__contains=name)
        serializer = ItemSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)