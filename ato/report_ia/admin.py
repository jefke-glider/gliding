from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import Vliegveld
from .models import Club
from .models import Startwijze
from .models import Opleiding
from .models import Type_voorval
from .models import Type_toestel
from .models import Voorval
from .models import Ato_gebruiker
from .models import Kern_activiteit
from .models import Kern_gevaar
from .models import Potentieel_risico
from .models import Ato_gebruiker
from .models import Nieuws
from .models import AantalStarts
from .models import Type_schade
from .models import Windsterkte
from .models import Windrichting
from .models import Wolken
from .models import Wolkenbasis
from .models import Thermiek
from .models import Zichtbaarheid

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class AtoGebruikerInline(admin.StackedInline):
    model = Ato_gebruiker
    can_delete = False
    verbose_name_plural = 'Ato gebruikers'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (AtoGebruikerInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Vliegveld)
admin.site.register(Club)
admin.site.register(Ato_gebruiker)
admin.site.register(Startwijze)
admin.site.register(Opleiding)
admin.site.register(Type_voorval)
admin.site.register(Type_toestel)
admin.site.register(Voorval)
admin.site.register(Kern_activiteit)
admin.site.register(Kern_gevaar)
admin.site.register(Potentieel_risico)
admin.site.register(Nieuws)
admin.site.register(AantalStarts)
admin.site.register(Type_schade)
admin.site.register(Windsterkte)
admin.site.register(Windrichting)
admin.site.register(Wolken)
admin.site.register(Wolkenbasis)
admin.site.register(Thermiek)
admin.site.register(Zichtbaarheid)

