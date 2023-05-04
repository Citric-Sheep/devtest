# Django Rest Framework Imports
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

# Machine Learning Imports
import numpy as np

# View imports
from elevator_api.elevator.serializers.demands import DemandGetSerializer, DemandSerializerCreate


class DemandViewSet(ModelViewSet):
    """A Django REST Framework viewset for handling CRUD operations
        on Demand models."""

    serializer_class = DemandGetSerializer
    model_class = serializer_class.Meta.model

    def get_queryset(self):
        queryset = self.model_class.objects.all()
        elevator = self.request.query_params.get('elevator', None)
        if elevator is not None:
            queryset = queryset.filter(elevator=elevator)
        return queryset

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create' or self.action == 'update':
            return DemandSerializerCreate
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def list_ml_demand_data(self, request):
        queryset = self.get_queryset()
        data = self.get_serializer(queryset, many=True).data

        process_data = np.array([[d['elevator'], d['moment'],
                                  d['source_floor'], d['destination_floor'],
                                  d['rest_floor'], d['max_floors']]
                                 for d in data])

        response_data = {'data': process_data.tolist()}
        return Response(response_data, status=status.HTTP_200_OK)
