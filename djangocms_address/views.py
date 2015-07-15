# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from djangocms_address.models import Location


class LocationDetailView(DetailView):
    model = Location
    template_name = 'djangocms_address/detail.html'
