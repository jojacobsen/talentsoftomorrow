from django.contrib import admin
from .models import Club, Coach, Player, ProfilePicture

# Re-register UserAdmin
admin.site.register(Coach)
admin.site.register(Club)
admin.site.register(Player)
admin.site.register(ProfilePicture)