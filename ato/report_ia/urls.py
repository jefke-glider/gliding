from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^lijst/$', views.voorval_list, name='voorval_lijst'),
    url(r'^lijst/(?P<pk>\d*$)', views.voorval_list, name='voorval_lijst'),
    url(r'^detail/(?P<pk>\d*$)', views.voorval_detail, name='voorval_detail'),
    url(r'^overzicht$', views.voorval_overzicht, name='voorval_overzicht'),
    url(r'^export$', views.voorval_export, name='voorval_export'),    
    url(r'^create$', views.voorval_create, name='voorval_create'),
    url(r'^created$', views.voorval_toegevoegd, name='voorval_toegevoegd'),    
    url(r'^edit/(?P<pk>\d+$)', views.voorval_update, name='voorval_update'),
    url(r'^delete/(?P<pk>\d+$)', views.voorval_delete, name='voorval_delete'),
    url(r'^upload/(?P<voorval_id>\d+$)', views.upload_bestand, name='upload_bestand'),
    url(r'^maatregel/lijst/(?P<pk>\d*$)', views.maatregel_list, name='maatregel_lijst'),
    url(r'^maatregel/create/(?P<voorval_pk>\d+$)', views.maatregel_create, name='maatregel_create'),
    url(r'^maatregel/created/(?P<voorval_id>\d+$)', views.maatregel_toegevoegd, name='maatregel_toegevoegd'),
    url(r'^maatregel/delete/(?P<pk>\d+$)', views.maatregel_delete, name='maatregel_delete'),
    url(r'^maatregel/edit/(?P<pk>\d+$)', views.maatregel_update, name='maatregel_update'),
    url(r'^starts/create/$', views.starts_create, name='starts_create'),
    url(r'^starts/lijst/$', views.starts_list, name='starts_list'),
    url(r'^bestand/lijst/(?P<pk>\d*$)', views.bestand_list, name='bestand_lijst'),
    url(r'^bestand/delete/(?P<pk>\d+$)', views.bestand_delete, name='bestand_delete'),
]
