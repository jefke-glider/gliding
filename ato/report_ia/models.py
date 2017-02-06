from django.db import models
from django import forms
from django.contrib.auth.models import User, Group
from multiselectfield import MultiSelectField

# Create your models here.

class Vliegveld(models.Model):
    naam = models.CharField(max_length=30)
    afkorting_icao = models.CharField(max_length=4)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Vliegvelden'

class Club(models.Model):
    naam = models.TextField()
    naam_kort = models.CharField(max_length=10)
    locatie = models.ForeignKey(Vliegveld, on_delete=models.CASCADE)

    def __str__(self):
        return self.naam

class Ato_gebruiker(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.club.naam + ' ' + self.user.username

class Opleiding(models.Model):
    naam = models.CharField(max_length=30)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Opleidingen'


class Startwijze(models.Model):
    naam = models.CharField(max_length=30)
    naam_kort = models.CharField(max_length=1, default='S')

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Startwijzen'



class Type_toestel(models.Model):
    naam = models.CharField(max_length=30)

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name_plural = 'Type toestellen'

class Type_voorval(models.Model):
    naam = models.CharField(max_length = 20)

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Type voorvallen'

class Kern_activiteit(models.Model):
    naam = models.CharField(max_length=100)

    def __str__(self):
        return self.naam
    
    class Meta:
        verbose_name_plural = 'Kern activiteit'

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
   
class Voorval(models.Model):
    ATO_VOORVAL = (
        (1, 'ATO voorval'),
        (2, 'niet ATO voorval'),
        )
    
    OORZAKEN_KEUZES = (
        (1, 'Mens'),
        (2, 'Uitrusting'),
        (3, 'Omgeving'),
        (4, 'Product'),
        (5, 'Organisatie'))
    
    ingave = models.DateTimeField(auto_now=True)
    datum = models.DateField()
    uur = models.TimeField()
    type_voorval = models.ForeignKey(Type_voorval, on_delete=models.CASCADE)    
    synopsis = models.TextField()
    opleiding = models.ForeignKey(Opleiding, on_delete=models.CASCADE)
    startwijze = models.ForeignKey(Startwijze, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    menselijke_schade = models.BooleanField(default=False)
    materiele_schade = models.BooleanField(default=False)
    schade_omschrijving = models.TextField()
    muopo = MultiSelectField(choices=OORZAKEN_KEUZES,
                             max_choices=5,
                             max_length=5)
    type_toestel = models.ForeignKey(Type_toestel, on_delete=models.CASCADE)
    kern_activiteit = models.ForeignKey(Kern_activiteit, on_delete=models.CASCADE)
    aantal_maatregelen = models.IntegerField(default=0)
    aantal_bestanden = models.IntegerField(default=0)
    ato = models.IntegerField(choices=ATO_VOORVAL, default=1)
    potentieel_risico = models.ForeignKey(Potentieel_risico, on_delete=models.CASCADE)

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
        if self.ingave.replace(tzinfo=None) < (datetime.today() - timedelta(days = 7)):
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
        return self.club.naam_kort + ' ' + self.voorval.datum + ' ' + self.voorval.uur

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
    ato = models.IntegerField()
    type_voorval = models.ForeignKey(Type_voorval, on_delete=models.DO_NOTHING)    
    synopsis = models.TextField()
    opleiding = models.ForeignKey(Opleiding, on_delete=models.DO_NOTHING)
    startwijze = models.ForeignKey(Startwijze, on_delete=models.DO_NOTHING)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    menselijke_schade = models.BooleanField(default=False)
    materiele_schade = models.BooleanField(default=False)
    schade_omschrijving = models.TextField()
    muopo = MultiSelectField()
    type_toestel = models.ForeignKey(Type_toestel, on_delete=models.DO_NOTHING)
    kern_activiteit = models.ForeignKey(Kern_activiteit, on_delete=models.DO_NOTHING)
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
    op_datum = models.DateField(auto_now=True)
    lier = models.IntegerField(blank=True, default=0)
    ato_lier = models.IntegerField(blank=True, default=0)
    sleep = models.IntegerField(blank=True, default=0)
    ato_sleep = models.IntegerField(blank=True, default=0)
    zelf = models.IntegerField(blank=True, default=0)
    ato_zelf = models.IntegerField(blank=True, default=0)
    totaal = models.IntegerField(blank=True, default=0)

    
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
