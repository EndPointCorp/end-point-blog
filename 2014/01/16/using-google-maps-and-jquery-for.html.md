---
author: Steph Skardal
gh_issue_number: 914
tags: maps, javascript, jquery
title: Using Google Maps and jQuery for Location Search
---

<div class="separator" style="clear: both; text-align: center;margin-bottom:10px;"><img border="0" src="/blog/2014/01/16/using-google-maps-and-jquery-for/image-0.png"/><br/>
Example of Google maps showing <a href="http://www.paper-source.com/">Paper Source</a> locations.</div>

A few months ago, I built out functionality to display physical store locations within a search radius for [Paper Source](http://www.paper-source.com/) on an interactive map. There are a few map tools out there to help accomplish this goal, but I chose Google Maps because of my familiarity and past success using it. Here I'll go through some of the steps to implement this functionality.

### Google Maps API Key

Before you start this work, you'll want to get a Google Maps API key. Learn more [here](https://developers.google.com/maps/documentation/javascript/tutorial#api_key).

### Geocoder Object

At the core of our functionality is the use of the [google.maps.Geocoder](https://developers.google.com/maps/documentation/javascript/geocoding) object. The Geocoder converts a search point or search string to into geographic coordinates. The most basic use of the geocoder might look like this:

```javascript
var geocoder = new google.maps.Geocoder();
//search is a string, input by user
geocoder.geocode({ 'address' : search }, function(results, status) {
  if(status == "ZERO_RESULTS") {
    //Indicate to user no location has been found
  } else {
    //Do something with resulting location(s)
  }
}
```

### Rendering a Map from the Results

After a geocoder results set is acquired, a map and locations might be displayed. A simple and standard implementation of Google Maps can be executed, with the map center set to the geocoder results set center:

```javascript
var mapOptions = {
  center: results[0].geometry.bounds.getCenter(),
  zoom: 10,
  mapTypeId: google.maps.MapTypeId.ROADMAP
};
var map = new google.maps.Map(document.getElementById("map"), mapOptions);
```

### Searching within a Radius

Next up, you may want to figure out how to display a set of locations inside the map bounds. At the time I implemented the code, I found no functionality that automagically did this, so I based my solution off of a few references I found online. The following code excerpt steps through the process:

```javascript
//search center is the center of the geocoded location
var search_center = results[0].geometry.bounds.getCenter();

//Earth's radius, used in distance calculation
var R = 6371;

//Step through each location
$.each(all_locations, function(i, loc) {
  //Calculate distance from map center
  var loc_position = new google.maps.LatLng(loc.latitude, loc.longitude);
  var dLat  = locations.rad(loc.latitude - search_center.lat());
  var dLong = locations.rad(loc.longitude - search_center.lng());
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(locations.rad(search_center.lat())) *
    Math.cos(locations.rad(search_center.lat())) *
    Math.sin(dLong/2) * Math.sin(dLong/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  var d = R * c;
  loc.distance = d;

  //Add the marker to the map
  var marker = new google.maps.Marker({
    map: map,
    position: loc_position,
    title: loc.store_title
  });

  //Convert distance to miles (readable distance) for display purposes
  loc.readable_distance = (google.maps.geometry.spherical.
    computeDistanceBetween(search_center, loc_position)*
    0.000621371).toFixed(2);
});
```

The important thing about this code is that it renders markers for all the locations, but a subset of them will be visible.

### Figuring out which Locations are Visible

If you want to display additional information in the HTML related to current visible locations (such as in the screenshot at the top of this post), you might consider using the map.getBounds.contains() method:

```javascript
var render_locations = function(map) {
  var included_locations = [];
  //Loop through all locations to determine which locations are contained in the map boundary
  $.each(all_locations, function(i, loc) {
    if(map.getBounds().contains(new google.maps.LatLng(loc.latitude, loc.longitude))) {
            _push(loc);
    }
  }

  // sort locations by distance if desired

  // render included_locations
};
```

The above code determines which locations are visible, sorts those locations by readable distance, and then those locations are rendered in the HTML.

### Adding Listeners

After you've got your map and location markers added, a few map listeners will add more functionality, described below:

```javascript
var listener = google.maps.event.addListener(map, "idle", function() {
  render_locations(map);
  google.maps.event.addListener(map, 'center_changed', function() {
    render_locations(map);
  });
  google.maps.event.addListener(map, 'zoom_changed', function() {
    render_locations(map);
  });
});
```

After the map has loaded (via the map "idle" event), render_locations is called to render the HTML for visible locations. This method is also triggered any time the map center or zoom level is changed, so the HTML to the left of the map is updated whenever a user modifies the map bounds.

### Advanced Elements

Two advanced pieces implemented were the use of extending the map bounds and modifying listeners in a mobile environment. When it was desired that the map explicitly contain a set of locations within the map bounds, the following code was used:

```javascript
var current_bounds = results[0].geometry.bounds;
$.each(locations_to_include, function(i, loc) {
  current_bounds.extend(loc_position);
});
map.fitBounds(current_bounds);
```

And in a mobile environment, it was desired to disable various map options such as draggability, zoomability, and scroll wheel use. This was done with the following conditional:

```javascript
if($(window).width() < 656) {
  map.setOptions({
    draggable: false,
    zoomControl: false,
    scrollwheel: false,
    scrollwheel: false,
    disableDoubleClickZoom: true,
    streetViewControl: false
  });
}
```

### Conclusion

Of course, all the code shown above is just in snippet form. Many of the building blocks described above were combined to build a user-friendly map feature. There are a lot of additional map features – [check out the documentation](https://developers.google.com/maps/documentation/webservices/) to learn more.
