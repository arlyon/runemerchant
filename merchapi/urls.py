from django.urls import path, include

from . import views

urlpatterns = [
    path('<str:version>/items/', views.ItemList.as_view(), name='items'),
    path('<str:version>/items/<int:item_id>/', views.ItemSingle.as_view(), name='item'),
    path('<str:version>/items/<int:item_id>/prices/', views.PriceLogsForItem.as_view(), name='item prices'),
    path('<str:version>/prices/', views.PriceLogList.as_view(), name='prices'),
]
