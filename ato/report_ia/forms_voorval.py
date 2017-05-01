from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Voorval, Club, Maatregel, AantalStarts, Bestand, Club_mail


class VoorvalForm1(ModelForm):
    boolean_set = ( 'mens', 'uitrusting', 'omgeving', 'product', 'organisatie' )
                               
    class Meta:
        model = Voorval

        ordering = ['-datum']
        fields = ( 'datum', 'uur', 'locatie', 'andere_locatie',
                   'domein', 'opleiding', 'type_voorval',
                   'type_schade', 'schade_omschrijving',
                   'synopsis',  'startwijze' ,
                   'type_toestel', 'kern_activiteit',
                   'windsterkte', 'windrichting', 'wolken', 'wolkenbasis', 'thermiek', 'zichtbaarheid',
                   )
        help_texts = { 'uur' : 'uur van het voorval in formaat hh:mm',
                       'synopsis' : 'omschrijf hier chronologisch en objectief wat er gebeurd is',
                       'kern_activiteit': 'de activiteit die werd uitgevoerd op het moment dat het fout is gelopen',
                       'windsterkte' : 'in knopen',
                       'wolken' : 'in okta\'s',
                       'thermiek' : 'in m/s',
                       'wolkenbasis' : 'in feet',
                       'zichtbaarheid' : 'in km',
                       'muopo_omschrijving' : 'verduidelijk nader voor ELK aangeduid MUOPO ascpect',
                       'domein' : 'voorval valt al dan niet binnen/buiten ATO opleiding',
                      }

    def __init__(self, *args, **kwargs):
        super(VoorvalForm1, self).__init__(*args, **kwargs)
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


class VoorvalForm2(ModelForm):
    boolean_set = ( 'mens', 'uitrusting', 'omgeving', 'product', 'organisatie' )
                               
    class Meta:
        model = Voorval

        fields = ( 
                   'mens', 'uitrusting', 'omgeving', 'product', 'organisatie',
                   'muopo_omschrijving',
                   )
        help_texts = { 
                       'mens' : 'persoonlijke gedragsbepalende factoren',                       
                       'uitrusting' : 'alle gebruikte hardware, technische factoren',
                       'omgeving' : 'gehele vliegomgeving en -inrichting',
                       'product' : 'het vlieggebeuren',
                       'organisatie' : 'het clubbeleid',
                        'muopo_omschrijving' : 'verduidelijk nader voor ELK aangeduid MUOPO ascpect',
                      }
        labels = {  'muopo_omschrijving' : 'MUOPO omschrijving'}

    def __init__(self, *args, **kwargs):
        super(VoorvalForm2, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'title':''})
