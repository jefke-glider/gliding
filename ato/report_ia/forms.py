from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Voorval, Club, Maatregel, AantalStarts, Bestand

class VoorvalForm(ModelForm):
    zoek_type_toestel = forms.CharField(label="zoek type toestel", required = False)
#    type_toestel = forms.CharField(label='', widget = forms.HiddenInput(), required = False)
#    type_toestel = forms.CharField(label='geselecteerd type toestel', required = False)
    boolean_set = ( 'mens', 'uitrusting', 'omgeving', 'product', 'organisatie' )
                               
    class Meta:
        model = Voorval

        ordering = ['-datum']
        fields = ( 'datum', 'uur', 'locatie', 'andere_locatie',
                   'ato', 'type_voorval', 'synopsis', 'opleiding', 'startwijze' ,
                   'zoek_type_toestel', 'type_toestel', 'kern_activiteit', 
                   'mens', 'uitrusting', 'omgeving', 'product', 'organisatie',
                   'type_schade', 'schade_omschrijving',
                   'potentieel_risico')
        help_texts = { 'uur' : 'uur van het voorval in formaat hh:mm',
                       'type_voorval' : 'Duid aan welk type voorval het is',
                       'synopsis' : 'omschrijving van het voorval',
                       'datum':'kies een datum',
                       'mens' : 'een menselijke fout ligt aan de oorzaak',
                      }
##        labels = { 'mens' : 'M', }
##         widgets = {
##             'datum': forms.DateInput(),
##         }

    def __init__(self, *args, **kwargs):
        super(VoorvalForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = ''
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class':'has-popover', 'data-content':help_text, 'data-placement':'bottom',
                     'data-container':'body', 'title':'ingave voorval'})
        self.fields['datum'].widget.attrs.update({
            'class': 'has-popover datepicker'
        })
        self.fields['andere_locatie'].required = False;
        self.fields['schade_omschrijving'].required = False;

class MaatregelForm(ModelForm):
    synopsis = forms.CharField(label='synopsis voorval',
                               required=False,
                               widget=forms.Textarea(attrs={'cols': '80',
                                                            'rows':'10', 'disabled':True}))
    in_werking = forms.DateField(required=False,
                                 widget=forms.DateInput(attrs={'format':'%d/%m/%Y',
                                                               'class': 'datepicker'}))
    
    class Meta:
        model = Maatregel
        fields = ('synopsis', 'omschrijving', 'in_werking')
        labels = {'omschrijving' : 'omschrijving maatregel'}
        help_texts = { 'synopsis' : 'Omschrijving van het voorval' ,
                       'omschrijving' : 'beschrijf de genomen maatregel (1 per keer)',
                       'in_werking' : 'vanaf wanneer is deze maatregel in werking getreden?'
                       }

    def __init__(self, *args, **kwargs):
        super(MaatregelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = ''
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class':'has-popover', 'data-content':help_text, 'data-placement':'bottom',
                     'data-container':'body', 'title':'ingave maatregel'})
        self.fields['in_werking'].widget.attrs.update({
                'class': 'has-popover datepicker'
                })
    

class UploadFileForm(ModelForm):
    synopsis = forms.CharField(label='synopsis voorval',
                               required=False,
                               widget=forms.Textarea(attrs={'cols': '80',
                                                            'rows':'10', 'disabled':True}))

    class Meta:
        model = Bestand
        fields = ('synopsis', 'bestand', 'opmerking')
        labels = {'Selecteer Bestand', 'Geef eventueel een omschrijving' }


class ExportForm(forms.Form):
    TYPE_EXPORT = (
        (1, "CSV"),
        )
    
    TABLES = (
        (1, 'Voorvallen - Maatregelen'),
        (2, 'Starts'),
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
                                       widget=forms.DateInput(attrs={'format':'%m/%d/%Y',
                                                                     'class': 'datepicker'}))
    #we autogenerate the filename for now
#    filename = forms.CharField(label='bestandsnaam', max_length=100,
#                               help_text='geef bestandsnaam met juiste extentie (.csv)')
    club_to_export = forms.ModelChoiceField(queryset=clubs, empty_label="Alle clubs",
                                            required=False,
                                            help_text='selecteer de club of geen voor alle clubs',
                                            )
    
class StartsForm(ModelForm):
    op_datum = forms.DateField(required=True,
                               widget=forms.DateInput(attrs={'format':'%d/%m/%Y',
                                                             'class': 'datepicker'}))

    def clean(self, *args, **kwargs):
        cleaned_data = super(StartsForm, self).clean()
        totaal=0
        totaal+=int(cleaned_data.get('lier'))
        totaal+=int(cleaned_data.get('ato_lier'))
        totaal+=int(cleaned_data.get('sleep'))
        totaal+=int(cleaned_data.get('ato_sleep'))
        totaal+=int(cleaned_data.get('zelf'))
        totaal+=int(cleaned_data.get('ato_zelf'))
        if totaal <= 0:
            raise forms.ValidationError("Gelieve aantal starts in te vullen")
        else:
            self.cleaned_data['totaal'] = totaal
            return self.cleaned_data

    class Meta:
        model = AantalStarts
        fields = ('club', 'lier', 'ato_lier', 'sleep', 'ato_sleep', 'zelf', 'ato_zelf', 'totaal')


           
        
