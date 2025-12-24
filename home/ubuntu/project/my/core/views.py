from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from .models import Flight, Airport

def home_view(request):
    return render(request, 'core/home.html')

def search_flights_view(request):
    flights = []
    searched = False
    if request.method == 'GET':
        departure_iata = request.GET.get('departure')
        arrival_iata = request.GET.get('arrival')
        date_str = request.GET.get('date')

        if departure_iata or arrival_iata or date_str:
            searched = True
            try:
                query = Flight.objects.all()
                if departure_iata:
                    departure_airport = Airport.objects.get(iata_code__iexact=departure_iata)
                    query = query.filter(departure_airport=departure_airport)
                if arrival_iata:
                    arrival_airport = Airport.objects.get(iata_code__iexact=arrival_iata)
                    query = query.filter(arrival_airport=arrival_airport)
                if date_str:
                    search_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                    query = query.filter(departure_time__date=search_date)

                flights = query.order_by('departure_time')

            except Airport.DoesNotExist:
                flights = []
            except ValueError:
                flights = []
        else:
            # Show all flights if no search criteria
            flights = Flight.objects.all().order_by('departure_time')

    context = {
        'flights': flights,
        'searched': searched
    }
    return render(request, 'core/search_flights.html', context)
