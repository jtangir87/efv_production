from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import date
from vehicles.models import Vehicle
from .models import ServiceRecord
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth import get_user_model
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import datetime
from django.db.models import Sum
User = get_user_model()

# Create your views here.
class CreateServiceRecord(CreateView):
    model = ServiceRecord
    fields = ('vehicle','date', 'servicer', 'invoice', 'cost', 'mileage', 'description')
   
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DateTimePickerInput(format='%m-%d-%Y')
        return form

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user      
        self.object.save()
        return super().form_valid(form)

class UpdateServiceRecord(UpdateView):
    model = ServiceRecord
    fields = ('vehicle', 'servicer', 'invoice', 'cost', 'mileage', 'description')
    template_name_suffix = '_update_form'


class ServiceRecordDetail(DetailView):
    model = ServiceRecord
    template_name = 'service/servicerecord_detail.html'


class ServiceList(ListView):
    model = ServiceRecord
    
    def get_context_data(self, **kwargs):
        context = super(ServiceList, self).get_context_data(**kwargs)
        context["is_complete"] = ServiceRecord.objects.filter(completed=True).order_by('-date')[:25]
        context["is_scheduled"] = ServiceRecord.objects.filter(completed=False).order_by('-date')
        return context
    


class AllServiceList(ListView):
    model = ServiceRecord
    template_name = 'service/all_servicerecord_list.html'
    paginate_by = 25

class VehicleServiceList(ListView):
    model = ServiceRecord
    paginate_by = 25
    template_name = 'service/vehicle_service_list.html'

    def get_context_data(self, **kwargs):
        context = super(VehicleServiceList, self).get_context_data(**kwargs)
        vehicle_id = self.kwargs['pk']
        context["vehicle"] = Vehicle.objects.get(id=vehicle_id)
        context["all_serv"] = ServiceRecord.objects.filter(vehicle_id=vehicle_id).order_by('-date') 
        return context
    
    

#SCHEDULED Service VIEWS

class CreateScheduledService(CreateView):
    model = ServiceRecord
    fields = ('vehicle', 'description', 'date', 'mileage')
    def get_form(self):
        form = super().get_form()
        form.fields['date'].widget = DateTimePickerInput(format='%m-%d-%Y')
        return form

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.completed = False
        self.object.save()
        return super().form_valid(form)

class CompleteScheduled(UpdateView):
    model = ServiceRecord
    fields = ('vehicle', 'servicer', 'invoice', 'cost', 'mileage', 'description')
    template_name_suffix = '_update_form'

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.completed = True
        self.object.date = date.today()
        vehicle_id = self.object.vehicle.pk
        mileage = self.object.mileage
        self.object.save()

        Vehicle.objects.filter(id=vehicle_id).update(current_mileage=mileage)
        return super().form_valid(form)
