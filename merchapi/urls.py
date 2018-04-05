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
    path('<api:version>/items/<int:item_id>/prices/', views.ItemPrices.as_view(), name='item prices'),
    path('<api:version>/items/<int:item_id>/tags/', views.ItemTags.as_view(), name='item tags'),
    path('<api:version>/items/<int:item_id>/favorite/', views.FavoriteSingle.as_view(), name='favorite'),
    path('<api:version>/prices/', views.PriceForItemList.as_view(), name='prices'),
    path('<api:version>/favorites/', views.FavoriteList.as_view(), name='favorites'),
    path('<api:version>/tags/', views.TagList.as_view(), name='tags'),
    path('<api:version>/tags/<str:tag_name>/', views.TagItems.as_view(), name='tag items'),

    path('<api:version>/auth/', include('rest_auth.urls'))
]
