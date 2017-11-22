---
author: Josh Tolley
gh_issue_number: 788
tags: google-earth, kamelopard, liquid-galaxy, open-source, ruby
title: Creating Smooth Flight Paths in Google Earth with Kamelopard and Math
---

<a href="http://commons.wikimedia.org/wiki/File:Camel_in_Petra3.jpg" imageanchor="1" style="padding: 10px"><img border="0" src="/blog/2013/04/15/creating-smooth-flight-paths-in-google/image-0.jpeg"/></a>

The major motivation for writing Kamelopard was that writing XML by hand is a pain in the neck. But there were other motivations as well. In particular we found some limitations of Google Earth's default FlyTo behavior, and wanted to be able to address them flexibly. Version 0.0.11, just released, does exactly that.

<a href="/blog/2013/04/15/creating-smooth-flight-paths-in-google/image-0-big.png" imageanchor="1"><img border="0" src="/blog/2013/04/15/creating-smooth-flight-paths-in-google/image-0.png"/></a>

Bezier curve, similar to a cspline

Our clients often want Google Earth's camera to fly smoothly from one place to another, through a precisely defined set of waypoints. Earth does this with a [FlyTo](https://developers.google.com/kml/documentation/kmlreference#gxflyto), one of Google's extensions to KML. It tells Earth to move from its current camera position to a new one, following a nice path Google Earth calculates automatically. Most of the time this works just fine, but on occasion, Earth's automatic path will run into buildings or mountains, or do other unexpected and strange things. There are a few KML tricks we've learned to handle those cases, but it would often be nice to have tighter control. Unfortunately getting that level of control means calculating the flight path ourselves. We've developed the smarts to do that, a little bit at a time.

The first version involved [Catmull-Rom splines](http://en.wikipedia.org/wiki/Cubic_Hermite_spline), a variant of a cubic spline (or "cspline") that gives nice results and is fairly simple to calculate. The idea of a spline is to build a curve that passes smoothly through a set of "control points". To achieve this, in essence we project those points into a vector space defined by a special set of cubic basis functions. In other words, we turn our control points into a matrix and multiply it by another matrix to end up with a function describing our path. The general cspline requires "tangents" in addition to the control points to define behavior at the ends of the curve; the Catmull-Rom variant derives the tangents from the control points, which limits flexibility but works well for our purposes. So if we want a path between several points on a globe, we use those points as the control points in the spline, and Kamelopard would make a nice path between them automatically. Better still, csplines can support any number of dimensions, so we can include factors such as altitude or heading in the generated curve. As it turned out, though, we didn't end up using this spline very much. It was built on top of some other code that later proved insufficient for what we wanted, and that was removed.

<a href="/blog/2013/04/15/creating-smooth-flight-paths-in-google/image-1-big.png" imageanchor="1"><img border="0" src="/blog/2013/04/15/creating-smooth-flight-paths-in-google/image-1.png"/></a>

Parabola defined by three points

The next iteration, recently committed, allows Kamelopard scripts to define mathematical functions in terms of the same control points, and asks Kamelopard to use those functions to build smooth paths. Right now Kamelopard supports cubic, quadratic, and linear functions; others would of course be possible given sufficient reason to develop them, but the existing functions seem to work very well. The matrix math to interpolate these types of functions based on control points was straightforward, and they can define a wide variety of paths.

One limitation of the new code compared to the old: the spline functions would take any number of control points, whereas the mathematical function versions are more limited. Three points in a particular order, for instance, uniquely describe a quadratic curve. As a result, our quadratic function implementation only supports three control points. I plan to reintroduce splines in the future for situations where this limitation causes problems. These functions are especially flexible, though, in that they can determine not only the camera's latitude and longitude, but also its heading, altitude, and various other things including the duration of each FlyTo. Our cspline implementation was intended to handle those dimensions as well, but never got that far along.

So how does all this work? Here is a simple example, showing an interpolated path from a point about 10 km above one of the cows near my house, to another point a bit to the north. First, the [KML itself is available for download](http://josh.endpoint.com/kamelopard_functions.kml); in Google Earth, it looks like this (click on the image to get the larger version):

<a href="/blog/2013/04/15/creating-smooth-flight-paths-in-google/image-2-big.png" imageanchor="1"><img border="0" src="/blog/2013/04/15/creating-smooth-flight-paths-in-google/image-2.png"/></a>

Here's the code:

```ruby
require 'rubygems'
require 'kamelopard'

include Kamelopard
include Kamelopard::Functions

a = make_function_path(10,
    :latitude => Line.interpolate(38.8, 40.3),
    :longitude => Cubic.interpolate(-112.4, -111.9, -0.5, -113, 0.5, -110),
    :altitude => Line.interpolate(10000, 2000),
    :heading => Line.interpolate(0, 90),
    :tilt => Line.interpolate(40.0, 90),
    :altitudeMode => :absolute,
    :show_placemarks => 1,
    :duration => Quadratic.interpolate(2.0, 4.0, 0.0, 1.0),
)

name_document 'Functions test'
name_folder 'Placemarks'
name_tour 'Function test'

write_kml_to 'doc.kml'
```

The make_function_path call does most of the work here. We've given it functions to interpolate the latitude, longitude, and other characteristics of the flight path we want, along with a few other options described in the gem documentation. We also tell it how many points to create in the path, in this case 10. The root of the flying is still Google Earth's FlyTo algorithm, but we set to *smooth* mode, to keep Earth doing more precisely what we want it to, and we create waypoints on the flight path frequently enough that we have tight control over where Earth actually flies.

Creating the functions themselves is relatively easy, but you need to remember the order of the arguments, which in this case at least can be confusing. I'll probably change it in a future version, once I come up with something better. This code defines the latitude function in terms of the beginning and ending latitude, and that's all since we only need two points to define a line. The quadratic and cubic functions take three and four points, respectively. Although not demonstrated here, make_function_paths can also take a code block for more complex behaviors at each point.

In the end this generates a Google Earth Tour, which flies from the start point to the end point very smoothly. This code has demonstrated that it works well for flights over large areas; my next goal is to use it to navigate between 3D buildings on a precisely defined path. That will be for another article, though.
