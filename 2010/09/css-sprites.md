---
author: Steph Skardal
title: CSS Sprites and a “Live” Demo
github_issue_number: 346
tags:
- ecommerce
- optimization
date: 2010-09-06
---

I’ve recently recommended CSS sprites to several clients, but the majority don’t understand what CSS sprites are or what their impact is. In this article I’ll present some examples of using CSS sprites and their impact.

First, an intro: CSS sprites is a technique that uses a combination of CSS rules and a single background image that is an aggregate of many smaller images to display the image elements on a webpage. The CSS rules set the boundaries and offset that define the part of the image to show. I like to refer to the technique as analogous to the “Ouija board”; the CSS acts as the little [rectangular] magnifying glass to show only a portion of the image.

It’s important to choose which images should be in a sprite based on how much each image is repeated throughout a site’s design and how often it might be replaced. For example, design border images and icons will likely be included in a sprite since they may be repeated throughout a site’s appearance, but a photo on the homepage that’s replaced daily is not a good candidate to be included in a sprite. I also typically exclude a site’s logo from a sprite since it may be used by externally linking sites. End Point uses CSS sprites, but only for a few elements:

<a href="/blog/2010/09/css-sprites/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5513845585604331394" src="/blog/2010/09/css-sprites/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 108px; height: 212px;"/></a>

End Point’s CSS sprite image only contains borders and Twitter and LinkedIn images.

### “Live” Demo

