from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from .models import Ato_gebruiker, Maatregel, Voorval, VoorvalMaatregel, Club
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

import csv
from datetime import datetime

def export(qs, fields=None):
    model = qs.model
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s_%s.csv' % (slugify(model.__name__),
                                                                          datetime.now().strftime('%Y%m%d_%H%M'))
    writer = csv.writer(response)
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
    print(headers)
    writer.writerow(headers)
    # Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field, '-')
                if callable(val):
                    val = val()
                row.append(val)
        writer.writerow(row)
    # Return CSV file to browser as download
    return response

def export_sql():
    with connection.cursor() as cursor:
        cursor.execute("""
        select * from report_ia_voorval vv left join report_ia_maatregel ma on (ma.voorval_id = vv.id);
        """)
        rows = cursor.fetchall()
    return rows



class Ato:
    """
    	there exist 3 type of user-groups :
        * ato_user : can report/edit incident/accident registrations -> club specific
        * ato_admin : ahot's and safety manager for a specific club
        * ato_super : superuser, access to reporting etc, not bound to a club
    """
    def __init__(self, web_user):
        self.ato_user = web_user
        try:
            self.ato = Ato_gebruiker.objects.get(user=web_user)
        except:
            self.ato = None

    def _admins(self):
        users = User.objects.filter(groups__name='ato_admin').filter(ato_gebruiker__club_id = self.ato.club.id)
        return users

    def _supers(self):
        users = User.objects.filter(groups__name='ato_super')
        return users

    def club(self):
        if self.ato:
            return (self.ato.club)
        else:
            return ('')
        
    def club_naam(self):
        if self.ato:
            return (self.ato.club.naam_kort)
        else:
            return ('')

    def club_id(self):
        if self.ato:
            return (self.ato.club.id)
        else:
            return ('')

    def user(self):
        return (self.ato_user)

    def email_admins(self):
        email = []
        for adm in self._admins():
            email.append(adm.email)
        return email

    def email_supers(self):
        email = []
        for sup in self._supers():
            email.append(sup.email)
        return email
    
    @property
    def is_user(self):
        return self.ato_user.groups.filter(name='ato_user').exists()

    @property
    def is_admin(self):
        return self.ato_user.groups.filter(name='ato_admin').exists()
    
    @property
    def is_super(self):
        return self.ato_user.groups.filter(name='ato_super').exists()

    
    
def test_ato():
    users = ['kac_user', 'kac_admin', 'kac_safety']
    for usri in users:

        print("-----------------------")
        print("getting info about user %s " % usri)
        usr=User.objects.get(username=usri)
        ato=Ato(usr)
        print(ato.user())
        print(ato.club())
        print(ato.club_naam())
        print(ato.club_id())
        print(ato.email_admins())
        print(ato.email_supers())
        print(ato.is_user)
        print(ato.is_admin)
        print(ato.is_super)
        email_to = ato.email_admins() + ato.email_supers()
        message = 'Nieuw voorval geregistreerd'
        send_mail(
            'Voorval geregistreerd',
            message,
            'ato@gmail.com',
            email_to,
            fail_silently=False,
            )

def test_export():
    vm = VoorvalMaatregel.objects.all()
    print(vm.values())

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def create_ato_users(apps, schema_editor):
    clubs = Club.objects.all()
    admin_group = Group.objects.get(name='ato_admin')
    user_group = Group.objects.get(name='ato_user')
    ato_gebruiker = Ato_gebruiker
    for club in clubs:
        username =  club.naam_kort.lower() + '_admin'
        print('creating user ', username)
        user = User.objects.create_user(username=username,
                                        email=None,
                                        password='Soth{og2')
        print('adding ', username , ' to group ato_admin')
        user.groups.add(admin_group)
        Ato_gebruiker.objects.create(club=club, user=user)
        username =  club.naam_kort.lower() + '_user'
        print('creating user ', username)        
        user = User.objects.create_user(username=username,
                                        email=None,
                                        password='Soth{og2')
        print('adding ', username , ' to group ato_user')
        user.groups.add(user_group)
        Ato_gebruiker.objects.create(club=club, user=user)



## def update_ato_passwords(apps, schema_editor):
##     clubs = Club.objects.all()
##     admin_group = Group.objects.get(name='ato_admin')
##     user_group = Group.objects.get(name='ato_user')
##     ato_gebruiker = Ato_gebruiker
##     for club in clubs:
##         username =  club.naam_kort.lower() + '_admin'
##         user = Users.objects.filter(username=username)
##         if user:
