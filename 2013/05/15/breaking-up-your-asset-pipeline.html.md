---
author: Mike Farmer
gh_issue_number: 801
tags: javascript, rails
title: Breaking Up Your Asset Pipeline
---



The [Rails Asset Pipeline](http://guides.rubyonrails.org/asset_pipeline.html) to me is kind of like [Bundler](http://gembundler.com/). At first I was very nervous about it and thought that it would be very troublesome. But after a while of using it, I realized the wisdom behind it and my life got a lot easier. The asset pipeline is fabulous for putting all your assets into a single file, compressing them, and serving them in your site without cluttering everything up. Remember these days?

```html
<%= javascript_include_tag 'jquery.validate.min.js','jquery.watermark.min.js','jquery.address-1.4.min','jquery.ba-resize.min','postmessage','jquery.cookie','jquery.tmpl.min','underscore','rails','knockout-1.3.0beta','knockout.mapping-latest' %>
```

A basic component of the Asset Pipeline is the manifest file. A manifest looks something like this

```javascript
// Rails asset pipeline manifest file
// app/assets/javascript/application.js

//= require jquery
//= require jquery_ujs
//= require_tree .
```

For a quick rundown on how the Asset Pipeline works, I highly recommend taking a few minutes to watch [Railscast episode 279](http://railscasts.com/episodes/279-understanding-the-asset-pipeline). But there are a few things that I'd like to point out here.

First, notice that the name of the file is application.js. This means that all the javascript specified in the manifest file will be compiled together into a single file named application.js. In production, if specified, it will also be compressed and uglified. So rather than specifying a really long and ugly javascript_include_tag, you just need one:

```
<%= javascript_include_tag "application.js" %>
```

Second, this means that if you only have one manifest file in your application, then all of your javascript will be loaded on every page, assuming that your javascript_include_tag is loading in the head of your layout. For small applications with very little javascript, this is fine, but for large projects where there are large client-side applications, this could be a problem for performance. For example, do you really need to load all of [ember.js](http://emberjs.com/) or [backbone.js](http://backbonejs.org/) or [knockout.js](http://knockoutjs.com/) in the admin portion of your app when it isn't used at all? Granted, these libraries are pretty small, but the applications that you build that go along with them don't need to be loaded on every page.

So I thought there should be a way to break up the manifest file so that only javascript we need is loaded. The need for this came when I was upgrading the main functionality of a website to use the Backbone.js framework. The app was large and complex and the "single-page-application" was only a part of it. I didn't want my application to load on the portion of the site where it wasn't need. I looked high and low on the web for a solution to this but only found obscure references so I thought I would take some time to put the solution out there cleanly hoping to save some of you from trying to figure it out on your own.

The solution lies in the first point raised earlier about the asset pipeline. The fact is, **you can create a manifest file anywhere in your assets directory and use the same directives to load the javascript**. For example, in the app/assets/javascripts/ directory the application.js file is used by default. But it can be named anything and placed anywhere. For my problem, I only wanted my javascript application loaded when I explicitly called it. My directory structure looked like this:

```nohighlight
|~app/
| |~assets/
| | |+fonts/
| | |+images/
| | |~javascripts/
| | | |+admin/
| | | |+lib/
| | | |+my_single_page_app/
| | | |-application.js
```

My application.js file looks just like the one above but I removed the require_tree directive. This is important because now I don't want all of my javascript to load from the application.js. I just want some of the big stuff that I use all over like jQuery. (Ok, I also added the [underscore](http://underscorejs.org/) library in there too because it's just so darn useful!) This file is loaded in the head of my layout just as I described above.

Then, I created another manifest file named load_my_app.js in the root of my_single_page_app/. It looks like this:

```javascript
//= require modernizr
//= require backbone-min
//= require Backbone.ModelBinder
//= require my_single_page_app/my_app
//= require_tree ./my_single_page_app/templates
//= require_tree ./my_single_page_app/models
//= require_tree ./my_single_page_app/collections
//= require_tree ./my_single_page_app/views
//= require_tree ./my_single_page_app/utils
```

Then in my view that displays the single page app, I have these lines:

```html
<% content_for :head do %>
  <%= javascript_include_tag "my_single_page_app/load_my_app.js" %>
<% end %>
```

Now my single page application is loaded into the page as my_single_page_app/load_my_app.js by the Asset Pipeline and it's only loaded when needed. And a big bonus is that I don't need to worry about any of the code that I wrote or libraries I want to use interfering with the rest of the site. 