I wanted to implement CSS sprites to demonstrate their performance impact. I chose to examine the homepages of my favorite ski resorts in Utah, [Snowbird](https://www.snowbird.com/) and [Alta](https://www.alta.com/). First, I used [WebPagetest.org](https://www.webpagetest.org/) to get a benchmark for each homepage:

<table cellpadding="5" cellspacing="0" width="100%">
<tbody><tr>
<td align="center" style="background-color:#CCEEFF;">
<a href="/blog/2010/09/css-sprites/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5513844443463352978" src="/blog/2010/09/css-sprites/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 124px;"/></a>
Without sprites, Alta’s homepage loaded in 3.440 seconds with a repeat request load time of 1.643 seconds. 22 requests are made on the homepage.
</td>
<td align="center" style="background-color:#FFEECC;">
<a href="/blog/2010/09/css-sprites/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5513844445344078146" src="/blog/2010/09/css-sprites/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 160px; height: 200px;"/></a>
Without sprites, Snowbird’s homepage loaded in 7.070 seconds with a repeat request load time of 3.146 seconds. 57 requests are made on the homepage.
</td>
</tr>
</tbody></table>

After I benchmarked the two pages, I downloaded each homepage and its files and examined the images to build a CSS sprite image. I created the sprite images shown below. I chose to exclude the logo from each sprite, in addition to other time-sensitive images. Each sprited image contains navigation elements, icons, and a few homepage specific images.

<table cellpadding="5" cellspacing="0" width="100%">
<tbody><tr>
<td align="center" style="background-color:#CCEEFF;">
<a href="/blog/2010/09/css-sprites/image-3-big.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5513842518135734066" src="/blog/2010/09/css-sprites/image-3.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 112px;"/></a><br/>
My resulting sprited image for Alta.
</td>
<td align="center" style="background-color:#FFEECC;">
<a href="/blog/2010/09/css-sprites/image-4-big.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5513842528749004610" src="/blog/2010/09/css-sprites/image-4.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 218px; height: 94px;"/></a><br/>
My resulting sprited image for Snowbird.
</td>
</tr>
</tbody></table>

I updated the HTML to remove individual image requests. Below are some examples:

Before:

```plain
<a href="https://www.alta.com/contact">
<img src="./alta_files/banner_contact.gif" name="ContactUs" width="100" height="20" border="0">
</a>
```

After:

```plain
<a href="/" class="sprite" id="banner_contact">
</a>
```


Before:

```plain
<a href="https://web.archive.org/web/20101128010936/http://shop.alta.com/CS/Browse.aspx?Catalog=AltaRetail&Category=Retail+Items" target="_self">
<img src="./alta_files/altaskishoplogo.jpg" alt="March Madness Logo" width="180" height="123" border="0">
</a>
```

After:

```plain
<a href="https://web.archive.org/web/20101128010936/http://shop.alta.com/CS/Browse.aspx?Catalog=AltaRetail&Category=Retail+Items" target="_self" id="skishoplogo" class="sprite">
</a>
```

Before:

```plain
<div class="icon">
<img src="./snowbird_files/icon_less_rain.gif" border="0" alt="Sunny" title="Sunny">
</div>
```

After:

```plain
<div class="icon sprite less_rain">
</div>
```

Before:

```plain
<div>
<input type="image" src="./snowbird_files/btn_check_rates.gif" border="0" alt="Check Rates">
</div>
```

After:

```plain
<div class="sprite" id="check_rates">
</div>
```

There are a few CSS tips to be aware of during CSS sprite implementation, such as:

- Padding on sprited elements will affect the sprite position.
- Links must have the “display:block” rule (combined with floating rules) to enforce a height and width.
- Parts of the sprite that are repeating may not have any other elements along the repeating axis. For example, in End Point’s sprite, the top and bottom repeating border are in the sprite. No other images may be included in the sprite to the left or right of the borders.

The CSS for the new sprites is shown below. For all sprited elements, a height and width is set in addition to a background position. The height, width, and background position are the rules that define the region of the sprited image to show.

Alta CSS sprite rules

```css
.sprite { background-image: url(sprites.gif); display: block; float: left; }
a#banner_logo { width: 100px; height: 100px; }
div#banner_top { width: 600px; height: 100px; background-position: -100px 0px; }
a#banner_home { width: 100px; height: 20px; background-position: -700px 0px; }
a#banner_contact { width: 100px; height: 20px; background-position: -700px -20px; }
a#banner_sitemap { width: 100px; height: 20px; background-position: -700px -40px; }
a#banner_press { width: 100px; height: 20px; background-position: -700px -60px; }
a#banner_weather { width: 100px; height: 20px; background-position: -700px -80px; }
a#skishoplogo { width: 180px; height: 123px; background-position: -298px 123px; }
a#skihistory { width: 164px; height: 61px; background-position: -479px 123px; margin-right: 40px; }
a#altaenviron { width: 298px; height: 61px; background-position: 0px 123px; }
```

Snowbird CSS sprite rules

```css
.sprite { background: url(sprites.gif); }
a.sprite { display: block; float: left; margin-right: 5px; border: 2px solid #FFF; }
div#headerWeather div.icon { width: 36px; height: 26px; }
div.less_rain { background-position: -118px -142px; }
div.sunny { background-position: -177px -116px; }
div.partly_cloudy { background-position: -138px -116px; }
a#facebook { width: 66px; height: 25px; background-position: 0px -142px; }
a#twitter { width: 55px; height: 25px; background-position: -66px -142px; }
a#youtube { width: 48px; height: 25px; background-position: 0px -116px; }
a#flickr { width: 94px; height: 25px; background-position: -48px -116px; }
a#picofday { width: 218px; height: 22px; border: none; margin: 2px 0px 0px 2px; }
div#check_rates { width: 89px; height: 21px; background-position: 0px -261px; margin: 10px 0px; float: right; }
div#br_corner_light { width: 17px; height: 14px; background-position: -89px -268px; }
div#bl_corner_light { width: 17px; height: 14px; background-position: -105px -268px; }
```

After spriting the images shown above, I returned to [WebPagetest.org](https://www.webpagetest.org/) to examine the impact of the sprites. In most cases, I maintained the image format to limit the performance change to spriting only. I also did not change HTML or CSS even if I noticed other performance improvement opportunities. Here are the new results:

<table cellpadding="5" cellspacing="0" width="100%">
<tbody><tr>
<td align="center" style="background-color:#CCEEFF;">
<a href="/blog/2010/09/css-sprites/image-5-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5513844658910543170" src="/blog/2010/09/css-sprites/image-5.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 88px;"/></a>
With sprites, Alta’s homepage loaded in 2.768 seconds with a repeat request load time of 1.093 seconds.
</td>
<td align="center" style="background-color:#FFEECC;">
<a href="/blog/2010/09/css-sprites/image-6-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5513844659980320130" src="/blog/2010/09/css-sprites/image-6.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 186px; height: 200px;"/></a>
With sprites, Snowbird’s homepage loaded in 6.289 seconds with a repeat request load time of 2.513 seconds.
</td>
</tr>
</tbody></table>

A summary of differences shows:

- Both pages decreased the number of requests by 10.
- Alta decreased homepage load by 0.672 seconds, or 20% of the original page load. Snowbird decreased homepage load by 0.781 seconds, or 11% of the original page load.
- On repeat views, Alta’s homepage load would be decreased by 0.665 seconds, or 40% of the original repeated page load. On repeat view, Snowbird’s homepage load would be decreased by 0.633 seconds, or 20% of the original repeat page load.

There is no reason to avoid sprites if a design has repeating elements or icons. An increase in performance will reduce load time for the customer. If a [CDN](https://en.wikipedia.org/wiki/Content_delivery_network) is in place, CSS sprites can result in a decreased bandwidth cost. The improved performance also can indirectly positively influence search engine performance since search engines may use performance as an influencing factor in search. This improved performance can also make for a better mobile browsing experience. In our examples, the use of CSS sprites decreased first request page load time by 10-20%, but this amount may vary depending on the frequency of images used in a site’s design.


