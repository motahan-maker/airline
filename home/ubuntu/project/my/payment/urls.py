from django.urls import path
from . import views

app_name = 'payment'
urlpatterns = [
    path('<int:booking_id>/process/', views.process_payment_view, name='process'),
    path('<int:payment_id>/success/', views.payment_success_view, name='success'),
]
