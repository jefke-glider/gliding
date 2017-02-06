from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect,reverse, get_list_or_404
from django.template import loader, Context
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django import forms
from django.db import connection
from django.core.mail import send_mail

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.forms import ModelChoiceField

from .forms import VoorvalForm, ExportForm, MaatregelForm, StartsForm, UploadFileForm
from .models import Voorval, Maatregel, VoorvalMaatregel, Nieuws, AantalStarts, Club, Bestand
from .utilities import export, Ato

import markdown
from templated_docs import fill_template
from templated_docs.http import FileResponse

        
@login_required
def index(request, template_name='home.html'):
    ausr = Ato(request.user)
    nieuws = Nieuws.objects.filter(online=True)
    #we first check if a group is specified
    if ausr.is_admin:
        fresh_news = nieuws.filter(groep__name='ato_admin')
    elif ausr.is_user:
        fresh_news = nieuws.filter(groep__name='ato_user')
    else:
        fresh_news = nieuws.filter(groep__name='ato_super')
    #if no specific news found for a group, then we check for a specific user
    nieuws_html=[]
    if len(fresh_news) == 0:
        fresh_news = nieuws.filter(user=ausr.user())
    if len(fresh_news) > 0:
        for art in fresh_news:
            nieuws_html.append(markdown.markdown(art.bericht))
    else:
        nieuws_html.append("<h4>Geen berichten")
    return render(request, template_name, {'data' : nieuws_html, 'club':ausr.club_naam(), 'ausr':ausr})

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
        # ok, new voorval has been saved to the database
        new_voorval_link = request.build_absolute_uri(reverse('report_ia:voorval_detail',
                                                              args=[my_model.pk]))

        #we send an email to responsable persons
        subject = "Voorval geregistreerd"
        email_to = ausr.email_admins() + ausr.email_supers()
        try:
            #we get the email txt from a template
            t = loader.get_template('nieuwe_registratie_email.txt')
            c= Context({'club': ausr.club_naam(), 'user': request.user, 'link': new_voorval_link})
            message = t.render(c)
            send_mail(
                subject,
                message,
                'eia@gmail.com',
                email_to,
                fail_silently=False,
                )
        except:
            pass
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
        return redirect('report_ia:voorval_lijst')
    return render(request, template_name, {'form':form, 'action':'update','club':ausr.club_naam()})

@login_required
def voorval_detail(request, pk, action=None, template_name="voorval_overview.html",
                   odt_template="voorval_detail.odt"):
    ausr = Ato(request.user)
    voorval = get_object_or_404(Voorval, pk=pk)
    if voorval.aantal_maatregelen > 0:
        maatregelen = get_list_or_404(Maatregel, voorval__id = pk)
    else:
        maatregelen = None
    if voorval.aantal_bestanden > 0:
        bestanden =  get_list_or_404(Bestand, voorval__id = pk)
    else:
        bestanden = None
    data = {}
    data['obj_voorval'] = voorval
    data['obj_maatregelen'] = maatregelen
    data['obj_bestanden'] = bestanden
    data['ausr'] = ausr
    data['club'] = ausr.club_naam()
    if action == 'doc':
        filename = fill_template(odt_template, data, output_format='odt')
        visible_filename = 'voorval_detail.odt'
        return FileResponse(filename, visible_filename)
    else:
        return render(request, template_name, data)

@login_required
def voorval_delete(request, pk, template_name='voorval_confirm_delete.html'):
    voorval = get_object_or_404(Voorval, pk=pk)
    ausr = Ato(request.user)
    if request.method=='POST':
        voorval.delete()
        return redirect('report_ia:voorval_lijst')
    return render(request, template_name, {'object':voorval, 'club':ausr.club_naam()})

