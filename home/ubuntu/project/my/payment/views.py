from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from booking.models import Booking
from .models import Payment
import stripe
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def process_payment_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    amount = booking.flight.price * booking.number_of_passengers

    if request.method == 'POST':
        try:
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # amount in cents
                currency='usd',
                metadata={'booking_id': booking.id},
            )

            payment, created = Payment.objects.get_or_create(
                booking=booking,
                defaults={'amount': amount, 'stripe_payment_intent_id': intent.id}
            )

            return redirect('payment:success', payment_id=payment.id)

        except Exception as e:
            messages.error(request, 'Payment processing failed. Please try again.')
            return redirect('payment:process', booking_id=booking.id)

    # Create PaymentIntent for the frontend
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency='usd',
            metadata={'booking_id': booking.id},
        )
        client_secret = intent.client_secret
    except Exception as e:
        client_secret = None

    context = {
        'booking': booking,
        'amount': amount,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': client_secret
    }
    return render(request, 'payment/process_payment.html', context)

@login_required
def payment_success_view(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, booking__user=request.user)
    messages.success(request, f'Payment of ${payment.amount} was successful! Your booking is confirmed.')
    return render(request, 'payment/payment_success.html', {'payment': payment})
