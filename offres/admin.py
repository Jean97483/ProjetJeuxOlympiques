from django.contrib import admin
from .models import Offre, Sport, Evenement, TypeOffre

admin.site.register(Offre)
admin.site.register(TypeOffre)
admin.site.register(Sport)
admin.site.register(Evenement)