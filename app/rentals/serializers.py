from rest_framework import serializers
from .models import Rental


class RentalSerializer(serializers.ModelSerializer):
    renter = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Rental
        fields = ('bicycle', 'renter', 'start_time', 'end_time', 'total_cost')
