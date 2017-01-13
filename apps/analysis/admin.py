from django.contrib import admin
from .models import KhamisRoche


class KhamisRocheAdmin(admin.ModelAdmin):
    list_display = ['player', 'predicted_height', 'get_current_height', 'get_current_weight',
                    'get_fathers_height', 'get_mothers_height', 'get_age', 'date', 'created']
    list_filter = ['player__club__name', 'date', 'created']
    search_fields = ['player__user__username']

    def get_current_weight(self, obj):
        return obj.current_weight.weight
    get_current_weight.short_description = 'Current Weight'  # Renames column head

    def get_current_height(self, obj):
        return obj.current_height.height
    get_current_height.short_description = 'Current Height'  # Renames column head

    def get_fathers_height(self, obj):
        return obj.parents_height.fathers_height
    get_fathers_height.short_description = 'Fathers Height'  # Renames column head

    def get_mothers_height(self, obj):
        return obj.parents_height.mothers_height
    get_mothers_height.short_description = 'Mothers Height'  # Renames column head

    def get_age(self, obj):
        return round((obj.current_height.date - obj.player.birthday).days / 365.25, 1)
    get_age.short_description = 'Age'  # Renames column head

admin.site.register(KhamisRoche, KhamisRocheAdmin)
