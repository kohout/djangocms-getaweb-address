# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from djangocms_address.models import TagList

from .models import LocationsList


class AddressPlugin(CMSPluginBase):
    model = LocationsList
    name = _(u'Address List')
    render_template = 'djangocms_address/list.html'

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['items'] = instance.get_items(context)
        return context


class AddressFilterPlugin(CMSPluginBase):
    model = TagList
    name = _(u'Address Filter')
    render_template = 'djangocms_address/filter.html'

    def render(self, context, instance, placeholder):
        context['filter_instance'] = instance
        context['filter_tags'] = instance.get_items()
        return context


plugin_pool.register_plugin(AddressPlugin)
plugin_pool.register_plugin(AddressFilterPlugin)
