from django.contrib import admin
from bicycles.models import Bicycle


@admin.register(Bicycle)
class BicycleAdmin(admin.ModelAdmin):
    list_display = ('model', 'id', 'price', 'in_rent')
    list_filter = ('in_rent',)
    search_fields = ('model',)
    list_editable = ('price',)
    list_per_page = 20
    actions = ['mark_as_rented', 'mark_as_available']

    def mark_as_rented(self, request, queryset):
        queryset.update(in_rent=True)

    mark_as_rented.short_description = "Mark selected as rented"

    def mark_as_available(self, request, queryset):
        queryset.update(in_rent=False)

    mark_as_available.short_description = "Mark selected as available"
