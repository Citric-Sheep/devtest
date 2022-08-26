from django.urls import path
from . import views # Importar el archivo con las vistas que está en el mismo directorio (.)

urlpatterns = [
    # -- Datos --
    path('', views.ShowData, name='showData'),
    path('add/', views.AddData, name='addData'),
    path('edit/', views.EditData, name='editData'),
    path('delete/', views.DeleteData, name='deleteData'),
]