@login_required
def voorval_export(request, template_name="export_table.html"):
    ausr = Ato(request.user)        
    ef = ExportForm(request.POST or None)
    if ausr.is_admin:
        #fix this choicefield for club to the admins club
        ef.fields['club_to_export'].initial=ausr.club_id()
        ef.fields['club_to_export'].disabled=True
    if ef.is_valid():
        if ef.cleaned_data['tabel_to_export'] == '1':
            if ef.cleaned_data['club_to_export']:
                vm = VoorvalMaatregel.objects.filter(club_id=ef.cleaned_data['club_to_export'])
            else:
                vm = VoorvalMaatregel.objects.all()
            if ef.cleaned_data['export_date_from']:
                vm=vm.filter(datum__gte=ef.cleaned_data['export_date_from'])
            if ef.cleaned_data['export_date_till']:
                vm=vm.filter(datum__lte=ef.cleaned_data['export_date_till'])
            return export(vm)
        elif ef.cleaned_data['tabel_to_export'] == '2':
            if ef.cleaned_data['club_to_export']:
                st = AantalStarts.objects.filter(club_id=ef.cleaned_data['club_to_export'])
            else:
                st = AantalStarts.objects.all()
            if ef.cleaned_data['export_date_from']:
                st=st.filter(op_datum__gte=ef.cleaned_data['export_date_from'])
            if ef.cleaned_data['export_date_till']:
                st=st.filter(op_datum__lte=ef.cleaned_data['export_date_till'])
            return export(st)            
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

        # ok, new voorval has been saved to the database
        new_link = request.build_absolute_uri(reverse('report_ia:voorval_detail',
                                                      args=[my_model.pk]))

        #print(new_link)
        #we send an email to responsable persons
        email_to = ausr.email_admins() + ausr.email_supers()
        try:
            #we get the email txt from a template
            t = loader.get_template('nieuwe_maatregel_email.txt')
            c= Context({'club': ausr.club_naam(), 'user': request.user, 'link': new_link})
            message = t.render(c)            
            send_mail(
                'Maatregel geregistreerd',
                message,
                'eia@gmail.com',
                email_to,
                fail_silently=False,
                )
        except:
            pass
        return redirect('report_ia:maatregel_toegevoegd', voorval_id=my_model.voorval.id)
    return render(request, template_name, {'form':form, 'action':'create', 'club':ausr.club_naam(),
                                           'voorval_id': voorval_pk})
    
@login_required
def maatregel_toegevoegd(request, voorval_id, template_name="maatregel_ingave_bevestiging.html"):
    ausr = Ato(request.user)
    emails = ausr.email_admins() + ausr.email_supers()
    return render(request, template_name, {'emails' : emails, 'club':ausr.club_naam(), 'voorval_id':voorval_id})

@login_required
def maatregel_list(request, pk = None, template_name='maatregel_lijst.html'):
    ausr = Ato(request.user)        
    if ausr.is_super:
        if pk:
            maatregel = Maatregel.objects.filter(voorval__id=pk)
        else:
            maatregel = Maatregel.objects.all()
    elif ausr.is_admin:
        maatregel = Maatregel.objects.filter(voorval__club=ausr.club())
        if pk:
            maatregel = maatregel.filter(voorval__id = pk)
    else:
        print('shouldnt reach this')
    #recent voorval where ingave < 1 week
    data = {}
    data['object_list'] = maatregel
    data['ausr'] = ausr
    data['club'] = ausr.club_naam()
    data['voorval_id'] = pk
    return render(request, template_name, data)

@login_required
def maatregel_delete(request, pk, template_name="maatregel_confirm_delete.html"):
    ausr = Ato(request.user)
    maatregel = get_object_or_404(Maatregel, pk=pk)
    voorval_id = maatregel.voorval.id
    if request.method=='POST':
        maatregel.delete()
        return redirect('report_ia:maatregel_lijst', pk=voorval_id)
    return render(request, template_name, {'maatregel':maatregel, 'club':ausr.club_naam(), 'voorval_id':voorval_id})
    
