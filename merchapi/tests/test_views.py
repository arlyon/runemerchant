from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

from merchapi.models import Item, User, Favorite


class ItemTest(APITestCase):
    """
    Regression tests to make sure the item API conforms to expectations.
    """

    fixtures = ['items.json']

    def test_get_items_list(self):
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

    def test_get_item_price_list(self):
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


class PricesTest(APITestCase):
    """
    Regression tests to make sure the prices API conforms to expectations.
    """
    def test_get_prices(self):
        url = reverse('prices', kwargs={"version": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)


class FavoriteTest(APITransactionTestCase):
    """
    Regression tests to make sure the favorite API conforms to expectations.
    """
    fixtures = ['items.json']

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

    def test_get_favorites_list(self):
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

    def test_get_favorite(self):
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


class TagsTest(APITransactionTestCase):
    """
    Regression tests to make sure the tags API conforms to expectations.
    """
    fixtures = ['items.json', 'tags.json', 'taggeditems.json', 'merchants.json']

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

    def test_get_tags_list(self):
        """
        Tests the tags list endpoint. /v1/tags/
        """
        url = reverse('tags', kwargs={"version": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_tag_items(self):
        """
        Tests the item tags endpoint. /v1/tags/weapon/
        """
        url = reverse('tags', kwargs={"version": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag = response.json()[0]

        tag_url = reverse('tag items', kwargs={"version": 1, "tag_name": tag})
        response = self.client.get(tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        items = response.json()
        self.assertIsInstance(items, list)

    def test_get_item_tags(self):
        """
        Tests the endpoint to get all tags for an item. /v1/items/2/tags/
        """
        invalid_id = 1
        item_id = 2

        # 404 for invalid id
        url = reverse('item tags', kwargs={'version': 1, 'item_id': invalid_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # 200 for valid id
        url = reverse('item tags', kwargs={'version': 1, 'item_id': item_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_add_tag(self):
        """
        Tests adding a tag to an item. /v1/items/2/tags/
        """
        invalid_id = 1
        item_id = 2
        tag = {"name": "weapon"}

        # forbidden without auth
        url = reverse('item tags', kwargs={'version': 1, 'item_id': invalid_id})
        response = self.client.post(url, tag)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 404 for invalid item id
        response = self.client.post(url, tag, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # adding should give a 201
        url = reverse('item tags', kwargs={'version': 1, 'item_id': item_id})
        response = self.client.post(url, tag, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # adding again should raise a 409
        response = self.client.post(url, tag, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # tag should not be there for other users
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertNotIn("weapon", data)

        # tag should be there for the owner
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertIn("weapon", data)

    def test_remove_tag(self):
        """
        Tests removing a tag from an item. /v1/items/2/tags/
        """
        invalid_id = 1
        item_id = 2

        # 403 without auth
        url = reverse('item tags', kwargs={'version': 1, 'item_id': invalid_id})
        response = self.client.delete(url, {"tags": ["weapon", "fuck"]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 404 with invalid id
        url = reverse('item tags', kwargs={'version': 1, 'item_id': invalid_id})
        response = self.client.delete(url, {"tags": ["weapon", "lol"]}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # create a tag
        url = reverse('item tags', kwargs={'version': 1, 'item_id': item_id})
        response = self.client.post(url, {"name": "weapon"}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # delete the tag
        response = self.client.delete(url, {"tags": ["weapon"]}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # tag should not be there
        url = reverse('item tags', kwargs={'version': 1, 'item_id': item_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)
        data = response.json()
        self.assertNotIn("weapon", data)
