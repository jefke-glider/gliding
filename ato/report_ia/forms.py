from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Voorval, Club, Maatregel, AantalStarts, Bestand

class VoorvalForm(ModelForm):
#    zoek_type_toestel = forms.CharField(label="zoek type toestel", required = False)
#    type_toestel = forms.CharField(label='', widget = forms.HiddenInput(), required = False)
#    type_toestel = forms.CharField(label='geselecteerd type toestel', required = False)
    boolean_set = ( 'mens', 'uitrusting', 'omgeving', 'product', 'organisatie' )
                               
    class Meta:
        model = Voorval

        ordering = ['-datum']
        fields = ( 'datum', 'uur', 'locatie', 'andere_locatie',
                   'ato', 'opleiding', 'type_voorval', 'synopsis',  'startwijze' ,
                   'type_toestel', 'kern_activiteit',
                   'windsterkte', 'windrichting', 'wolken', 'wolkenbasis', 'thermiek', 'zichtbaarheid',
                   'mens', 'uitrusting', 'omgeving', 'product', 'organisatie',
                   'type_schade', 'schade_omschrijving',
                   'potentieel_risico')
        help_texts = { 'uur' : 'uur van het voorval in formaat hh:mm',
                       'type_voorval' : """
Een incident is een voorval dat verband houdt met het functioneren van een luchtvaartuig en dat afbreuk doet of zou kunnen doen aan veilige vluchtuitvoering,met uitzondering van een ongeval – OFWEL EEN ONVEILIGE SITUATIE
Een ernstig incident is een incident dat zich voordoet onder omstandigheden die erop wijzen dat bijna een ongeval heeft plaatsgevonden – OFWEL EEN SCHIERONGEVAL
Een ongeval is een voorval dat verband houdt met het gebruik van een luchtvaartuig waarbij:
- een persoon dodelijk of ernstig gewond raakt 
- het luchtvaartuig schade of een structureel defect oploop
- het luchtvaartuig vermist of volledig onbereikbaar is
	<b>OFWEL EEN ACCIDENT</b>
""",
                       'synopsis' : 'omschrijf hier chronologisch en objectief wat er gebeurd is',
                       'mens' : 'persoonlijke gedragsbepalende factoren',                       
                       'uitrusting' : 'alle gebruikte hardware, technische factoren',
                       'omgeving' : 'gehele vliegomgeving en -inrichting',
                       'product' : 'het proces/wat vervaardigd of bewerkt wordt',
                       'organisatie' : 'beleid en werkorganisatie',
                       'kern_activiteit': 'de activiteit die werd uitgevoerd op het moment dat het fout is gelopen',
                       'windsterkte' : 'in knopen',
                       'wolken' : 'in okta\'s',
                       'thermiek' : 'in m/s',
                       'wolkenbasis' : 'in feet',
                       'zichtbaarheid' : 'in km',
                      }
        labels = { 'ato' : 'ATO' ,}
##        labels = { 'mens' : 'M', }
##         widgets = {
##             'datum': forms.DateInput(),
##         }

    def __init__(self, *args, **kwargs):
        super(VoorvalForm, self).__init__(*args, **kwargs)
##         for field in self.fields:
##             help_text = self.fields[field].help_text
##             self.fields[field].help_text = ''
##             if help_text != '':
##                 self.fields[field].widget.attrs.update(
##                     {'class':'has-popover', 'data-content':help_text, 'data-placement':'bottom',
##                      'data-container':'body', 'title':'ingave voorval'})
        self.fields['datum'].widget.attrs.update({
            'class': 'has-popover datepicker'
        })
        self.fields['andere_locatie'].required = False;
        self.fields['schade_omschrijving'].required = False;
        for field in self.fields:
            self.fields[field].widget.attrs.update({'title':''})

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
##         for field in self.fields:
##             help_text = self.fields[field].help_text
##             self.fields[field].help_text = ''
##             if help_text != '':
##                 self.fields[field].widget.attrs.update(
##                     {'class':'has-popover', 'data-content':help_text, 'data-placement':'bottom',
##                      'data-container':'body', 'title':'ingave maatregel'})
        self.fields['in_werking'].widget.attrs.update({
                'class': 'datepicker'
                })
        for field in self.fields:
            self.fields[field].widget.attrs.update({'title':''})
    

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
        fields = ('club',
                  'lier','sleep', 'zelf','auto','bungee',
                  'ato_lier','ato_sleep','ato_zelf','ato_auto','ato_bungee',
                  'totaal',
                  'vliegdagen', 'ato_vliegdagen')
        
        labels = { 'lier' : 'Non ATO lier',
                   'sleep' : 'Non ATO sleep',
                   'zelf' : 'Non ATO zelf',
                   'auto' : 'Non ATO auto',
                   'bungee' : 'Non ATO bungee',
                   'ato_lier' : 'ATO lier',
                   'ato_sleep' : 'ATO sleep',
                   'ato_zelf' : 'ATO zelf',
                   'ato_auto' : 'ATO auto',
                   'ato_bungee' : 'ATO bungee',
                   'vliegdagen' : 'Non ATO vliegdagen',
                   'ato_vliegdagen' : 'ATO vliegdagen'}
        help_texts = {'vliegdagen' : 'geldt voor elke dag waarvoor het vliegplein werd geopend, dit ongeacht de duurtijd van de dag en het aantal starten', }


           
        
