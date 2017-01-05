from django.contrib import admin
from .models import Height, Weight, PredictedHeight, ParentsHeight, BioAge, SittingHeight, PHV

admin.site.register(Height)
admin.site.register(Weight)
admin.site.register(PredictedHeight)
admin.site.register(ParentsHeight)
admin.site.register(BioAge)
admin.site.register(SittingHeight)
admin.site.register(PHV)
