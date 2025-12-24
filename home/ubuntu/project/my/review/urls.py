from django.urls import path
from . import views

app_name = 'review'
urlpatterns = [
    path('<int:flight_id>/submit/', views.submit_review_view, name='submit'),
]
