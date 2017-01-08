from django.contrib import admin
from .models import Height, Weight, PredictedHeight, ParentsHeight, BioAge, SittingHeight, PHV
import datetime

class HeightAdmin(admin.ModelAdmin):
    list_display = ['player', 'height', 'date', 'created']
    list_filter = ['player__club__name', 'date', 'created']
    search_fields = ['player__user__username']


class WeightAdmin(admin.ModelAdmin):
    list_display = ['player', 'weight', 'date', 'created']
    list_filter = ['player__club__name', 'date', 'created']
    search_fields = ['player__user__username']


class PredictedHeightAdmin(admin.ModelAdmin):
    list_display = ['player', 'predicted_height', 'date', 'created']
    list_filter = ['player__club__name', 'date', 'created']
    search_fields = ['player__user__username']


class SittingHeightAdmin(admin.ModelAdmin):
    list_display = ['player', 'sitting_height', 'date', 'created']
    list_filter = ['player__club__name', 'date', 'created']
    search_fields = ['player__user__username']


class ParentsHeightAdmin(admin.ModelAdmin):
    list_display = ['player', 'fathers_height', 'mothers_height', 'created']
    list_filter = ['player__club__name', 'created']
    search_fields = ['player__user__username']


class BioAgeAdmin(admin.ModelAdmin):
    list_display = ['player', 'bio_age', 'get_age', 'get_predicted_height', 'get_current_height', 'created']
    list_filter = ['player__club__name', 'created']
    search_fields = ['player__user__username']

    def get_predicted_height(self, obj):
        return obj.predicted_height.predicted_height
    get_predicted_height.short_description = 'Predicted Height'  # Renames column head

    def get_current_height(self, obj):
        return obj.current_height.height
    get_current_height.short_description = 'Current Height'  # Renames column head

    def get_age(self, obj):
        return round((obj.predicted_height.date - obj.player.birthday).days / 365.25, 1)
    get_age.short_description = 'Age'  # Renames column head


class PHVAdmin(admin.ModelAdmin):
    list_display = ['player', 'phv_date', 'get_phv_age', 'get_age', 'get_current_weight', 'get_current_height',
                    'get_sitting_height', 'date', 'created']
    list_filter = ['player__club__name', 'created']
    search_fields = ['player__user__username']

    def get_current_weight(self, obj):
        return obj.current_weight.weight
    get_current_weight.short_description = 'Weight'  # Renames column head

    def get_current_height(self, obj):
        return obj.current_height.height
    get_current_height.short_description = 'Height'  # Renames column head

    def get_sitting_height(self, obj):
        return obj.sitting_height.sitting_height
    get_sitting_height.short_description = 'Sitting Height'  # Renames column head

    def get_age(self, obj):
        age = (obj.date - obj.player.birthday).days / 365.25
        return round(age, 1)
    get_age.short_description = 'Age'  # Renames column head

    def get_phv_age(self, obj):
        age = (obj.date - obj.player.birthday).days / 365.25
        return round(age + ((obj.phv_date - obj.date).days / 365.25), 1)
    get_phv_age.short_description = 'PHV Age'


admin.site.register(Height, HeightAdmin)
admin.site.register(Weight, WeightAdmin)
admin.site.register(PredictedHeight, PredictedHeightAdmin)
admin.site.register(ParentsHeight, ParentsHeightAdmin)
admin.site.register(BioAge, BioAgeAdmin)
admin.site.register(SittingHeight, SittingHeightAdmin)
admin.site.register(PHV, PHVAdmin)
