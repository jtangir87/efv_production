from django.contrib import admin
from .models import FuelEntry
# Register your models here.

admin.site.register(FuelEntry)

class FuelEntryAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date')
    ordering = ("-date")
