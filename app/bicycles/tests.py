from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django.contrib.auth.models import Permission
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import APIClient

from bicycles.admin import BicycleAdmin

from bicycles.models import Bicycle
from bicycles.serializers import BicycleSerializer
from users.models import User

User = get_user_model()


class BicycleModelTestCase(TestCase):
    def setUp(self):
        self.bicycle = Bicycle.objects.create(
            model='bike', price=Decimal('599.99'), in_rent=False
        )

    def test_price_validator(self):
        # Test that price cannot be less than 0.01
        invalid_price_bicycle = Bicycle(
            model='bad bike', price=Decimal('0.005'), in_rent=False
        )
        with self.assertRaises(ValidationError):
            invalid_price_bicycle.full_clean()

    def test_bicycle_creation(self):
        # Test creation of a Bicycle object
        self.assertEqual(self.bicycle.model, 'bike')
        self.assertEqual(self.bicycle.price, Decimal('599.99'))
        self.assertFalse(self.bicycle.in_rent)

    def test_bicycle_in_rent(self):
        # Test setting bicycle in_rent status
        self.bicycle.in_rent = True
        self.bicycle.save()
        self.assertTrue(self.bicycle.in_rent)


class BicycleAdminTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.admin_user = User.objects.create_superuser(
            email='admin@example.com', password='testpass123'
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        permission = Permission.objects.get(codename='change_bicycle')
        self.admin_user.user_permissions.add(permission)

        # Log in the admin user
        self.client.force_login(self.admin_user)

        # Create Bicycle instances
        self.bicycle1 = Bicycle.objects.create(
            model='Mountain Bike', price='599.99', in_rent=False
        )
        self.bicycle2 = Bicycle.objects.create(
            model='Road Bike', price='799.99', in_rent=True
        )

    def test_mark_as_rented(self):
        # Test mark_as_rented action
        request = self.factory.post(
            '/admin/bicycles/bicycle/',
            {
                'action': 'mark_as_rented',
                '_selected_action': [self.bicycle1.id],
            },
        )
        request.user = self.admin_user
        queryset = Bicycle.objects.filter(id=self.bicycle1.id)
        admin_instance = BicycleAdmin(Bicycle, AdminSite())
        admin_instance.mark_as_rented(request, queryset)
        self.assertTrue(Bicycle.objects.get(id=self.bicycle1.id).in_rent)

    def test_mark_as_available(self):
        # Test mark_as_available action
        request = self.factory.post(
            '/admin/bicycles/bicycle/',
            {
                'action': 'mark_as_available',
                '_selected_action': [self.bicycle2.id],
            },
        )
        request.user = self.admin_user
        queryset = Bicycle.objects.filter(id=self.bicycle2.id)
        admin_instance = BicycleAdmin(Bicycle, AdminSite())
        admin_instance.mark_as_available(request, queryset)
        self.assertFalse(Bicycle.objects.get(id=self.bicycle2.id).in_rent)

    def test_search_fields(self):
        # Test search_fields functionality
        request = self.factory.get(
            '/admin/bicycles/bicycle/', {'q': 'Mountain'}
        )
        request.user = self.admin_user
        admin_instance = BicycleAdmin(Bicycle, AdminSite())
        queryset = admin_instance.get_search_results(
            request, admin_instance.get_queryset(request), 'Mountain'
        )
        self.assertEqual(queryset[0][0].model, self.bicycle1.model)

    def test_list_display(self):
        # Test list_display fields
        request = self.factory.get('/admin/bicycles/bicycle/')
        request.user = self.admin_user
        admin_instance = BicycleAdmin(Bicycle, AdminSite())
        result = admin_instance.changelist_view(request)
        self.assertIn(self.bicycle1.model, result.rendered_content)
        self.assertIn(str(self.bicycle1.id), result.rendered_content)
        self.assertIn(str(self.bicycle1.price), result.rendered_content)
        self.assertIn(
            'Yes' if self.bicycle1.in_rent else 'No', result.rendered_content
        )


class AvailableBicyclesListAPIViewTestCase(TestCase):
    def setUp(self):
        # Set up test data
        self.user = User.objects.create_superuser(
            email='admin@example.com', password='testpass123'
        )
        self.client = APIClient()
        self.bicycle1 = Bicycle.objects.create(
            model='Mountain Bike', price='599.99', in_rent=False
        )
        self.bicycle2 = Bicycle.objects.create(
            model='Road Bike', price='799.99', in_rent=True
        )
        self.url = reverse('available-bicycles-list')

    def test_available_bicycles_list(self):
        # Test available bicycles list view
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check that only available bicycles are returned in the response
        self.assertIn(self.bicycle1.model.encode(), response.content)
        self.assertNotIn(self.bicycle2.model.encode(), response.content)


class BicycleSerializerTestCase(TestCase):
    def setUp(self):
        self.bicycle_data = {
            'model': 'Mountain Bike',
            'price': '599.99',
            'in_rent': False,
        }

    def test_valid_serializer(self):
        serializer = BicycleSerializer(data=self.bicycle_data)
        self.assertTrue(serializer.is_valid())

    def test_serialization(self):
        bicycle = Bicycle.objects.create(**self.bicycle_data)
        serializer = BicycleSerializer(instance=bicycle)
        expected_fields = set(['id', 'model', 'price', 'in_rent'])
        self.assertEqual(set(serializer.data.keys()), expected_fields)
        self.assertEqual(serializer.data['model'], 'Mountain Bike')
        self.assertEqual(serializer.data['price'], '599.99')
        self.assertFalse(serializer.data['in_rent'])
