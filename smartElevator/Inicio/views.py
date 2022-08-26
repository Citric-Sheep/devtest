from django.shortcuts import render
from django.http import HttpRequest
from Elevator.models import Data

# Create your views here.
# Core code here: train, evaluate, etc.
def Inicio(request: HttpRequest) -> render:
    return render(request, 'home.html')