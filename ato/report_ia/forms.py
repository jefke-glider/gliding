from django.forms import ModelForm
from django import forms

from .models import Voorval

class VoorvalForm(ModelForm):

    class Meta:
        model = Voorval
        fields = ( 'datum', 'uur', 'type_voorval', 'synopsis', 'opleiding', 'startwijze' ,
                   'type_toestel', 'kern_activiteit', 'muopo', 'menselijke_schade',
                   'materiele_schade', 'schade_omschrijving')
        help_texts = {
            'datum': ('Datum van het voorval.'),
            'uur': ('Uur van het voorval.'),
            'type_voorval': ('Wat soort voorval betreft het hier'),
            'synopsis': ('Geeft een omschrijving van het voorval'),
            'opleiding': ('De opleiding waarin de leerling zich momenteel bevindt'),
            'startwijze': ('Geef de startwijze aan'),
            },
        widgets = {
            'datum': forms.DateInput(attrs={'class': 'datepicker'}),
        }

