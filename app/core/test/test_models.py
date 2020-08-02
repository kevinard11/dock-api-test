from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_email_with_email_successfull(self):
        """Testing creating new user with email"""
        email = 'aaa@gmail.com'
        password = 'testpass123'
        user= get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normalized"""
        email = "asaa@GMAIL.coms"
        user = get_user_model().objects.create_user(email,'testpass123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        """Test creating a new user"""
        user = get_user_model().objects.create_superuser(
            'aaa@gmail.com', 'testspass123'
            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
