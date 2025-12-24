from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models import Flight
from booking.models import Booking
from payment.models import Payment
from .serializers import FlightSerializer, BookingSerializer, PaymentSerializer

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    # Only authenticated users can view flights, but we will keep it open for now
    # to allow searching. We will enforce stricter permissions on sensitive endpoints.
    # permission_classes = [IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter bookings to only show the current user's bookings
        return self.queryset.filter(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter payments to only show payments for the current user's bookings
        return self.queryset.filter(booking__user=self.request.user)
