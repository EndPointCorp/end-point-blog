---
author: Steph Skardal
gh_issue_number: 408
tags: tips, tools
title: Web Friendly Tools
---

Over the past few weeks, I found a few nice tools that I wanted to share:

### Spritebox

The first tool I found came across and wanted to share is [Spritebox](http://www.spritebox.net/). Spritebox is a WYSIWIG tool to create CSS sprite rules from an image on the web or an uploaded image. Once a sprite image is loaded, regions can be selected, assigned classes or ids, display settings, and background repeat settings. The preview region shows you which part of the sprited image will display in your DOM element. After all sprite regions are defined, CSS is automagically generated, ready for copy and paste into a stylesheet. This is a user-friendly visual tool that's likely to replace my tool of choice (Firebug) for generating CSS sprite rules.

<table width="100%">
<tbody><tr>
<td valign="top">
<a href="/blog/2011/02/07/web-friendly-tools/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5571075103783708706" src="/blog/2011/02/07/web-friendly-tools/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 324px;"/></a>
I select the twitter region and assign several CSS properties.
</td>
<td valign="top">
<a href="/blog/2011/02/07/web-friendly-tools/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5571075104896395570" src="/blog/2011/02/07/web-friendly-tools/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 330px;"/></a>
I select the header background region and assign several CSS properties.
</td>
</tr>
</tbody></table>

### Typekit

Another tool / service I've come across on the design side of web development is [Typekit](http://typekit.com/). Typekit is a font hosting service that allows you to retrieve web fonts and render text with those fonts instead of using Flash or images. I recently noticed severe lag time on font rendering for one of our Spree clients. I was curious about font hosting services, specifically regarding the accessibility, usage, and payment options. Typekit offers four different plans. The lowest plan is free, allows 2 fonts to be used on one site, and the font selection is limited. The highest price-point plan gives you full font library access and can use an unlimited number of fonts on an unlimited number of sites in addition to a few other features.

<a href="/blog/2011/02/07/web-friendly-tools/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5571075122847433106" src="/blog/2011/02/07/web-friendly-tools/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 310px;"/></a>

A "kit" I created for use on a personal site.

I signed up for a free Typekit account and created a "kit" with 2 fonts to be used on my personal site. After publishing my kit, I implement the kit by including some Javascript (shown below), and adding my typekit classes (tk-fertigo-script and tk-ff-enzo-web) to the regions where the kit fonts should apply.

```nohighlight
<script type="text/javascript" src="http://use.typekit.com/kitid.js"></script>
<script type="text/javascript">try{Typekit.load();}catch(e){}</script>
```

I was impressed by typekit's font rendering speed. There are several other font hosting services out there that offer similar paid plans. Regardless of which service is chosen, a hosted font service is an affordable way to use "pretty" fonts, have fast rendering speeds, and have a site with SEO-friendly text.

<a href="/blog/2011/02/07/web-friendly-tools/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5571075112301676898" src="/blog/2011/02/07/web-friendly-tools/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 163px;"/></a>

An example of Typekit in action.

### Awesome Screenshot

The final tool I've been using **tons** is [Awesome Screenshot](http://awesomescreenshot.com/), a Chrome plugin (also available on Safari). It allows you to grab a screenshot, a screenshot region, or the entire page and annotate it with rectangles, circles, arrows, lines and text. You can download the image or upload to provide a shareable link. All the screenshots in this article were created with Awesome Screenshot. This free tool has replaced my screenshot and editing [via Gimp] work flow. I recommend trying this one out!

<a href="/blog/2011/02/07/web-friendly-tools/image-4-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5571075129152738770" src="/blog/2011/02/07/web-friendly-tools/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 361px;"/></a>

Awesome Screenshot in action.
