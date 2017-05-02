from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404,render,redirect,reverse, get_list_or_404
from django.template import loader, Context
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django import forms
from django.db import connection
from django.core.mail import send_mail
from django.utils import timezone
from formtools.wizard.views import SessionWizardView

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.forms import ModelChoiceField, modelformset_factory, BaseModelFormSet

from .forms import VoorvalForm, ExportForm, MaatregelForm, StartsForm, UploadFileForm, StartsForm, GenerateStartRecords
from .forms_voorval import VoorvalForm1, VoorvalForm2
from .models import Voorval, Maatregel, VoorvalMaatregel, Nieuws, AantalStarts, Club, Bestand, Club_mail
from .models import Type_toestel
from .utilities import export, Ato, get_email_list_club

import markdown
from templated_docs import fill_template
from templated_docs.http import FileResponse

@login_required
def faq(request, template_name='faq.html'):
    ausr = Ato(request.user)
    faq_html = markdown.markdown(render_to_string('faq.md'))
    return render(request, template_name, {'data':faq_html, 'ausr':ausr})
            
@login_required
def index(request, template_name='home.html'):
    ausr = Ato(request.user)
    nieuws = Nieuws.objects.filter(online=True)
    #we first check if a group is specified
    newsl=[]
    news = ''
    if ausr.is_admin:
        news = nieuws.filter(groep__name='ato_admin')
    elif ausr.is_user:
        news = nieuws.filter(groep__name='ato_user')
    elif ausr.is_super:
        news = nieuws.filter(groep__name='ato_super')
    if len(news) > 0:
        newsl.append(news)
    #messages for all
    news = nieuws.filter(groep__name='ato_all')
    if len(news) > 0:
        newsl.append(news)
    #messages for a specific user
    news = nieuws.filter(user=ausr.user())
    if len(news) > 0:
        newsl.append(news)
    print(newsl)
    #if no specific news found for a group, then we check for a specific user
    nieuws_html=[]
    if len(newsl) > 0:
        for qs in newsl:
            msgs=qs.values('bericht')
            print(msgs)
            for msg in msgs:
                if msg['bericht']:
                    nieuws_html.append(markdown.markdown(msg['bericht']))
                    nieuws_html.append("<hr>")
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


class VoorvalWizard(SessionWizardView):
##     TEMPLATES = {
##         '0': 'voorval_ingave_wizard.html',
##         '1': 'voorval_ingave_wizard.html',
##         }
    instance = None
    form_list = [VoorvalForm1, VoorvalForm2]
##     initial = {
##         '0': {'locatie': },
##         '1': {}
##         }

#    @method_decorator(login_required)
#    def dispatch(self, *args, **kwargs):
#        return super(VoorvalWizard, self).dispatch(*args, **kwargs)
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.ausr = Ato(request.user)
        return super(VoorvalWizard, self).dispatch(request, *args, **kwargs)

    
    def get_form_instance( self, step ):
        print('get_form_instance')
        if self.instance is None:
            self.instance = Voorval()

        return self.instance

    def done(self, form_list, **kwargs):
        #ausr = Ato(self.request.user)
        form_clean_values = [form.cleaned_data for form in form_list]
        print(form_clean_values)
        self.instance.club = self.ausr.club()
        self.instance.save()
        return  redirect('report_ia:voorval_toegevoegd')
    
    def get_template_names(self):
        """
        Custom templates for the different steps
        """
        print(self.steps.current)
        return [self.TEMPLATES[self.steps.current]]

@login_required
def voorval_create(request, template_name="voorval_ingave.html"):
    ausr = Ato(request.user)
    print(ausr.is_super)
    print(ausr.is_admin)
    print(ausr.is_user)
    form = VoorvalForm(request.POST or None, initial={'locatie':ausr.club().locatie})
    fieldset = ( 'mens', 'uitrusting', 'omgeving', 'product', 'organisatie' ) 
    if form.is_valid():
        my_model = form.save(commit=False)
        my_model.club = ausr.club()
        my_model.save()
        # ok, new voorval has been saved to the database
        new_voorval_link = request.build_absolute_uri(reverse('report_ia:voorval_detail',
                                                              args=[my_model.pk]))

        #we send an email to responsable persons
        subject = "Voorval geregistreerd"
        email_to = get_email_list_club(ausr, 'voorval')
        try:
            #we get the email txt from a template
            t = loader.get_template('nieuwe_registratie_email.txt')
            c= Context({'club': ausr.club_naam(), 'user': request.user, 'link': new_voorval_link})
            message = t.render(c)
            print('message' ,message)
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
    return render(request, template_name, {'form':form, 'action':'Ingave', 'fieldset' : fieldset,
                                           'club':ausr.club_naam(), 'ausr' : ausr})

@login_required
def voorval_toegevoegd(request, template_name="voorval_ingave_bevestiging.html"):
    ausr = Ato(request.user)
    emails = get_email_list_club(ausr, 'voorval')
    return render(request, template_name, {'emails' : emails, 'club':ausr.club_naam(), 'ausr':ausr})

@login_required
def voorval_update(request, pk, template_name='voorval_ingave.html'):
    ausr = Ato(request.user)
    voorval = get_object_or_404(Voorval, pk=pk)
    form = VoorvalForm(request.POST or None, instance=voorval)
    if form.is_valid():
        form.save()
        return redirect('report_ia:voorval_lijst')
    return render(request, template_name, {'form':form, 'action':'Aanpassen','club':ausr.club_naam(), 'ausr':ausr})

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
    return render(request, template_name, {'object':voorval, 'club':ausr.club_naam(), 'ausr':ausr})

