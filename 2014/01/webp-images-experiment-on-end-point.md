---
author: Jon Jensen
title: WebP images experiment on End Point website
github_issue_number: 918
tags:
- browsers
- graphics
- nginx
date: 2014-01-28
---

WebP is an image format for RGB images on the web that supports both lossless (like PNG) and lossy (like JPEG) compression. It was released by Google in September 2010 with open source reference software available under the BSD license, accompanied by a royalty-free public patent license, making it clear that they want it to be widely adopted by any and all without any encumbrances.

Its main attraction is smaller file size at similar quality level. It also supports an alpha channel (transparency) and animation for both lossless and lossy images. Thus it is the first image format that offers the transparency of PNG in lossy images at much smaller file size, and animation only available in the archaic limited-color GIF format.

### Comparing quality & size

While considering WebP for an experiment on our own website, we were very impressed by its file size to quality ratio. In our tests it was even better than generally claimed. Here are a few side-by-side examples from our site. You’ll only see the WebP version if your browser supports it:

<table cellspacing="10">
<tbody><tr>
<td><img alt="" height="133" src="/blog/2014/01/webp-images-experiment-on-end-point/image-0.jpeg" width="133"/><br/>12,956 bytes JPEG</td>
<td><img alt="" height="133" src="/blog/2014/01/webp-images-experiment-on-end-point/image-1.webp" width="133"/><br/>2186 bytes WebP</td>
</tr>
<tr>
<td><img alt="" height="133" src="/blog/2014/01/webp-images-experiment-on-end-point/image-2.jpeg" width="133"/><br/>11,149 bytes JPEG</td>
<td><img alt="" height="133" src="/blog/2014/01/webp-images-experiment-on-end-point/image-3.webp" width="133"/><br/>2530 bytes WebP</td>
</tr>
</tbody></table>

The original PNG images were converted by ImageMagick to JPEG, and by `cwebp -q 80` to WebP. I think we probably should increase the WebP quality a bit to keep a little of the facial detail that flattens out, but it’s amazing how good these images look for file sizes that are only 17% and 23% of the JPEG equivalent.

One of our website’s background patterns has transparency, making the PNG format a necessity, but it also has a gradient, which PNG compression is particularly inefficient with. WebP is a major improvement there, at 13% the size of the PNG. The image is large so I won’t show it here, but you can follow the links if you’d like to see it:

<table cellspacing="15">
<tbody><tr>
<td align="right">337,186 bytes</td><td><a href="http://jon.endpoint.com/blog/container-pattern.png">container-pattern.png</a></td>
</tr>
<tr>
<td align="right">43,270 bytes</td><td><a href="http://jon.endpoint.com/blog/container-pattern.webp">container-pattern.webp</a></td>
</tr>
</tbody></table>

### Browser support

So, what is the downside? WebP is currently natively supported only in Chrome and Opera among the major browsers, though amazingly, support for other browsers can be added via WebPJS, a JavaScript WebP renderer.

Why don’t the other browsers add support given the liberal license? Especially Firefox you’d expect to support it. In fact a patch has been pending for years, and a debate about adding support still smolders. Why?

WebP does not yet support progressive rendering, Exif tagging, non-RGB color spaces such as CMYK, and is limited to 16,384 pixels per side. Some Firefox developers feel that it would do the Internet community a disservice to support an image format still under development and cause uncertain levels of support in various clients, so they will not accept WebP in its current state.

Many batch image-processing tools now support WebP, and there is a free Photoshop plug-in for it. Some websites are quietly using it just because of the cost savings due to reduced bandwidth.

For our first experiment serving WebP images from the End Point website, I decided to serve WebP images only to browsers that claim to be able to support it. They advertise that support in this HTTP request header:

```
Accept: image/webp,*/*;q=0.8
```

That says explicitly that the browser can render image/webp, so we just need to configure the server to send WebP images. One way to do that is in the application server, by having it send URLs pointing to WebP files.

Let’s plan to have both common format (JPEG or PNG) and WebP files side by side, and then try a way that is transparent to the application and can be enabled or disabled very easily.

### Web server rewrites

It’s possible to set up the web server to transparently serve WebP instead of JPEG or PNG if a matching file exists. Based on some examples other people posted, we used this nginx configuration:

```nohighlight
    set $webp "";
    set $img "";
    if ($http_accept ~* "image/webp") { set $webp "can"; }
    if ($request_filename ~* "(.*)\.(jpe?g|png)$") { set $img $1.webp; }
    if (-f $img) { set $webp "$webp-have"; }
    if ($webp = "can-have") {
        add_header Vary Accept;
        rewrite "(.*)\.\w+$" $1.webp break;
        break;
    }
```

It’s also good to add to /etc/nginx/mime.types:

```
image/webp .webp
```

so that .webp files are served with the correct MIME type instead of the default application/octet-stream, or worse, text/plain with perhaps a bogus character set encoding.

Then we just make sure identically-named .webp files match .png or .jpg files, such as those for our examples above:

```
-rw-rw-r-- 337186 Nov  6 14:10 container-pattern.png
-rw-rw-r--  43270 Jan 28 08:14 container-pattern.webp
-rw-rw-r--  14734 Nov  6 14:10 josh_williams.jpg
-rw-rw-r--   3386 Jan 28 08:14 josh_williams.webp
-rw-rw-r--  13420 Nov  6 14:10 marina_lohova.jpg
-rw-rw-r--   2776 Jan 28 08:14 marina_lohova.webp
```

