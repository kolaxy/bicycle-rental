from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal

from .admin import RentalAdmin
from .models import Rental
from bicycles.models import Bicycle
from users.models import User

from .serializers import RentalSerializer

User = get_user_model()


class RentalModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.bicycle = Bicycle.objects.create(model='Test Bicycle', price=Decimal('10.00'))

    def test_rental_creation(self):
        rental = Rental.objects.create(bicycle=self.bicycle, renter=self.user)
        self.assertTrue(isinstance(rental, Rental))
        self.assertEqual(rental.bicycle, self.bicycle)
        self.assertEqual(rental.renter, self.user)
        self.assertFalse(rental.is_returned)

    def test_rental_str_method(self):
        rental = Rental.objects.create(bicycle=self.bicycle, renter=self.user)
        self.assertEqual(str(rental), f"{self.bicycle} by {self.user.email}")

    def test_rental_clean_method_valid_dates(self):
        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(hours=1)
        rental = Rental(bicycle=self.bicycle, renter=self.user, start_time=start_time, end_time=end_time)
        rental.clean()  # должен пройти без ошибок

    def test_rental_clean_method_invalid_dates(self):
        start_time = timezone.now()
        end_time = start_time - timezone.timedelta(hours=1)
        rental = Rental(bicycle=self.bicycle, renter=self.user, start_time=start_time, end_time=end_time)
        with self.assertRaises(ValidationError):
            rental.clean()

    def test_rental_calculate_cost_method(self):
        start_time = timezone.now() - timezone.timedelta(hours=2)
        end_time = timezone.now()
        rental = Rental.objects.create(bicycle=self.bicycle, renter=self.user, start_time=start_time, end_time=end_time)
        rental.calculate_cost()
        self.assertGreater(rental.total_cost, 0)

    def test_rental_return_bicycle_method(self):
        rental = Rental.objects.create(bicycle=self.bicycle, renter=self.user)
        rental.return_bicycle()
        self.assertTrue(rental.is_returned)
        self.assertIsNotNone(rental.end_time)
        self.assertFalse(rental.bicycle.in_rent)

    def test_rental_permission_to_return_not_returned(self):
        rental = Rental.objects.create(bicycle=self.bicycle, renter=self.user, is_returned=False)
        rental.return_bicycle()
        self.assertTrue(rental.is_returned)

    def test_rental_permission_to_return_with_end_time(self):
        end_time = timezone.now() + timezone.timedelta(hours=1)
        rental = Rental.objects.create(bicycle=self.bicycle, renter=self.user, is_returned=False, end_time=end_time)
        rental.return_bicycle()
        self.assertTrue(rental.is_returned)


class RentalAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.rental_admin = RentalAdmin(Rental, self.site)

        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.bicycle = Bicycle.objects.create(model='Test Bicycle', price='10.00')
        self.rental = Rental.objects.create(bicycle=self.bicycle, renter=self.user, start_time=timezone.now())

    def test_list_display(self):
        expected_list_display = ('id', 'bicycle', 'renter', 'start_time', 'end_time', 'total_cost', 'is_returned')
        self.assertEqual(self.rental_admin.list_display, expected_list_display)

    def test_list_filter(self):
        expected_list_filter = ('bicycle', 'renter', 'start_time', 'end_time', 'is_returned')
        self.assertEqual(self.rental_admin.list_filter, expected_list_filter)

    def test_readonly_fields(self):
        expected_readonly_fields = ('total_cost',)
        self.assertEqual(self.rental_admin.readonly_fields, expected_readonly_fields)


class RentalSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com', password='password')
        self.bicycle = Bicycle.objects.create(model='Test Bicycle', price='10.00')

    def test_rental_serializer_update(self):
        rental = Rental.objects.create(bicycle=self.bicycle, renter=self.user, start_time=timezone.now())
        data = {
            'end_time': timezone.now(),
        }
        serializer = RentalSerializer(instance=rental, data=data, partial=True,
                                      context={'request': None})
        serializer.is_valid(raise_exception=True)
        updated_rental = serializer.save()

        self.assertEqual(updated_rental.end_time, data['end_time'])
