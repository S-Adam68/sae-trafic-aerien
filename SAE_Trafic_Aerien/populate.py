import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trafic_aerien.settings')
django.setup()

from django.utils import timezone
from gestion.models import Aeroport, Piste, Compagnie, TypeAvion, Avion, Vol

print("Nettoyage des données existantes...")
Vol.objects.all().delete()
Avion.objects.all().delete()
TypeAvion.objects.all().delete()
Compagnie.objects.all().delete()
Piste.objects.all().delete()
Aeroport.objects.all().delete()

print("Création des aéroports...")
cdg = Aeroport.objects.create(nom="Charles de Gaulle", pays="France")
orly = Aeroport.objects.create(nom="Paris Orly", pays="France")
lhr = Aeroport.objects.create(nom="London Heathrow", pays="Royaume-Uni")
ams = Aeroport.objects.create(nom="Amsterdam Schiphol", pays="Pays-Bas")
mad = Aeroport.objects.create(nom="Madrid Barajas", pays="Espagne")
fco = Aeroport.objects.create(nom="Rome Fiumicino", pays="Italie")

print("Création des pistes...")
Piste.objects.create(aeroport=cdg, numero="09L", longueur=4200)
Piste.objects.create(aeroport=cdg, numero="09R", longueur=2700)
Piste.objects.create(aeroport=cdg, numero="27L", longueur=3600)
Piste.objects.create(aeroport=orly, numero="08",  longueur=3650)
Piste.objects.create(aeroport=orly, numero="26",  longueur=2400)
Piste.objects.create(aeroport=lhr, numero="09L", longueur=3902)
Piste.objects.create(aeroport=lhr, numero="27R", longueur=3660)
Piste.objects.create(aeroport=ams, numero="18R", longueur=3800)
Piste.objects.create(aeroport=ams, numero="36L", longueur=3400)
Piste.objects.create(aeroport=mad, numero="18L", longueur=4350)
Piste.objects.create(aeroport=mad, numero="32R", longueur=3500)
Piste.objects.create(aeroport=fco, numero="16R", longueur=3900)
Piste.objects.create(aeroport=fco, numero="34L", longueur=3600)

print("Création des compagnies...")
af  = Compagnie.objects.create(nom="Air France", pays_rattachement="France",
      description="Compagnie nationale française fondée en 1933.")
ba  = Compagnie.objects.create(nom="British Airways", pays_rattachement="Royaume-Uni",
      description="Compagnie nationale britannique, membre de l'alliance Oneworld.")
klm = Compagnie.objects.create(nom="KLM", pays_rattachement="Pays-Bas",
      description="Royal Dutch Airlines, fondée en 1919, plus ancienne compagnie aérienne au monde.")
ib  = Compagnie.objects.create(nom="Iberia", pays_rattachement="Espagne",
      description="Compagnie nationale espagnole, fondée en 1927.")
az  = Compagnie.objects.create(nom="ITA Airways", pays_rattachement="Italie",
      description="Successeur d'Alitalia, compagnie nationale italienne.")
u2  = Compagnie.objects.create(nom="easyJet", pays_rattachement="Royaume-Uni",
      description="Compagnie low-cost européenne basée à Luton.")

print("Création des types d'avions...")
a320 = TypeAvion.objects.create(marque="Airbus", modele="A320",
       description="Avion moyen-courrier très répandu, capacité ~180 passagers.", longueur_piste_necessaire=2100)
a330 = TypeAvion.objects.create(marque="Airbus", modele="A330-300",
       description="Long-courrier bimoteur, capacité ~290 passagers.", longueur_piste_necessaire=3000)
a380 = TypeAvion.objects.create(marque="Airbus", modele="A380",
       description="Le plus grand avion de ligne, capacité ~555 passagers.", longueur_piste_necessaire=3100)
b737 = TypeAvion.objects.create(marque="Boeing", modele="737-800",
       description="Moyen-courrier très populaire, capacité ~162 passagers.", longueur_piste_necessaire=2090)
b777 = TypeAvion.objects.create(marque="Boeing", modele="777-300ER",
       description="Long-courrier bimoteur, capacité ~396 passagers.", longueur_piste_necessaire=3050)
b787 = TypeAvion.objects.create(marque="Boeing", modele="787-9",
       description="Dreamliner long-courrier, capacité ~296 passagers.", longueur_piste_necessaire=2800)

