from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('addGarage', views.addGarage),
    path('addVehicle', views.addVehicle),
    path('addGaragePass', views.addGaragePass),
    path('gateCheck', views.gateCheck),
]