"""vehicles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from vehicles import views
from vehicles.views import (VehicleList, CreateVehicle, UpdateVehicle, VehicleDetail,
    DeleteVehicle, DamageList, DamageDetail, VehicleDamageList)

app_name = 'vehicles'

urlpatterns = [
    path('', VehicleList.as_view(), name='vehicle_list'),
    path('add', CreateVehicle.as_view(), name='create_vehicle'),
    path('update/<int:pk>', UpdateVehicle.as_view(), name='update_vehicle'),
    path('<int:pk>', VehicleDetail.as_view(), name='vehicle_detail'),
    path('delete/<int:pk>', DeleteVehicle.as_view(), name='delete_vehicle'),
    path('damage', DamageList.as_view(), name='damage_list'),
    path('damage/new', views.new_damage, name='new_damage'),
    path('damage/<int:pk>', DamageDetail.as_view(), name='damage_detail'),
    path('damage/vehicle/<int:pk>/all/', VehicleDamageList.as_view(), name='vehicle_all_damage'),

]
