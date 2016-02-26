from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from dashboard.models import Coach, Club, Player


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CoachInline(admin.StackedInline):
    model = Coach
    can_delete = False
    verbose_name_plural = 'club'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (CoachInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Coach)
admin.site.register(Club)
admin.site.register(Player)
