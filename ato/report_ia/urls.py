from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.voorval_list, name='voorval_list'),
    url(r'^lijst/(?P<pk>\d+$)', views.voorval_list, name='voorval_lijst'),
    url(r'^overzicht$', views.voorval_overzicht, name='voorval_overzicht'),    
    url(r'^create$', views.voorval_create, name='voorval_create'),
    url(r'^edit/(?P<pk>\d+$)', views.voorval_update, name='voorval_update'),
    url(r'^delete/(?P<pk>\d+$)', views.voorval_delete, name='voorval_delete'),
]
