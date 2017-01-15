
from django.forms import ModelForm, Textarea
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Voorval, Club, Maatregel

class VoorvalForm(ModelForm):

    class Meta:
        model = Voorval
        fields = ( 'datum', 'uur', 'type_voorval', 'synopsis', 'opleiding', 'startwijze' ,
                   'type_toestel', 'kern_activiteit', 'muopo', 'menselijke_schade',
                   'materiele_schade', 'schade_omschrijving')
        help_texts = {
            'datum': _('Datum van het voorval.'),
            'uur': _('Uur van het voorval.'),
            'type_voorval': _('Wat soort voorval betreft het hier'),
            'synopsis': _('Geeft een omschrijving van het voorval'),
            'opleiding': _('De opleiding waarin de leerling zich momenteel bevindt'),
            'startwijze': _('Geef de startwijze aan'),
            },
        widgets = {
            'datum': forms.DateInput(attrs={'class': 'datepicker'}),
        }

class MaatregelForm(ModelForm):
    synopsis = forms.CharField(label='synopsis voorval',
                               required=False,
                               widget=forms.Textarea(attrs={'cols': '80', 'rows':'10', 'disabled':True}))
    class Meta:
        model = Maatregel
        fields = ('synopsis', 'omschrijving',)
        labels = {'omschrijving' : 'omschrijving maatregel'}


class ExportForm(forms.Form):
    TYPE_EXPORT = (
        (1, "CSV"),
        )
    
    TABLES = (
        (1, 'Voorvallen'),
        (2, 'Maatregelen'),
        (3, 'Voorvallen-maatregelen'),
        )
##         (2, 'Vliegvelden'),
##         (3, 'Clubs'),
##         (4, 'Opleidingen'),
##         (5, 'Startwijzen'),
##         )

    clubs = Club.objects.all()
    type_export = forms.ChoiceField(TYPE_EXPORT, label='type export', initial=1,
                                    help_text='geef het type bestand aan')
    tabel_to_export = forms.ChoiceField(TABLES, label='tabel', 
                                        help_text='welke tabel exporteren')
    export_date_from = forms.DateField(label='datum vanaf', widget=forms.DateInput(format='%m/%d/%Y'),
                                       input_formats=('%m/%d/%Y',), required=False)
    export_date_till = forms.DateField(label='datum tot', required=False)
    club_to_export = forms.ModelChoiceField(queryset=clubs, empty_label="Alle clubs", required=False,
                                            help_text='selecteer de club of geen voor alle clubs')
    #we autogenerate the filename for now
#    filename = forms.CharField(label='bestandsnaam', max_length=100,
#                               help_text='geef bestandsnaam met juiste extentie (.csv)')
