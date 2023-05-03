# Django Rest Framework Imports
from rest_framework.viewsets import ModelViewSet

# View imports
from elevator_api.elevator.serializers.calls import CallGetSerializer, CallSerializerCreate


class CallViewSet(ModelViewSet):
    """A Django REST Framework viewset for handling CRUD operations
        on Call models."""

    serializer_class = CallGetSerializer
    model_class = serializer_class.Meta.model
    queryset = model_class.objects.all()

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create' or self.action == 'update':
            return CallSerializerCreate
        return self.serializer_class
