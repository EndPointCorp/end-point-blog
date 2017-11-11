---
author: Steph Skardal
gh_issue_number: 771
tags: interchange, javascript, jquery, maps
title: Interchange Case Study with Google Maps API
---

<img border="0" src="/blog/2013/03/29/paper-source-case-study-with-google/image-0.png"/>

Basic Google map with location markers.

Recently, I've been working with the [Google Maps API](https://developers.google.com/maps/) for one of our large [Interchange](/technology/perl-interchange) clients with over 40 physical stores throughout the US. On their website, they had previously been managing static HTML pages for these 40 physical stores to share store information, location, and hours. They wanted to move in the direction of something more dynamic with interactive maps. After doing a bit of research on search options out there, I decided to go with the Google Maps API. This article discusses basic implementation of map rendering, search functionality, as well as interesting edge case behavior.

### **Basic Map Implementation**

In it's most simple form, the markup required for adding a basic map with markers is the shown below. Read more at [Google Maps Documentation](https://developers.google.com/maps/).

**HTML**

```html
&lt;div id="map"&gt;&lt;/div&gt;
```

**CSS**

```html
#map {
  height: 500px;
  width: 500px;
}
```

**JavaScript**

```javascript
//mapOptions defined here
var mapOptions = {
  center: new google.maps.LatLng(40, -98),
  zoom: 3,
  mapTypeId: google.maps.MapTypeId.ROADMAP
};

//map is the HTML DOM element ID where it will be rendered
var map = new google.maps.Map(document.getElementById("map"), mapOptions);

//all locations is a JSON object representing locations,
//where each location has a latitude and longitude
$.each(all_locations, function(i, loc) {
  var marker = new google.maps.Marker({
    map: map,
    position: new google.maps.LatLng(loc.latitude, loc.longitude)
  });
})
```

### **Building Search Functionality**

<img border="0" src="/blog/2013/03/29/paper-source-case-study-with-google/image-1.png" width="700"/>

Search interface. Search results are listed on the left, and map with markers is shown on the right.

Next up, I needed to build out search functionality. Google has its own geocoder to allow address searches. Here is the basic markup for running a search:

```javascript
var geocoder = new google.maps.Geocoder();
//search is a variable representing the user search, such as a zip code, city name, or state name
geocoder.geocode({ 'address' : search }, function(results, status) {
  var search_center = results[0].geometry.bounds.getCenter();

  var mapOptions = {
    center: search_center,
    zoom: 10,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById("map"), mapOptions);

  $.each(all_locations, function(i, loc) {
    var marker = new google.maps.Marker({
      map: map,
      position: new google.maps.LatLng(loc.latitude, loc.longitude)
    });
  })
}
```

In the above code, the search term is passed into the Geocoder object and a map with all locations marked is rendered. To determine which markers are in the visible map boundaries, the following map.getBounds().contains() method would be leveraged:

```javascript
var visible_locations = [];
$.each(all_locations, function(i, loc) {
  if(map.getBounds().contains(new google.maps.LatLng(loc.latitude, loc.longitude))) {
    visible_locations.push(loc);
  }
});
//render visible locations to the left of the map
```

One final step here is to add a listener to the map, so that visible locations are updated when the user zooms in and out. This is accomplished with the following listener:

```javascript
google.maps.event.addListener(map, 'zoom_changed', function() {
  //call method to rerender visible locations
});
```

### **Handling Zero Results**

What happens if your Geocoder object can't find the address? A simple conditional can be used:

```javascript
geocoder.geocode({ 'address' : search }, function(results, status) {
  if(status == "ZERO_RESULTS") {
    //notify customer that no results have been found
  } else {
    //got results, render location
  }
}
```

### **Calculate and Sort by Distance**

The next layer of logic I needed to add was the ability to determine the distance between the search address and sort the results by distance. To calculate distance, I did some research and settled on the following code:

```javascript
var R = 6371;
$.each(all_locations, function(i, loc) {
  var loc_position = new google.maps.LatLng(loc.latitude, loc.longitude);
  var dLat  = locations.rad(loc.latitude - search_center.lat());
  var dLong = locations.rad(loc.longitude - search_center.lng());

  //calculate spherical distance between search position and location
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
  Math.cos(locations.rad(search_center.lat())) *
    Math.cos(locations.rad(search_center.lat())) *
    Math.sin(dLong/2) * Math.sin(dLong/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  var d = R * c;
  loc.distance = d;

  //convert distance to miles
  loc.readable_distance =
    (google.maps.geometry.spherical.computeDistanceBetween(search_center, loc_position) *
    0.000621371).toFixed(2);
});
```

To sort the locations by distance, I leverage jQuery sort:

```javascript
var sort_by_distance = function(obj) {
  return obj.sort(function(a, b) {
    if(a.distance &gt; b.distance) {
      return 1;
    } else {
      return -1;
    }
  })
};
var sorted_locations = sort_by_distance(all_locations);
```

### **Adjust Map Boundaries to Include Specific Markers**

Another interesting use case I needed to handle was forcing the map to zoom out to include stores within 100 miles if there was nothing in the initial map boundaries, e.g.:

<img border="0" src="/blog/2013/03/29/paper-source-case-study-with-google/image-2.png" width="700"/>

The search for "27103" doesn't return any nearby stores, so the map is extended to include stores within 100 miles.

To accomplish this functionality, I added a bit of code to extend the map boundaries:

```javascript
geocoder.geocode({ 'address' : search }, function(results, status) {
  var search_center = results[0].geometry.bounds.getCenter();

  var mapOptions = {
    center: search_center,
    zoom: 10,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById("map"), mapOptions);
  var current_bounds = results[0].geometry.bounds;

  $.each(all_locations, function(i, loc) {
    var loc_position = new google.maps.LatLng(loc.latitude, loc.longitude);
    var dLat  = locations.rad(loc.latitude - search_center.lat());
    var dLong = locations.rad(loc.longitude - search_center.lng());

    //calculate spherical distance between search position and location
    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(locations.rad(search_center.lat())) *
      Math.cos(locations.rad(search_center.lat())) *
      Math.sin(dLong/2) * Math.sin(dLong/2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c;
    loc.distance = d;

    //convert distance to miles
    loc.readable_distance =
      (google.maps.geometry.spherical.computeDistanceBetween(search_center, loc_position) *
      0.000621371).toFixed(2);

    var marker = new google.maps.Marker({
      map: map,
      position: new google.maps.LatLng(loc.latitude, loc.longitude)
    });

    if(loc.readable_distance &lt; 100) {
      current_bounds.extend(loc_position);
    }
  });

  //Google map method to fit map boundaries to desired boundaries
  map.fitBounds(current_bounds);
}
```

### **Disable Scroll and Zoom on Mobile-Sized Devices**

One final behavior needed was to disable map zooming and scrolling on mobile devices, to improve the usability on mobile/touch interfaces. Here's how this was accomplished:

```javascript
var options_listener = google.maps.event.addListener(map, "idle", function() {
  if($(window).width() &lt; 656) {
    map.setOptions({
      draggable: false,
      zoomControl: false,
      scrollwheel: false,
      disableDoubleClickZoom: true,
      streetViewControl: false
    });
  }
  google.maps.event.removeListener(options_listener);
});
```

### **Conclusion**

With all this code, the final location search functionality includes:

- Basic United States map rendering to display all physical store locations.
- Search by location which shows stores within 100 miles, and allows users to zoom in and out to adjust their search. Search lists results sorted by distance.
- "Saved" or "Quick" searches by states, which displays all physical stores by state.
- Adjustment of mobile display map options.
