---
author: Marina Lohova
gh_issue_number: 1037
tags: javascript, jquery
title: Using jQuery Migrate plugin
---



We all know these tricky situations, like introducing a new feature on top of old code, when it seems we’re about to step into a tedious swamp of workarounds and dirty hacks. Fortunately, [jQuery Migrate plugin](http://jquery.com/upgrade-guide/1.9/#jquery-migrate-plugin) is here to make these situations easier, at least in JavaScript. So for any of you who wondered about a real-life example of using jQuery Migrate plugin I have one!

My task was to add an editable combomonster, oh sorry, combobox (even though editable comboboxes remind me of UX Frankenstein's Monster, they are still requested a lot) to a rather old website built on jQuery v1.4.2.

I downloaded the most recent jQuery UI (at that time it was v1.10.4) and a very neat [editable combobox component](https://github.com/jquery/jquery-ui/blob/master/demos/autocomplete/combobox.html) to go with it. It was expected that it wouldn’t work out of box with the rather outdated jQuery we had. It didn't work and the page produced the following JavaScript error:

```javascript
TypeError: t.cssHooks is undefined
```
```javascript
...t(" ");f(i,function(e,i){t.cssHooks[i]={set:function(e,n){var a,o,r="";if("trans...
```

No problem, I grab the newer compatible jQuery v1.10.2 from the website and yield it into head in that particular page.

```ruby
<% content_for :head do %>
  javascript_include_tag "jquery-1.10.2.min.js"
  javascript_include_tag "jquery-ui-1.10.4.min.js"
  javascript_include_tag "jquery.editableselect.js"
<% end %>
```
There’s good news and bad news. Good - the old error is gone. Bad - there's a new one:

```html
TypeError: jQuery.browser is undefined
```
```javascript
if (jQuery.browser.safari && document.readyState != "complete”)
function stretchbar(){
  /* the if block is for safari 4, it was disrupting the display on refresh. */
  if (jQuery.browser.safari && document.readyState != "complete")
    {
     setTimeout( arguments.callee, 100 );
     return;
   }
```
We have a lot of old components on that page and they fail to work with the new jQuery. Why? All versions of jQuery after v.1.9 are stripped of certain components that are not 'core' ones. jQuery offers a migration technique to restore deprecated and removed functionality using [jQuery Migrate plugin](http://jquery.com/upgrade-guide/1.9/#jquery-migrate-plugin) so the older code could work. The plugin can be included with versions of jQuery as old as 1.6.4. However, the plugin is only required for version 1.9.0 or higher.

The section ["Changes of Note in jQuery 1.9"](http://jquery.com/upgrade-guide/1.9/#jquery-browser-removed) explains the particular error I got. Finally, I downloaded [jQuery Migrate plugin](https://github.com/jquery/jquery-migrate/) v1.2.1 (the most recent at the time) and put it after the script for jQuery:

```ruby
<% content_for :head do %>
  javascript_include_tag "jquery-1.10.2.min.js"
  javascript_include_tag "jquery-ui-1.10.4.min.js"
  javascript_include_tag "jquery.editableselect.js"
  javascript_include_tag "jquery-migrate-1.2.1.min.js"
<% end %>
```

Voila! The website gets an instant design boost with this brand new, sleek grey editable combobox:

<a href="/blog/2014/09/26/using-jquery-migrate-plugin/image-0-big.png" imageanchor="1"><img border="0" src="/blog/2014/09/26/using-jquery-migrate-plugin/image-0.png"/></a>


