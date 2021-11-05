---
author: Josh Tolley
title: Kamelopard Release
github_issue_number: 517
tags:
- visionport
- open-source
- ruby
- kamelopard
date: 2011-11-30
---

<a href="/blog/2011/11/kamelopard-release/image-0.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" src="/blog/2011/11/kamelopard-release/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 320px; height: 238px;"/></a>

After completing no small amount of refactoring, I’m pleased to announce a new release of [Kamelopard](https://github.com/eggyknap/Kamelopard), a Ruby gem for generating [KML](https://en.wikipedia.org/wiki/Keyhole_Markup_Language). KML, as with most XML variants, requires an awful lot of typing to write by hand; Kamelopard makes it all much easier by mechanically generating all the repetitive XML bits and letting the developer focus on content. An example of this appears below, but first, here’s what has changed most recently:

- All KML output comes via Ruby’s REXML library, rather than simply as string data that happens to contain XML. This not only makes it much harder for Kamelopard developers to mess up basic syntax, it also allows examination and modification of the KML data using XML standards such as XPath.
- Kamelopard classes now live within a module, preventing namespace collisions. This is important for any large-ish library, and probably should have been done all along. Previous to this, some classes had awfully strange names designed to prevent namespace collisions; these classes have been changed to simpler, more intuitive names now that collisions aren’t a problem.
- Perhaps the biggest change is the incorporation of a large and (hopefully) comprehensive test suite. I’m a fan of test-driven development, but didn’t start off on the right foot with Kamelopard. It originally shipped with a Ruby script that tried a few examples and hoped it didn’t crash; that has been replaced with a full [RSpec](http://rspec.info/)-based test suite, including tests for each class and in particular, extensive test of the KML output to ensure it meets the KML specification. Run these tests from the Kamelopard source with the command

```plain
rspec spec/*
```

Now for some code. We recently got a data set containing several thousand locations, describing the movement of an aircraft on final approach and landing, with the request that we turn it into a Google Earth tour, where the viewer would follow the aircraft’s path, flight simulator style. The actual KML result is over 56,000 lines, but the KML code is fairly simple:

```ruby
require 'rubygems'
require 'kamelopard'
require 'csv'

CSV.foreach(ARGV[0]) do |row|
    time = row[0]
    lon = row[1].to_f
    lat = row[2].to_f
    alt = row[3].to_f

    p = Kamelopard::Point.new lon, lat, alt, :absolute
    c = Kamelopard::Camera.new(p, get_heading, get_tilt, get_roll, :absolute)
    f = Kamelopard::FlyTo.new c, nil, pause, :smooth
end

puts Kamelopard::Document.instance.get_kml_document.to_s
```

Along with some trigonometry and linear algebra to calculate the heading, tilt, and roll, and a CSV file of data points, the script above is all it took; the KML result runs correctly in Google Earth without further modification. Kamelopard has been published to RubyGems.org, so installation is simply 

```plain
gem install kamelopard
```

Give it a try!
