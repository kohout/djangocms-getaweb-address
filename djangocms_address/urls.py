# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import LocationDetailView

urlpatterns = patterns(
    '',
    url(r'^location/(?P<pk>[\w-]+)/$',
        LocationDetailView.as_view(),
        name='location-detail'),
)
