from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django import forms
from django.db import connection
from django.core.mail import send_mail

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.forms import ModelChoiceField

from .forms import VoorvalForm, ExportForm, MaatregelForm
from .models import Voorval, Maatregel, VoorvalMaatregel

from .models import Club
from .utilities import export, Ato

        

def index(request):
    laatste_voorvallen_lijst = Voorval.objects.order_by('-ingave')[:5]
    context = {
        'laatste_voorvallen_lijst': laatste_voorvallen_lijst,
    }
    return render(request, 'index.html', context, request)

@login_required
def voorval_list(request, pk = None, template_name='voorval_lijst.html'):
    ausr = Ato(request.user)        
    if ausr.is_super:
        if pk:
            voorval = Voorval.objects.filter(club__id=pk)
        else:
            voorval = Voorval.objects.all()
    else:
        voorval = Voorval.objects.filter(club=ausr.club())
    #recent voorval where ingave < 1 week
    data = {}
    data['object_list'] = voorval
    data['ausr'] = ausr
    data['club'] = ausr.club_naam()
    return render(request, template_name, data)

@login_required
def voorval_overzicht(request,template_name='voorval_overzicht.html'):
    ausr = Ato(request.user)        
    if request.user.is_superuser:
        voorval = Voorval.objects.values('club__id', 'club__naam').annotate(aantal_voorvallen=Count('club')).order_by()
        #print (connection.queries)
    else:
        voorval = Voorval.objects.filter(club=ausr.club()).annotate(aantal_voorvallen=Count('club'))
    data = {}
    data['object_list'] = voorval
    data['ausr'] = ausr
    data['club'] = ausr.club_naam()
    return render(request, template_name, data)

@login_required
def voorval_create(request, template_name="voorval_ingave.html"):
    ausr = Ato(request.user)
    form = VoorvalForm(request.POST or None)
    if form.is_valid():
        my_model = form.save(commit=False)
        my_model.club = ausr.club()
        my_model.save()
        #we send an email to responsable persons
        email_to = ausr.email_admins() + ausr.email_supers()
        message = 'Er werd een nieuw voorval geregistreerd voor de club ' + ausr.club_naam()
        send_mail(
            'Voorval geregistreerd',
            message,
            'eia@gmail.com',
            email_to,
            fail_silently=False,
            )
        return redirect('report_ia:voorval_toegevoegd')
    return render(request, template_name, {'form':form, 'action':'create', 'club':ausr.club_naam()})

@login_required
def voorval_toegevoegd(request, template_name="voorval_ingave_bevestiging.html"):
    ausr = Ato(request.user)
    emails = ausr.email_admins() + ausr.email_supers()
    return render(request, template_name, {'emails' : emails, 'club':ausr.club_naam()})

@login_required
def voorval_update(request, pk, template_name='voorval_ingave.html'):
    ausr = Ato(request.user)
    voorval = get_object_or_404(Voorval, pk=pk)
    form = VoorvalForm(request.POST or None, instance=voorval)
    if form.is_valid():
        form.save()
        return redirect('report_ia:voorval_list')
    return render(request, template_name, {'form':form, 'action':'update','club':ausr.club_naam()})

@login_required
def voorval_delete(request, pk, template_name='voorval_confirm_delete.html'):
    voorval = get_object_or_404(Voorval, pk=pk)    
    if request.method=='POST':
        voorval.delete()
        return redirect('report_ia:voorval_list')
    return render(request, template_name, {'object':voorval})

