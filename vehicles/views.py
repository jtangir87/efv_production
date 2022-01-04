from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Vehicle, DamageReport, DamageImages
from fuellog.models import FuelEntry
from service.models import ServiceRecord
from django.http import Http404, HttpResponseRedirect
from django.forms import modelformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .forms import DamageForm
from bootstrap_datepicker_plus import DateTimePickerInput
from datetime import datetime
from django.db.models import Sum

# Create your views here.


class VehicleList(ListView):
    model = Vehicle
    paginate_by = 25


class CreateVehicle(CreateView):
    model = Vehicle
    fields = ["name", 'make', 'model', 'year', 'vin', 'gvw',
              'license_plate', 'purchase_date', 'title_num', 'current_mileage']

    def get_form(self):
        form = super().get_form()
        form.fields['purchase_date'].widget = DateTimePickerInput(
            format='%m-%d-%Y')
        return form


class UpdateVehicle(UpdateView):
    model = Vehicle
    fields = ["name", 'make', 'model', 'year', 'vin', 'gvw',
              'license_plate', 'purchase_date', 'title_num', 'current_mileage']
    template_name_suffix = '_update_form'


class VehicleDetail(DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'

    def get_context_data(self, **kwargs):
        context = super(VehicleDetail, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['fuel_entries'] = FuelEntry.objects.filter(vehicle_id=pk)
        context['service_records'] = ServiceRecord.objects.filter(
            vehicle_id=pk)
        context['damage_reports'] = DamageReport.objects.filter(vehicle_id=pk)
        # Calculate ytd fuel total
        today = datetime.now()
        ytd_fuel_total = FuelEntry.objects.filter(
            vehicle_id=pk, date__year=today.year).aggregate(Sum('cost'))
        context['ytd_fuel_total'] = ytd_fuel_total['cost__sum']
        # Calculate ytd service total
        today = datetime.now()
        ytd_serv_total = ServiceRecord.objects.filter(
            vehicle_id=pk, date__year=today.year).aggregate(Sum('cost'))
        context['ytd_serv_total'] = ytd_serv_total['cost__sum']
        # Calculate lifetime service total
        lifetime_serv_total = ServiceRecord.objects.filter(
            vehicle_id=pk).aggregate(Sum('cost'))
        context['lifetime_serv_total'] = lifetime_serv_total['cost__sum']

        return context


class DeleteVehicle(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('vehicles:vehicle_list')


# DAMAGE REPORT VIEWS
class DamageList(ListView):
    model = DamageReport
    paginate_by = 25


def new_damage(request):
    ImageFormset = modelformset_factory(
        DamageImages, fields=('image',), extra=5)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = DamageForm(request.POST)
            formset = ImageFormset(request.POST or None, request.FILES or None)
            if form.is_valid() and formset.is_valid():
                report = form.save(commit=False)
                report.user = request.user
                report.save()

                for f in formset:
                    try:
                        photo = DamageImages(
                            report=report, image=f.cleaned_data['image'])
                        photo.save()
                    except Exception as e:
                        break
                return redirect('vehicles:damage_list')
    else:
        form = DamageForm()
        formset = ImageFormset(queryset=DamageImages.objects.none())

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'vehicles/damagereport_form.html', context)


class DamageDetail(DetailView):
    model = DamageReport
    template_name = 'vehicles/damagereport_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DamageDetail, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['damage_images'] = DamageImages.objects.filter(report_id=pk)
        return context


class VehicleDamageList(ListView):
    model = DamageReport
    paginate_by = 25
    template_name = 'vehicles/vehicle_damage_list.html'

    def get_context_data(self, **kwargs):
        context = super(VehicleDamageList, self).get_context_data(**kwargs)
        vehicle_id = self.kwargs['pk']
        context["vehicle"] = Vehicle.objects.get(id=vehicle_id)
        context["all_damage"] = DamageReport.objects.filter(
            vehicle_id=vehicle_id).order_by('-date')
        return context


class DeleteDamage(DeleteView):
    model = DamageReport
    success_url = reverse_lazy('vehicles:damage_list')
