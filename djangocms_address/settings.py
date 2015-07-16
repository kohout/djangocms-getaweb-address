# -*- coding: utf-8 -*-
from django.conf import settings

# --- do-not-change ---
GEOCODING_API_HTTP = 'http://maps.googleapis.com/maps/api/geocode/'
GEOCODING_API_HTTPS = 'https://maps.googleapis.com/maps/api/geocode/'
GEOCODING_OUTPUT_JSON = 'json'
GEOCODING_OUTPUT_XML = 'xml'
# --- end do-not-change ---

# allow manual entry of latitude and longitude in forms
# WARNING! if you set this to 'True', latitude and longitude will no longer be automatically re-fetched if
# an address is changed. You will have to make sure that latitude and longitude are correct yourself!
ALLOW_MANUAL_LAT_LONG = getattr(settings, 'ADDRESS_ALLOW_MANUAL_LAT_LNG',
                                False)

# choose first result that google maps sends back.
# makes it easier to handle ambiguous information
CHOOSE_FIRST_RESULT = getattr(settings, 'ADDRESS_CHOOSE_FIRST_RESULT',
                              True)

# easy thumbnails settings for preview displays (admin view)
IMG_OPTIONS_PREVIEW = getattr(settings, 'ADDRESS_IMG_OPTIONS_PREVIEW',
                              {'size': (64, 64), 'crop': True, 'upscale': True})

# easy thumbnails settings for logo displays
IMG_OPTIONS_LOGO = getattr(settings, 'ADDRESS_IMG_OPTIONS_LOGO',
                           {'size': (250, 55), 'crop': True, 'upscale': True})

# if true, filter requests will be sent via ajax and the teaser and gmap containers will be updated.
# if false, page reload will occur
FILTER_USING_AJAX = getattr(settings, 'ADDRESS_FILTER_USING_AJAX',
                            True)

# --- GEOCODING SETTINGS ---
# for more info see https://developers.google.com/maps/documentation/geocoding/intro

# the API url
GEOCODING_API = getattr(settings, 'ADDRESS_GEOCODING_API', GEOCODING_API_HTTPS)

# can be either XML or JSON
# please use settings GEOCODING_OUTPUT_JSON or GEOCODING_OUTPUT_XML
GEOCODING_OUTPUT = getattr(settings, 'ADDRESS_GEOCODING_OUTPUT', GEOCODING_OUTPUT_JSON)

# API key of application, get a key via https://console.developers.google.com/
GEOCODING_KEY = getattr(settings, 'ADDRESS_GEOCODING_KEY', None)
GEOCODING_KEY_URL = '&key=%s' % GEOCODING_KEY  # do not change

# Language in which to return results. If it is set to "None", the geocoder will attempt to use
# the native language of the domain from which the request is sent.
# List of supported languages: https://developers.google.com/maps/faq#languagesupport
GEOCODING_LANGUAGE = getattr(settings, 'ADDRESS_GEOCODING_LANGUAGE', None)
GEOCODING_LANGUAGE_URL = '&language=%s' % GEOCODING_LANGUAGE  # do not change

