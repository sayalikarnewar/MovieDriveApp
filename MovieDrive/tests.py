from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Collection, Movie, CollectionMovie

class UserRegistrationTest(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)

class MovieListViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(RefreshToken.for_user(self.user).access_token))

    def test_movie_list(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)

class CollectionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(RefreshToken.for_user(self.user).access_token))

    def test_create_collection(self):
        url = reverse('collection-list-create')
        data = {
            "title": "My Collection",
            "description": "A collection of my favorite movies",
            "movies": [
                {
                    "title": "Movie 1",
                    "description": "A great movie",
                    "genres": "Action",
                    "uuid": "123e4567-e89b-12d3-a456-426614174000"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('uuid', response.data)

    def test_list_collections(self):
        # Create a collection first
        collection = Collection.objects.create(
            title="My Collection",
            description="A collection of my favorite movies",
            user=self.user
        )
        Movie.objects.create(
            title="Movie 1",
            description="A great movie",
            genres="Action",
            uuid="123e4567-e89b-12d3-a456-426614174000"
        )
        url = reverse('collection-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_collection(self):
        collection = Collection.objects.create(
            title="My Collection",
            description="A collection of my favorite movies",
            user=self.user
        )
        url = reverse('collection-detail', args=[collection.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_collection(self):
        collection = Collection.objects.create(
            title="My Collection",
            description="A collection of my favorite movies",
            user=self.user
        )
        url = reverse('collection-detail', args=[collection.uuid])
        data = {
            "title": "Updated Collection",
            "description": "An updated collection of my favorite movies"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Collection')
