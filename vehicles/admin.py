from django.contrib import admin
from .models import Vehicle, DamageReport, DamageImages
# Register your models here.

admin.site.register(Vehicle)
admin.site.register(DamageReport)
admin.site.register(DamageImages)
