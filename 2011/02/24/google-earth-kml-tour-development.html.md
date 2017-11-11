---
author: Adam Vollrath
gh_issue_number: 416
tags: google-earth, liquid-galaxy
title: Google Earth KML Tour Development Challenges on Liquid Galaxy
---

Because Liquid Galaxy runs Google Earth, it can easily visualize an organization's GIS data.  End Point also develops tours within Google Earth to better present this data.  A Liquid Galaxy's networked multi-system architecture presents unique technical challenges to these tours.

Many Google Earth tours incorporate [animations and dynamic updates](http://code.google.com/apis/kml/documentation/touring.html#updates)
using the <gx:AnimatedUpdate> element.  KML features in the Earth
environment can be modified, changed, or created during a tour,
including the size, style, and location of placemarks, the addition of
ground overlays, geometry, and more.

However, these updates are only executed on the Liquid Galaxy master
system running the tour, not sent to its slaves. Liquid Galaxy nodes communicate primarily via [ViewSync UDP datagrams](http://code.google.com/p/liquid-galaxy/wiki/GoogleEarth_ViewSync). These datagrams contain only the master's position in space and time. This means we cannot use <gx:AnimatedUpdate> to animate features across all Liquid Galaxy systems, sharply limiting its utility.

But tours can also [use chronological elements](http://code.google.com/apis/kml/documentation/time.html) to display, animate, and hide features.  Using <gx:TimeSpan> or <gx:TimeStamp> within an tour stop enables flying to a specific location in space *and* time.  All Google Earth features may be assigned a TimeStamp, and all Liquid Galaxy screens display the same chronological range of features.  This works around the single-system limitation on animation, and enables sweeping changes across all screens.  The picture below shows a data animation in progress across three screens; the green dots are filling in the area previously occupied by the red dots, while the time sliders in the upper left corners advance.

<a href="/blog/2011/02/24/google-earth-kml-tour-development/image-0.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577750933549080418" src="/blog/2011/02/24/google-earth-kml-tour-development/image-0.jpeg" style="display: block; margin: 0px auto 10px; text-align: center; cursor: pointer; width: 720px;"/></a>

Taking this technique a step further, we also "wrapped" some very large
KML datasets in NetworkLink elements, and wrapped those NetworkLinks in
Folder elements with TimeStamp elements as well.  This allowed fine
control over when to fetch and render the large set, just-in-time to be
featured in its own tour.  These large loads can cause the Earth client
to stutter, so we also stopped the flight motion and displayed a balloon
full of text for the audience.  A KML example of this wrapper is below.

```nohighlight
&lt;Folder&gt;
       &lt;name&gt;Region Link Two&lt;/name&gt;
       &lt;TimeStamp&gt;&lt;when&gt;2010-09-19T16:00:00Z&lt;/when&gt;&lt;/TimeStamp&gt;
       &lt;NetworkLink&gt;
               &lt;name&gt;Region Link Two&lt;/name&gt;
               &lt;Region&gt;
                       &lt;LatLonAltBox&gt;
                               &lt;north&gt;41.8&lt;/north&gt;
                               &lt;south&gt;41.6&lt;/south&gt;
                               &lt;east&gt;-86.1&lt;/east&gt;
                               &lt;west&gt;-86.3&lt;/west&gt;
                       &lt;/LatLonAltBox&gt;
                       &lt;Lod&gt;
                               &lt;minLodPixels&gt;256&lt;/minLodPixels&gt;
                               &lt;maxLodPixels&gt;-1&lt;/maxLodPixels&gt;
                       &lt;/Lod&gt;
               &lt;/Region&gt;
               &lt;Link&gt;
                       &lt;href&gt;network_view.kml&lt;/href&gt;
                       &lt;viewRefreshMode&gt;onRegion&lt;/viewRefreshMode&gt;
               &lt;/Link&gt;
       &lt;/NetworkLink&gt;
&lt;/Folder&gt;
```

These techniques, and the Liquid Galaxy platform, combine to coordinate a moving visual experience across the audience's entire field of view.  Animations highlight GIS data and narrate its story, creating an impressive presentation.
