import csv
import io
from datetime import timedelta, datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .models import Aeroport, Piste, Compagnie, TypeAvion, Avion, Vol
from .forms import (
    AeroportForm, PisteForm, CompagnieForm, TypeAvionForm,
    AvionForm, VolForm, FicheVolsForm, ImportVolsForm
)


# Page d'accueil : on affiche les stats globales et les 5 derniers vols
def index(request):
    nb_aeroports = Aeroport.objects.count()
    nb_pistes = Piste.objects.count()
    nb_compagnies = Compagnie.objects.count()
    nb_types_avions = TypeAvion.objects.count()
    nb_avions = Avion.objects.count()
    nb_vols = Vol.objects.count()
    derniers_vols = Vol.objects.order_by('-datetime_depart')[:5]

    return render(request, 'gestion/index.html', {
        'nb_aeroports': nb_aeroports,
        'nb_pistes': nb_pistes,
        'nb_compagnies': nb_compagnies,
        'nb_types_avions': nb_types_avions,
        'nb_avions': nb_avions,
        'nb_vols': nb_vols,
        'derniers_vols': derniers_vols,
    })


# ---- Aéroports ----

def aeroport_list(request):
    aeroports = Aeroport.objects.all()
    return render(request, 'gestion/aeroport_list.html', {'aeroports': aeroports})


def aeroport_create(request):
    if request.method == 'POST':
        form = AeroportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Aéroport ajouté avec succès.")
            return redirect('aeroport_list')
    else:
        form = AeroportForm()
    return render(request, 'gestion/aeroport_form.html', {'form': form, 'titre': 'Nouvel aéroport'})


def aeroport_update(request, pk):
    aeroport = get_object_or_404(Aeroport, pk=pk)
    if request.method == 'POST':
        form = AeroportForm(request.POST, instance=aeroport)
        if form.is_valid():
            form.save()
            messages.success(request, "Aéroport modifié.")
            return redirect('aeroport_list')
    else:
        form = AeroportForm(instance=aeroport)
    return render(request, 'gestion/aeroport_form.html', {'form': form, 'titre': 'Modifier un aéroport'})


def aeroport_delete(request, pk):
    aeroport = get_object_or_404(Aeroport, pk=pk)
    if request.method == 'POST':
        aeroport.delete()
        messages.success(request, "Aéroport supprimé.")
        return redirect('aeroport_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objet': aeroport,
        'type_objet': "l'aéroport",
        'retour_url': 'aeroport_list',
    })


def aeroport_detail(request, pk):
    aeroport = get_object_or_404(Aeroport, pk=pk)
    pistes = Piste.objects.filter(aeroport=aeroport)
    vols_depart = Vol.objects.filter(aeroport_depart=aeroport).order_by('-datetime_depart')[:10]
    vols_arrivee = Vol.objects.filter(aeroport_arrivee=aeroport).order_by('-datetime_arrivee')[:10]
    return render(request, 'gestion/aeroport_detail.html', {
        'aeroport': aeroport,
        'pistes': pistes,
        'vols_depart': vols_depart,
        'vols_arrivee': vols_arrivee,
    })


# ---- Pistes ----

def piste_list(request):
    pistes = Piste.objects.all()
    return render(request, 'gestion/piste_list.html', {'pistes': pistes})


def piste_create(request):
    if request.method == 'POST':
        form = PisteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Piste ajoutée.")
            return redirect('piste_list')
    else:
        form = PisteForm()
    return render(request, 'gestion/piste_form.html', {'form': form, 'titre': 'Nouvelle piste'})


def piste_update(request, pk):
    piste = get_object_or_404(Piste, pk=pk)
    if request.method == 'POST':
        form = PisteForm(request.POST, instance=piste)
        if form.is_valid():
            form.save()
            messages.success(request, "Piste modifiée.")
            return redirect('piste_list')
    else:
        form = PisteForm(instance=piste)
    return render(request, 'gestion/piste_form.html', {'form': form, 'titre': 'Modifier une piste'})


def piste_delete(request, pk):
    piste = get_object_or_404(Piste, pk=pk)
    if request.method == 'POST':
        piste.delete()
        messages.success(request, "Piste supprimée.")
        return redirect('piste_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objet': piste,
        'type_objet': 'la piste',
        'retour_url': 'piste_list',
    })


