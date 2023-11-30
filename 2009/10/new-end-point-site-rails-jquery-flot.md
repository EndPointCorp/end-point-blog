---
author: Steph Skardal
title: 'New End Point site launched: Rails, jQuery, Flot, blog feed'
github_issue_number: 206
tags:
- browsers
- company
- javascript
- rails
- cms
date: 2009-10-07
---

This week we launched a new website for End Point. Not only did the site get a facelift, but the backend content management system was entirely redesigned.

Goodbye Old Site:

![Old site](/blog/2009/10/new-end-point-site-rails-jquery-flot/oldsite.png)

Hello New Site:

![New site](/blog/2009/10/new-end-point-site-rails-jquery-flot/newsite.png)

Our old site was a Rails app with a Postgres database running on Apache and Passenger. It used a custom CMS to manage dynamic content for the bio, articles, and service pages. The old site was essentially JavaScript-less, with the exception of Google Analytics.

Although the new site is still a Rails application, it no longer uses the Postgres database. As developers, we found that it is more efficient to use Git as our "CMS" rather than developing and maintaining a custom CMS to meet our ever-changing needs. We also trimmed down the content significantly, which further justified the design; the entire site and content is now comprised of Rails views and partial views. Also included in the new site is cross browser functioning [jQuery](http://jquery.com/) and [flot](http://code.google.com/p/flot/). Some of the interesting implementation challenges are discussed below.

### jQuery Flot Integration

The first interesting JavaScript component I worked on was using flot to improve interactivity to the site and to decrease the excessive text that End Pointers are known for (for example, this article). Flot is a jQuery data plotting tool that contains functionality for plot zooming, data interactivity, and various configuration display settings (see more [flot examples](http://people.iola.dk/olau/flot/examples/)). I've used flot before in several experiments but had yet to use it on a live site. For the implementation, we chose to plot our consultant locations over a map of the US to present our locations in an interactive and fun to use way. The tedious part of this implementation was actually creating the datapoints to align with cities. Check out the images below for examples.

Flot has built in functionality for on hover events. When a point on the plot is hovered over, correlating employees are highlighted using jQuery and their information is presented to the right of the map.

![End Point team page, hovering on New York](/blog/2009/10/new-end-point-site-rails-jquery-flot/hover1.png)

When a bio picture is hovered over, the correlating location is highlighted using jQuery and flot data point highlighting.

![End Point team page, hovering on Rick’s portrait in New York](/blog/2009/10/new-end-point-site-rails-jquery-flot/hover2.png)

We also implemented a timeline using flot to map End Point's history. Check out the images below.

When a point on the plot is hovered over, the history details are revealed in the section below.

![History plot, hovering on 1963 (Founders Ben and Rick meet each other on a playground)](/blog/2009/10/new-end-point-site-rails-jquery-flot/hover3.png)

The triangle image CSS position is adjusted when a point on the plot is activated.

![History plot, hovered over 2008-2009](/blog/2009/10/new-end-point-site-rails-jquery-flot/hover4.png)

### Dynamic Rails Partial Generation

One component of the old site that was generated dynamically sans-CMS was blog article integration into the site. A cron job ran daily to import new blog article title, link, and content snippets into the Postgres database.  We opted for removing dependency on a database with the new site, so we investigated creative ways to include the dynamic blog content. We developed a rake task that is run via cron job to dynamically generate partial Rails views containing blog content. Below is an example and explanation of how the blog RSS feed is retrieved and a partial is generated:

Open URI and REXML are used to retrieve and parse the XML feed.

```ruby
require 'open-uri'
require 'rexml/document'
...
```

The feed is retrieved and a REXML object created from the feed in the rake task:

```ruby
data = open('https://www.endpointdev.com/blog/feed.xml', 'User-Agent' => 'Ruby-Wget').read
doc = REXML::Document.new(data)
```

The REXML object is iterated through. An array containing the blog links and titles is created.

```ruby
results = []
doc.root.each_element('//item') do |item|
  author = item.elements['author'].text.match(/\(.+/).to_s.gsub(/\.|\(|\)/,'')
  results << '<a href="' + item.elements['link'].text + '">' + item.elements['title'].text + '</a>'
end
```

Finally, a Rails dynamic partial is written containing the contents of the results array:

```ruby
  File.open(#{RAILS_ROOT}/app/views/blog/_index.rhtml", 'w') { |f| f.write(results.inject('') { |s, v| s = s + '<p>' + v  + '</p>'}) }
```

A similar process was applied for bio and tag dynamic partials. The partials are included on pages such as the End Point service pages, End Point bio pages, and End Point home page.

### jQuery Carousel Functionality

Another interesting JavaScript component I worked on for the new site was the carousel functionality for the home page and client page. Carousels are a common "web 2.0" JavaScript component where visible items slide one direction out of view and new items slide into view from the other direction. I initially planned on implementing a simple carousel with a jQuery plugin, such as [jCarousel](http://sorgalla.com/jcarousel/). Other JavaScript frameworks also include carousel functionality such as the [YUI Carousel Control](http://developer.yahoo.com/yui/carousel/) or the [Prototype UI](http://www.prototype-ui.com/). I went along planning to implement the existing jQuery carousel functionality, but then was asked, "Can you make it a circular carousel where the left and right buttons are always clickable?" In many of the existing carousel plugins and widgets, the carousel is not circular, so this request required custom jQuery. After much cross-browser debugging, I implemented the following (shown in images for a better explanation):

Step 1: The page loads with visible bios surrounded by empty divs with preset width. The visibility of the bios is determined by CSS use of the overflow, position, and left attributes.

![](/blog/2009/10/new-end-point-site-rails-jquery-flot/image-6.gif)

Step 2: Upon right carousel button click, new bios populate the right div via jQuery.

![](/blog/2009/10/new-end-point-site-rails-jquery-flot/image-7.gif)

Step 3: To produce the carousel or slider effect, the left div uses jQuery animation functionality and shrinks to a width of 0px.

![](/blog/2009/10/new-end-point-site-rails-jquery-flot/image-8.gif)

Step 4: Upon completion of the animation, the empty left div is removed, and a new empty div is created to the right of the new visible bios.

![](/blog/2009/10/new-end-point-site-rails-jquery-flot/image-9.gif)

Step 5: Finally, the left div's contents are emptied and the carousel is in its default position ready for action!

![](/blog/2009/10/new-end-point-site-rails-jquery-flot/image-10.gif)

Another request for functionality came from [Jon](/team/jon-jensen/). He asked that we create and use "web 2.0" URLs to load specific content on page load for the dynamic content throughout our site, such as www.endpoint.com/clients#citypass, www.endpoint.com/clients#backcountry.

Upon page load, JavaScript is used to detect if a relative link exists:

```ruby
if(document.location.href.match('#.+')) {
    var id = document.location.href.match('#.*').toString().replace('#', '');
}
```

The id retrieved from the code snippet above is used to populate the dynamic page content. Then, JavaScript is used during dynamic page functionality, such as carousel navigation, to update the relative link:

```ruby
document.location.href = document.location.href.split('#')[0] + '#' + anchor;
```

### Twitter Integration

Another change in the new site was importing existing functionality previously written in Python to update [End Point's Twitter](https://twitter.com/endpoint) feed automagically. The rake task uses the [Twitter4R](http://twitter4r.rubyforge.org/) gem to update the Twitter feed and is run via cron job every 30 minutes. See the explanation below:

The public twitter feed is retrieved using Open URI and REXML.

```ruby
    data = open('https://twitter.com/statuses/user_timeline/endpoint.xml', 'User-Agent' => 'Ruby-Wget').read
    doc = REXML::Document.new(data)
```

An array containing all the titles of all tweets is created.

```ruby
    doc.each_element('statuses/status/text') do |item|
      twitter << item.text.gsub(/ http:\/\/j\.mp.*/, '')
    end
```

The blog RSS feed is retrieved and parsed. An array of hashes is created to track the un-tweeted blog articles.

```ruby
    data = open('https://www.endpointdev.com/blog/feed.xml', 'User-Agent' => 'Ruby-Wget').read
    doc = REXML::Document.new(data)
    found_recent = false
    doc.root.each_element('//item') do |item|
      found_recent = true if twitter.include?(item.elements['title'].text)
      blog << { 'title' => item.elements['title'].text, 'link' => item.elements['link'].text } if !found_recent
    end
```

Using the j.mp api, a short url is generated. A Twitter message is created from the short URL.

```ruby
      data = open('http://api.j.mp/shorten?version=2.0.1&longUrl=' + blog.last['link'] + '&login=**&apiKey=*****&format=xml')
      ...
      twitter_msg = blog.last['title'] + ' ' + short_url
```

The twitter4r gem is used to login and update the Twitter status message.

```ruby
      client = Twitter::Client.new(:login => **, :password => *****)
      begin
        status = client.status(:post, twitter_msg)
      rescue
      end
```

### Google Event Tracking

Finally, since we implemented dynamic content throughout the site, we decided to use Google Event Tracking to track user interactivity. We followed the standard Google Analytics event tracking to add events for events such as the slider carousel user involvement, the team page bio and history hover user involvement:

```javascript
//pageTracker._trackEvent(category, action, optional_label, optional_value);
pageTracker._trackEvent('Team Page Interaction', 'Map Hover', bio);
```

We are happy with the new site and we hope that it presents our skillz well!
