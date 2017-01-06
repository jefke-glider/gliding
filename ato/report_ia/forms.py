
from django.forms import ModelForm
from django import forms

from .models import Voorval, Club

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


class ExportForm(forms.Form):
    TYPE_EXPORT = (
        (1, "CSV"),
        (2, "PDF"))
    
    TABLES = (
        (1, 'Voorvallen'),
        (2, 'Vliegvelden'),
        (3, 'Clubs'),
        (4, 'Opleidingen'),
        (5, 'Startwijzen'),
        )

    clubs = Club.objects.values_list('id','naam')
    type_export = forms.ChoiceField(TYPE_EXPORT, label='type export', initial=1, help_text='geef het type bestand aan')
    tabel_to_export = forms.ChoiceField(TABLES, label='tabel', initial=1)
    export_date_from = forms.DateField(label='datum vanaf', required=False)
    export_date_to = forms.DateField(label='datum tot', required=False)
    club_to_export = forms.TypedChoiceField(clubs, required=False, empty_value=None)
    filename = forms.CharField(label='bestandsnaam', max_length=100)


    class Meta:
        help_texts = {
            'clubs': ('Data van welke club exporteren'),
            }
