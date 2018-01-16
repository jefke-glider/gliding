from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Voorval, Club, Maatregel, AantalStarts, Bestand, Club_mail

class VoorvalForm(ModelForm):
    boolean_set = ( 'mens', 'uitrusting', 'omgeving', 'product', 'organisatie' )
                               
    class Meta:
        model = Voorval

        ordering = ['-datum']
        fields = ( 'datum', 'uur', 'locatie', 'andere_locatie',
                   'domein', 'opleiding', 'type_voorval',
                   'type_schade', 'schade_omschrijving',
                   'synopsis',  'startwijze' ,
                   'type_toestel', 'kern_activiteit',
                   'windsterkte', 'windrichting', 'wolken', 'wolkenbasis', 'thermiek', 'zichtbaarheid', 'piste',
                   'mens', 'uitrusting', 'omgeving', 'product', 'organisatie',
                   'muopo_omschrijving',
                   )
        help_texts = { 'uur' : 'uur van het voorval in formaat hh:mm',
                       'synopsis' : 'omschrijf hier chronologisch en objectief wat er gebeurd is',
                       'mens' : 'gedrag, mentale en fysieke toestand',                       
                       'uitrusting' : 'de hardware, technische factoren, de infrastructuur, de middelen die nodig zijn voor de vliegactiviteiten',
                       'omgeving' : 'gehele vliegomgeving, klimatologische omstandigheden...',
                       'product' : 'het vlieggebeuren, de clubactiviteiten op zich',
                       'organisatie' : 'het clubbeleid, procedures, clubwerking, taakverdeling',
                       'kern_activiteit': 'de activiteit die werd uitgevoerd op het moment dat het fout is gelopen',
#                       'windsterkte' : 'in knopen',
#                       'wolken' : 'in okta\'s',
#                       'thermiek' : 'in m/s',
#                       'wolkenbasis' : 'in feet',
#                       'zichtbaarheid' : 'in km',
                       'muopo_omschrijving' : 'verduidelijk nader voor ELK aangeduid MUOPO ascpect',
                       'domein' : 'voorval valt al dan niet binnen/buiten ATO opleiding',
                       'piste' : 'welke piste was in gebruik, vb 07 of 25',
                      }
        labels = {  'muopo_omschrijving' : 'MUOPO omschrijving',
                    'synopsis' : 'relaas',
                    'zichtbaarheid' : 'zichtbaarheid van op de grond (km)',
                    'wolkenbasis' : 'wolkenbasis (ft)',
                    'thermiek' : 'thermiek (m/s)',
                    'windsterkte' : 'windsterkte (kts)',
                    'wolken' : 'wolken (okta\'s of 8 stes)',
}

    def __init__(self, *args, **kwargs):
        super(VoorvalForm, self).__init__(*args, **kwargs)
        self.fields['datum'].widget.attrs.update({
            'class': 'has-popover datepicker'
        })
        self.fields['andere_locatie'].required = False
        self.fields['schade_omschrijving'].required = False
        self.fields['windsterkte'].required = False
        self.fields['windrichting'].required = False
        self.fields['wolken'].required = False
        self.fields['wolkenbasis'].required = False
        self.fields['thermiek'].required = False
        self.fields['zichtbaarheid'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs.update({'title':''})

class MaatregelForm(ModelForm):
    synopsis = forms.CharField(label='relaas voorval',
                               required=False,
                               widget=forms.Textarea(attrs={'cols': '80',
                                                            'rows':'10', 'disabled':True}))
    in_werking = forms.DateField(required=False,
                                 widget=forms.DateInput(attrs={'format':'%d/%m/%Y',
                                                               'class': 'datepicker'}))
    
    class Meta:
        model = Maatregel
        fields = ('synopsis', 'omschrijving', 'in_werking')
        labels = {'omschrijving' : 'omschrijving maatregel',
                  'synopsis' : 'relaas'}
        help_texts = { 'synopsis' : 'Omschrijving van het voorval' ,
                       'omschrijving' : 'beschrijf de genomen maatregel (1 per keer)',
                       'in_werking' : 'vanaf wanneer is deze maatregel in werking getreden?'
                       }

    def __init__(self, *args, **kwargs):
        super(MaatregelForm, self).__init__(*args, **kwargs)
        self.fields['in_werking'].widget.attrs.update({
                'class': 'datepicker'
                })
        for field in self.fields:
            self.fields[field].widget.attrs.update({'title':''})
    

class UploadFileForm(ModelForm):
    synopsis = forms.CharField(label='relaas voorval',
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
#    op_datum = forms.DateField(required=True,
#                               widget=forms.DateInput(attrs={'format':'%d/%m/%Y','class': 'datepicker'}))
 #   totaal_starts = forms.IntegerField(disabled=True)
    def clean(self, *args, **kwargs):
        cleaned_data = super(StartsForm, self).clean()
        totaal=0
        totaal+=int(cleaned_data.get('lier'))
        totaal+=int(cleaned_data.get('ato_lier'))
        totaal+=int(cleaned_data.get('sleep'))
        totaal+=int(cleaned_data.get('ato_sleep'))
        totaal+=int(cleaned_data.get('zelf'))
        totaal+=int(cleaned_data.get('ato_zelf'))
        totaal+=int(cleaned_data.get('auto'))
        totaal+=int(cleaned_data.get('ato_auto'))
        totaal+=int(cleaned_data.get('bungee'))
        totaal+=int(cleaned_data.get('ato_bungee'))
        print(totaal)
        if totaal <= 0:
            raise forms.ValidationError("Gelieve aantal starts in te vullen")
        else:
            self.cleaned_data['totaal_starts'] = totaal

        totaal_vd=0
        totaal_vd=int(cleaned_data.get('vliegdagen'))
        if totaal_vd <= 0:
            raise forms.ValidationError("Gelieve aantal vliegdagen in te vullen")
        print(self.cleaned_data)
        return self.cleaned_data

    class Meta:
        model = AantalStarts
        fields = ('club',
                  'lier','sleep', 'zelf','auto','bungee',
                  'ato_lier','ato_sleep','ato_zelf','ato_auto','ato_bungee',
                  'vliegdagen', 'totaal_starts')
        
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
                   }
        help_texts = {'vliegdagen' : 'geldt voor elke dag waarvoor het vliegplein werd geopend, dit ongeacht de duurtijd van de dag en het aantal starten',
                      'totaal_starts': 'niet in te vullen, wordt automatisch berekend'}


           
        
class GenerateStartRecords(forms.Form):
    clubs = Club.objects.all()
    date_from = forms.DateField(label='datum vanaf', required=False,
                                widget=forms.DateInput(attrs={'format':'%m/%d/%Y',
                                                              'class':'datepicker'}),
                                
                                )
    date_till = forms.DateField(label='datum tot', required=False,
                                widget=forms.DateInput(attrs={'format':'%m/%d/%Y',
                                                              'class': 'datepicker'}))

    

class MailForm(ModelForm):
    
    class Meta:
        model = Club_mail
        fields = ('club', 'funktie', 'naam', 'email','voorval','maatregel',
                  'starts', 'ato', 'non_ato')
