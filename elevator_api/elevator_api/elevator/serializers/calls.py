from rest_framework import serializers
from elevator_api.elevator.models import Call
from elevator_api.elevator.serializers.elevators import CallElevatorSerializer


class CallGetSerializer(serializers.ModelSerializer):
    """Serializer to present relevant data of a call"""

    elevator = CallElevatorSerializer(read_only=True)

    class Meta:
        model = Call
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        elevator = representation.pop('elevator')
        representation['max_floors'] = elevator['max_floors']
        representation['elevator'] = elevator['name']
        return representation


class CallSerializerCreate(serializers.ModelSerializer):
    """Serializer for create and update calls"""

    class Meta:
        model = Call
        fields = '__all__'
