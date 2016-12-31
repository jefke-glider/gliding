from django.db import models
from django import forms
from django.contrib.auth.models import User

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


class Voorval(models.Model):
    ingave = models.DateTimeField(auto_now=True)
    datum = models.DateField()
    uur = models.TimeField()
    type_voorval = models.ForeignKey(Type_voorval, on_delete=models.CASCADE)
    synopsis = models.TextField()
    opleiding = models.ForeignKey(Opleiding, on_delete=models.CASCADE)
    startwijze = models.ForeignKey(Startwijze, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    #def __str__(self):
    #    return self.ingave.value

    class Meta:
        verbose_name_plural = 'Voorvallen'
