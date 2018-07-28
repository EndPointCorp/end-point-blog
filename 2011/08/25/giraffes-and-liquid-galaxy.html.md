---
author: Josh Tolley
gh_issue_number: 489
tags: google-earth, liquid-galaxy
title: Giraffes and Liquid Galaxy
---

<a href="https://en.wikipedia.org/wiki/File:Al_Ain_Zoo_Giraffe.JPG" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" src="/blog/2011/08/25/giraffes-and-liquid-galaxy/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 614px; height: 411px;"/></a>

We build lots and lots of Google Earth tours, typically for use with a [Liquid Galaxy](https://liquidgalaxy.endpoint.com/). These tours tell Google Earth to start at one point and fly to another, displaying various images along the way. They’re written in an XML-based language called [Keyhole Markup Language](https://en.wikipedia.org/wiki/Keyhole_Markup_Language), or [KML](https://developers.google.com/kml/documentation/kmlreference?csw=1). Various KML elements describe points on the globe, 3D objects, tracks through space, or other items, and a series of Google-specific KML extensions can define an automated tour in which Google Earth flies through these objects.

Now for a bit of dogma: writing large volumes of XML by hand is a drag. Writing KML is no exception. So when I started building KML tours, I was keen to build or find tools to make it easier. For my first KML project, making a tour through each End Point employee’s home city, I built a Perl script to convert a file of employee data to KML. This worked well enough, but I soon learned typing out all the KML was just half the pain. The other half was adjusting camera paths, camera angles, timing, and all sorts of other little things. Unfortunately all these adjustments had to be done by trial and error, and all by hand. Getting Google Earth’s camera to circle a particular point, for instance, takes about three screens worth of KML code. If a point’s coordinates were off or a tour’s timing wasn’t quite right, I had to find the right spot in a vast field of KML, tweak a number, and try it all again.

Enter [Kamelopard](https://github.com/eggyknap/Kamelopard). Named, as dictated by long-standing [End Point tradition](https://www.bucardo.org), after a strange animal, Kamelopard is a Ruby gem designed to make all this easier (“Camelopard” is the ancient English word for “giraffe” and several mythical and heraldic giraffe-like creatures; the various modern giraffe sub-species are grouped under the name *Giraffa camelopardalis*). Right now it’s not much more than a set of classes which mirror the basic KML objects—​or most of them, anyway—​but already it has proven itself very useful. For instance, for one project we’re working on, a Ruby script of about 150 lines uses Kamelopard to digest a set of data files and produce a 12,000 line KML file. Fortunately, Kamelopard is sufficiently flexible that I can finish adjusting all the timing and camera angles and other details in the Ruby code, without having to dig through the KML output itself; we can regenerate the KML with whatever tweaks we need, as often as we need it.

As a very simple example, here’s a Kamelopard script to turn a CSV file into KML. The CSV contains the name, description, latitude, and longitude of a bunch of placemarks (e.g. “Mount Everest”,“The world’s tallest mountain”,“27d58m37.15s N”,“86d55m15.93s E”), and the script turns them into KML, including a Google Earth tour that will fly past each in turn. The KML result amounts to about 45 lines per placemark, so the Ruby version is much more concise and much simpler to modify.

```ruby
require 'rubygems'
require 'kamelopard'
require 'csv'

CSV.foreach('placemarks.csv') do |a|
    pl = Placemark.new a[0], point(a[3], a[2])
    pl.description = a[1]

    mod_popup_for pl, 1
    fly_to pl, 5
    pause 3
    mod_popup_for pl, 0
end

puts get_kml
```

Along with its library of classes, Kamelopard does have a (fairly unorganized, ad hoc) set of helper functions which I hope one day will evolve into a full-fledged domain-specific language. While they’re currently loosely organized and none too intelligent, there are a few jewels worth noting. For instance, my multi-page KML to orbit a point takes one line of Kamelopard. Conversion from one latitude / longitude notation to another happens automatically (manually converting 24°10’44.3994” N, 55°44’25.7274” E to the decimal notation KML requires becomes a dreary task when performed manually for ten or twenty different points). Finally, Kamelopard includes a helper function for Google’s Geocoding API, so users can translate addresses and location names to latitude and longitude.

Kamelopard’s future development will most likely follow whatever lines our clients, and any contributors that care to help out, most wish to pursue, but I suspect it will include increased automation of tour timing, so developers don’t need to figure out timings for each step in a tour manually, and more helper functions to create objects, so users don’t have to instantiate classes directly, and can get more done in a line of code.

I imagine the audience is fairly small, but I’d welcome any feedback, suggestions, patches, and interest.
