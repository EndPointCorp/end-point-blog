---
author: Steph Skardal
gh_issue_number: 691
tags: jquery, rails, tips
title: 'Three Things: Times Two'
---



It’s been a while since I’ve written up a “Three Things” article where I share a few featured web development tidbits picked up recently. So I made this a double episode!

### 1. event.stopPropagation() and event.stopImmediatePropagation()

I recently came across these two methods in jQuery, described [here](http://api.jquery.com/event.stopPropagation/) and [here](http://api.jquery.com/event.stopImmediatePropagation/). Both of these methods [prevent the event from bubbling up the DOM tree, preventing any parent handlers from being notified of the event]. In my web application, my $('html') element had a listener on it, but I added specific listeners to children elements that when clicked on calls event.stopPropagation to cancel the event on the $('html') element. See the code below for a simplified example:

```javascript
jQuery(function() {
    jQuery('html').click(function() {
        jQuery.hideSomething();
    });
    jQuery('.popup').click(function(event) {
        event.stopPropagation();
    });
})
```

### 2. alias_attribute

The alias method in Rails is one that I use frequently. But I recently came across the [alias_attribute](http://apidock.com/rails/Module/alias_attribute) method as well. This might make the most sense to use when using shared views for multiple models with varying attributes.

### 3. Excel behavior in jQuery

Recently, there was a bit of discussion about jQuery tools that emulate spreadsheet behavior. A couple of the tools that came up were [Handsontable](http://warpech.github.com/jquery-handsontable/index.html) and [DataTables](http://datatables.net/). They are worth checking out if you are looking to add Excel-like behavior to your web application!

### 4. Rack::SslEnforcer

I recently had a need on a Rails application to force some pages as secure, but have other pages be forced as non-secure. Instead of the common practice of adding controller before filters to force a redirect, this was included via the Gemfile, bundle install, and then configured in config/application.rb. Here’s an example configuration setup that I’m using:

```ruby
config.middleware.use Rack::SslEnforcer,
        :only => [/\/checkout\/$/, /\/users$/, ‘/admin’],
        :strict => true
```

The one interesting caveat I found in working with this is that you absolutely must have all CSS and JavaScript assets precompiled in order for them to be served via SSL. The JS and CSS assets would not be forced to SSL, so they must exist in the Rails public directory via the precompiling, or this gem will redirect https requests on a secure page to http, resulting in the browser reporting that some non-secure elements are being served from a secure page.

### 5. Setting a viewport

I was recently troubleshooting a CSS issue for a client who was examining their website on an iPad. The iPad was setting the width of the viewport to a value that resulted in mis-alignment of floating elements. After a bit of research, I found that setting the viewport to the desired static width of my page fixed this issue. [Here](http://dev.opera.com/articles/view/an-introduction-to-meta-viewport-and-viewport/) is a nice overview of the viewport attribute.

### 6. Line Specific Substitution in vi

Several of my coworkers are vi experts. When I’m in a shared screen with them, I pick up small tips for improving efficiency. One that I picked up on a few months ago and practiced enough to remember was line-specific substitution, e.g. 4,10s/moo/meow/g will substitute all occurrences of “moo” to “meow” in lines 4 through 10. I use this technique frequently.


