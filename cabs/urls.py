from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static  # Import the static function
from .views import *

router = DefaultRouter()
router.register(r"cabs", CabsViewSet, basename="cabs")
router.register(r"profit_loss", ProfitLossViewSet, basename="profit_loss")
router.register(r"city", CityViewSet, basename="city")
router.register(r"trips", TripsViewSet, basename="trips")
router.register(r"timetable", TripTimeTableViewSet, basename="timetable")
router.register(r"booking", BookingViewSet, basename="booking")
router.register(r"trip_status", TripStatusViewSet, basename="booking")

urlpatterns = [
    path('api/v3/', include(router.urls)),
]


