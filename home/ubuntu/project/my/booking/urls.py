from django.urls import path
from . import views

app_name = 'booking'
urlpatterns = [
    path('', views.booking_list_view, name='list'),
    path('<int:flight_id>/book/', views.book_flight_view, name='book_flight'),
    path('<int:booking_id>/', views.booking_detail_view, name='detail'),
    path('<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel'),
]
