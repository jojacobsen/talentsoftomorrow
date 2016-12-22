from django.contrib import admin
from .models import Measurement, Unit, Performance


class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'get_measurement', 'value', 'get_unit', 'date']

    def get_user(self, obj):
        return obj.player.user.username
    get_user.admin_order_field = 'player'   #Allows column order sorting
    get_user.short_description = 'User id'  #Renames column head

    def get_measurement(self, obj):
        return obj.measurement.name
    get_measurement.short_description = 'Measurement'  #Renames column head
    get_user.admin_order_field = 'player'   #Allows column order sorting

    def get_unit(self, obj):
        return obj.measurement.unit.name
    get_unit.short_description = 'Unit'  #Renames column head

admin.site.register(Measurement)
admin.site.register(Unit)
admin.site.register(Performance, PerformanceAdmin)