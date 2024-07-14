from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Rental(models.Model):
    bicycle = models.ForeignKey("bicycles.Bicycle", related_name='rentals', on_delete=models.CASCADE)
    renter = models.ForeignKey("users.User", related_name='rentals', on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_returned = models.BooleanField(default=False)

    def calculate_cost(self):
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
            cost_per_second = float(self.bicycle.price) / 3600
            self.total_cost = Decimal(round(duration * cost_per_second, 2))

    def save(self, *args, **kwargs):
        if self.end_time:
            self.calculate_cost()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError(_('End time must be greater than start time.'))

    def return_bicycle(self):
        if not self.is_returned:
            self.end_time = timezone.now()
            self.is_returned = True
            self.bicycle.in_rent = False
            self.save()
            self.bicycle.save()

    def __str__(self):
        return f"{self.bicycle} by {self.renter}"