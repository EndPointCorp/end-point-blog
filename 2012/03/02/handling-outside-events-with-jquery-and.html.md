---
author: Greg Davidson
gh_issue_number: 564
tags: javascript, jquery
title: Handling outside events with jQuery and Backbone.js
---



I recently worked on a user interface involving a persistent shopping cart on an ecommerce site. The client asked to have the persistent cart close whenever a user clicked outside or “off” of the cart while it was visible. The cart was built with [Backbone.js](http://backbonejs.org/), and [jQuery](https://jquery.com/) so the solution would need to play nicely with those tools.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/03/02/handling-outside-events-with-jquery-and/image-0.png" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2012/03/02/handling-outside-events-with-jquery-and/image-0.png"/></a></div>

The first order of business was to develop a way to identify the “outside” click events. I discussed the scenario with a colleague and YUI specialist and he suggested the YUI [Outside Events](http://yuilibrary.com/gallery/show/outside-events) module. Since the cart was built with jQuery and I enjoyed using that library, I looked for a comparable jQuery plugin and found [Ben Alman’s](http://benalman.com/) [Outside Events plugin](http://benalman.com/projects/jquery-outside-events-plugin/). Both projects seemed suitable and a review of their source code revealed a similar approach. They listened to events on the document or the <html> element and examined the event.target property of the element that was clicked. Checking to see if the element was a descendant of the containing node revealed whether the click was “inside” or “outside”.

With this in mind, I configured the plugin to listen to clicks outside of the persistent cart like so:

```javascript
  $(function(){
    $('#modal-cart').bind('clickoutside', function(event) {
    });
  });
```

The plugin worked just like it said on the tin, however further testing revealed a challenge. The site included ads and several of them were \<iframe\> elements. Clicks on these ads were not captured by the clickoutside event listener. This was a problem because the outside event listening code could be ignored depending on where the user clicked on the page.

To mitigate this issue, a second approach was taken. A “mask” element was added below the persistent cart. CSS was used to position the mask below the persistent cart using the z-index property. The mask was invisible to the user because the background was transparent. Instead of listening to clicks outside of the persistent cart, clicks on the mask element could be captured. Thanks to the magic of CSS, the mask covered the entire page (including those pesky \<iframes\>).

Now that I was able to handle the “outside” clicks properly, the event handling code needed to be configured inside the Backbone.js cart view. Backbone uses jQuery to handle events behind the scenes but the syntax is a little bit different.

Where with jQuery you might set up an event handler like this:

```javascript
  $('#mask').click(maskClickHandler);
```

This would be the Backbone.js equivalent:

```javascript
  "click #mask": "maskClickHandler"
```

Here is how it all shaped up inside the Backbone view. First, the event handler on the mask element was configured inside the events object of the view:

```javascript
window.cartView = Backbone.View.extend({
  template: '#cart-template',

  initialize: function() {
    _.bindAll(this, 'render');
    this.initializeTemplate();
  },

  initializeTemplate: function() {
    this.template = _.template($(this.template).html());
  },  

  // set up event listener on the mask element
  events: function() {
    "click #modal-cart-mask": "closeCart"
  },
```

The openCart function was augmented to show the mask element each time the persistent cart was shown:

```javascript
  openCart: function () {
    // show the mask element when the cart is opened
    $(this.el).find('#modal-cart-mask').show();
    this.render();
    $(this.el).removeClass("closed");
    this.isClosed = false;
  },  
```

Lastly, the closeCart function was modified to hide the mask element each time the persistent cart was closed:

```javascript
  closeCart: function () {
    $(this.el).addClass("closed");
    this.isClosed = true;
    // hide the mask element when the cart is closed
    $(this.el).find('#modal-cart-mask').hide();
  },  

  render: function() {
    $(this.el).html(this.template(this.model.toJSON()));
    return this;
  }
});
```

With this in place, the outside events were properly captured and handled by the same Backbone view that managed the persistent cart. How’s that for playing nice?


