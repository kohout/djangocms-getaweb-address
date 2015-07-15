# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import LocationsList


class AddressPlugin(CMSPluginBase):
    model = LocationsList
    name = _("Address List")
    render_template = 'djangocms_address/list.html'

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['items'] = instance.get_items()
        return context

plugin_pool.register_plugin(AddressPlugin)
