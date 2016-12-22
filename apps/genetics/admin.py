from django.contrib import admin
from .models import DnaMeasurement, DnaResult

admin.site.register(DnaMeasurement)
admin.site.register(DnaResult)
