from django import forms
from vehicles.models import Vehicle
from .models import FuelEntry


class CreateEntryForm(forms.ModelForm):
    class Meta:
        model = FuelEntry
        fields = ('vehicle', 'current', 'after', 'gallons', 'cost', 'mileage')

        def clean_mileage(self):
            vehicle = self.cleaned_data['vehicle']
            current_mileage = Vehicle.objects.get(id=vehicle_id).current_mileage
            if current_mileage > self.cleaned_data['mileage']:
                raise forms.ValidationError("Incorrect mileage reading")
        
        