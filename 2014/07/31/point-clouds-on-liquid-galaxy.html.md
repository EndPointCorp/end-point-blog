---
author: Joshua Tolley
gh_issue_number: 1019
tags: graphics, liquid-galaxy
title: Point Clouds on the Liquid Galaxy
---



<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/07/31/point-clouds-on-liquid-galaxy/image-0.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="262" src="/blog/2014/07/31/point-clouds-on-liquid-galaxy/image-0.jpeg" width="400"/></a><p><small>Image by <a href="http://commons.wikimedia.org/wiki/User:Stoermerjp">Stoermerjp</a>, unmodified <a href="http://creativecommons.org/licenses/by-sa/3.0/">(CC BY-SA 3.0)</a></small></p></div>

The Liquid Galaxy began as a system to display geographic data through Google Earth, but it has expanded quickly as a display platform for other types of information. We've used Liquid Galaxies for panoramic images and video, three dimensional models of all sorts, as well as time-lapse renderings of weather, infrastructure, and economic data. Now we've added support for a new type of data, the [point cloud](http://en.wikipedia.org/wiki/Point_cloud).

"Point cloud" is simply the common term for a data set consisting of individual points, often in three-dimensional space, and frequently very large, containing thousands or millions of entries. Points in a cloud can include not just coordinate data, but other information as well, and because this sort of data can come from many different fields, the possible variations are endless. For instance, the terrain features visible in Google Earth began life as point clouds, the output of an aerial scanning device such as a LIDAR scanner. These scanners sweep their field of view rapidly, scanning millions of points to determine their location and any other interesting measurements -- color, for instance, or temperature -- and with that data create a point cloud. Smaller scale hardware scanners have made their way into modern life, scanning rooms and buildings, or complex objects. A few years ago, [the band Radiohead collaborated with Google](http://techcrunch.com/2008/07/14/radiohead-partners-with-google-for-music-video-launch/) to use the 3-D scanning techniques to film a music video, and published the resulting point cloud on [Google Code](https://code.google.com/p/radiohead/).

<div class="separator" style="clear: both; text-align: center; float: right; clear: right"><p><a href="/blog/2014/07/31/point-clouds-on-liquid-galaxy/image-1.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" height="320" src="/blog/2014/07/31/point-clouds-on-liquid-galaxy/image-1.jpeg" width="228"/></a></p><p><small>Image by <a href="http://commons.wikimedia.org/wiki/User:Xorx">Xorx</a>, unmodified <a href="http://creativecommons.org/licenses/by-sa/3.0/">(CC BY-SA 3.0)</a></small></p><p></p></div>

For the Liquid Galaxy platform, we modified an open source point cloud viewer called [Potree](http://potree.org/) to allow one master instance to control several others. Potree is a WebGL application. It runs in a browser, and depends on [three.js](http://threejs.org/), a widely used WebGL library. Generally speaking, to convert an application to run on a Liquid Galaxy, the developer must give the software two separate modes: one which allows normal user control and transmits information to a central data bus, and another which receives information from the bus and uses it to create its own modified display. In this case, where the application simply loads a model and lets the user move it around, the "master" mode tracks all camera movements and sends them to the other Liquid Galaxy nodes, which will draw the same point cloud in the same orientation as the master, but with the camera pointing offset to the left or right a certain amount. We've dubbed our version [lg-potree](https://github.com/EndPointCorp/lg-potree).

This marks the debut of a simple three.js extension we've been working on, which we've called [lg-three.js](https://github.com/EndPointCorp/lg-three), designed to make it easy to adapt three.js applications for the Liquid Galaxy. lg-three.js gives the programmer an interface for capturing and serializing things like camera movements or other scene changes on the master node, and de-serializing and using that data on the other nodes, hopefully without having to modify the original application much. Some applications' structure doesn't lend itself well to lg-three, but potree proved fairly straightforward.

With that introduction, please enjoy this demonstration.

<iframe allowfullscreen="" frameborder="0" height="315" src="//www.youtube.com/embed/GiWjUI97viQ" width="560"></iframe>


