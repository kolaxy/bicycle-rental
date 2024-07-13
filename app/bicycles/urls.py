from django.urls import path
from bicycles.views import AvailableBicyclesListAPIView

urlpatterns = [
    path(
        'available/',
        AvailableBicyclesListAPIView.as_view(),
        name='available-bicycles-list',
    ),
]
