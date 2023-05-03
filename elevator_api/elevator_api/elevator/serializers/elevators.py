from rest_framework import serializers
from elevator_api.elevator.models import Elevator


class ElevatorSerializer(serializers.ModelSerializer):
    """General serializer for data transformation """
    class Meta:
        model = Elevator
        fields = '__all__'


class CallElevatorSerializer(serializers.ModelSerializer):
    """Serializer for displaying relevant elevator data"""

    class Meta:
        model = Elevator
        fields = ['id', 'name', 'max_floors']
