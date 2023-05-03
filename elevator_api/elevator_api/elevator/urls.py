"""Rides URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import elevators, calls

router = DefaultRouter()
router.register(
    'elevators',
    elevators.ElevatorViewSet,
    basename='elevators'
)

router.register(
    'calls',
    calls.CallViewSet,
    basename='calls'
)


urlpatterns = [
    path('', include(router.urls))
]
