---
author: Phin Jensen
title: Supporting Apple Retina displays on the Web
github_issue_number: 987
tags:
- graphics
- browsers
date: 2014-05-27
---

Apple’s [Retina displays](https://en.wikipedia.org/wiki/Retina_Display) (on Mac desktop & laptop computers, and on iPhones and iPads) have around twice the pixel density of traditional displays. Most recent Android phones and tablets have higher-resolution screens as well.

I was recently given the task of adding support for these higher-resolution displays to our [End Point company website](/). Our imagery had been created prior to Retina displays being commonly used, but even now many web developers still overlook supporting high-resolution screens because it hasn’t been part of the website workflow before, because they aren’t simple to cope with, and since most people don’t notice any lack of sharpness without comparing low & high-resolution images side by side.

Most images which are not designed for Retina displays look blurry on them, like this:

<a href="/blog/2014/05/supporting-apple-retina-displays-on-web/image-0-big.png" imageanchor="1" style="display:inline"><img border="0" height="266" src="/blog/2014/05/supporting-apple-retina-displays-on-web/image-0.png" width="266"/></a>
<a href="/blog/2014/05/supporting-apple-retina-displays-on-web/image-1-big.png" imageanchor="1" style="display:inline"><img border="0" height="266" src="/blog/2014/05/supporting-apple-retina-displays-on-web/image-1.png" width="266"/></a>

The higher-resolution image is on the left, and the lower-resolution image is on the right.

Now, to solve this problem, you need to serve a larger, higher quality image to Retina displays. There are several different ways to do this. I’ll cover a few ways to do it, and explain how I implemented it for our site.

### Retina.js

As I was researching ways to implement support for Retina displays, I found that a popular suggestion is the JavaScript library [Retina.js](http://imulus.github.io/retinajs/). Retina.js automatically detects Retina screens, and then for each image on the page, it checks the web server for a Retina image version under the same name with @2x before the suffix. For example, when fetching the image background.jpg on a Retina-capable system, it would afterward look for background@2x.jpg and serve that if it’s available.

Retina.js makes it relatively painless to deal with serving Retina images to the correct people, but it has a couple of large problems. First, it fetches and replaces the Retina image *after* the default image, serving both the normal and Retina images to Retina users, greatly increasing download size and time.

Second, Retina.js does not use the correct image if the browser window is moved from a Retina display to a non-Retina display or vice versa when using multiple monitors. For example, if an image is loaded on a standard 1080p monitor and then the browser is moved to a Retina display, it will show the incorrect, low-res image.

### Using CSS for background images

Doesn’t the “modern web” have a way to handle this natively in HTML & CSS? For sites using CSS background images, CSS media queries will do the trick:

```css
@media only screen and (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .icon {
    background-image: url(icon@2x.png);
    background-size: 20px 20px;
  }
}
```

But this method only works with CSS background images, so for our site and a lot of other sites, it will only be useful for a small number of images.

Take a look at this [CSS-Tricks](https://css-tricks.com/snippets/css/retina-display-media-query/) page for some excellent examples of Retina (and other higher-res display) support.

### Server-side checks for Retina images

A very efficient way to handle all types of images is to have the browser JavaScript set a cookie that tells the web server whether to serve Retina or standard images. That will keep data transfer to a minimum, with a minimum of trickery required in the browser. You’ll still need to create an extra Retina-resolution image for every standard image on the server. And you’ll need to have a dynamic web process run for every image served. The [Retina Images](http://retina-images.complexcompulsions.com/) open source PHP program shows how to do this.

### Why we didn’t use these methods

There is one reason common to all of these methods which made us decide against them: All of them require you to maintain multiple versions of each image. This ends up taking a lot of time and effort. It also means your content distribution network (CDN) or other HTTP caches will have twice as many image files to load and cache, increasing cache misses and data transfer. It also uses more disk space, which isn’t a big problem for the small number of images on our website, but on an ecommerce website with many thousands of images, it adds up quickly.

We would feel compelled to have the separate images if it were necessary if the Retina images were much larger and slow down the browsing experience for non-Retina users for no purpose. But instead we decided on the following solution that we saw others describe.

### Serving Retina images to everybody (how we did it)

We read that you can serve Retina images to everyone, but we immediately thought that wouldn’t work out well. We were sure that the Retina images would be several times larger than the normal images, wasting a ton of bandwidth for anyone not using a Retina screen. We were very pleasantly surprised to find out that this wasn’t the case at all.

After testing on a few images, I found I could get Retina images within 2-3 KB of the normal images while keeping the visual fidelity, by dropping the JPEG compression rate. How? Because the images were being displayed at a smaller size than they were, the compression artifacts weren’t nearly as noticeable.

These are the total file sizes for each image on our [team page](/team):

```plain
Retina  Normal  Filename
 10K    9.3K    adam_spangenthal.jpg
 13K     13K    adam_vollrath.jpg
 12K     11K    benjamin_goldstein.jpg
7.6K    4.2K    bianca_rodrigues.jpg
 14K     13K    brian_buchalter.jpg
 13K     15K    brian_gadoury.jpg
7.5K    8.0K    brian_zenone.jpg
9.8K    6.6K    bryan_berry.jpg
 12K     11K    carl_bailey.jpg
6.9K     15K    dave_jenkins.jpg
 13K     13K    david_christensen.jpg
7.7K     21K    emanuele_calo.jpg
 16K     16K    erika_hamby.jpg
 13K     11K    gerard_drazba.jpg
 14K     14K    greg_davidson.jpg
 14K     12K    greg_sabino_mullane.jpg
 14K     15K    jeff_boes.jpg
 14K     12K    jon_jensen.jpg
 13K     12K    josh_ausborne.jpg
 13K     14K    josh_tolley.jpg
 13K     11K    josh_williams.jpg
8.9K    9.5K    kamil_ciemniewski.jpg
 13K     21K    kent_krenrich.jpg
 15K     12K    kiel_christofferson.jpg
9.9K     11K    kirk_harr.jpg
7.7K     13K    marco_manchego.jpg
 12K     13K    marina_lohova.jpg
 14K     11K    mark_johnson.jpg
7.3K     13K    matt_galvin.jpg
 15K     12K    matt_vollrath.jpg
6.6K     14K    miguel_alatorre.jpg
 13K     14K    mike_farmer.jpg
7.1K     19K    neil_elliott.jpg
9.9K    9.0K    patrick_lewis.jpg
 13K    5.6K    phin_jensen.jpg
 12K     14K    richard_templet.jpg
 12K    9.9K    rick_peltzman.jpg
 14K     13K    ron_phipps.jpg
9.7K     14K    selvakumar_arumugam.jpg
9.3K     15K    spencer_christensen.jpg
 12K     12K    steph_skardal.jpg
 15K     18K    steve_yoman.jpg
6.7K     15K    szymon_guz.jpg
7.5K    6.8K    tim_case.jpg
 15K     21K    tim_christofferson.jpg
9.3K     12K    will_plaut.jpg
 12K     14K    wojciech_ziniewicz.jpg
 12K    9.9K    zed_jensen.jpg

TOTALS

Retina: 549.4K
Normal: 608.8K
```

This is where I found the biggest, and best, surprise. The cumulative size of the Retina image files was *less* than that of the original images. So now we have support for Retina displays, making our website look nice on modern screens, while actually using less data transfer. We don’t need JavaScript, cookies, or any extra server-side trickery to do this. And best of all, we don’t have to maintain a separate set of Retina images.

Once you’ve seen the difference in quality on a Retina screen or a new Android phone, you’ll wonder how you ever were able to tolerate the lower-resolution images. And at least for our selection of JPEG images, there’s not even a file size penalty to pay!

### Reference reading

- [A guide for creating a better retina web](https://ivomynttinen.com/blog/a-guide-for-creating-a-better-retina-web/) by Ivo Mynttinen
- [5 Things I Learned Designing For High-Resolution Retina Displays](https://www.leemunroe.com/designing-for-high-resolution-retina-displays/) by Lee Munroe
- [About Proper Image Delivery on the Web](https://developer.apple.com/library/safari/documentation/NetworkingInternet/Conceptual/SafariImageDeliveryBestPractices/Introduction/Introduction.html) on the Safari Developer Library
- [Serving Images Efficiently to Displays of Varying Pixel Density](https://developer.apple.com/library/safari/documentation/NetworkingInternet/Conceptual/SafariImageDeliveryBestPractices/ServingImagestoRetinaDisplays/ServingImagestoRetinaDisplays.html) on the Safari Developer Library
