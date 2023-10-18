---
author: Steph Skardal
title: CSS Fixed, Static Position Toggle
github_issue_number: 495
tags:
- css
- javascript
- jquery
date: 2011-09-09
---

In a recent [Rails](/expertise/ruby-on-rails/) project, I had to implement a simple but nifty CSS trick. A request came in to give a DOM element fixed positioning, meaning as the user navigates throughout the page, the DOM element stays in one place while the rest of the page updates. This is pretty common behavior for menu bars that show up along one of the borders of a window while a user navigates throughout the site. However, this situation was a bit trickier because the menu bar that needed fixed positioning was already a few hundred pixels down the page below header and navigation content:

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5650381299067538866" src="/blog/2011/09/css-fixed-static-position-toggle/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 745px;"/>

I came up with a nifty way of using jQuery to toggle the menu bar CSS between fixed and static positioning. The code uses jQuery’s scroll event handler to adjust the CSS position setting of the menu bar as users scroll through the page. If the window scroll position is below it’s original top offset, the menu has fixed positioning at the top of the window. If the window scroll position is above it’s original top offset, the menu has static positioning. Here’s what the code looks like:

```javascript
var head_offset = jQuery('#fixed_header').offset();
jQuery(window).scroll(function() {
    if(jQuery(window).scrollTop() < head_offset.top) {
        jQuery('#fixed_header').css({ position: "static"});
    } else {
        jQuery('#fixed_header').css({ position: "fixed", top: "0px" });
    }
});
```

And perhaps the most effective demonstration of this behavior comes in the form of a video, created with [Screencast-O-Matic](https://www.screencast-o-matic.com/). I also tried capturing with [Jing](http://www.techsmith.com/jing/), which is another handy tool for quick Screenshots and Screencasts. Note that the header content has CSS adjustments for demo purposes only:

<iframe allowfullscreen="" frameborder="0" height="447" src="https://player.vimeo.com/video/28823480?title=0&byline=0&portrait=0" webkitallowfullscreen="" width="745"></iframe>
