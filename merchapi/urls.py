from django.urls import path, include, register_converter

from . import views


class ApiConverter:
    regex = 'v[1]'

    @staticmethod
    def to_python(value):
        return int(value[1:])

    @staticmethod
    def to_url(value):
        return f"v{value}"


register_converter(ApiConverter, 'api')

urlpatterns = [
    path('<api:version>/items/', views.ItemList.as_view(), name='items'),
    path('<api:version>/items/<int:item_id>/', views.ItemSingle.as_view(), name='item'),
    path('<api:version>/items/<int:item_id>/prices/', views.PriceLogsForItem.as_view(), name='item prices'),
    path('<api:version>/items/<int:item_id>/favorite/', views.FavoriteCreateDestroy.as_view(), name='favorite'),
    path('<api:version>/prices/', views.ItemPriceLogList.as_view(), name='prices'),
    path('<api:version>/favorite/', views.UserFavoriteList.as_view(), name='favorite'),
    path('<api:version>/auth/', include('rest_auth.urls'))
]
