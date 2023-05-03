from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from elevator_api.elevator.serializers.elevators import ElevatorSerializer


class ElevatorViewSet(ModelViewSet):
    """A Django REST Framework viewset for handling CRUD operations
        on Elevator models."""

    serializer_class = ElevatorSerializer
    model_class = serializer_class.Meta.model
    queryset = model_class.objects.all()

    filter_backends = [filters.SearchFilter]

    search_fields = ['name']
