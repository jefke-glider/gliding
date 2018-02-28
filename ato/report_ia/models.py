from django.db import models
from django import forms
from django.contrib.auth.models import User, Group
from multiselectfield import MultiSelectField

# Create your models here.

class Vliegveld(models.Model):
    naam = models.CharField(max_length=30)
    afkorting_icao = models.CharField(max_length=4)

    def __str__(self):
        return self.afkorting_icao + ' ' + self.naam

    class Meta:
        verbose_name_plural = 'Vliegvelden'

class Club(models.Model):
    naam = models.TextField()
    naam_kort = models.CharField(max_length=10)
    locatie = models.ForeignKey(Vliegveld, on_delete=models.CASCADE)

    def __str__(self):
        return self.naam_kort + ' ' + self.naam

class Club_mail(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    funktie = models.CharField(max_length=100, default='')
    naam = models.CharField(max_length=50)
    email = models.EmailField()
    voorval = models.BooleanField(default=False)
    maatregel = models.BooleanField(default=False)
    starts = models.BooleanField(default=False)
    ato = models.BooleanField(default=False)
    non_ato = models.BooleanField(default=False)

    def __str__(self):
        return self.club.naam + ' ' + self.naam

    
class Ato_gebruiker(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.club.naam + ' ' + self.user.username

class Domein(models.Model):
    naam = models.CharField(max_length=50)

    def __str__(self):
        return self.naam


class Opleiding(models.Model):
    naam = models.CharField(max_length=30)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Opleidingen'


class Startwijze(models.Model):
    naam = models.CharField(max_length=30)
    naam_kort = models.CharField(max_length=1)
    prio = models.IntegerField()

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Startwijzen'
        ordering = ['prio']



class Type_toestel(models.Model):
    naam = models.CharField(max_length=30)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Type toestellen'
        ordering = ['naam']

class Type_voorval(models.Model):
    naam = models.CharField(max_length = 50)

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Type voorvallen'

class Kern_activiteit(models.Model):
    naam = models.CharField(max_length=100)
    prio = models.IntegerField()

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Kern activiteit'
        ordering = ['prio']

class Kern_gevaar(models.Model):
    naam = models.CharField(max_length=100)

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Kern gevaar'
    
class Potentieel_risico(models.Model):
    naam = models.CharField(max_length=100)
    
    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Potentieel_risico'


class Schade(models.Model):
    omschrijving = models.TextField()

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Schade'

class Type_schade(models.Model):
    naam = models.CharField(max_length = 30)

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Type schades'

class Windsterkte(models.Model):
    kts = models.CharField(max_length=10)

    def __str__(self):
        return self.kts

    class Meta:
        verbose_name_plural = 'Wind sterktes'
        
class Windrichting(models.Model):
    uit = models.CharField(max_length=10)

    def __str__(self):
        return self.uit

    class Meta:
        verbose_name_plural = 'Wind richtingen'

class Wolken(models.Model):
    okta = models.CharField(max_length=5)
    metar_code = models.CharField(max_length=3)
    omschrijving = models.TextField()

    def __str__(self):
        return self.okta + " " + self.metar_code + " " + self.omschrijving

    class Meta:
        verbose_name_plural = 'Wolken'

class Wolkenbasis(models.Model):
    feet = models.CharField(max_length=15)
    
    def __str__(self):
        return self.feet

    class Meta:
        verbose_name_plural = 'Wolkenbasissen'

class Thermiek(models.Model):
    sterkte = models.CharField(max_length=10)
    omschrijving = models.TextField()
    
    def __str__(self):
        return self.sterkte + " " + self.omschrijving

    class Meta:
        verbose_name_plural = 'Thermiek-sterktes'

class Zichtbaarheid(models.Model):
    km = models.CharField(max_length=5)
    omschrijving = models.TextField()
    
    def __str__(self):
        return self.km + " " + self.omschrijving

    class Meta:
        verbose_name_plural = 'Zichtbaarheden'
    
   
class Voorval(models.Model):
    
    ingave = models.DateTimeField(auto_now=True)
    datum = models.DateField()
    uur = models.TimeField()
    locatie = models.ForeignKey(Vliegveld, on_delete=models.CASCADE, null=True, blank=True)
    andere_locatie = models.TextField(null=True, blank=True)
    type_voorval = models.ForeignKey(Type_voorval, on_delete=models.CASCADE)    
    synopsis = models.TextField()
    opleiding = models.ForeignKey(Opleiding, on_delete=models.CASCADE, null=True, blank=True)
    startwijze = models.ForeignKey(Startwijze, on_delete=models.CASCADE, null=True, blank=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    type_schade = models.ForeignKey(Type_schade, on_delete=models.CASCADE)
    schade_omschrijving = models.TextField(null=True, blank=True)
    mens = models.BooleanField(default=False)
    uitrusting =  models.BooleanField(default=False)
    omgeving =  models.BooleanField(default=False)
    product =  models.BooleanField(default=False)
    organisatie =  models.BooleanField(default=False)
    type_toestel = models.ForeignKey(Type_toestel, on_delete=models.CASCADE, null=True, blank=True)
    kern_activiteit = models.ForeignKey(Kern_activiteit, on_delete=models.CASCADE)
    aantal_maatregelen = models.IntegerField(default=0)
    aantal_bestanden = models.IntegerField(default=0)
    domein = models.ForeignKey(Domein, on_delete=models.CASCADE)
    windsterkte = models.ForeignKey(Windsterkte, on_delete=models.CASCADE, null=True, blank=True)
    windrichting = models.ForeignKey(Windrichting, on_delete=models.CASCADE, null=True, blank=True)
    piste = models.CharField(max_length=2, null=True, blank=True)
    wolken = models.ForeignKey(Wolken, on_delete=models.CASCADE, null=True, blank=True)
    thermiek = models.ForeignKey(Thermiek, on_delete=models.CASCADE,null=True, blank=True)
    wolkenbasis = models.ForeignKey(Wolkenbasis, on_delete=models.CASCADE,null=True, blank=True)
    zichtbaarheid = models.ForeignKey(Zichtbaarheid, on_delete=models.CASCADE, null=True, blank=True)
    muopo_omschrijving = models.TextField(null=True, blank=True)

    def __iter__(self):
        fieldnames = [f.name for f in self._meta.get_fields()]
        for field_name in fieldnames:
            value = getattr(self, field_name, None)
            yield (field_name, value)
    
#    def __str__(self):
#        return self.club.naam_kort + ' ' + self.id + ' ' + self.uur

    @property
    def is_recent(self):
        #a voorval is recent if it has been entered less than a week ago
        from datetime import datetime, timedelta
        if self.ingave.replace(tzinfo=None) < (datetime.today() - timedelta(days = 14)):
            return False
        else:
            return True

    @property
    def has_maatregel(self):
        if self.aantal_maatregelen > 0:
            return True
        else:
            return False
        
    class Meta:
        verbose_name_plural = 'Voorvallen'
        ordering = ['-datum']


class Maatregel(models.Model):
    ingave =  models.DateTimeField(auto_now=True)
    omschrijving = models.TextField()
    voorval = models.ForeignKey(Voorval, on_delete=models.CASCADE)
    in_werking = models.DateField(null=True)

    class Meta:
        verbose_name_plural = 'Maatregelen'
        ordering = ['-ingave']
        
    def __str__(self):
        return self.voorval.club.naam_kort + ' ' + str(self.voorval.datum) + ' ' + str(self.voorval.uur)

    def __iter__(self):
        fieldnames = [f.name for f in self._meta.get_fields()]
        for field_name in fieldnames:
            value = getattr(self, field_name, None)
            yield (field_name, value)


#
# this models refers to a view!!!
# this view is called voorval_maatregel, and is needed
# to export the combination (join) of the tables Voorval & Maatregel
# -> extra meta attributes need to be specified
#
class VoorvalMaatregel(models.Model):
    id = models.IntegerField(primary_key=True)
    datum_voorval = models.DateField()
    uur = models.TimeField()
    domein = models.ForeignKey(Domein, on_delete=models.DO_NOTHING)
    type_voorval = models.ForeignKey(Type_voorval, on_delete=models.DO_NOTHING)    
    synopsis = models.TextField()
    opleiding = models.ForeignKey(Opleiding, on_delete=models.DO_NOTHING)
    startwijze = models.ForeignKey(Startwijze, on_delete=models.DO_NOTHING)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    type_schade = models.ForeignKey(Type_schade, on_delete=models.DO_NOTHING)
    schade_omschrijving = models.TextField()
    mens = models.BooleanField(default=False)
    uitrusting =  models.BooleanField(default=False)
    omgeving =  models.BooleanField(default=False)
    product =  models.BooleanField(default=False)
    organisatie =  models.BooleanField(default=False)
    muopo_omschrijving = models.TextField()
    type_toestel = models.ForeignKey(Type_toestel, on_delete=models.DO_NOTHING)
    kern_activiteit = models.ForeignKey(Kern_activiteit, on_delete=models.DO_NOTHING)
    windsterkte = models.ForeignKey(Windsterkte, on_delete=models.DO_NOTHING)
    windrichting = models.ForeignKey(Windrichting, on_delete=models.DO_NOTHING)
    wolken = models.ForeignKey(Wolken, on_delete=models.DO_NOTHING)
    wolkenbasis = models.ForeignKey(Wolkenbasis, on_delete=models.DO_NOTHING)
    thermiek = models.ForeignKey(Thermiek, on_delete=models.DO_NOTHING)
    zichtbaarheid = models.ForeignKey(Zichtbaarheid, on_delete=models.DO_NOTHING)
    maatregel_omschrijving =  models.TextField()
    in_werking = models.DateField()

    class Meta:
        managed = False
        db_table = 'voorval_maatregel'


class Nieuws(models.Model):
    bericht = models.TextField()
    groep = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    online = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Berichten'

class AantalStarts(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    ingevuld_op = models.DateTimeField(null=True)
    lier = models.IntegerField(blank=True, default=0)
    ato_lier = models.IntegerField(blank=True, default=0)
    sleep = models.IntegerField(blank=True, default=0)
    ato_sleep = models.IntegerField(blank=True, default=0)
    zelf = models.IntegerField(blank=True, default=0)
    ato_zelf = models.IntegerField(blank=True, default=0)
    auto  = models.IntegerField(blank=True, default=0)
    ato_auto = models.IntegerField(blank=True, default=0)
    bungee  = models.IntegerField(blank=True, default=0)
    ato_bungee = models.IntegerField(blank=True, default=0)
    totaal_starts = models.IntegerField(blank=True, default=0)
    vliegdagen  = models.IntegerField(blank=True, default=0)
    van = models.DateField(blank=True, null=True)
    tot = models.DateField(blank=True, null=True)

    @property
    def has_been_updated(self):
        #this model has been updated, when totaal_starts and totaal_vbliegdagen
        #both are different from 0
        if self.totaal_starts == 0:
            return False
        else:
            return True
    
    class Meta:
        verbose_name_plural = 'Aantal starts'

def club_directory_path(instance, filename):
    short_club_name = instance.voorval.club.naam_kort.lower()
    return 'club/{0}/{1:%Y}/{2}'.format(short_club_name, instance.voorval.datum, filename)


class Bestand(models.Model):
    voorval = models.ForeignKey(Voorval, on_delete=models.CASCADE)
    op =  models.DateTimeField(auto_now=True)
    bestand = models.FileField(upload_to=club_directory_path)
    opmerking = models.TextField()

    class Meta:
        verbose_name_plural = 'Bestanden'

    def __iter__(self):
        fieldnames = [f.name for f in self._meta.get_fields()]
        for field_name in fieldnames:
            value = getattr(self, field_name, None)
            yield (field_name, value)
