from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, ContentItem

class UserCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Testpass123',
            'full_name': 'Test User',
            'phone': '1234567890',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'pincode': '123456'
        }

    def test_create_valid_user(self):
        response = self.client.post(reverse('user-create'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email'] = ''
        response = self.client.post(reverse('user-create'), invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='Testpass123')
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'Testpass123'
        }
        self.invalid_payload = {
            'email': 'test@example.com',
            'password': 'Wrongpass'
        }

    def test_login_valid_user(self):
        response = self.client.post(reverse('login'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid_user(self):
        response = self.client.post(reverse('login'), self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ContentItemListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='Testpass123')
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'title': 'Test Title',
            'body': 'Test Body',
            'summary': 'Test Summary',
            'categories': 'Test,Sample'
        }

    def test_create_valid_content_item(self):
        response = self.client.post(reverse('contentitem-list-create'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_content_item(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['title'] = ''
        response = self.client.post(reverse('contentitem-list-create'), invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_content_items(self):
        response = self.client.get(reverse('contentitem-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ContentItemDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='Testpass123')
        self.client.force_authenticate(user=self.user)
        self.content_item = ContentItem.objects.create(
            author=self.user, 
            title='Test Title', 
            body='Test Body', 
            summary='Test Summary', 
            categories='Test,Sample'
        )

    def test_get_valid_content_item(self):
        response = self.client.get(reverse('contentitem-detail', kwargs={'pk': self.content_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_content_item(self):
        response = self.client.get(reverse('contentitem-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_content_item(self):
        updated_payload = {
            'title': 'Updated Title',
            'body': 'Updated Body',
            'summary': 'Updated Summary',
            'categories': 'Updated,Sample'
        }
        response = self.client.put(reverse('contentitem-detail', kwargs={'pk': self.content_item.pk}), updated_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_content_item(self):
        response = self.client.delete(reverse('contentitem-detail', kwargs={'pk': self.content_item.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ContentItemSearchViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='Testpass123')
        self.client.force_authenticate(user=self.user)
        ContentItem.objects.create(author=self.user, title='Test Title', body='Test Body', summary='Test Summary', categories='Test,Sample')
        ContentItem.objects.create(author=self.user, title='Another Test', body='Another Body', summary='Another Summary', categories='Another,Sample')

    def test_search_content_items(self):
        response = self.client.get(reverse('contentitem-search'), {'query': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_no_results(self):
        response = self.client.get(reverse('contentitem-search'), {'query': 'Nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

