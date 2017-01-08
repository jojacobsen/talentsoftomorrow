from django.contrib import admin
from .models import Club, Coach, Player, ProfilePicture
import datetime

from django.utils.translation import ugettext_lazy as _


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('born year')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('1999', _('1999')),
            ('2000', _('2000')),
            ('2001', _('2001')),
            ('2002', _('2002')),
            ('2003', _('2003')),
            ('2004', _('2004')),
            ('2005', _('2005')),
            ('2006', _('2006')),
            ('2007', _('2007')),
            ('2008', _('2008')),
            ('2009', _('2009')),
            ('2010', _('2010')),
            ('2011', _('2011')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            year = int(self.value())
            return queryset.filter(birthday__gte=datetime.date(year, 1, 1),
                                   birthday__lte=datetime.date(year, 12, 31))


class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'measurement_system']
    list_filter = ['measurement_system']
    search_fields = ['name', 'user__username']


class CoachAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_first_name', 'get_last_name', 'club']
    list_filter = ['club__name']
    search_fields = ['user__username']

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'  # Renames column head

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'  # Renames column head


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'club', 'lab_key', 'active', 'archived', 'birthday', 'get_age']
    list_filter = ['club__name', 'active', 'archived', DecadeBornListFilter]
    search_fields = ['user__username', 'lab_key']

    def get_age(self, obj):
        return round((datetime.date.today() - obj.birthday).days / 365.25, 1)
    get_age.short_description = 'Age'  # Renames column head


class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = ['user', 'url']
    search_fields = ['user__username']


# Re-register UserAdmin
admin.site.register(Coach, CoachAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(ProfilePicture, ProfilePictureAdmin)
