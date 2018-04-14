from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

from merchapi.models import Item, User, Favorite


class ItemTest(APITestCase):
    """
    Regression tests to make sure the item API conforms to expectations.
    """

    fixtures = ['items.json']

    def test_get_all_items(self):
        """
        Tests the endpoint to get all items. /v1/items/
        """
        url = reverse('items', kwargs={'version': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(Item.objects.count(), len(data))

    def test_get_item(self):
        """
        Tests the endpoint to get an item. /v1/items/2/
        """
        invalid_id = 1

        url = reverse('item', kwargs={'version': 1, 'item_id': invalid_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        item_id = 2

        url = reverse('item', kwargs={'version': 1, 'item_id': item_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["item_id"], item_id)

    def test_get_item_prices(self):
        """
        Tests the endpoint to get all prices for an item. /v1/items/2/prices/
        """
        invalid_id = 1

        url = reverse('item prices', kwargs={'version': 1, 'item_id': invalid_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        item_id = 2

        url = reverse('item prices', kwargs={'version': 1, 'item_id': item_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_item_tags(self):
        """
        Tests the endpoint to get all tags for an item. /v1/items/2/tags/
        """
        invalid_id = 1

        url = reverse('item tags', kwargs={'version': 1, 'item_id': invalid_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        item_id = 2

        url = reverse('item prices', kwargs={'version': 1, 'item_id': item_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)


class PricesTest(APITestCase):
    """
    Regression tests to make sure the prices API conforms to expectations.
    """
    def test_prices(self):
        url = reverse('prices', kwargs={"version": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)


class FavoriteTest(APITransactionTestCase):
    """
    Regression tests to make sure the favorite API conforms to expectations.
    """

    def setUp(self):
        User.objects.create_user(
            username="test",
            password="test"
        )

        auth_url = "/api/v1/auth/login/"
        response = self.client.post(auth_url, {
            "username": "test",
            "password": "test"
        }, 'json')

        self.client.logout()  # testing token only

        token = response.json()["key"]
        self.auth = f"Token {token}"

    fixtures = ['items.json']

    def test_list_favorites(self):
        """
        Tests that:
         - you need an auth token to see favorites
         - the favorites is a list
         - the list returns a 200 OK
        """
        url = reverse('favorites', kwargs={'version': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        favorites = response.json()
        self.assertIsInstance(favorites, list)

    def test_view_favorite(self):
        """
        Tests that:
         - you need an auth token to see
         - invalid item ids are 404'd
         - correct ids and tokens are given the favorite status
        """
        missing_url = reverse('favorite', kwargs={'version': 1, 'item_id': 1})
        response = self.client.get(missing_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(missing_url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('favorite', kwargs={'version': 1, 'item_id': 2})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        value = response.json()
        self.assertEqual(value, False)

    def test_create_favorite(self):
        """
        Tests that:
         - no auth is a 403
         - invalid item is a 404
         - newly created is a 201
         - creating again is a 409
        """
        missing_url = reverse('favorite', kwargs={'version': 1, 'item_id': 1})
        response = self.client.post(missing_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(missing_url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('favorite', kwargs={'version': 1, 'item_id': 2})
        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.count(), 1)

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(Favorite.objects.count(), 1)

    def test_delete_favorite(self):
        """
        Tests that:
         - no auth is a 403
         - invalid item is a 404
         - delete on a false favorite is a 404
         - delete of a true favorite is a 204
        """
        missing_url = reverse('favorite', kwargs={'version': 1, 'item_id': 1})
        response = self.client.delete(missing_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(missing_url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('favorite', kwargs={'version': 1, 'item_id': 2})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Favorite.objects.count(), 0)

        response = self.client.post(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Favorite.objects.count(), 1)

        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Favorite.objects.count(), 0)


class TagsTest(APITestCase):
    """
    Regression tests to make sure the tags API conforms to expectations.
    """
    fixtures = ['items.json', 'tags.json', 'taggeditems.json', 'merchants.json']

    def test_tags_list(self):
        url = reverse('tags', kwargs={"version": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_tag_items(self):
        url = reverse('tags', kwargs={"version": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag = response.json()[0]

        tag_url = reverse('tag items', kwargs={"version": 1, "tag_name": tag})
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.json()
        self.assertIsInstance(items, list)
