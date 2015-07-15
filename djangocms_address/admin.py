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
    list_display = ('render_preview', 'get_name', 'description')
    list_display_links = ('render_preview', 'get_name')
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

    render_preview.allow_tags = True
    render_preview.short_description = _(u'Preview')

admin.site.register(Tag, TagAdmin)
admin.site.register(Location, LocationAdmin)
