from django.contrib import admin
from elevator.models import Elevator,ElevatorCall,Person,Movement


admin.site.register(Elevator)
admin.site.register(ElevatorCall)
admin.site.register(Person)
admin.site.register(Movement)