# ---- Compagnies ----

def compagnie_list(request):
    compagnies = Compagnie.objects.all()
    return render(request, 'gestion/compagnie_list.html', {'compagnies': compagnies})


def compagnie_create(request):
    if request.method == 'POST':
        form = CompagnieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compagnie ajoutée.")
            return redirect('compagnie_list')
    else:
        form = CompagnieForm()
    return render(request, 'gestion/compagnie_form.html', {'form': form, 'titre': 'Nouvelle compagnie'})


def compagnie_update(request, pk):
    compagnie = get_object_or_404(Compagnie, pk=pk)
    if request.method == 'POST':
        form = CompagnieForm(request.POST, instance=compagnie)
        if form.is_valid():
            form.save()
            messages.success(request, "Compagnie modifiée.")
            return redirect('compagnie_list')
    else:
        form = CompagnieForm(instance=compagnie)
    return render(request, 'gestion/compagnie_form.html', {'form': form, 'titre': 'Modifier une compagnie'})


def compagnie_delete(request, pk):
    compagnie = get_object_or_404(Compagnie, pk=pk)
    if request.method == 'POST':
        compagnie.delete()
        messages.success(request, "Compagnie supprimée.")
        return redirect('compagnie_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objet': compagnie,
        'type_objet': 'la compagnie',
        'retour_url': 'compagnie_list',
    })


# ---- Types d'avions ----

def type_avion_list(request):
    types = TypeAvion.objects.all()
    return render(request, 'gestion/type_avion_list.html', {'types': types})


def type_avion_create(request):
    if request.method == 'POST':
        form = TypeAvionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Type d'avion ajouté.")
            return redirect('type_avion_list')
    else:
        form = TypeAvionForm()
    return render(request, 'gestion/type_avion_form.html', {'form': form, 'titre': "Nouveau type d'avion"})


def type_avion_update(request, pk):
    type_avion = get_object_or_404(TypeAvion, pk=pk)
    if request.method == 'POST':
        form = TypeAvionForm(request.POST, request.FILES, instance=type_avion)
        if form.is_valid():
            form.save()
            messages.success(request, "Type d'avion modifié.")
            return redirect('type_avion_list')
    else:
        form = TypeAvionForm(instance=type_avion)
    return render(request, 'gestion/type_avion_form.html', {
        'form': form,
        'titre': "Modifier un type d'avion",
        'objet': type_avion,
    })


def type_avion_delete(request, pk):
    type_avion = get_object_or_404(TypeAvion, pk=pk)
    if request.method == 'POST':
        type_avion.delete()
        messages.success(request, "Type d'avion supprimé.")
        return redirect('type_avion_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objet': type_avion,
        'type_objet': "le type d'avion",
        'retour_url': 'type_avion_list',
    })


# ---- Avions ----

def avion_list(request):
    avions = Avion.objects.all()
    return render(request, 'gestion/avion_list.html', {'avions': avions})


def avion_create(request):
    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Avion ajouté.")
            return redirect('avion_list')
    else:
        form = AvionForm()
    return render(request, 'gestion/avion_form.html', {'form': form, 'titre': 'Nouvel avion'})


