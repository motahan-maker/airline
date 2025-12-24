from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Booking
from core.models import Flight

@login_required
def booking_list_view(request):
    bookings = Booking.objects.filter(user=request.user).select_related('flight')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

@login_required
def book_flight_view(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    if request.method == 'POST':
        # Simple booking logic for now
        # In a real app, this would involve a form and validation
        number_of_passengers = int(request.POST.get('passengers', 1))
        if flight.available_seats >= number_of_passengers:
            booking = Booking.objects.create(
                user=request.user,
                flight=flight,
                number_of_passengers=number_of_passengers,
                status='Pending' # Pending payment
            )
            # Redirect to payment
            return redirect('payment:process', booking_id=booking.id)
        else:
            # Handle not enough seats
            pass
    return render(request, 'booking/book_flight.html', {'flight': flight})

@login_required
def booking_detail_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'booking/booking_detail.html', {'booking': booking})

@login_required
@require_POST
def cancel_booking_view(request, booking_id):
    # This is the view that had the runtime error in the previous session.
    # The fix is to ensure we are not trying to modify a property (available_seats)
    # and that we correctly update the booking status.
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    booking.status = 'Cancelled'
    booking.save()
    # In a real app, you would also handle refunds and updating seat counts.
    return redirect('booking:list')
