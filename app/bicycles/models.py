from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from common.models import BaseModel


class Bicycle(BaseModel):
    model = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    in_rent = models.BooleanField(default=False)
