from django.urls import path

from . import views

app_name = 'garage'
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.landingPage),
    path('addGarage', views.addGarage),
    path('addVehicle', views.addVehicle),
    path('addGaragePass', views.addGaragePass),
    path('gateCheck', views.gateCheck),
    path('getOpenSpaces', views.getOpenSpaces),
    path('allGarages', views.showAllGarages),
    path('test', views.test),
]
