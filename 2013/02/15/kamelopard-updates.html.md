---
author: Josh Tolley
gh_issue_number: 762
tags: google-earth, liquid-galaxy, open-source, ruby, kamelopard
title: Kamelopard Updates
---

I’ve just pushed [Kamelopard v0.0.10](https://rubygems.org/gems/kamelopard) to RubyGems. With the last couple of releases, Kamelopard has gained a couple of useful features I felt deserved some additional attention.

### Support for viewsyncrelay actions

Many of our Liquid Galaxy tours require more than just Google Earth. For instance, it’s not uncommon to want audio or video media to play at a certain point in the tour. We may want our Liquid Galaxy enabled panoramic image viewer to start up and display an image, or perhaps we need to signal some other external process. Unfortunately Google Earth tours don’t support configuration to run these actions directly upon reaching a certain point, but there are alternatives. Google Earth synchronizes nodes in a Liquid Galaxy with what are called ViewSync packets, which tell all the slave nodes exactly where a master node’s camera is positioned, in terms of latitude, longitude, tilt, etc. We can watch this traffic to determine the master node’s progress through a tour and trigger actions at defined locations, and we use an application called viewsyncrelay (available [here](http://code.google.com/p/liquid-galaxy/source/browse/gnu_linux/home/lg/bin/viewsyncrelay.pl)) to do exactly that. We configure viewsyncrelay to run certain *actions* when the ViewSync traffic matches a set of constraints. For instance, an action might require ViewSync packets to fall within a certain latitude, longitude, altitude, and heading, and a particular previous action might have to run first in order to activate this one.

This works well enough for most purposes, but the viewsyncrelay configuration files can become complicated, and difficult to debug. Here’s where Kamelopard comes in. Now, the same code that creates a tour can create viewsyncrelay actions. Here’s an example. The code is still a bit unwieldy; it will get simpler and more elegant in future versions, after we’ve seen the best ways people come up with to use the feature.

```ruby
require 'rubygems'
require 'kamelopard'

name_folder 'test'
name_document 'test'
pt = point 100, 100
pl = placemark 'test placemark', :geometry => pt
get_folder << pl

Kamelopard::VSRAction.new('action name',
    :action => 'mplayer play_this_video.webm',
    :constraints => {
        :latitude => to_constraint(band(100, 0.1).collect{ |l| lat_check(l) }),
        :longitude => to_constraint(band(100, 0.1).collect{ |l| long_check(l) }),
    }
)

write_kml_to 'doc.kml'
write_actions_to 'actions.yml'
```

In addition to the VSRAction object, these changes introduce a few new functions, including those shown here: band(a, b) returns a +/- b, in an array; lat_check() and long_check() ensure each value in the array is a valid latitude or longitude; and to_constraint() turns this validated array into a string suitable for use in a viewsyncrelay constraint. As I mentioned, this may prove awkward, but it’s a first step. This code creates a file called actions.yml, ready for use in viewsyncrelay:

```nohighlight
---
actions:
- name: action name
  input: ALL
  action: mplayer play_this_video.webm
  repeat: DEFAULT
  constraints:
    :latitude: ! '[-80.1, -79.9]'
    :longitude: ! '[99.9, 100.1]'
```

### Master/slave modes

Liquid Galaxy tours often consist of two different KML files: one to run on the master, and another to run on each of the slaves. The slave versions generally don’t include all of the screen overlay and network link objects used by the master, in particular, but there are plenty of objects that you might not want on the slaves. In the past we’ve had to edit the KML files manually to remove unnecessary objects, which is of course error prone, sometimes difficult, and something we have to redo every time we run our Kamelopard script and create a new tour version. Now, Kamelopard supports tagging objects as “master-only”, and creating KML documents in either normal or master-only mode, to make this process entirely automatic. Here’s an example:

```ruby
require 'rubygems'
require 'kamelopard'

name_folder 'test'
name_document 'test'
pt = point 100, 100
pl = placemark 'test placemark', :geometry => pt
get_folder << pl

get_folder.master_only = true
write_kml_to 'slave.kml'
get_document.master_mode = true
write_kml_to 'master.kml'
```

This results in two files, called master.kml and slave.kml. Only master.kml contains the Folder object:

```xml
<!--?xml version="1.0" encoding="UTF-8"?-->
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2">
  <document id="Document_1">
    <name>test</name>
    <visibility>1</visibility>
    <open>0</open>
    <folder id="Folder_2">
      <name>test</name>
      <visibility>1</visibility>
      <open>0</open>
      <placemark id="Placemark_4">
        <name>test placemark</name>
        <visibility>1</visibility>
        <open>0</open>
        <point id="Point_3">
          <coordinates>100.0, 100.0, 0</coordinates>
          <extrude>0</extrude>
          <altitudemode>clampToGround</altitudemode>
        </point>
      </placemark>
    </folder>
  </document>
</kml>
```

The slave is essentially empty, because we didn’t tell Kamelopard about any objects that weren’t master-only:

```xml
<!--?xml version="1.0" encoding="UTF-8"?-->
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2">
  <document id="Document_1">
    <name>test</name>
    <visibility>1</visibility>
    <open>0</open>
  </document>
</kml>
```

### New repository

Since Kamelopard is developed primarily for our use creating Liquid Galaxy tours, it has been moved from github to a portion of the [GitHub Liquid Galaxy project](https://github.com/liquidgalaxy/liquid-galaxy). Clone the repository at https://github.com/liquidgalaxy/liquid-galaxy to get your own copy, or install the gem from rubygems to play around.
