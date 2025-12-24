from django.db import models
from booking.models import Booking

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.status}"
