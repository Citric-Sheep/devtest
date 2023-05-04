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

    def validate(self, validated_data):
        elevator_max_floors = validated_data['elevator'].max_floors
        source_floor = validated_data['source_floor']
        destination_floor = validated_data['destination_floor']
        rest_floor = validated_data['rest_floor']

        if elevator_max_floors < source_floor or \
            elevator_max_floors < destination_floor or \
                elevator_max_floors < rest_floor:

            raise serializers.ValidationError('Floor number must be a less or equal '
                                              'to max_floors elevator')

        return validated_data
