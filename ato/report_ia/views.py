from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect
from django.template import loader
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django import forms
from django.db import connection


# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.forms import ModelChoiceField

from .forms import VoorvalForm
from .models import Voorval
from .models import Ato_gebruiker
from .models import Club

#which club the web user is a member of
def club(web_user):
    try:
        ato = Ato_gebruiker.objects.get(user=web_user)
        return ato.club
    except:
        return None
        

def index(request):
    laatste_voorvallen_lijst = Voorval.objects.order_by('-ingave')[:5]
    context = {
        'laatste_voorvallen_lijst': laatste_voorvallen_lijst,
    }
    return render(request, 'index.html', context, request)

@login_required
def voorval_list(request, pk = None, template_name='voorval_lijst.html'):
    aclub = club(request.user)        
    if request.user.is_superuser:
        if pk:
            voorval = Voorval.objects.filter(club__id=pk)
        else:
            voorval = Voorval.objects.all()
    else:
        voorval = Voorval.objects.filter(club=aclub)
    data = {}
    data['object_list'] = voorval
    data['club'] = aclub.naam
    return render(request, template_name, data)

@login_required
def voorval_overzicht(request,template_name='voorval_overzicht.html'):
    aclub = club(request.user)        
    if request.user.is_superuser:
        voorval = Voorval.objects.values('club__id', 'club__naam').annotate(aantal_voorvallen=Count('club')).order_by()
        #print (connection.queries)
    else:
        voorval = Voorval.objects.filter(club=aclub).annotate(aantal_voorvallen=Count('club'))
    data = {}
    data['object_list'] = voorval
    data['club'] = aclub.naam
    return render(request, template_name, data)



@login_required
def voorval_create(request, template_name="voorval_ingave.html"):
    aclub = club(request.user)
    form = VoorvalForm(request.POST or None)
    if form.is_valid():
        my_model = form.save(commit=False)
        my_model.club = aclub
        my_model.save()
        return redirect('report_ia:voorval_list')
    return render(request, template_name, {'form':form, 'action':'create', 'club':aclub.naam})

@login_required
def voorval_update(request, pk, template_name='voorval_ingave.html'):
    aclub = club(request.user)
    voorval = get_object_or_404(Voorval, pk=pk)
    form = VoorvalForm(request.POST or None, instance=voorval)
    if form.is_valid():
        form.save()
        return redirect('report_ia:voorval_list')
    return render(request, template_name, {'form':form, 'action':'update','club':aclub.naam})

@login_required
def voorval_delete(request, pk, template_name='voorval_confirm_delete.html'):
    voorval = get_object_or_404(Voorval, pk=pk)    
    if request.method=='POST':
        voorval.delete()
        return redirect('report_ia:voorval_list')
    return render(request, template_name, {'object':voorval})


    
