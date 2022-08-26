from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from .models import Data

# Create your views here.
def ShowData(request: HttpRequest) -> render:
    data = Data.objects.filter(active__exact=True)
    activeDicc = {
        'showData': 'active'
    }
    return render(request, 'showData.html', {'showData': data, 'active': activeDicc})

def AddData(request: HttpRequest) -> render:
    rowData = Data.objects.create(
        date = request.POST['addDate'],
        time = request.POST['addTime'],
        demandFloor = request.POST['addDemandFloor'],
        endFloor = request.POST['addEndFloor'],
        people = request.POST['addPeople'],
        active = True
    )
    return redirect('showData')

def EditData(request: HttpRequest) -> render:
    rowData = Data.objects.get(id=int(request.POST['id']))
    rowData.date = request.POST['editDate']
    rowData.time = request.POST['editTime']
    rowData.demandFloor = request.POST['editDemandFloor']
    rowData.endFloor = request.POST['editEndFloor']
    rowData.people = request.POST['editPeople']
    rowData.save()
    return redirect('showData')

def DeleteData(request: HttpResponse) -> render:
    rowData = Data.objects.get(id=int(request.POST['id']))
    rowData.active = False
    rowData.save()
    return redirect('showData')