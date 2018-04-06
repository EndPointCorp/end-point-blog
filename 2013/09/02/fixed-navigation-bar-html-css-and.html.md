---
author: Steph Skardal
gh_issue_number: 850
tags: css, html, javascript, jquery
title: 'Fixed Navigation Bar: HTML, CSS, and JavaScript Breakdown'
---

Something that I’ve seen frequently these days on content rich sites are fixed navigation bars, or small abbreviated header in the form of a horizontal bar at the top of the screen that shows after a user has scrolled below the header. Here’s an example:

<img border="0" src="/blog/2013/09/02/fixed-navigation-bar-html-css-and/image-0.png" width="740px;"/>A live example of an abbreviated fixed navigation bar at the top of the articles at [ABCNews.com](http://abcnews.go.com/).
The background has a grey opaque layer for demonstration purposes only.

I recently implemented this functionality for [H2O](http://cyber.law.harvard.edu/research/h2o), and I’ll go through the tools needed to do this.

### HTML Markup

First thing’s first, you need the HTML markup for this. The only tricky thing here is that the horizontal bar must be outside of any wrapping dividers on the page that are confining the content to a set width. For example, if your content is limited to 900 pixels in width, the horizontal bar markup must be outside that constraint. Here’s what the HTML might look like:

```html
<div id="fixed_bar">
  <div class="wrapper">
    Links & content here.
  </div>
</div>
```

Note that in the above HTML, the “wrapper” div may be constraining the content width to match the remaining content, such as in the example above. This HTML may go at the beginning or end of the page HTML. I prefer to see it at the top of the page HTML. Another note is that other HTML elements may be used in place of the div, but I chose the div above because it defaults to a block element (an element where the CSS display default value is block).Finally, one more note here is that HTML5 elements can be used in place of the div as well (section or nav might make sense) if the site is HTML5 compliant.

### CSS Settings

The secret to this interactive feature lies in the CSS settings. Here’s what the CSS for my example code above might look like:

```css
body {
  margin: 0px;
  padding: 0px;
}
#fixed_bar {
  width: 100%;
  position: fixed;
  z-index: 100; //exceed z-index of other elements on the page
  display: none;
  background: transparent url(/images/fixed_bar.png) bottom repeat-x;
  top: 0px;
}
.wrapper {
  width: 900px;
  margin: 0px auto;
}
```

Here are the important bits of the CSS above:

- The fixed positioning setting is what keeps the bar in one place as the user scrolls up and down (line 7).
- The body must have margin and padding settings at 0px to ensure that the fixed bar is flush against the top of the screen (line 2 & 3).
- The fixed bar spans the width of the browser, but in this case, the .wrapper element is constrained to 900 pixels wide (line 14).
- The default state of the #fixed_bar element is none, which is hidden upon page load (line 9).
- The background of the #fixed_bar can be a small image with a gradient to transparency, such as in the example above (line 10).

### Scroll Event Listener

Finally, after the HTML and CSS markup is good to go, here’s what the interactive JavaScript (via jQuery) might look like:

```javascript
var offset = 100; // some offset value for which when the header becomes hidden
jQuery(window).scroll(function() { //also an option: jQuery .on('scroll') method
  if(jQuery('#fixed_bar').is(':visible') && jQuery(window).scrollTop() < offset) {
    jQuery('#fixed_bar').fadeOut(200);
  } else if(!jQuery('#fixed_bar').is(':visible') && jQuery(window).scrollTop() > offset) {
    jQuery('#fixed_bar').fadeIn(200);
  }
});
```

The jQuery above checks for two scenarios:

- a) If the #fixed_bar div is visible and the scroll position is less than the offset, fade the #fixed_bar div to a hidden state.
- b) If the #fixed_bar div is not visible and the scroll position is greater than the offset, fade the #fixed_bar div to a visible state.

These two use cases will toggle the visibility of the fixed bar to a hidden and visible state. With these combined elements of HTML, CSS, and jQuery & JavaScript, a nice user interactivity feature adds to the usability of the site by providing valuable links and content as the user scrolls down the page.
