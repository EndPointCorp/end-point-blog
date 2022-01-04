---
author: Steph Skardal
title: 'Rails 3.1: Upgrading a Simple App — Part 2'
github_issue_number: 502
tags:
- rails
date: 2011-09-29
---



I recently [wrote about upgrading a simple Rails app](/blog/2011/09/rails-31-upgrading-simple-app-part-1), which involved applying routing, mailer, ActiveRecord, etc. updates to my Rails 2.1.2 application. An equally important part of the upgrade is working with the [asset pipeline](http://guides.rubyonrails.org/asset_pipeline.html), a framework that creates an architecture for managing JavaScript, CSS, and image assets in your Rails 3.1 application.

### File Reorganization

Prior to the upgrade, my assets were organized in the following structure:

```plain
RAILS_ROOT/
  public/
    javascripts/
      jquery.site.js
      jquery.home.js
      jquery.services.js
      jquery.team.js
      jquery.bios.js
      ...
    stylesheets/
      site.css
    images/
      .. a lot of images ..
```

As you can see, the JavaScript files were already split into page specific code that was included where it was needed. But the application had one global stylesheet which included styles for the entire site. In general, the site followed performance best practices of minimizing http requests with this organization.

In Rails 3.1, the generators encourage you to build out individual JavaScript and CSS files for each controller by creating the files upon each controller instantiation. While in development, those files are served individually, but production serves compiled files application.js and application.css by default (Note: you have the option of controlling the compiled file name and you have the option of including more than one compiled file). With this organization structure in mind, I reorganized my JavaScript and stylesheet assets to the following structure:

```plain
RAILS_ROOT/
  app/
    assets/
      javascripts/
        application.js
        bios.js
        clients.js
        contact.js
        home.js
        services.js
        team.js
      stylesheets/
        application.css
        bios.css
        clients.css
        contact.css
        home.css
        services.css
        sitemap.css
        team.css
```

I also moved external JavaScript code to the vendor/assets directory, which can be explicitly included in application.js, to add separation between application specific JavaScript and external libraries. Note that Rails will look in app/assets, vendor/assets, and lib/assets for assets by default, and additional locations may be added by updating the **Rails.application.config.assets.paths** variable.

```plain
RAILS_ROOT/
  vendor/
    assets/
      javascripts/
        excanvas.min.js
        jquery.flot.js
        jquery.lightbox.js
```

To enforce loading order of JavaScript files, application.js contains the following. Note that [jQuery-ujs](https://github.com/rails/jquery-ujs) is not included because the application does not have any AJAX form submissions.

```plain
//= require jquery
//= require excanvas.min
//= require jquery.flot
//= require jquery.lightbox
//= require_tree .
```

I did not decide to reorganize images at this point in time, since many of our blog articles references on-site images and I didn’t want to address blog article updates with this upgrade.

### Learning the Asset Tasks

After I reorganized my assets, I was ready to go (sort of)! I read up on rake tasks for working with assets. **rake assets:clean** removes all compiled assets and **rake assets:precompile** compiles all assets named in config.assets.precompile. I precompiled my assets and *then* was ready to go. I tried running the application both in development and production to verify assets were served separately in development and assets were served compiled in production.

### JavaScript Namespacing

As soon as I got my app up and running, I noticed there were issues with interactive functionality that relied on JavaScript. After I debugged the functionality a bit, I determined that conflicting JavaScript functions in the compiled version of application.js was the cause of the issues, which was not an issue before the upgrade since these files were served on distinct pages. I added basic JavaScript namespacing to sort this out.

Instead of:

```javascript
/* home.js */
var shift_right = function() {
  //...
};
var shift_left = function() {
  //...
};

/* clients.js */
var shift_right = function() {
  //...
};
var shift_left = function() {
  //...
};
```

I tried:

```javascript
/* home.js */
var home = {
  shift_right: function() {
    //...
  },
  shift_left: function() {
    //...
  };
};

/* clients.js */
var clients = {
  shift_right: function() {
    //...
  },
  shift_left: function() {
    //...
  };
};
```

These updates sorted out the JavaScript errors.

### Sass

One of the great things about Rails 3.1 is that it makes using Sass or scss very easy. I’ve written about Sass a couple of times before ([here](/blog/2011/05/sass-at-railsconf-2011) and [here](/blog/2011/05/railsconf-2011-day-one)) and am happy to leverage its functionality. The stylesheets were updated to have a *.scss extension to force scss template rendering. I introduced variables, which allow you to easily represent and update colors used globally:

```scss
$blue: #195065;
a { text-decoration: none; color: $blue; }
.menu { border-top: 1px solid $blue; }
...
```

And I introduced nesting, which is a great tool for minimizing retyping style definitions and therefore reduces the risk of mislabeling styles:

```css
/* Sitemap */
.sitemap { background: #FFF url(/images/manhattan.jpg) right 100px no-repeat; 
  p { margin: 0px 0px 3px 25px; }
  p.indent { margin-left: 35px; }
  a { color: #404040; font-weight: normal; }
}
```

Read more about other great Sass features like Mixins, Selector Inheritance, Functions, and Operations [here](https://sass-lang.com/).

### Conclusion

Closing thoughts:

- I spent equal time on asset pipeline updates and non-asset pipeline updates described in [the previous article](/blog/2011/09/rails-31-upgrading-simple-app-part-1). A coworker commented that he was surprised it took so long to work through the upgrade. The upgrade to Rails 3.1 is not trivial, but there are plenty of great resources out there. I found the [Rails Guides](http://guides.rubyonrails.org/index.html) to be particularly helpful.
- I did not leverage [CoffeeScript](https://coffeescript.org/), which is a meta language that compiles into JavaScript much like how scss compiles into css. I don’t have experience working with CoffeeScript and I didn’t feel like this was the project to start learning it.
- I did not reorganize any image assets. However, I’ve done this in another Rails 3.1 application and have found it to be relatively painless.


