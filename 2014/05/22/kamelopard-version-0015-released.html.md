---
author: Josh Tolley
gh_issue_number: 984
tags: gis, google-earth, kamelopard, liquid-galaxy, open-source
title: Kamelopard version 0.0.15 released
---

<div class="separator" style="clear: both; text-align: center; float: left"><a href="https://en.wikipedia.org/wiki/Camelopardalis" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="https://upload.wikimedia.org/wikipedia/en/5/55/Camelopardalisurania.jpg"/></a><p align="center"><small>The Camelopardalis constellation, as shown in <a href="http://www.ianridpath.com/atlases/urania.htm">Urania's Mirror</a></small></p></div>

I've just pushed [version 0.0.15 of Kamelopard](http://rubygems.org/gems/kamelopard) to RubyGems. As described in [several](http://blog.endpoint.com/2011/08/giraffes-and-liquid-galaxy.html) [previous](http://blog.endpoint.com/2011/11/kamelopard-release.html) [blog](http://blog.endpoint.com/2013/02/kamelopard-updates.html) [posts](http://blog.endpoint.com/2013/12/new-kamelopard-version.html), Kamelopard is a Ruby gem designed to create KML documents quickly and easily. We use it to create content for our [Liquid Galaxy](http://liquidgalaxy.endpoint.com/) customers. This release doesn't include any major new features, rather it provides a number of small but very helpful modifications that taken together make life much easier.

## New Spline Types

Perhaps the most useful of these new features relate to spline functions, introduced in Kamelopard version 0.0.12. The original spline function interface [described here](https://code.google.com/p/liquid-galaxy/wiki/KamelopardFunctions#Multidimensional_functions) accepts a series of equi-dimensional vectors as control points, and returns vectors as results, but there's no indication of what each dimension in the vector means. This is convenient in that you can use splines to make nice paths through any number of dimensions and use them however you'd like, but in practice we most commonly want to make tours which fly through sets of either KML *Points* or *AbstractViews* (*Points* include just a latitude, longitude, and altitude, but *AbstractViews* include a direction vector, so they describe cameras and their positions). Two new classes, called *PointSplineFunction* and *ViewSplineFunction*, accept *Points* and *AbstractViews* respectively as their control points, and return those types when evaluated, freeing the user from having to map each control point's coordinates to a simple vector.

Often when creating tours, we'll use Google Earth to find a set of views we like, save them to a KML file, and then write a script to make a tour out of those placemarks. With these new classes, that becomes much easier. Here's an example which ingests a KML file containing several placemarks, and creates a simple spline-based tour through them, in the order in which they appear in the KML file.

```ruby
sp = Kamelopard::Functions::ViewSpline.new
each_placemark(XML::Document.file('waypoints.kml')) do |p, v|
  sp.add_control_point(w, 10)
end

(1..30).each do |i|
  fly_to sp.run_function(i.to_f/30.0), :duration => 0.8, :mode => :smooth
end
```

This uses the *each_placemark* function Kamelopard has had for quite a while to iterate through the file's placemarks and create control points, and then calculates the value of the spline along 30 points to create the flight path. This is such a common idiom when making tours that this Kamelopard version makes it even easier with a new *fly_placemarks* helper function. Using the new function, the code above becomes simply this:

```ruby
fly_placemarks XML::Document.file('waypoints.kml')
```

## More Flexible Geocoding

Kamelopard tries to make it easy to use geocoding services, which allow users to convert things like street addresses into latitudes and longitudes. This has its difficulties, as service providers regularly change formats or requirements, or quit the business altogether. Kamelopard has supported various geocoders in its time; this version finally adds support for Google's service. I'd left it out in previous versions because of an incorrect understanding of Google's licensing terms. It became important now because for the data we had from one particular client, Google's geocoding was significantly more accurate than the MapQuest geocoder I had been using previously. For different data sets, of course, some other service might get the most accurate results, but geocoding accuracy is a big concern for the work we do. No client wants to ask their shiny new Liquid Galaxy to zoom in on the corporate headquarters and see instead a seven screen panorama of the neighboring grocery store.

For geocoding projects of your own, there are a few considerations to keep in mind. First, geocoding services often impose usage limits. We'll sometimes find when geocoding a list of addresses that the service rejects every third or fourth query simply because we're querying faster than it wants to allow. They generally limit the number of queries allowed in one day, too, so debug your scripts using a small list of addresses before trying out a whole bunch at once. Having a project delayed simply because the geocoding service has stopped talking to you for the day is frustrating. Finally, it's often a good idea to geocode in one step, save the results somewhere, and make the tour in a second step using the saved results. This frees you from dependence on access to the service, and allows manual tweaking of the geocoded results. Note, however, that some services' licenses forbid saving the results anywhere.

Whichever service you end up using, Kamelopard code for geocoding generally looks like this:

```ruby
g = GoogleGeocoder.new('my-api-key')
results = {}

Addresses.each do |t|
  results[t] = g.lookup(t)
end
```

Most services require an API key used for authorization, and return a large JSON structure which includes latitude and longitude, a status code, result quality, and any other useful information the service provider thinks you should have.

## Other Updates

It seems it has always been hard for newcomers to get used to Kamelopard. This version includes a number of updates to [the documentation](http://rubydoc.info/gems/kamelopard/0.0.15/), which will hopefully make it easier for them. It also includes new helper functions for writing out all KML documents in memory at once, and creating KMZ files automatically where desired.

Please give the new version a try. We'd love to hear how it's being used.
