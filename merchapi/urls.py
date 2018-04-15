from django.urls import path, include, register_converter

from . import views


class ApiConverter:
    """
    Interprets the api version and filters validity.

    Currently there is only version 1.
    """
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
    path('<api:version>/items/<int:item_id>/favorite/', views.ItemFavorite.as_view(), name='item favorite'),
    path('<api:version>/items/<int:item_id>/flips/', views.ItemFlips.as_view(), name='item flips'),

    path('<api:version>/prices/', views.PriceForItemList.as_view(), name='prices'),

    path('<api:version>/favorites/', views.FavoriteList.as_view(), name='favorites'),

    path('<api:version>/tags/', views.TagList.as_view(), name='tags'),
    path('<api:version>/tags/<str:tag_name>/', views.TagItems.as_view(), name='tag items'),

    path('<api:version>/flips/', views.FlipList.as_view(), name='flips'),
    path('<api:version>/flips/<int:id>', views.FlipSingle.as_view(), name='flip'),

    path('<api:version>/auth/', include('rest_auth.urls'))
]