A request for a given $file.png will work as normal in browsers that don’t advertise WebP support, while those that do will instead receive the $file.webp image.

The image is still being requested with a name ending in .jpg or .png, but that’s just a name as far as both browser and server are concerned, and the image type is determined by the MIME type in the HTTP response headers (and/or by looking at the file’s magic numbers). So the browser will have a file called $something.jpg in the DOM and in its cache, but it will actually be a WebP file. That’s ok, but could be confusing to users who save the file for whatever reason and find it isn’t actually the JPEG they were expecting.

### 301/302 redirect option

One remedy for that is to serve the WebP file via a 301 or 302 redirect instead of transparently in the response, so that the browser knows it’s dealing with a different file named $something.webp. To do that we changed the nginx configuration like this:

```nohighlight
    rewrite "(.*)\.\w+$" $1.webp permanent;
```

That adds a little bit of overhead, around 100-200 bytes unless large cookies are sent in the request headers, and another network round-trip or two, though it’s still a win with the reduced file sizes we saw. However, I found that it isn’t even necessary right now due to an interesting behavior in Chrome that may even be intentional to cope with this very situation. (Or it may be a happy accident.)

### Chrome image download behavior

Versions of Chrome I tested only send the Accept: image/webp [etc.] request header when fetching images from an HTML page, not when you manually request a single file or asking the browser to save the image from the page by right-clicking or similar. In those cases the Accept header is not sent, so the server doesn’t know the browser supports WebP, so you get the JPEG or PNG you asked for. That was actually a little confusing to hunt down by sniffing the HTTP traffic on the wire, but it may be a nice thing for users as long as WebP is still less-known.

### Batch conversion

It’s fun to experiment, but we needed to actually get all the images converted for our website. Surprisingly, even converting from JPEG isn’t too bad, though you need a higher quality setting and the file size will be larger. Still, for best image quality at the smallest file size, we wanted to start with original PNG images, not recompress JPEGs.

To make that easy, we wrote [two shell scripts](https://gist.github.com/jonjensen/8677031) for Linux, bash, and cwebp. We found a few exceptional images that were larger in WebP than in PNG or JPEG, so the script deletes any WebP file that is not smaller, and our nginx configuration will in that case not find a .webp file and will serve the original PNG or JPEG.

### Full-page download sizes compared

Here are performance tests run by WebPageTest.org using Chrome 32 on Windows 7 on a simulated cable Internet connection. The total download size difference is most impressive, and on a slower mobile network or with higher latency (greater distance from the server) would affect the download time more.

<table id="pagespeeds">
<tbody><tr>
<th align="center" rowspan="2">Page URL</th>
<th align="center" colspan="3">With WebP</th>
<th align="center" colspan="3">Without WebP</th>
</tr>

<tr>
<th align="center">Bytes</th>
<th align="center">Time</th>
<th align="center">Details</th>

<th align="center">Bytes</th>
<th align="center">Time</th>
<th align="center">Details</th>
</tr>

<tr>
<td><a href="http://www.endpoint.com/">http://www.endpoint.com/</a></td>

<td align="right">374 KB</td>
<td align="right">2.9s</td>
<td><a href="http://www.webpagetest.org/result/140128_2D_XJY/">report</a></td>

<td align="right">850 KB</td>
<td align="right">3.4s</td>
<td><a href="http://www.webpagetest.org/result/140128_RC_10M6/">report</a></td>
</tr>

<tr>
<td><a href="http://www.endpoint.com/team">http://www.endpoint.com/team</a></td>

<td align="right">613 KB</td>
<td align="right">3.6s</td>
<td><a href="http://www.webpagetest.org/result/140128_YD_ZRK/">report</a></td>

<td align="right">1308 KB</td>
<td align="right">4.1s</td>
<td><a href="http://www.webpagetest.org/result/140128_F8_10MA/">report</a></td>
</tr>
</tbody></table>

### Conclusion

This article is not even close to a comprehensive shootout between WebP and other image types. There are other sites that consider the image format technical details more closely and have well-chosen sample images.

My purpose here was to convert a real website in bulk to WebP without hand-tuning individual images or spending too much time on the project overall, and to see if the overall infrastructure is easy enough to set up, and the download size and speed improved enough to make it worth the trouble, and get real-world experience with it to see if we can recommend it for our clients, and in which situations.

So far it seems worth it, and we plan to continue using WebP on our website. With empty browser caches, visit [www.endpoint.com](/) using Chrome and then one of the browsers that doesn’t support WebP, and see if you notice a speed difference on first load, or any visual difference.

I hope to see WebP further developed and more widely supported.

### Further reading

- [WebP project home](https://developers.google.com/speed/webp/)
- [Wikipedia on WebP](http://en.wikipedia.org/wiki/WebP)
- Firefox debate: [bug #600919](https://bugzilla.mozilla.org/show_bug.cgi?id=600919), [bug #856375](https://bugzilla.mozilla.org/show_bug.cgi?id=856375)
- [WebPJS](http://webpjs.appspot.com/)
