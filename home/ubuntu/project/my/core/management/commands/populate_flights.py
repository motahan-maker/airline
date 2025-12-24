from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import Flight, Airport

class Command(BaseCommand):
    help = 'Populate sample flights and airports'

    def handle(self, *args, **options):
        # Create airports
        airports_data = [
            {'iata_code': 'JFK', 'city': 'New York', 'country': 'USA'},
            {'iata_code': 'LAX', 'city': 'Los Angeles', 'country': 'USA'},
            {'iata_code': 'ORD', 'city': 'Chicago', 'country': 'USA'},
            {'iata_code': 'MIA', 'city': 'Miami', 'country': 'USA'},
            {'iata_code': 'SFO', 'city': 'San Francisco', 'country': 'USA'},
            {'iata_code': 'LHR', 'city': 'London', 'country': 'UK'},
            {'iata_code': 'CDG', 'city': 'Paris', 'country': 'France'},
            {'iata_code': 'FRA', 'city': 'Frankfurt', 'country': 'Germany'},
            {'iata_code': 'DXB', 'city': 'Dubai', 'country': 'UAE'},
            {'iata_code': 'NRT', 'city': 'Tokyo', 'country': 'Japan'},
        ]

        airports = {}
        for data in airports_data:
            airport, created = Airport.objects.get_or_create(
                iata_code=data['iata_code'],
                defaults=data
            )
            airports[data['iata_code']] = airport
            if created:
                self.stdout.write(f'Created airport: {airport.iata_code} - {airport.city}')

        # Create aircraft
        aircraft, created = Aircraft.objects.get_or_create(
            model_name='Boeing 737',
            defaults={'capacity': 150}
        )
        if created:
            self.stdout.write('Created aircraft: Boeing 737')

        # Create flights with future dates
        base_time = timezone.now() + timedelta(days=1)  # Start from tomorrow

        flights_data = [
            {'flight_number': 'AA101', 'departure': 'JFK', 'arrival': 'LAX', 'price': 299.99, 'duration_hours': 6},
            {'flight_number': 'UA202', 'departure': 'ORD', 'arrival': 'SFO', 'price': 249.99, 'duration_hours': 4},
            {'flight_number': 'DL303', 'departure': 'MIA', 'arrival': 'JFK', 'price': 199.99, 'duration_hours': 3},
            {'flight_number': 'BA404', 'departure': 'LHR', 'arrival': 'JFK', 'price': 599.99, 'duration_hours': 8},
            {'flight_number': 'AF505', 'departure': 'CDG', 'arrival': 'JFK', 'price': 549.99, 'duration_hours': 8},
            {'flight_number': 'LH606', 'departure': 'FRA', 'arrival': 'ORD', 'price': 699.99, 'duration_hours': 9},
            {'flight_number': 'EK707', 'departure': 'DXB', 'arrival': 'JFK', 'price': 899.99, 'duration_hours': 13},
            {'flight_number': 'JL808', 'departure': 'NRT', 'arrival': 'LAX', 'price': 799.99, 'duration_hours': 11},
        ]

        for i, data in enumerate(flights_data):
            departure_time = base_time + timedelta(days=i, hours=i*2)
            arrival_time = departure_time + timedelta(hours=data['duration_hours'])

            flight, created = Flight.objects.get_or_create(
                flight_number=data['flight_number'],
                departure_time=departure_time,
                defaults={
                    'departure_airport': airports[data['departure']],
                    'arrival_airport': airports[data['arrival']],
                    'aircraft': aircraft,
                    'arrival_time': arrival_time,
                    'price': data['price'],
                }
            )
            if created:
                self.stdout.write(f'Created flight: {flight.flight_number} from {flight.departure_airport.city} to {flight.arrival_airport.city}')

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data'))