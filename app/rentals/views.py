from django.core.exceptions import ValidationError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Rental
from .permissions import IsRentalOwnerOrSuperuser
from .serializers import RentalSerializer


class RentalCreateAPIView(generics.CreateAPIView):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated, IsRentalOwnerOrSuperuser]

    def perform_create(self, serializer):
        bicycle_instance = serializer.validated_data.get('bicycle')

        if bicycle_instance.in_rent:
            raise ValidationError("This bicycle is already rented.")

        serializer.save(renter=self.request.user)
        bicycle_instance.in_rent = True
        bicycle_instance.save()


class RentalDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated, IsRentalOwnerOrSuperuser]
    http_method_names = ['get', 'patch']

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_returned:
            return Response({"error": "Cannot finish a returned rental."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        instance.return_bicycle()
        instance.save()

        return Response(serializer.data)


class RentalHistoryAPIView(generics.ListAPIView):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Rental.objects.filter(renter=user)
