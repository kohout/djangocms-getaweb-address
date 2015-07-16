# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from djangocms_address.models import Location


class LocationDetailView(DetailView):
    model = Location
    template_name = 'djangocms_address/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(LocationDetailView, self).get_context_data(**kwargs)
        ctx['items'] = [self.object, ]
        ctx['first'] = self.object
        return ctx
