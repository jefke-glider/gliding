from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Voorval, Club, Maatregel, AantalStarts, Bestand

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
                       'datum':'kies een datum',
                      }
##         widgets = {
##             'datum': forms.DateInput(),
##         }

    def __init__(self, *args, **kwargs):
        print('init voorvalform')
        super(VoorvalForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            print(help_text)
            self.fields[field].help_text = ''
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class':'has-popover', 'data-content':help_text, 'data-placement':'bottom',
                     'data-container':'body', 'title':'ingave voorval'})
        self.fields['datum'].widget.attrs.update({
            'class': 'has-popover datepicker'
        })

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
        print('init maatregelform')
        super(MaatregelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            print(help_text)
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
            print(self.cleaned_data)
            self.cleaned_data['totaal'] = totaal
            return self.cleaned_data

    class Meta:
        model = AantalStarts
        fields = ('club', 'lier', 'ato_lier', 'sleep', 'ato_sleep', 'zelf', 'ato_zelf', 'totaal')


           
        