@login_required
def maatregel_update(request, pk, template_name='maatregel_ingave.html'):
    ausr = Ato(request.user)
    maatregel = get_object_or_404(Maatregel, pk=pk)
    form = MaatregelForm(request.POST or None, instance = maatregel, initial={'synopsis':maatregel.voorval.synopsis})
    #print (form.fields['voorval_.id)
    if form.is_valid():
        form.save()
        return redirect('report_ia:maatregel_lijst', pk=maatregel.voorval.id )
    return render(request, template_name, {'form':form, 'action':'update','club':ausr.club_naam(),
                                           'voorval_id':maatregel.voorval.id})


@login_required
def starts_create(request, template_name="starts_ingave.html"):
    ausr = Ato(request.user)
    form = StartsForm(request.POST or None)
    form.fields['totaal'].editable = False
    if ausr.is_admin:
        #fix this choicefield for club to the admins club
        form.fields['club'].initial=ausr.club_id()
        form.fields['club'].disabled=True
    if form.is_valid():
        my_model = form.save(commit=False)
        #my_model.club = ausr.club()
        my_model.save()

        return redirect('report_ia:home')
    return render(request, template_name, {'form':form, 'action':'create', 'club':ausr.club_naam()})


@login_required
def starts_toegevoegd(request, id, template_name="starts_ingave_bevestiging.html"):
    ausr = Ato(request.user)
    emails = ausr.email_admins() + ausr.email_supers()
    return render(request, template_name, {'emails' : emails, 'club':ausr.club_naam(),
                                           'voorval_id':voorval_id})

@login_required
def starts_list(request, pk = None, template_name='starts_lijst.html'):
    ausr = Ato(request.user)        
    if ausr.is_super:
        if pk:
            starts = AantalStarts.objects.filter(club__id=pk)
        else:
            starts = AantalStarts.objects.all()
    else:
        starts = AantalStarts.objects.filter(club=ausr.club())
    #print(starts.count())
    #recent voorval where ingave < 1 week
    data = {}
    data['object_list'] = starts
    data['ausr'] = ausr
    data['club'] = ausr.club_naam()
    return render(request, template_name, data)

@login_required
def upload_bestand(request, voorval_id, template_name="upload_bestand.html"):
    voorval = get_object_or_404(Voorval, pk=voorval_id)
    form = UploadFileForm(request.POST or None, request.FILES or None, initial={'synopsis':voorval.synopsis})
    if request.method == 'POST':
        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.voorval = voorval
            my_form.save()
            #handle_uploaded_file(request.FILES['file'])
            return redirect('report_ia:bestand_lijst', pk=my_form.voorval.id)
    #else:
    #    form = UploadFileForm()
    return render(request, template_name, {'form': form})

@login_required
def bestand_list(request, pk = None, template_name='bestand_lijst.html'):
    ausr = Ato(request.user)        
    if ausr.is_super:
        if pk:
            bestand = Bestand.objects.filter(voorval__id=pk)
        else:
            bestand = Bestand.objects.all()
    elif ausr.is_admin or ausr.is_user:
        bestand = Bestand.objects.filter(voorval__club=ausr.club())
        if pk:
            bestand = bestand.filter(voorval__id = pk)
    else:
        print('should never be here!')
    #recent voorval where ingave < 1 week
    data = {}
    data['object_list'] = bestand
    data['ausr'] = ausr
    data['club'] = ausr.club_naam()
    data['bestand_id'] = pk
    return render(request, template_name, data)

@login_required
def bestand_delete(request, pk, template_name="bestand_confirm_delete.html"):
    ausr = Ato(request.user)
    bestand = get_object_or_404(Bestand, pk=pk)
    voorval_id = bestand.voorval.id
    if request.method=='POST':
        bestand.delete()
        return redirect('report_ia:bestand_lijst', pk=voorval_id)
    return render(request, template_name, {'bestand':bestand, 'club':ausr.club_naam(), 'voorval_id':voorval_id})
