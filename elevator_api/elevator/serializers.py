from rest_framework import serializers
from elevator.models import Elevator,ElevatorCall,Person,Movement

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'

class ElevatorCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorCall
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class MovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movement
        fields = '__all__'
