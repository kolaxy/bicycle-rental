from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .serializers import UserSerializer


User = get_user_model()


class AdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com', password='testpass123'
        )
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(
            email='test@example.com', password='testpass123', name='Test User'
        )

    def test_user_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:users_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:users_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:users_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_fieldsets(self):
        """Test the fieldsets are correctly displayed onthe user change page"""
        url = reverse('admin:users_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Check that fieldsets are present in the form
        self.assertContains(res, 'User additional data')
        self.assertContains(res, 'Authorization')
        self.assertContains(res, 'Authentication')

    def test_add_fieldsets(self):
        """Test the fieldsets are correctly displayed on the user add page"""
        url = reverse('admin:users_user_add')
        res = self.client.get(url)

        # Check that add_fieldsets are present in the form
        self.assertContains(res, 'Authorization')
        self.assertContains(res, 'Authenticated')


class UserManagerTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EXAMPLE.COM'
        user = User.objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'test123')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        email = 'superuser@example.com'
        password = 'testpass123'
        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_superuser_must_have_is_staff(self):
        """Test creating superuser with is_staff=False raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='superuser@example.com',
                password='test123',
                is_staff=False,
            )

    def test_superuser_must_have_is_superuser(self):
        """Test creating superuser with is_superuser=False raises error"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='superuser@example.com',
                password='test123',
                is_superuser=False,
            )

    def test_validate_password(self):
        """Test that password validation hashes the password correctly"""
        manager = User.objects
        password = 'testpass123'
        hashed_password = manager.validate_password(password)

        self.assertNotEqual(password, hashed_password)
        self.assertTrue(User.objects.make_random_password, hashed_password)


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        """Test user registration endpoint"""
        url = reverse('user-registration')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_user_registration_missing_email(self):
        """Test user registration with missing email"""
        url = reverse('user-registration')
        data = {'password': 'testpass123', 'name': 'Test User'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_me_view_authenticated(self):
        """Test 'user-me' endpoint when user is authenticated"""
        user = User.objects.create_user(
            email='test@example.com', password='testpass123', name='Test User'
        )
        self.client.force_authenticate(user=user)

        url = reverse('user-me')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_me_view_unauthenticated(self):
        """Test 'user-me' endpoint when user is not authenticated"""
        url = reverse('user-me')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('email', response.data)


class UserSerializerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating a new user"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User',
        }
        serializer = UserSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_update_user(self):
        """Test updating an existing user"""
        user = User.objects.create_user(
            email='test@example.com', password='testpass123', name='Test User'
        )
        new_email = 'new_email@example.com'
        new_name = 'Updated Name'

        payload = {
            'email': new_email,
            'name': new_name,
        }
        serializer = UserSerializer(instance=user, data=payload, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(updated_user.email, new_email)
        self.assertEqual(updated_user.name, new_name)
        self.assertEqual(updated_user.password, user.password)

    def test_serializer_invalid_password(self):
        """Test serializer with invalid password"""
        payload = {
            'email': 'test@example.com',
            'password': '',
            'name': 'Test User',
        }
        serializer = UserSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_serializer_empty_data(self):
        """Test serializer with empty data"""
        serializer = UserSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('password', serializer.errors)
        self.assertIn('name', serializer.errors)
