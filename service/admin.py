from django.contrib import admin
from .models import ServiceRecord
# Register your models here.
admin.site.register(ServiceRecord)


class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date')
    ordering = ("-date")


