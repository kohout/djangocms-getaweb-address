# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext as _
from easy_thumbnails.exceptions import InvalidImageFormatError
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer


class Tag(models.Model):
    """
    Addresses can be tagged, which makes it easier to filter or group them.
    """
    name = models.CharField(
        max_length=255,
        help_text=_(u'Name of a tag, e.g. "Music", which allow for customized grouping or filtering.'),
        verbose_name=_(u'Tag'))

    def tag_count(self):
        return self.location_set.all().count()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Tag')
        verbose_name_plural = _(u'Tags')


class Location(models.Model):
    """
    A location with descriptive data.
    The address of the location can be displayed via google maps.
    """
    name = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'Name or title of location, e.g. "Opera House".'),
        verbose_name=_(u'Name'))

    logo = ThumbnailerImageField(
        upload_to='djangocms_address/',
        blank=True, null=True,
        help_text=_(u'Image of location.'),
        verbose_name=_(u'Logo'))

    description = models.TextField(
        blank=True, null=True,
        help_text=_(u'Description of the location, e.g. '
                    u'"World-famous opera house offering major productions, '
                    u'original decor & multilingual guided tours."'),
        verbose_name=_(u'Description'))

    link = models.URLField(
        blank=True, null=True,
        help_text=_(u'A link that provides further information about the location, e.g. '
                    u'"http://www.wiener-staatsoper.at/".'),
        verbose_name=_(u'Link'))

    tags = models.ManyToManyField(
        Tag,
        blank=True, null=True,
        help_text=_(u'Tags of the location, e.g. "Music", which allow for customized grouping or filtering.'),
        verbose_name=_(u'Tags'))

    street = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'The street (and street number) the location is located at, e.g. "Opernring 2".'),
        verbose_name=_(u'Street'))

    zipcode = models.IntegerField(
        blank=True, null=True,
        help_text=_(u'The zipcode of the city in which the location is located in, e.g. "1200"'),
        verbose_name=_(u'Zipcode'))

    city = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'The city the location is located in, e.g. "Vienna".'),
        verbose_name=_(u'City'))

    state = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'The state the location is situated in, e.g. "Vienna".'),
        verbose_name=_(u'State'))

    country = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'The country the location is situated in, e.g. "Austria".'),
        verbose_name=_(u'Country'))

    formatted_address = models.CharField(
        # automatically set on save (either by google maps response or via set fields)
        max_length=255,
        blank=True,
        help_text=_(u'The formatted address string, e.g. "Opernring 2, 1010 Vienna, Austria".'),
        verbose_name=_(u'Formatted address'))

    latitude = models.FloatField(
        # automatically set on save if ALLOW_MANUAL_LAT_LONG is False
        blank=True,
        help_text=_(u'The latitude of the location, e.g. 48.203493.'),
        verbose_name=_(u'Latitude'))

    longitude = models.FloatField(
        # automatically set on save if ALLOW_MANUAL_LAT_LONG is False
        blank=True,
        help_text=_(u'The longitude of the location, e.g. 16.369168.'),
        verbose_name=_(u'Longitude'))

    def get_name(self):
        if not self.name:
            return self.formatted_address
        return self.name

    def get_lat_long_str(self):
        # e.g. 48.203493, 16.369168
        return '%s, %s' % (self.latitude, self.longitude)

    def get_absolute_url(self):
        return reverse_lazy('location-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.get_name()

    class Meta:
        verbose_name = _(u'Location')
        verbose_name_plural = _(u'Locations')


class LocationsList(CMSPlugin):
    def get_items(self):
        items = Location.objects.all()
        return items
