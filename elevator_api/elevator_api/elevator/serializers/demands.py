from rest_framework import serializers
from elevator_api.elevator.models import Demand
from elevator_api.elevator.serializers.elevators import DemandElevatorSerializer


class DemandGetSerializer(serializers.ModelSerializer):
    """Serializer to present relevant data of a demand"""

    elevator = DemandElevatorSerializer(read_only=True)

    class Meta:
        model = Demand
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        elevator = representation.pop('elevator')
        representation['max_floors'] = elevator['max_floors']
        representation['elevator'] = elevator['name']
        return representation


class DemandSerializerCreate(serializers.ModelSerializer):
    """Serializer for create and update demands"""

    class Meta:
        model = Demand
        fields = '__all__'
