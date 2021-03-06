from django.contrib import admin
from .models import DnaHeight


class DnaHeightAdmin(admin.ModelAdmin):
    list_display = ['player', 'predicted_height', 'date', 'created']
    list_filter = ['player__club__name', 'date', 'created']
    search_fields = ['player__user__username']

admin.site.register(DnaHeight, DnaHeightAdmin)
