"""Rides URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import elevators, demands

router = DefaultRouter()
router.register(
    'elevators',
    elevators.ElevatorViewSet,
    basename='elevators'
)

router.register(
    'demands',
    demands.DemandViewSet,
    basename='demands'
)


urlpatterns = [
    path('', include(router.urls))
]