def avion_update(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        form = AvionForm(request.POST, instance=avion)
        if form.is_valid():
            form.save()
            messages.success(request, "Avion modifié.")
            return redirect('avion_list')
    else:
        form = AvionForm(instance=avion)
    return render(request, 'gestion/avion_form.html', {'form': form, 'titre': 'Modifier un avion'})


def avion_delete(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        avion.delete()
        messages.success(request, "Avion supprimé.")
        return redirect('avion_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objet': avion,
        'type_objet': "l'avion",
        'retour_url': 'avion_list',
    })


# ---- Logique de recherche de piste libre ----

# Cette fonction cherche une piste disponible pour l'atterrissage.
# Le sujet demande qu'une piste soit bloquée 10 minutes autour de chaque atterrissage.
# On parcourt toutes les pistes de l'aéroport d'arrivée qui sont assez longues
# pour le type d'avion, et on vérifie qu'aucun autre vol n'arrive au même moment.
# Si toutes les pistes sont prises, on suggère 15 minutes plus tard.
def trouver_piste_libre(aeroport_arrivee, type_avion, heure_arrivee):

    # On filtre les pistes dont la longueur est suffisante pour ce type d'avion
    pistes_assez_longues = Piste.objects.filter(
        aeroport=aeroport_arrivee,
        longueur__gte=type_avion.longueur_piste_necessaire
    )

    # Cas où aucune piste de cet aéroport n'est compatible avec ce type d'avion
    if not pistes_assez_longues:
        return None, None

    # On teste chaque piste une par une
    for piste in pistes_assez_longues:

        # La piste est "occupée" entre heure_arrivee - 10min et heure_arrivee + 10min
        debut_occupation = heure_arrivee - timedelta(minutes=10)
        fin_occupation = heure_arrivee + timedelta(minutes=10)

        # On cherche si un vol utilise déjà cette piste dans cet intervalle
        # __gte = supérieur ou égal, __lte = inférieur ou égal (filtres Django)
        vols_sur_cette_piste = Vol.objects.filter(
            piste_arrivee=piste,
            datetime_arrivee__gte=debut_occupation,
            datetime_arrivee__lte=fin_occupation
        )

        # Si aucun vol n'occupe la piste à ce moment, elle est libre
        if not vols_sur_cette_piste:
            return piste, heure_arrivee

    # Aucune piste n'est libre : on propose un créneau 15 minutes plus tard
    heure_suggeree = heure_arrivee + timedelta(minutes=15)
    return None, heure_suggeree


# ---- Vols ----

def vol_list(request):
    vols = Vol.objects.all()
    return render(request, 'gestion/vol_list.html', {'vols': vols})


def vol_create(request):
    suggestion = None

    if request.method == 'POST':
        form = VolForm(request.POST)
        if form.is_valid():
            # On utilise commit=False pour ne pas encore sauvegarder en base.
            # Cela nous permet de récupérer les données du vol (notamment l'avion
            # et l'aéroport d'arrivée) pour trouver une piste, avant d'enregistrer.
            vol = form.save(commit=False)

            # On récupère le type d'avion pour connaître la longueur de piste nécessaire
            type_avion = vol.avion.modele

            piste, heure = trouver_piste_libre(vol.aeroport_arrivee, type_avion, vol.datetime_arrivee)

            if piste is None and heure is None:
                # Aucune piste de cet aéroport n'est compatible avec ce type d'avion
                messages.error(request, "Aucune piste compatible avec ce type d'avion dans cet aéroport.")

            elif piste is None:
                # Des pistes existent mais elles sont toutes occupées à l'heure demandée
                suggestion = heure
                messages.warning(request, "Toutes les pistes sont occupées à cette heure. Créneau suggéré : " + heure.strftime('%d/%m/%Y à %H:%M'))

            else:
                # On assigne la piste trouvée au vol, puis on sauvegarde
                vol.piste_arrivee = piste
                vol.save()
                messages.success(request, "Vol créé ! Piste assignée : " + piste.numero)
                return redirect('vol_list')

    else:
        form = VolForm()

    return render(request, 'gestion/vol_form.html', {
        'form': form,
        'titre': 'Nouveau vol',
        'suggestion': suggestion,
    })


def vol_update(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    suggestion = None

    if request.method == 'POST':
        form = VolForm(request.POST, instance=vol)
        if form.is_valid():
            vol_modifie = form.save(commit=False)
            type_avion = vol_modifie.avion.modele

            piste, heure = trouver_piste_libre(vol_modifie.aeroport_arrivee, type_avion, vol_modifie.datetime_arrivee)

            if piste is None and heure is None:
                messages.error(request, "Aucune piste compatible à l'aéroport d'arrivée.")
            elif piste is None:
                suggestion = heure
                messages.warning(request, "Toutes les pistes sont occupées. Créneau suggéré : " + heure.strftime('%d/%m/%Y à %H:%M'))
            else:
                vol_modifie.piste_arrivee = piste
                vol_modifie.save()
                messages.success(request, "Vol modifié ! Piste assignée : " + piste.numero)
                return redirect('vol_list')
    else:
        form = VolForm(instance=vol)

    return render(request, 'gestion/vol_form.html', {
        'form': form,
        'titre': 'Modifier le vol',
        'suggestion': suggestion,
    })


def vol_delete(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    if request.method == 'POST':
        vol.delete()
        messages.success(request, "Vol supprimé.")
        return redirect('vol_list')
    return render(request, 'gestion/confirm_delete.html', {
        'objet': vol,
        'type_objet': 'le vol',
        'retour_url': 'vol_list',
    })


# Fiche des vols : affiche les départs et/ou arrivées d'un aéroport sur une période donnée
def vol_fiche(request):
    vols_depart = []
    vols_arrivee = []
    form = FicheVolsForm(request.GET or None)

    if form.is_valid():
        aeroport = form.cleaned_data['aeroport']
        date_debut = form.cleaned_data['date_debut']
        date_fin = form.cleaned_data['date_fin']
        sens = form.cleaned_data['sens']

        # On construit deux datetimes : minuit le jour de début, 23h59 le jour de fin
        debut = timezone.make_aware(datetime(date_debut.year, date_debut.month, date_debut.day, 0, 0))
        fin = timezone.make_aware(datetime(date_fin.year, date_fin.month, date_fin.day, 23, 59))

        if sens == 'depart' or sens == 'les_deux':
            vols_depart = Vol.objects.filter(
                aeroport_depart=aeroport,
                datetime_depart__gte=debut,
                datetime_depart__lte=fin
            ).order_by('datetime_depart')

        if sens == 'arrivee' or sens == 'les_deux':
            vols_arrivee = Vol.objects.filter(
                aeroport_arrivee=aeroport,
                datetime_arrivee__gte=debut,
                datetime_arrivee__lte=fin
            ).order_by('datetime_arrivee')

    return render(request, 'gestion/vol_fiche.html', {
        'form': form,
        'vols_depart': vols_depart,
        'vols_arrivee': vols_arrivee,
    })


# Import de vols depuis un fichier CSV
# Colonnes attendues : avion_id, pilote, datetime_depart, aeroport_arrivee_id, datetime_arrivee
# Le format de date attendu est : YYYY-MM-DD HH:MM  (ex: 2026-06-01 08:00)
def vol_import(request):
    nb_ok = 0
    nb_erreurs = 0
    form = ImportVolsForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        aeroport_depart = form.cleaned_data['aeroport_depart']
        fichier = form.cleaned_data['fichier']

        # On lit le fichier texte et on le passe à csv.DictReader
        # DictReader utilise la première ligne comme noms de colonnes
        contenu = fichier.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(contenu))

        for ligne in reader:
            try:
                # On récupère l'avion et l'aéroport d'arrivée depuis leurs identifiants
                avion = Avion.objects.get(pk=int(ligne['avion_id']))
                aeroport_arrivee = Aeroport.objects.get(pk=int(ligne['aeroport_arrivee_id']))

                # On convertit les chaînes de caractères en objets datetime
                dt_depart = timezone.make_aware(
                    datetime.strptime(ligne['datetime_depart'].strip(), '%Y-%m-%d %H:%M')
                )
                dt_arrivee = timezone.make_aware(
                    datetime.strptime(ligne['datetime_arrivee'].strip(), '%Y-%m-%d %H:%M')
                )

                # On vérifie qu'une piste est disponible à l'heure d'arrivée
                piste, heure = trouver_piste_libre(aeroport_arrivee, avion.modele, dt_arrivee)

                if piste is None:
                    nb_erreurs += 1
                    continue

                Vol.objects.create(
                    avion=avion,
                    pilote=ligne['pilote'].strip(),
                    aeroport_depart=aeroport_depart,
                    datetime_depart=dt_depart,
                    aeroport_arrivee=aeroport_arrivee,
                    datetime_arrivee=heure,
                    piste_arrivee=piste,
                )
                nb_ok += 1

            except Exception:
                nb_erreurs += 1

        messages.success(request, str(nb_ok) + " vol(s) importé(s). " + str(nb_erreurs) + " ligne(s) ignorée(s).")

    return render(request, 'gestion/vol_import.html', {'form': form})
