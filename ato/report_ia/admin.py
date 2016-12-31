from django.contrib import admin

# Register your models here.
from .models import Vliegveld
from .models import Club
from .models import Startwijze
from .models import Opleiding
from .models import Type_voorval
from .models import Type_toestel
from .models import Voorval
from .models import Ato_gebruiker

admin.site.register(Vliegveld)
admin.site.register(Club)
admin.site.register(Ato_gebruiker)
admin.site.register(Startwijze)
admin.site.register(Opleiding)
admin.site.register(Type_voorval)
admin.site.register(Type_toestel)
admin.site.register(Voorval)
