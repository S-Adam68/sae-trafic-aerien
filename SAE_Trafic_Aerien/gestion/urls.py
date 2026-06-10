from django.urls import path
from . import views

urlpatterns = [
    # Accueil
    path('', views.index, name='index'),

    # Aéroports
    path('aeroports/', views.aeroport_list, name='aeroport_list'),
    path('aeroports/nouveau/', views.aeroport_create, name='aeroport_create'),
    path('aeroports/<int:pk>/', views.aeroport_detail, name='aeroport_detail'),
    path('aeroports/<int:pk>/modifier/', views.aeroport_update, name='aeroport_update'),
    path('aeroports/<int:pk>/supprimer/', views.aeroport_delete, name='aeroport_delete'),

    # Pistes
    path('pistes/', views.piste_list, name='piste_list'),
    path('pistes/nouveau/', views.piste_create, name='piste_create'),
    path('pistes/<int:pk>/modifier/', views.piste_update, name='piste_update'),
    path('pistes/<int:pk>/supprimer/', views.piste_delete, name='piste_delete'),

    # Compagnies
    path('compagnies/', views.compagnie_list, name='compagnie_list'),
    path('compagnies/nouveau/', views.compagnie_create, name='compagnie_create'),
    path('compagnies/<int:pk>/modifier/', views.compagnie_update, name='compagnie_update'),
    path('compagnies/<int:pk>/supprimer/', views.compagnie_delete, name='compagnie_delete'),

    # Types d'avions
    path('types-avions/', views.type_avion_list, name='type_avion_list'),
    path('types-avions/nouveau/', views.type_avion_create, name='type_avion_create'),
    path('types-avions/<int:pk>/modifier/', views.type_avion_update, name='type_avion_update'),
    path('types-avions/<int:pk>/supprimer/', views.type_avion_delete, name='type_avion_delete'),

    # Avions
    path('avions/', views.avion_list, name='avion_list'),
    path('avions/nouveau/', views.avion_create, name='avion_create'),
    path('avions/<int:pk>/modifier/', views.avion_update, name='avion_update'),
    path('avions/<int:pk>/supprimer/', views.avion_delete, name='avion_delete'),

    # Vols
    path('vols/', views.vol_list, name='vol_list'),
    path('vols/nouveau/', views.vol_create, name='vol_create'),
    path('vols/<int:pk>/modifier/', views.vol_update, name='vol_update'),
    path('vols/<int:pk>/supprimer/', views.vol_delete, name='vol_delete'),
    path('vols/fiche/', views.vol_fiche, name='vol_fiche'),
    path('vols/import/', views.vol_import, name='vol_import'),
]
