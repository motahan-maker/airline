from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from core.models import Flight

@login_required
def submit_review_view(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    if request.method == 'POST':
        # In a real app, this would involve a form
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        Review.objects.create(
            user=request.user,
            flight=flight,
            rating=rating,
            comment=comment
        )
        return redirect('home') # Redirect to home or flight detail page
    return render(request, 'review/submit_review.html', {'flight': flight})
