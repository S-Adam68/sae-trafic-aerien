from django.db import models


class Aeroport(models.Model):
    nom = models.CharField(max_length=200)
    pays = models.CharField(max_length=100)

    def __str__(self):
        return self.nom + " (" + self.pays + ")"

    class Meta:
        verbose_name = "Aéroport"
        verbose_name_plural = "Aéroports"


class Piste(models.Model):
    numero = models.CharField(max_length=20)
    # ForeignKey : chaque piste appartient à un aéroport
    # CASCADE = si on supprime l'aéroport, ses pistes sont supprimées aussi
    aeroport = models.ForeignKey(Aeroport, on_delete=models.CASCADE)
    longueur = models.PositiveIntegerField()

    def __str__(self):
        return "Piste " + self.numero + " - " + self.aeroport.nom

    class Meta:
        verbose_name = "Piste"
        verbose_name_plural = "Pistes"


class Compagnie(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pays_rattachement = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Compagnie"
        verbose_name_plural = "Compagnies"


# TypeAvion représente un modèle d'avion (ex: Boeing 737, Airbus A320)
# Un avion concret est une instance du modèle Avion ci-dessous
class TypeAvion(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='types_avions/', blank=True, null=True)
    longueur_piste_necessaire = models.PositiveIntegerField()

    def __str__(self):
        return self.marque + " " + self.modele

    class Meta:
        verbose_name = "Type d'avion"
        verbose_name_plural = "Types d'avions"


class Avion(models.Model):
    nom = models.CharField(max_length=200)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)
    modele = models.ForeignKey(TypeAvion, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Avion"
        verbose_name_plural = "Avions"


class Vol(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    pilote = models.CharField(max_length=200)

    # On a deux ForeignKey vers Aeroport (départ et arrivée).
    # Django demande un related_name différent pour chacune,
    # sinon il ne sait pas comment nommer l'accès inverse.
    aeroport_depart = models.ForeignKey(Aeroport, on_delete=models.CASCADE, related_name='vols_depart')
    datetime_depart = models.DateTimeField()
    aeroport_arrivee = models.ForeignKey(Aeroport, on_delete=models.CASCADE, related_name='vols_arrivee')
    datetime_arrivee = models.DateTimeField()

    # La piste est assignée automatiquement à la création du vol.
    # null=True permet de laisser ce champ vide si aucune piste n'est encore assignée.
    piste_arrivee = models.ForeignKey(Piste, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "Vol " + str(self.pk) + " : " + self.aeroport_depart.nom + " -> " + self.aeroport_arrivee.nom

    class Meta:
        verbose_name = "Vol"
        verbose_name_plural = "Vols"
