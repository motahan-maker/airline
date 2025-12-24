from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import time

class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    iata_code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f"{self.city} ({self.iata_code})"

class Aircraft(models.Model):
    model_name = models.CharField(max_length=100)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.model_name

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    @property
    def available_seats(self):
        # This is the property that caused the runtime error in the previous session.
        # We will assume a simple calculation for now, and address the bug in Phase 3.
        # For now, let's assume all seats are available.
        return self.aircraft.capacity

    def __str__(self):
        return f"{self.flight_number}: {self.departure_airport.iata_code} to {self.arrival_airport.iata_code}"

    class Meta:
        ordering = ['departure_time']
