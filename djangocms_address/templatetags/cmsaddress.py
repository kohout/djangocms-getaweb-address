# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from djangocms_address import settings

register = template.Library()

@register.filter()
def render_logo(item):
    image = item.logo
    if not image:
        return u''

    thumb_url = get_thumbnailer(image).get_thumbnail(settings.IMG_OPTIONS_LOGO).url
    return mark_safe('<img src="%s" alt="%s" />' % (thumb_url, item.name))

@register.simple_tag()
def gmaps_api_key():
    if settings.GEOCODING_KEY:
        return settings.GEOCODING_KEY_URL
    return ''

@register.simple_tag()
def filter_via_ajax():
    return 'ajax_filter' if settings.FILTER_USING_AJAX else ''
