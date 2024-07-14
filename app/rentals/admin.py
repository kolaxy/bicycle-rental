from django.contrib import admin
from .models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('id', 'bicycle', 'renter', 'start_time', 'end_time', 'total_cost', 'is_returned')
    list_filter = ('bicycle', 'renter', 'start_time', 'end_time', 'is_returned')
    search_fields = ('bicycle__model', 'renter__username')
    readonly_fields = ('total_cost',)
