from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, BookingViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = router.urls
