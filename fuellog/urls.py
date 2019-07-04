"""fuellog URL Configuration

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
from fuellog.views import CreateEntry, UpdateEntry, FuelList, EntryDetail, VehicleFuelList

app_name = 'fuellog'

urlpatterns = [
    path('', FuelList.as_view(), name='entry_list'),
    path('new', CreateEntry.as_view(), name='create_entry'),
    path('update/<int:pk>', UpdateEntry.as_view(), name='update_entry'),
    path('<int:pk>', EntryDetail.as_view(), name='entry_detail'),
    path('vehicle/<int:pk>/all/', VehicleFuelList.as_view(), name='vehicle_all'),
]
