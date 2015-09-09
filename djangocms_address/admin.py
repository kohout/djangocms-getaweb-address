# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _
from easy_thumbnails.files import get_thumbnailer
from djangocms_address.forms import LocationForm

from djangocms_address import settings
from djangocms_address.models import Tag, Location


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_count')
    search_fields = ('name', )


class LocationAdmin(admin.ModelAdmin):
    list_display = ('render_preview', '_get_name', '_description')
    list_display_links = ('render_preview', '_get_name')
    search_fields = ('name', 'description', 'street', 'zipcode', 'city', 'state',
                     'country', 'latitude', 'longitude')
    readonly_fields = ('render_preview', )
    form = LocationForm

    def render_preview(self, location):
        location_image = location.logo
        if not location_image:
            return u''

        img_options = settings.IMG_OPTIONS_PREVIEW
        thumb_url = get_thumbnailer(location_image).get_thumbnail(img_options).url
        if not thumb_url:
            return u''
        return u'<img src="%s">' % thumb_url

    def _get_name(self, location):
        return location.get_name()

    def _description(self, location):
        return location.description

    _get_name.short_description = _(u'Name')
    _description.allow_tags = True
    _description.short_description = _(u'Description')
    render_preview.allow_tags = True
    render_preview.short_description = _(u'Preview')

admin.site.register(Tag, TagAdmin)
admin.site.register(Location, LocationAdmin)