@login_required
def voorval_export(request, template_name="export_table.html"):
    ausr = Ato(request.user)        
    ef = ExportForm(request.POST or None)
    if ef.is_valid():
        print('ef is valid')
        print(ef.cleaned_data['tabel_to_export'])
        if ef.cleaned_data['tabel_to_export'] == '1':
            print('table to export is voorvallen')
            #retrieve the data
            if ef.cleaned_data['club_to_export']: 
                voorvallen = Voorval.objects.filter(club_id=ef.cleaned_data['club_to_export'])
            else:
                voorvallen = Voorval.objects.all()
            print (ef.cleaned_data['export_date_from'])
            if ef.cleaned_data['export_date_from']:
                voorvallen=voorvallen.filter(datum__gte=ef.cleaned_data['export_date_from'])
            if ef.cleaned_data['export_date_till']:
                voorvallen=voorvallen.filter(datum__lte=ef.cleaned_data['export_date_till'])
            return export(voorvallen)
        elif ef.cleaned_data['tabel_to_export'] == '2':
            print('table to export is voorvalmaatregelen')
            if ef.cleaned_data['club_to_export']:
                vm = VoorvalMaatregel.objects.filter(club_id=ef.cleaned_data['club_to_export'])
            else:
                vm = VoorvalMaatregel.objects.all()
            if ef.cleaned_data['export_date_from']:
                vm=vm.filter(datum__gte=ef.cleaned_data['export_date_from'])
            if ef.cleaned_data['export_date_till']:
                vm=vm.filter(datum__lte=ef.cleaned_data['export_date_till'])
            return export(vm)
        elif ef.cleaned_data['tabel_to_export'] == '3':
            all_rows = export_sql()
        else:
            print('no matching choice for table to export')
    return render(request, template_name, {'form':ef, 'club':ausr.club_naam()})



@login_required
def maatregel_create(request, voorval_pk=None, template_name="maatregel_ingave.html"):
    ausr = Ato(request.user)
    voorval = get_object_or_404(Voorval, pk=voorval_pk)
    form = MaatregelForm(request.POST or None, initial={'synopsis':voorval.synopsis})
    if form.is_valid():
        my_model = form.save(commit=False)
        my_model.voorval = voorval
        my_model.save()
        #we send an email to responsable persons
        email_to = ausr.email_admins() + ausr.email_supers()
        message = 'Er werd een nieuwe maatregel geregistreerd voor de club ' + ausr.club_naam()
        send_mail(
            'Maatregel geregistreerd',
            message,
            'eia@gmail.com',
            email_to,
            fail_silently=False,
            )
        return redirect('report_ia:maatregel_toegevoegd')
    return render(request, template_name, {'form':form, 'action':'create', 'club':ausr.club_naam()})
    
@login_required
def maatregel_toegevoegd(request, template_name="maatregel_ingave_bevestiging.html"):
    ausr = Ato(request.user)
    emails = ausr.email_admins() + ausr.email_supers()
    return render(request, template_name, {'emails' : emails, 'club':ausr.club_naam()})

@login_required
def maatregel_list(request, pk = None, template_name='maatregel_lijst.html'):
    ausr = Ato(request.user)        
    if ausr.is_super:
        if pk:
            maatregel = Maatregel.objects.filter(voorval__club_id=pk)
        else:
            maatregel = Maatregel.objects.all()
    else:
        maatregel = Maatregel.objects.filter(voorval__club=ausr.club())
    #recent voorval where ingave < 1 week
    data = {}
    data['object_list'] = maatregel
    data['ausr'] = ausr
    data['club'] = ausr.club_naam()
    return render(request, template_name, data)

@login_required
def maatregel_delete(request, pk, template_name="maatregel_confirm_delete.html"):
    maatregel = get_object_or_404(Maatregel, pk=pk)    
    if request.method=='POST':
        maatregel.delete()
        return redirect('report_ia:maatregel_lijst')
    return render(request, template_name, {'object':maatregel})
    
@login_required
def maatregel_update(request, pk, template_name='maatregel_ingave.html'):
    ausr = Ato(request.user)
    maatregel = get_object_or_404(Maatregel, pk=pk)
    form = MaatregelForm(request.POST or None, instance = maatregel, initial={'synopsis':maatregel.voorval.synopsis})
    if form.is_valid():
        form.save()
        return redirect('report_ia:maatregel_lijst')
    return render(request, template_name, {'form':form, 'action':'update','club':ausr.club_naam()})


