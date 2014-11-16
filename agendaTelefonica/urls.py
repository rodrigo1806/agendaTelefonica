from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('agenda.views',
    url(r'^$', 'index'),
    url(r'^entrar/$', 'entrar'),
    url(r'^agenda/$', 'agenda'),
    url(r'^salvar/$', 'salvar'),

)
