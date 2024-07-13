from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from bicycles.models import Bicycle
from bicycles.serializers import BicycleSerializer


class AvailableBicyclesListAPIView(generics.ListAPIView):
    queryset = Bicycle.objects.filter(in_rent=False)
    serializer_class = BicycleSerializer
    permission_classes = [IsAuthenticated]
