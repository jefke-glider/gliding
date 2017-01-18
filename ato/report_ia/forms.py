from django.forms import ModelForm, Textarea
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Voorval, Club, Maatregel

class VoorvalForm(ModelForm):

    class Meta:
        model = Voorval

        ordering = ['-datum']
        fields = ( 'datum', 'uur', 'type_voorval', 'synopsis', 'opleiding', 'startwijze' ,
                   'type_toestel', 'kern_activiteit', 'muopo', 'menselijke_schade',
                   'materiele_schade', 'schade_omschrijving', 'ato', 'potentieel_risico')
        help_texts = { 'uur' : 'uur van het voorval in formaat hh:mm',
                       'type_voorval' : 'Duid aan welk type voorval het is',
                       'synopsis' : 'omschrijving van het voorval',
                      }
        widgets = {
            'datum': forms.DateInput(attrs={'class': 'datepicker'}),
        }

        def __init__(self, *args, **kwargs):
            super(VoorvalForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                help_text = self.fields[field].help_text
                self.fields[field].help_text = ''
                if help_text != '':
                    self.fields[field].widget.attrs.update(
                        {'class':'has-popover', 'data-content':help_text, 'data-placement':'right',
                         'data-container':'body'})

class MaatregelForm(ModelForm):
    synopsis = forms.CharField(label='synopsis voorval',
                               required=False,
                               widget=forms.Textarea(attrs={'cols': '80', 'rows':'10', 'disabled':True}))
    in_werking = forms.DateField(required=False,
                                 widget=forms.DateInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        model = Maatregel
        fields = ('synopsis', 'omschrijving', 'in_werking')
        labels = {'omschrijving' : 'omschrijving maatregel'}
        help_texts = { 'synopsis' : 'Omschrijving van het voorval' , },


class ExportForm(forms.Form):
    TYPE_EXPORT = (
        (1, "CSV"),
        )
    
    TABLES = (
#        (1, 'Voorvallen'),
        (1, 'Voorvallen - Maatregelen'),
#        (3, 'Voorvallen-maatregelen'),
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
    export_date_from = forms.DateField(label='datum vanaf', required=False,
                                       widget=forms.DateInput(attrs={'format':'%m/%d/%Y',
                                                                     'class':'datepicker'}),
                                                                                          
                                       )
    export_date_till = forms.DateField(label='datum tot', required=False,
                                       widget=forms.DateInput(attrs={'class': 'datepicker'}))
    #we autogenerate the filename for now
#    filename = forms.CharField(label='bestandsnaam', max_length=100,
#                               help_text='geef bestandsnaam met juiste extentie (.csv)')
    club_to_export = forms.ModelChoiceField(queryset=clubs, empty_label="Alle clubs", required=False,
                                            help_text='selecteer de club of geen voor alle clubs',
                                            )
    



           
        