@login_required
def voorval_export(request, template_name="export_table.html"):
    ausr = Ato(request.user)
    print(ausr.is_super)
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
    return render(request, template_name, {'form':ef, 'club':ausr.club_naam(), 'ausr':ausr})

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
        email_to = get_email_list_club(ausr, 'maatregel')

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
    return render(request, template_name, {'form':form, 'action':'Aanmaken', 'club':ausr.club_naam(),
                                           'voorval_id': voorval_pk, 'ausr':ausr})
    
@login_required
def maatregel_toegevoegd(request, voorval_id, template_name="maatregel_ingave_bevestiging.html"):
    ausr = Ato(request.user)
    emails = get_email_list_club(ausr, 'maatregel')
    return render(request, template_name, {'emails' : emails, 'club':ausr.club_naam(), 'voorval_id':voorval_id,
                                            'ausr':ausr})

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
    return render(request, template_name, {'maatregel':maatregel, 'club':ausr.club_naam(), 'voorval_id':voorval_id,
                                            'ausr':ausr})
    
@login_required
def maatregel_update(request, pk, template_name='maatregel_ingave.html'):
    ausr = Ato(request.user)
    maatregel = get_object_or_404(Maatregel, pk=pk)
    form = MaatregelForm(request.POST or None, instance = maatregel, initial={'synopsis':maatregel.voorval.synopsis})
    #print (form.fields['voorval_.id)
    if form.is_valid():
        form.save()
        return redirect('report_ia:maatregel_lijst', pk=maatregel.voorval.id )
    return render(request, template_name, {'form':form, 'action':'Aanpassen','club':ausr.club_naam(),
                                           'voorval_id':maatregel.voorval.id, 'ausr':ausr})


@login_required
def starts_create(request, template_name="starts_ingave.html"):
    ausr = Ato(request.user)
    form = StartsForm(request.POST or None)
    form.fields['totaal_starts'].editable = False
    if ausr.is_admin:
        #fix this choicefield for club to the admins club
        form.fields['club'].initial=ausr.club_id()
        form.fields['club'].disabled=True
    if form.is_valid():
        my_model = form.save(commit=False)
        #my_model.club = ausr.club()
        my_model.save()

        return redirect('report_ia:home')
    return render(request, template_name, {'form':form, 'action':'create', 'club':ausr.club_naam(),
                                           'ausr':ausr})

@login_required
def starts_update(request, start_id, template_name="starts_ingave.html"):
    ausr = Ato(request.user)
    starts = get_object_or_404(AantalStarts, pk=start_id)
    form = StartsForm(request.POST or None, instance=starts)
    form.fields['club'].initial=ausr.club_id()
    form.fields['club'].disabled=True
    if form.is_valid():
        myform = form.save(commit=False)
        myform.ingevuld_op = timezone.now()
        myform.save()
        
        email_to = get_email_list_club(ausr, 'starts')

        try:
            #we get the email txt from a template
            t = loader.get_template('starts_aangepast.txt')
            c= Context({'club': ausr.club_naam(), 'user': request.user, 'myform' : myform })
            message = t.render(c)            
            send_mail(
                'Starts aangepast',
                message,
                'eia@gmail.com',
                email_to,
                fail_silently=False,
                )
        except:
            print('something went wrong')
            pass
        
        return redirect('report_ia:starts_lijst')
    return render(request, template_name, {'form':form, 'action':'update','club':ausr.club_naam(),
                                           'ausr':ausr})
    

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
def starts_generate(request, template_name="starts_generate.html"):
    ausr = Ato(request.user)        
    gsr = GenerateStartRecords(request.POST or None)
    if gsr.is_valid():
        #should generate start records for all clubs here
        van = gsr.cleaned_data['date_from']
        tot = gsr.cleaned_data['date_till']
        clubs = Club.objects.all()
        for club in clubs:
            AantalStarts.objects.create(club=club, van=van, tot=tot)
        return redirect('report_ia:starts_lijst')
    return render(request, template_name, {'form':gsr, 'club':ausr.club_naam(), 'ausr':ausr})
    

@login_required
def upload_bestand(request, voorval_id, template_name="upload_bestand.html"):
    ausr = Ato(request.user)        
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
    return render(request, template_name, {'form': form,  'ausr':ausr})

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
    if request.method == 'POST':
        bestand.delete()
        return redirect('report_ia:bestand_lijst', pk=voorval_id)
    return render(request, template_name, {'bestand':bestand, 'club':ausr.club_naam(), 'voorval_id':voorval_id})

@login_required
def search_gliders(request, template_name="search_resp.html"):
    if request.method == "GET":
        q = request.GET.get('term', '')
        if q:
            gliders = Type_toestel.objects.filter(naam__icontains=q)
            results = [ {'id': x.id , 'label' : x.naam, 'value': x.naam } for x in gliders ]
            response = JsonResponse(results, safe=False)
        else:
            return render(request, template_name)
    return HttpResponse(response, content_type='application/json')


@login_required
def club_mail(request, template_name="club_mail.html"):
    ausr = Ato(request.user)
    ClubMailFormset = modelformset_factory(Club_mail, fields=('naam', 'email', 'voorval', 'maatregel','starts'), max_num=5, extra=1)
    if request.method == 'POST':
        form_set = ClubMailFormset(request.POST, queryset=Club_mail.objects.filter(club__id=ausr.club_id()))
        if form_set.is_valid():
            for form in form_set:
                my_form = form.save(commit=False)
                my_form.club = ausr.club()
                my_form.save()
            return redirect('report_ia:home')
    else:
        form_set = ClubMailFormset(queryset=Club_mail.objects.filter(club__id=ausr.club_id()))
    return render(request, template_name,  {'formset': form_set,  'ausr':ausr})




