---
author: Marina Lohova
title: 'How To: Big Beautiful Background Video'
github_issue_number: 1147
tags:
- html
- javascript
- video
date: 2015-08-04
---

One pretty common request for every web developer is to “please, make our Stone age website look sleek and modern”. Well, no more head scratching about the meaning of “sleek” or “modern” (or “the Stone age” for some?). In times of the crisp and stunning visuals there’s no better way to make an impression than to use a big beautiful background video on the home page.

Paired with some impressive infinite scroll which I already [covered here](/blog/2013/11/pagination-days-are-over-infinite) and a nice full-screen image gallery (which I will cover later), it will definitely help to bring your website up to date.

Lucky for us, there is a very popular library called [BigVideo.js](http://dfcb.github.io/BigVideo.js/) which is based on another well known library [videojs](http://www.videojs.com/), which is a wrapper around HTML5 \<video\> tag.

### Converting the video.

To ensure the cross browser support, it’s best to supply the desired video in several formats. The most common formats to use are [mp4](https://en.wikipedia.org/wiki/H.264/MPEG-4_AVC), [ogg](https://en.wikipedia.org/wiki/Ogg) and [webm](https://en.wikipedia.org/wiki/WebM). Here is [the browser support chart](https://en.wikipedia.org/wiki/HTML5_video#Browser_support) to give you a better idea of why it’s so important to use more than one format on your page.

There are a lot of ways to convert the file, but since I’m not particularly good with compression settings or codecs, I’m using the following easy workflow:

- Upload the video to Vimeo or YouTube.

There is even a handy “Share” setting straight from Final Cut for us, Apple users.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/08/how-to-big-beautiful-background-video/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="284" src="/blog/2015/08/how-to-big-beautiful-background-video/image-0.png" width="500"/></a></div>

- Go to Vimeo/YouTube and download it from there. 

This way I’m leveraging these web services’ optimized and perfected compressing algorithms for web and also getting the smallest file size possible without too much quality loss. The target file should ideally be less than 3MB, otherwise it will slow down your browser, especially Firefox with Firebug installed.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/08/how-to-big-beautiful-background-video/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="332" src="/blog/2015/08/how-to-big-beautiful-background-video/image-1.png" width="500"/></a></div>

- The last step is to generate webm and ogg with [Firefogg](http://firefogg.org/make/index.html)

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/08/how-to-big-beautiful-background-video/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="300" src="/blog/2015/08/how-to-big-beautiful-background-video/image-2.png" width="500"/> </a></div>

You may find another process that works best for you, but this is what works for me.

### Using BigVideo.js to display video

We will need to include the libraries:

```javascript
<script src="//vjs.zencdn.net/4.3/video.js"></script>
<script src="http://imagesloaded.desandro.com/imagesloaded.pkgd.min.js"></script>
<script src="http://dfcb.github.io/BigVideo.js/bower_components/BigVideo/lib/bigvideo.js"></script>
```

And the following javascript:

```javascript
var BV = new $.BigVideo({
  controls: false,
  forceAutoplay: true, 
  container: $('#video')
});
BV.init();
BV.show([
  { type: "video/webm", src: "http://vjs.zencdn.net/v/oceans.webm" },
  { type: "video/mp4", src: "http://vjs.zencdn.net/v/oceans.mp4" }
], {ambient: true});
```

Please, note the “ambient:true” setting. This setting does the trick of playing the video in the background.

### Mobile and Tablet Support

The sad truth is that the video backgrounds are not supported on touch devices, because HTML5 does not allow autoplay there. Instead there will be a “play” button underneath your content and the user will need to click on it to activate the ambient video. Not so ambient anymore, right? The best option for now is to use a full screen image instead of the video as described [here](http://dfcb.github.io/BigVideo.js/example-ambient-touch.html).

Hope you enjoyed the blog post. Let me know your thoughts!
