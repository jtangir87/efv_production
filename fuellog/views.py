from django.shortcuts import render
from django.urls import reverse_lazy
from vehicles.models import Vehicle
from .models import FuelEntry
from .forms import CreateEntryForm
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth import get_user_model
from django.db.models import Sum
from datetime import datetime
User = get_user_model()

# Create your views here.
class CreateEntry(CreateView):
    model = FuelEntry
    fields = ('vehicle', 'current', 'after', 'gallons', 'cost', 'mileage')

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        vehicle_id = self.object.vehicle.pk
        mileage = self.object.mileage

        current_mileage = Vehicle.objects.get(id=vehicle_id).current_mileage
        if current_mileage > mileage:
            form.add_error('mileage', 'Incorrect mileage reading! Mileage cannot be lower than previous record')
            return super().form_invalid(form)
        
        self.object.save()


        Vehicle.objects.filter(id=vehicle_id).update(current_mileage=mileage)
        Vehicle.objects.filter(id=vehicle_id).update(five_hundred_miles=int(mileage + 500))
        return super().form_valid(form)

class UpdateEntry(UpdateView):
    model = FuelEntry
    fields = ('after', 'gallons', 'cost')
    template_name_suffix = '_update_form'   
      
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        
        self.object.save()

        return super().form_valid(form)




class EntryDetail(DetailView):
    model = FuelEntry
    template_name = 'fuellog/fuelentry_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FuelList(ListView):
    model = FuelEntry
    paginate_by = 25

class VehicleFuelList(ListView):
    model = FuelEntry
    paginate_by = 25
    template_name = 'fuellog/vehicle_fuelentry_list.html'

    def get_context_data(self, **kwargs):
        context = super(VehicleFuelList, self).get_context_data(**kwargs)
        vehicle_id = self.kwargs['pk']
        context["vehicle"] = Vehicle.objects.get(id=vehicle_id)
        context["all_fuel"] = FuelEntry.objects.filter(vehicle_id=vehicle_id).order_by('-date') 
        return context