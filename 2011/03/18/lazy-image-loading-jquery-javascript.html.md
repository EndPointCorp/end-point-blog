---
author: Steph Skardal
gh_issue_number: 430
tags: javascript, jquery
title: Lazy Image Loading in JavaScript with jQuery
---



This week I had a *duh* moment while working on a little jQuery-driven interface for a side [hobby](http://stephskardal.com/).

I've occasionally used or attempted to do image preloading in JavaScript, jQuery, and YUI. Preloading images happens after a page is loaded: follow-up image requests are made for images that may be needed, such as hover images, larger sizes of thumbnail images on the page, or images below the fold that do not need to load at page request time. Adobe Fireworks spits out this code for preloading images, which is a bit **gross** because the JavaScript is typically inline and it doesn't take advantage of common JavaScript libraries. But this is probably acceptable for standalone HTML files that get moved between various locations during design iterations.

```nohighlight
&lt;body onload="MM_preloadImages('/images/some_image.png','/images/some_other_image.png')"&gt;
```

I found many examples of preloading images with jQuery that look something like this:

```javascript
jQuery.preloadImages = function()
{
  for(var i = 0; i&lt;arguments.length; i++)
  {
    jQuery("&lt;img&gt;").attr("src", arguments[i]);
  }
}
```

I implemented this method, but in my code the preloading was happening asynchronously and I needed to find something that would execute some other behavior after the image was loaded. Before I found the solution I wanted, I tried using jQuery's [get](http://api.jquery.com/jQuery.get/) method and tested jQuery's [ready](http://api.jquery.com/ready/) method, but neither was suitable for the desired behavior. I came across jQuery's [load](http://api.jquery.com/load-event/) event, which binds an event handler to the "load" JavaScript event and can be used on images. So, I came up with the following bit of code to lazily load images:

```javascript
 var img = $('&lt;img&gt;')
  .attr('src', some_image_source);
 $(element).append(img);
 if($(img).height() &gt; 0) {
  // do something awesome
 } else {
  var loader = $('&lt;img&gt;')
   .attr('src', 'images/ajax_loader.gif')
   .addClass('loader');
  $(element).append(loader); 
  $(img).load(function() {
   // do something awesome (the same awesome thing as above)
   loader.remove();
  });
 }
```

So my bit of code creates a new image element. If the image's height is greater than 0 because it's already been requested, it does some awesome method. If its height is 0, it displays an ajax loader image, then does the same awesome method and removes the ajax loader image. See the screenshot below to get an idea of how this is used.

<a href="/blog/2011/03/18/lazy-image-loading-jquery-javascript/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5585481609153615714" src="/blog/2011/03/18/lazy-image-loading-jquery-javascript/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 283px;"/></a>

The image on the left has been loaded and resized to fit its frame. The image to be displayed on the right is loading.

Interestingly enough, the code above works in IE 8, Chrome, and Firefox, but it appears that IE handles image loading a bit differently than the other two browsers — I haven't investigated this further. This lazy-image loading reduces unnecessary requests made to pre-load images that may or may not be accessed by users and the added touch of an ajax loader image communicates to the user that the image is loading. I haven't added a response for image load failure, which might be important, but for now the code makes the assumption that the images exist.

I found a few jQuery plugins for lazy image loading, but I think they might overkill in this situation. One of the jQuery plugins I found is based on YUI's [ImageLoader](http://developer.yahoo.com/yui/3/imageloader/), a utility that similarly delays loading of images.


