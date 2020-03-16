---
author: Greg Davidson
gh_issue_number: 1134
tags: html, javascript
title: Google Maps JavaScript API LatLng Property Name Changes
---

### Debugging Broken Maps

A few weeks ago I had to troubleshoot some Google Maps related code that had suddenly stopped working. Some debugging revealed the issue: the code adding markers to the page was attempting to access properties that did not exist. This seemed odd because the latitude and longitude values were the result of a geocoding request which was completing successfully. The other thing which stood out to me were the property names themselves:

```
var myLoc = new google.maps.LatLng(results[0].geometry.location.k, results[0].geometry.location.D);
```

It looked like the original author had inspected the geocoded response, found the ‘k’ and ‘D’ properties which held latitude and longitude values and used them in their maps code. This had all been working fine until Google released a [new version](https://groups.google.com/forum/#!topic/google-maps-js-api-v3-notify/tYp4JKtkDg0) of their JavaScript API. Sites that did not [specify a particular version](https://developers.google.com/maps/documentation/javascript/basics#Versioning) of the API were upgraded to the new version automatically. If you have Google Maps code which stopped working recently this might be the reason why.  

### The Solution: Use the built-in methods in the LatLng class

<img alt="Screen Shot 2015 06 10 at 3 47 32 PM" border="0" height="308" src="/blog/2015/06/11/google-maps-javascript-api-latlng/image-0.png" title="Screen Shot 2015-06-10 at 3.47.32 PM.png" width="419"/> 

I recalled there being some helper methods for LatLng objects and confirmed this with a visit to the [docs for the LatLng class](https://developers.google.com/maps/documentation/javascript/3.exp/reference#LatLng) which had recently been updated and given the [Material design](https://material.io/guidelines/material-design/introduction.html) treatment—​thanks Google! The lat() and lng() methods were what I needed and updating the code with them fixed the issue. The fixed code was similar to this: 

```
var myLoc = new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng());
```

### Digging Deeper

I was curious about this so I mapped out the differences between the three latest versions of the API:

<div class="table-scroll">
<table><thead>
<tr>       <th>API Version</th>       <th>Latitude Property</th>       <th>Longitude Property</th>       <th>Constructor Name</th>     </tr>
</thead>   <tbody>
<tr>      <td>3.21.x (experimental)</td>      <td>A</td>      <td>F</td>      <td>rf</td>     </tr>
<tr>      <td>3.20.x (release)</td>      <td>A</td>      <td>F</td>      <td>pf</td>     </tr>
<tr>      <td>3.19.x (frozen)</td>      <td>k</td>      <td>D</td>      <td>pf</td>     </tr>
</tbody> </table>
</div>

It seems to me that the property name changes are a result of running the Google Maps API code through the [Closure Compiler](https://developers.google.com/closure/compiler/). Make sure to use the built-in lat() and lng() methods as these property names are very likely to change again in future!
