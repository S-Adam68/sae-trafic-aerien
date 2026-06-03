from django.contrib import admin
from .models import Aeroport, Piste, Compagnie, TypeAvion, Avion, Vol


class PisteInline(admin.TabularInline):
    model = Piste
    extra = 1


@admin.register(Aeroport)
class AeroportAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pays']
    search_fields = ['nom', 'pays']
    inlines = [PisteInline]


@admin.register(Piste)
class PisteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'aeroport', 'longueur']
    list_filter = ['aeroport']
    search_fields = ['numero', 'aeroport__nom']


@admin.register(Compagnie)
class CompagnieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'pays_rattachement']
    search_fields = ['nom', 'pays_rattachement']


@admin.register(TypeAvion)
class TypeAvionAdmin(admin.ModelAdmin):
    list_display = ['marque', 'modele', 'longueur_piste_necessaire']
    search_fields = ['marque', 'modele']


@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'compagnie', 'modele']
    list_filter = ['compagnie', 'modele']
    search_fields = ['nom']


@admin.register(Vol)
class VolAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'pilote', 'avion', 'datetime_depart', 'datetime_arrivee', 'piste_arrivee']
    list_filter = ['aeroport_depart', 'aeroport_arrivee']
    search_fields = ['pilote', 'avion__nom']
    date_hierarchy = 'datetime_depart'