print("Création des avions...")
avions = [
    Avion.objects.create(nom="F-GKXA", compagnie=af,  modele=a320),
    Avion.objects.create(nom="F-GSQI", compagnie=af,  modele=a380),
    Avion.objects.create(nom="F-HJAZ", compagnie=af,  modele=b787),
    Avion.objects.create(nom="G-EUYA", compagnie=ba,  modele=a320),
    Avion.objects.create(nom="G-STBH", compagnie=ba,  modele=b777),
    Avion.objects.create(nom="PH-BXA", compagnie=klm, modele=b737),
    Avion.objects.create(nom="PH-BQA", compagnie=klm, modele=b777),
    Avion.objects.create(nom="EC-LQM", compagnie=ib,  modele=a320),
    Avion.objects.create(nom="EC-MKL", compagnie=ib,  modele=a330),
    Avion.objects.create(nom="EI-DTG", compagnie=az,  modele=a320),
    Avion.objects.create(nom="G-EZWA", compagnie=u2,  modele=a320),
    Avion.objects.create(nom="G-EZOP", compagnie=u2,  modele=a320),
]

print("Création des vols...")
now = timezone.now().replace(minute=0, second=0, microsecond=0)

vols_data = [
    (avions[0],  "Martin Dupont",    cdg,  now + timedelta(hours=1),  orly, now + timedelta(hours=2)),
    (avions[1],  "Sophie Laurent",   cdg,  now + timedelta(hours=2),  lhr,  now + timedelta(hours=3, minutes=30)),
    (avions[2],  "Pierre Moreau",    orly, now + timedelta(hours=1, minutes=30), ams, now + timedelta(hours=3)),
    (avions[3],  "James Smith",      lhr,  now + timedelta(hours=3),  cdg,  now + timedelta(hours=4, minutes=15)),
    (avions[4],  "Emma Johnson",     lhr,  now + timedelta(hours=4),  mad,  now + timedelta(hours=6)),
    (avions[5],  "Hans Müller",      ams,  now + timedelta(hours=2),  cdg,  now + timedelta(hours=3, minutes=20)),
    (avions[6],  "Anna De Vries",    ams,  now + timedelta(hours=5),  lhr,  now + timedelta(hours=6)),
    (avions[7],  "Carlos García",    mad,  now + timedelta(hours=1),  fco,  now + timedelta(hours=3, minutes=30)),
    (avions[8],  "María Rodríguez",  mad,  now + timedelta(hours=6),  cdg,  now + timedelta(hours=8)),
    (avions[9],  "Luca Bianchi",     fco,  now + timedelta(hours=2),  orly, now + timedelta(hours=4)),
    (avions[10], "Tom Wilson",       cdg,  now + timedelta(hours=3),  ams,  now + timedelta(hours=4, minutes=40)),
    (avions[11], "Julie Petit",      orly, now + timedelta(hours=4),  lhr,  now + timedelta(hours=5, minutes=15)),
    (avions[0],  "Nicolas Bernard",  lhr,  now + timedelta(hours=7),  orly, now + timedelta(hours=8, minutes=20)),
    (avions[3],  "Sarah Brown",      cdg,  now + timedelta(hours=8),  fco,  now + timedelta(hours=10)),
    (avions[5],  "Pieter Jansen",    ams,  now + timedelta(hours=9),  mad,  now + timedelta(hours=11, minutes=30)),
]

from gestion.views import trouver_piste_libre

created = 0
for avion, pilote, ap_dep, dt_dep, ap_arr, dt_arr in vols_data:
    piste, _ = trouver_piste_libre(ap_arr, avion.modele, dt_arr)
    Vol.objects.create(
        avion=avion, pilote=pilote,
        aeroport_depart=ap_dep, datetime_depart=dt_dep,
        aeroport_arrivee=ap_arr, datetime_arrivee=dt_arr,
        piste_arrivee=piste,
    )
    created += 1

print(f"\nTerminé !")
print(f"  {Aeroport.objects.count()} aéroports")
print(f"  {Piste.objects.count()} pistes")
print(f"  {Compagnie.objects.count()} compagnies")
print(f"  {TypeAvion.objects.count()} types d'avions")
print(f"  {Avion.objects.count()} avions")
print(f"  {Vol.objects.count()} vols")
