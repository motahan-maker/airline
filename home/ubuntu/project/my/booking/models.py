from django.db import models
from django.conf import settings
from core.models import Flight

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    number_of_passengers = models.IntegerField(default=1)

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} for {self.flight.flight_number}"
