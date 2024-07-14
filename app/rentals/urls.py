from django.urls import path
from .views import RentalCreateAPIView, RentalDetailAPIView, RentalHistoryAPIView

urlpatterns = [

    path(
        '<int:pk>/',
        RentalDetailAPIView.as_view(),
        name='rental-detail'
    ),
    path(
        'history/',
        RentalHistoryAPIView.as_view(),
        name='rental-history'
    ),
    path(
        'create/',
        RentalCreateAPIView.as_view(),
        name='rental-create'
    ),
]
