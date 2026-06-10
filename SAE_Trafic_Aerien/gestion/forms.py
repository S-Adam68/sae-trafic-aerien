from django import forms
from .models import Aeroport, Piste, Compagnie, TypeAvion, Avion, Vol


class AeroportForm(forms.ModelForm):
    class Meta:
        model = Aeroport
        fields = ['nom', 'pays']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PisteForm(forms.ModelForm):
    class Meta:
        model = Piste
        fields = ['numero', 'aeroport', 'longueur']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'aeroport': forms.Select(attrs={'class': 'form-select'}),
            'longueur': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CompagnieForm(forms.ModelForm):
    class Meta:
        model = Compagnie
        fields = ['nom', 'description', 'pays_rattachement']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pays_rattachement': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TypeAvionForm(forms.ModelForm):
    class Meta:
        model = TypeAvion
        fields = ['marque', 'modele', 'description', 'image', 'longueur_piste_necessaire']
        widgets = {
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'modele': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'longueur_piste_necessaire': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ['nom', 'compagnie', 'modele']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'compagnie': forms.Select(attrs={'class': 'form-select'}),
            'modele': forms.Select(attrs={'class': 'form-select'}),
        }


class VolForm(forms.ModelForm):
    class Meta:
        model = Vol
        fields = ['avion', 'pilote', 'aeroport_depart', 'datetime_depart',
                  'aeroport_arrivee', 'datetime_arrivee']
        widgets = {
            'avion': forms.Select(attrs={'class': 'form-select'}),
            'pilote': forms.TextInput(attrs={'class': 'form-control'}),
            'aeroport_depart': forms.Select(attrs={'class': 'form-select'}),
            # type="datetime-local" est un champ HTML5 qui affiche un sélecteur de date + heure
            'datetime_depart': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'aeroport_arrivee': forms.Select(attrs={'class': 'form-select'}),
            'datetime_arrivee': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On doit préciser le format d'entrée pour que Django sache lire
        # la valeur renvoyée par le champ datetime-local du navigateur
        self.fields['datetime_depart'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['datetime_arrivee'].input_formats = ['%Y-%m-%dT%H:%M']

    # Validation : on vérifie que l'heure d'arrivée est bien après le départ
    def clean(self):
        cleaned_data = super().clean()
        depart = cleaned_data.get('datetime_depart')
        arrivee = cleaned_data.get('datetime_arrivee')

        if depart and arrivee:
            if depart >= arrivee:
                raise forms.ValidationError("L'heure d'arrivée doit être après l'heure de départ.")

        return cleaned_data


# Formulaire de recherche pour la fiche des vols (non lié à un modèle)
class FicheVolsForm(forms.Form):
    SENS_CHOICES = [
        ('depart', 'Vols au départ'),
        ('arrivee', 'Vols à destination'),
        ('les_deux', 'Les deux'),
    ]

    aeroport = forms.ModelChoiceField(
        queryset=Aeroport.objects.all(),
        label="Aéroport",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_debut = forms.DateField(
        label="Date de début",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_fin = forms.DateField(
        label="Date de fin",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    sens = forms.ChoiceField(
        choices=SENS_CHOICES,
        label="Type de vols",
        widget=forms.Select(attrs={'class': 'form-select'})
    )


# Formulaire pour l'import CSV (non lié à un modèle)
class ImportVolsForm(forms.Form):
    aeroport_depart = forms.ModelChoiceField(
        queryset=Aeroport.objects.all(),
        label="Aéroport de départ (commun à tous les vols du fichier)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fichier = forms.FileField(
        label="Fichier CSV",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
