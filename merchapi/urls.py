from django.urls import path

from . import views

urlpatterns = [
    # ex: /
    path('items/<int:item_id>', views.item_get, name='index'),
    path('items/<str:name>', views.item_search, name='index'),
    path('items', views.ItemList.as_view(), name='index'),
]
