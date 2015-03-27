from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^check', 'LicensesPlates.views.capturePlate', name='check'),
                       url(r'^$', 'LicensesPlates.views.home', name='home'),

                       )
