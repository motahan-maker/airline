from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from booking.models import Booking
from .models import Payment
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def process_payment_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    amount = booking.flight.price * booking.number_of_passengers

    if request.method == 'POST':
        # In a real application, you would handle the Stripe token/source here
        # For this example, we'll simulate a successful payment
        try:
            # Simulate a Stripe charge
            charge = stripe.Charge.create(
                amount=int(amount * 100), # amount in cents
                currency='usd',
                source=request.POST.get('stripeToken', 'tok_visa'), # Use a test token
                description=f"Charge for booking {booking.id}",
            )

            payment, created = Payment.objects.get_or_create(booking=booking, defaults={'amount': amount})
            payment.status = 'Completed'
            payment.stripe_charge_id = charge.id
            payment.save()
            booking.status = 'Paid'
            booking.save()
            return redirect('payment:success', payment_id=payment.id)

        except stripe.error.CardError as e:
            # Handle card errors
            pass
        except Exception as e:
            # Handle other errors
            pass

    context = {
        'booking': booking,
        'amount': amount,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'payment/process_payment.html', context)

@login_required
def payment_success_view(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, booking__user=request.user)
    return render(request, 'payment/payment_success.html', {'payment': payment})
