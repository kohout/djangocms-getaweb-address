/*
  Get a list of url parameters, allows multiple values for one key
 */
function get_url_params() {
  var query = location.search.substr(1);
  var params = query.split("&");
  var result = {};
  for (var i = 0; i < params.length; i++) {
    var item = params[i].split("=");
    result[item[0]] = result[item[0]] || [];
    result[item[0]].push(item[1]);
  }
  return result;
}

/*
  Handles filter specific functionality, such as checking the checkboxes and
  replacing the content via ajax (if that is set in the settings)
 */
var init_filter = function ($content) {
  /* Make sure that form fields are pre-filled (when there is a page reload) */
  $content.find('form.djangocms_address_filter_form').each(function () {
    var $form = $(this);
    var url_params = get_url_params();

    // check search bar
    if (url_params.hasOwnProperty('search')) {
      $form.find('input[name="search"]').val(url_params['search']);
    }

    // check tag checkboxes
    if (url_params.hasOwnProperty('tags')) {
      $.each(url_params['tags'], function (index, value) {
        $form.find('input[name="tags"][value="' + value + '"]').attr('checked', 'checked');
      });
    }
  });

  /* Stop pagereload, get and replace content via ajax instead. */
  $content.find('form.djangocms_address_filter_form.ajax_filter').each(function () {
    var $form = $(this);
    $form.find('button[type=submit]').on('click', function (e) {
      e.preventDefault();
      var url = window.location.pathname;

      $.ajax({
        url: url,
        data: $form.serialize(),
        method: 'GET'
      }).success(function (res, status, xhr, form) {
        // replace content
        var $new_teaser = $(res).find('.djangocms_address_teaser_container');
        var $new_gmap = $(res).find('.djangocms_address_gmap_container');
        $content.find('.djangocms_address_teaser_container').replaceWith($new_teaser);
        $content.find('.djangocms_address_gmap_container').replaceWith($new_gmap);

        // re-init the map
        init_gmap($content);
      }).error(function (res, status, xhr, form) {
        console.log(res, status, xhr, form);
      });
    });
  });
};

/*
  Initializes the google map by checking data attributes of djangocms_address containers.
  If you change the templates but want to keep this functionality, make sure to have wrappers
    --- .djangocms_address_teaser, .djangocms_address_detail ---
  and that these wrapper divs have the following data attributes
    --- data-lat, data-lng, data-name, data-url, data-description, data-formaddr ---
  also, there has to be a container with the id
    --- map-canvas ---
  in which the map will be rendered in.
 */
var init_gmap = function ($content) {
  if ($content === undefined)
    $content = $('body');

  // initial map options, close zoom, focus on first location
  var $teasers = $content.find('.djangocms_address_teaser, .djangocms_address_detail');

  // check if we actually have any results
  var $first_teaser = $teasers.first();
  $content.find('#djangocms_address_noresults').css('display', 'none');
  if ($first_teaser.length == 0) {
    $content.find('#djangocms_address_noresults').css('display', 'block');
    return;
  }

  var first_lat = $first_teaser.attr('data-lat');
  var first_lng = $first_teaser.attr('data-lng');

  var latlngbounds = new google.maps.LatLngBounds();
  var mapOptions = {
    zoom: 12,
    center: new google.maps.LatLng(parseFloat(first_lat), parseFloat(first_lng))
  };

  // setup map
  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  // now go through each location element to add markers and infowindows
  $.each($teasers, function (index, value) {
    var $value = $(value);
    var lat = $value.attr('data-lat');
    var lng = $value.attr('data-lng');
    var title = $value.attr('data-name');
    var url = $value.attr('data-url');
    var formatted_address = $value.attr('data-formaddr');
    var description = $value.attr('data-description');

    var latlng = new google.maps.LatLng(parseFloat(lat), parseFloat(lng));
    latlngbounds.extend(latlng);

    var marker = new google.maps.Marker({
      position: latlng,
      map: map,
      title: title
    });

    var infowindow = new google.maps.InfoWindow({
      content: '<h3><a href="' + url + '">' + title + '</a></h3>' +
      '<p>' + formatted_address + '</p><p>' + description + '</p>'
    });

    google.maps.event.addListener(marker, 'click', function () {
      infowindow.open(map, marker);
    });
  });

  // refocus the map so that all current markers are visible
  map.setCenter(latlngbounds.getCenter());
  map.fitBounds(latlngbounds);
};

/*
  Asynchronous loading of the google maps api with a callback to "init_gmap"
 */
function load_gmap() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://maps.googleapis.com/maps/api/js?v=3.exp' +
      '&callback=init_gmap';
  document.body.appendChild(script);
}


$(document).ready(function () {
  var $body = $('body');
  init_filter($body);
  load_gmap();
});
