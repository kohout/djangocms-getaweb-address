# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from cms.models.pagemodel import Site, Page
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from easy_thumbnails.fields import ThumbnailerImageField
from tinymce.models import HTMLField

try:
    # >= Django 1.7
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site


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

    sites = models.ManyToManyField(
        Site,
        blank=True, null=True,
        help_text=_(u'Location is associated with a certain site.'),
        verbose_name=_(u'Site'))

    logo = ThumbnailerImageField(
        upload_to='djangocms_address/',
        blank=True, null=True,
        help_text=_(u'Image of location.'),
        verbose_name=_(u'Logo'))

    description = HTMLField(
        blank=True, null=True,
        help_text=_(u'Description of the location, e.g. '
                    u'"World-famous opera house offering major productions, '
                    u'original decor & multilingual guided tours."'),
        verbose_name=_(u'Description'))

    cms_link = models.ForeignKey(
        Page,
        blank=True, null=True,
        help_text=_(u'A link to a page on this website, e.g. "/oper-information/".'),
        verbose_name=_(u'CMS page link'))

    external_link = models.URLField(
        blank=True, null=True,
        help_text=_(u'A link that provides further information about the location, e.g. '
                    u'"http://www.wiener-staatsoper.at/".'),
        verbose_name=_(u'External link'))

    link_title = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'Title that is displayed and wrapped with either CMS page link or External link, e.g. '
                    u'"More information".'),
        verbose_name=_(u'Link title'))

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

    @property
    def get_lat_lng_str(self):
        # e.g. 48.203493, 16.369168
        return '%s, %s' % (self.latitude, self.longitude)

    def get_set_link(self):
        if self.cms_link:
            return self.cms_link.get_absolute_url()
        elif self.external_link:
            return self.external_link
        else:
            return None

    def get_link_title(self):
        return self.link_title if self.link_title else self.get_set_link()

    @property
    def get_link_str(self):
        link = self.get_set_link()
        if not link:
            return ''

        res = u''.join(['<a href="', link, '" target="_blank">', self.get_link_title(), '</a>'])
        return mark_safe(res)

    def get_absolute_url(self):
        return reverse_lazy('location-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.get_name()

    class Meta:
        verbose_name = _(u'Location')
        verbose_name_plural = _(u'Locations')


class LocationsList(CMSPlugin):
    title = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'The title that is displayed above the location list.'),
        verbose_name=_(u'Title'))

    def filter_items(self, tags, search):
        qs = Location.objects.all()
        f = Q()

        if tags:
            f = Q(tags__in=tags)
        if search:
            if f is None:
                f = Q(name__icontains=search) | Q(description__icontains=search) | \
                    Q(formatted_address__icontains=search)
            else:
                f = f & (Q(name__icontains=search) | Q(description__icontains=search) |
                         Q(formatted_address__icontains=search))

        return qs.filter(f)

    def get_items(self, context):
        tags = context['request'].GET.get('tags', None)
        search = context['request'].GET.get('search', None)
        items = self.filter_items(tags, search)

        current_site = get_current_site(context['request'])
        items = items.filter(sites__id=current_site.id)
        return items


class AddressTagList(CMSPlugin):
    title = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'The title that is displayed above the tag list.'),
        verbose_name=_(u'Title'))

    def get_items(self):
        items = Tag.objects.all()
        return items

    def __unicode__(self):
        return self.title or 'TagList'

    class Meta:
        verbose_name = _(u'Tag List Plugin')
        verbose_name_plural = _(u'Tag List Plugins')
