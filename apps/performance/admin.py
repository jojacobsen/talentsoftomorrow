from django.contrib import admin
from .models import Measurement, Unit, Performance, Benchmark


class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'get_measurement', 'value', 'get_unit', 'date', 'created']
    list_filter = ['measurement__name', 'measurement__unit__name', 'player__club__name', 'date', 'created']
    search_fields = ['player__user__username', 'measurement__name']

    def get_user(self, obj):
        return obj.player.user.username
    get_user.admin_order_field = 'player'   # Allows column order sorting
    get_user.short_description = 'Player'  # Renames column head

    def get_measurement(self, obj):
        return obj.measurement.name
    get_measurement.short_description = 'Measurement'  # Renames column head

    def get_unit(self, obj):
        return obj.measurement.unit.name
    get_unit.short_description = 'Unit'  # Renames column head


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'category', 'smaller_is_better', 'precision', 'slug_name']
    list_filter = ['unit', 'category', 'smaller_is_better', 'precision', 'unit__system']
    search_fields = ['name', 'slug_name']


class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'get_measurement', 'get_performance', 'get_unit',
                    'benchmark', 'benchmark_bio', 'get_age', 'get_bioage', 'created']
    list_filter = ['performance__measurement__name', 'performance__player__club__name', 'created']
    search_fields = ['performance__player__user__username']

    def get_user(self, obj):
        return obj.performance.player.user.username
    get_user.admin_order_field = 'player'   # Allows column order sorting
    get_user.short_description = 'Player'  # Renames column head

    def get_measurement(self, obj):
        return obj.performance.measurement.name
    get_measurement.short_description = 'Measurement'  # Renames column head

    def get_performance(self, obj):
        return obj.performance.value
    get_performance.short_description = 'Value'  # Renames column head

    def get_unit(self, obj):
        return obj.performance.measurement.unit
    get_unit.short_description = 'Unit'  # Renames column head

    def get_bioage(self, obj):
        if obj.bio_age:
            return round(obj.bio_age.bio_age, 1)
    get_bioage.short_description = 'Bio Age'  # Renames column head

    def get_age(self, obj):
        return round((obj.performance.date - obj.performance.player.birthday).days / 365.25, 1)
    get_age.short_description = 'Age'  # Renames column head


class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'system']
    list_filter = ['system']
    search_fields = ['name', 'abbreviation']


admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Benchmark, BenchmarkAdmin)
