# djangocms-getaweb-address
A DjangoCMS plugin for managing addresses (in combination with Google Maps v3)

## Settings
Default values for settings and short descriptions below

* ``ADDRESS_ALLOW_MANUAL_LAT_LNG``: ``False``
> allow manual entry of latitude and longitude in forms<br/>
> WARNING! if you set this to 'True', latitude and longitude will no longer be automatically re-fetched if
> an address is changed. You will have to make sure that latitude and longitude are correct yourself!

* ``ADDRESS_CHOOSE_FIRST_RESULT`` = ``True``
> choose first result that google maps sends back.<br/>
> makes it easier to handle ambiguous information

* ``ADDRESS_IMG_OPTIONS_PREVIEW`` = ``{'size': (64, 64), 'crop': True, 'upscale': True}``
> easy thumbnails settings for preview displays (admin view)<br/>
> for syntax see [https://github.com/SmileyChris/easy-thumbnails]()

* ``ADDRESS_IMG_OPTIONS_LOGO`` = ``{'size': (250, 55), 'crop': True, 'upscale': True}``
> easy thumbnails settings for logo displays

* ``ADDRESS_FILTER_USING_AJAX`` = ``True``
> if true, filter requests will be sent via ajax and the teaser and gmap containers will be updated.<br/>
> if false, page reload will occur

### GEOCODING SETTINGS
for more info see [https://developers.google.com/maps/documentation/geocoding/intro]()

* ``ADDRESS_GEOCODING_API`` = ``https://maps.googleapis.com/maps/api/geocode/``
> the API url

* ``ADDRESS_GEOCODING_OUTPUT`` = ``json``
> can be either ``xml`` or ``json``

* ``ADDRESS_GEOCODING_KEY`` = ``None``
> API key of application, get a key via https://console.developers.google.com/

* ``GEOCODING_LANGUAGE`` = ``None``
> Language in which to return results. If it is set to "None", the geocoder will attempt to use
> the native language of the domain from which the request is sent.<br/>
> List of supported languages: [https://developers.google.com/maps/faq#languagesupport]()