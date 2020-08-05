from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
# ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the users api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with payload is successful"""

        payload = {
            'email': 'aaa@gmail.com',
            'password': 'testpass123',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists is failed"""
        payload = {
            'email': 'aaa@gmail.com',
            'password': 'testpass123'
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):
        """Test the password must be more than 5 characters"""
        payload = {
            'email': 'aaa@gmail.com',
            'password': 'pw',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email= payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for the user"""
        payload = {
            'email':'aaa@gmail.com',
            'password':'testpass123'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        print(res.data)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email = 'aaa@gmail.com', password='testpass123')
        payload={
            'email':'aaa@gmail.com',
            'password':'wreng'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exists"""
        payload={
            'email':'aaa@gmail.com',
            'password':'wreng'
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """Test that email and password are required"""
        payload={
            'email':'aaa@gmail.com',
            'password':''
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_retrieve_user_unauthorized(self):
    #     """Test that authentication is required for users"""
    #     res = self.client.get(ME_URL)
    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# class PrivateUserApiTests(self):
#     """Test API requests that require authentication"""
#     def setUp(self):
#         self.user = create_user(
#         email = 'aaa@gmail.com',
#         password = 'testpass123',
#         name = 'Test'
#         )
#         self.client = APIClient()
#         self.client.force_authenticate(user =self.user)
#
#     def test_retrieve_profile_success(self):
#         """Test retrieving profile for logged in use"""
#         res = self.client.get(ME_URL)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {
#             'email': self.user.email,
#             'name': self.user.name
#         })
#
#     def test_post_me_not_allowed(self):
#         """Test taht POST is not allowed on the me URL"""
#         res = self.client.post(ME_URL,{})
#         self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_update_user_profile(self):
#         """Test updating the user profile for authenticated user"""
#         payload = {'name':'New Test', 'password':'newtestpass123'}
#         res = self.client.patch(ME_URL, payload)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.name, payload['name'])
#         self.assertTrue(self.user.check_password, payload['password'])
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
