from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from .models import Flight, Airport

def home_view(request):
    return render(request, 'core/home.html')

def search_flights_view(request):
    flights = []
    if request.method == 'GET' and 'departure' in request.GET:
        departure_iata = request.GET.get('departure')
        arrival_iata = request.GET.get('arrival')
        date_str = request.GET.get('date')

        try:
            departure_airport = Airport.objects.get(iata_code=departure_iata)
            arrival_airport = Airport.objects.get(iata_code=arrival_iata)
            # Use datetime.strptime to parse the date string
            search_date = datetime.strptime(date_str, '%Y-%m-%d').date()

            flights = Flight.objects.filter(
                departure_airport=departure_airport,
                arrival_airport=arrival_airport,
                # Filter by date part of the datetime field
                departure_time__date=search_date
            ).order_by('departure_time')

        except Airport.DoesNotExist:
            # Handle case where airport code is invalid
            pass
        except ValueError:
            # Handle case where date format is invalid
            pass

    context = {
        'flights': flights
    }
    return render(request, 'core/search_flights.html', context)
