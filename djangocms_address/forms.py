# -*- coding: utf-8 -*-
import ast
import codecs
import json
import urllib
import urllib2
from django import forms
from django.core.exceptions import ValidationError
from djangocms_address import settings
from djangocms_address.models import Location


class LocationForm(forms.ModelForm):
    lat = None
    lng = None
    formatted_address = None

    def address_has_changed(self, address):
        """
        :param address: The location address.
        :return: Whether or not any parameters of the address have changed.
        """
        has_changed = False
        if self.instance.pk is not None:
            if self.instance.street != address['street'] \
                    or self.instance.zipcode != address['zipcode']\
                    or self.instance.city != address['city']\
                    or self.instance.state != address['state']\
                    or self.instance.country != address['country']:
                has_changed = True
        else:
            has_changed = True
        return has_changed

    def set_lat_lng(self, address, latitude, longitude, has_changed):
        # latitude and longitude will be set if they are either empty,
        # or if the address has changed (as long as ALLOW_MANUAL_LAT_LONG is False!)
        if not (latitude or longitude) or has_changed:
            # combine strings and make url ready
            zip_city = u' '.join(filter(None, [str(address['zipcode']), address['city']]))
            adr_url = u', '.join(filter(None, [address['street'], zip_city, address['state'], address['country']]))

            # adjust the formatted address
            self.formatted_address = adr_url

            if not settings.ALLOW_MANUAL_LAT_LONG:
                adr_url = codecs.encode(adr_url, 'utf-8')
                adr_url = urllib.quote_plus(adr_url)

                # build url
                url = settings.GEOCODING_API + settings.GEOCODING_OUTPUT + '?'
                url += 'address=' + adr_url
                if settings.GEOCODING_LANGUAGE:
                    url += settings.GEOCODING_LANGUAGE_URL
                if settings.GEOCODING_KEY:
                    url += settings.GEOCODING_KEY_URL

                # send to gmaps
                req = urllib2.Request(url)
                res = urllib2.urlopen(req)
                values = res.read()
                values = json.loads(values)

                # get lat/long
                if values['status'] != 'OK':
                    raise ValidationError('Error! Status %s. Please check your information and settings.' % values['status'])

                if len(values['results']) > 1 and not settings.CHOOSE_FIRST_RESULT:
                    raise ValidationError('More than one result for this location found. Please enter more information!')

                location = values['results'][0]['geometry']['location']
                self.lat = location['lat']
                self.lng = location['lng']

    def check_addr_set(self, cleaned_data):
        street = cleaned_data.get('street', None)
        zipcode = cleaned_data.get('zipcode', None)
        city = cleaned_data.get('city', None)
        state = cleaned_data.get('state', None)
        country = cleaned_data.get('country', None)

        if not (street or zipcode or city or state or country):
            raise ValidationError('Please fill out at least one of the address fields!')

        return {u'street': street, u'zipcode': zipcode, u'city': city,
                u'state': state, u'country': country}

    def check_link(self, cleaned_data):
        cms_link = cleaned_data.get('cms_link', None)
        external_link = cleaned_data.get('external_link', None)

        if cms_link and external_link:
            raise ValidationError('Please only enter a CMS page link OR an external link!')

    def clean(self):
        cleaned_data = super(LocationForm, self).clean()

        self.check_link(cleaned_data)
        addr = self.check_addr_set(cleaned_data)
        has_changed = self.address_has_changed(addr)

        latitude = cleaned_data.get('latitude', None)
        longitude = cleaned_data.get('longitude', None)

        # get lat/lng via google maps api and set them
        self.set_lat_lng(addr, latitude, longitude, has_changed)

        return super(LocationForm, self).clean()

    def save(self, commit=True):
        instance = super(LocationForm, self).save(commit=False)
        instance.latitude = self.lat
        instance.longitude = self.lng
        instance.formatted_address = self.formatted_address
        if commit:
            instance.save(commit=True)
        return instance

    class Meta:
        model = Location
        exclude = (
            'formatted_address',
        )
        if not settings.ALLOW_MANUAL_LAT_LONG:
            exclude += (
                'latitude',
                'longitude'
            )
