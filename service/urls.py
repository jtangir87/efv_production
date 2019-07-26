"""Service URL Configuration

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
from service.views import (CreateServiceRecord, UpdateServiceRecord,
    ServiceRecordDetail, ServiceList, AllServiceList, AllScheduledList,
    CreateScheduledService, CompleteScheduled, VehicleServiceList,
    ScheduledDetail, UpdateScheduledService
    )


app_name = 'service'

urlpatterns = [
    path('', ServiceList.as_view(), name='service_list'),
    path('new', CreateServiceRecord.as_view(), name='create_record'),
    path('update/<int:pk>', UpdateServiceRecord.as_view(), name='update_record'),
    path('<int:pk>', ServiceRecordDetail.as_view(), name='record_detail'),
    path('scheduled/new', CreateScheduledService.as_view(), name='create_scheduled'),
    path('scheduled/<int:pk>', ScheduledDetail.as_view(), name='scheduled_detail'),
    path('scheduled/update/<int:pk>', UpdateScheduledService.as_view(), name='update_scheduled'),
    path('scheduled/complete/<int:pk>', CompleteScheduled.as_view(), name='complete_scheduled'),
    path('vehicle/<int:pk>/all/', VehicleServiceList.as_view(), name='vehicle_all'),
    path('records/all/', AllServiceList.as_view(), name="service_all"),
    path('scheduled/all/', AllScheduledList.as_view(), name="scheduled_all"),

]
