from django.contrib import admin
from .models import Offre, Sport, Evenement, TypeOffre, Panier

from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
from django.db.models import Count

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ('offre', 'get_evenement', 'quantite', 'get_type_offre')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.get_sales_data())
        return super().changelist_view(request, extra_context=extra_context)
     
    def get_evenement(self, obj):
        return obj.evenement.date if obj.evenement else "Pas de date"
    get_evenement.short_description = 'Date Événement'

    def get_type_offre(self, obj):
        return obj.type_offre.nom if obj.type_offre else "Pas de type"
    get_type_offre.short_description = 'Type Offre'

    def get_sales_data(self):
        sales_data = Panier.objects.values('type_offre').annotate(total_sales=Count('id'))
        return {
            'solo_sales': sales_data.filter(type_offre='solo').aggregate(total_solo_sales=Count('id'))['total_solo_sales'],
            'duo_sales': sales_data.filter(type_offre='Duo').aggregate(total_duo_sales=Count('id'))['total_duo_sales'],
            'familliale_sales': sales_data.filter(type_offre='Familliale').aggregate(total_familliale_sales=Count('id'))['total_familliale_sales'],
                }

        

        

@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'sport', 'description', 'get_date', 'prix')
    fields = ('titre', 'description', 'image', 'sport', 'prix')

    def get_date(self, obj):
        # Renvoie la date du premier événement lié
        evenement = obj.evenements.first()
        return evenement.date if evenement else "Pas de date"
    get_date.short_description = 'Date Événement'

admin.site.register(TypeOffre)
admin.site.register(Sport)
admin.site.register(Evenement)