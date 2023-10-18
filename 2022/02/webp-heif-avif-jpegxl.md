---
author: "Jon Jensen"
title: "Image compression: WebP presets, HEIC, AVIF, JPEG XL"
tags:
- compression
- graphics
- browsers
- optimization
github_issue_number: 1832
date: 2022-02-15
---

![Rubble of a demolished house in front of a guilty-looking Caterpillar excavator](/blog/2022/02/webp-heif-avif-jpegxl/20211223-224644-sm.webp)

<!-- Photo by Jon Jensen -->

How time flies. Eight years ago I wrote the blog post [WebP images experiment on End Point website](/blog/2014/01/webp-images-experiment-on-end-point/) to describe and demonstrate how the WebP image format can store an equivalent-quality image in a much smaller file size than the older JPEG, PNG, and GIF formats.

My WebP examples there were 17–23% of the JPEGs they came from, or about 5–6× smaller. While experimenting with higher levels of compression, I found that WebP tends to leave less-noticeable artifacts than JPEG does.

The main drawback at the time was that, among major browsers, only Chrome and Opera supported WebP, and back then, Chrome was far less popular than it is now.

### Can I use it?

Since Apple's iOS 14 and macOS 11 (Big Sur) became available in late 2020, the WebP image format now works in all the currently supported major operating systems and browsers: Linux, Windows, and macOS, running Chromium, Chrome, Brave, Edge, Opera, Firefox, and Safari. You can see the specifics at the ever-useful site ["Can I use"](https://www.caniuse.com/webp).

It only took about 10 years! 😁

So for you who are hosting websites, all your site visitors can see WebP images and animations except those vanishing few using Internet Explorer (now long past its end of support by Microsoft and dangerous to use), and people (or their organizations) who intentionally do not allow their older browsers and operating systems to be updated.

That means you may want to continue using JPEG, PNG, and/or GIF images in places crucial for rendering your main site features, for people to be able to understand the main things your site is trying to communicate.

But for any images that are less essential and primarily making it prettier, or where you don't mind suggesting that users of old browsers upgrade to see them, WebP can now be your default image format.

### How do I create WebP images?

Mobile phones and digital cameras typically save JPEG, HEIF, or raw (uncompressed) images. Some stock photography collections offer WebP downloads, but many still use JPEG.

So in many cases you won't be starting with a WebP image, and you'll convert some other image to WebP, likely after cropping, scaling, and other adjustments.

GIMP (GNU Image Manipulation Program) supports WebP images since about 2017, and Adobe Photoshop does not natively but can use the [free WebPShop plugin](https://developers.google.com/speed/webp/docs/webpshop).

The oldest way to convert images to WebP, and still very useful for batch processing or fine-tuning, is [Google's WebP converter "cwebp"](https://developers.google.com/speed/webp).

### cwebp settings

With the power "cwebp" offers comes some complexity, but it is mostly harmless.

Run this to see its many options:

```sh
cwebp -longhelp
```

Or read the same thing in its [online documentation](https://developers.google.com/speed/webp/docs/cwebp).

There among other things you will see the `-z` option which activates preset features for lossless encoding, with an integer level chosen from 0 to 9 where 0 is fastest but compresses less and 9 is slowest but compresses better. Use this to replace PNG files when you want no degradation of the image at all.

The documentation also shows the useful `-preset` and `-hint` options for lossy compression similar to what JPEG does, but better:

```plain
-preset <string> ....... preset setting, one of:
                          default, photo, picture,
                          drawing, icon, text

-hint <string> ......... specify image characteristics hint,
                         one of: photo, picture or graph
```

The meaning of a few of those terms, especially "photo" and "picture", was not clear to me and not defined elsewhere in the documentation that I could see.

To find that out I had to make a quick trip into the source code, and there are comments explaining each option's use case a bit:

The comments for the [`-preset` option](https://chromium.googlesource.com/webm/libwebp/+/refs/heads/main/src/webp/encode.h#159):

```plain
WEBP_PRESET_PICTURE,  // digital picture, like portrait, inner shot
WEBP_PRESET_PHOTO,    // outdoor photograph, with natural lighting
WEBP_PRESET_DRAWING,  // hand or line drawing, with high-contrast details
WEBP_PRESET_ICON,     // small-sized colorful images
WEBP_PRESET_TEXT      // text-like
```

And the comments for the [`-hint` option](https://chromium.googlesource.com/webm/libwebp/+/refs/heads/main/src/webp/encode.h#88):

```plain
WEBP_HINT_PICTURE,    // digital picture, like portrait, inner shot
WEBP_HINT_PHOTO,      // outdoor photograph, with natural lighting
WEBP_HINT_GRAPH,      // Discrete tone image (graph, map-tile etc).
```

So in short, "cwebp" considers a "picture" to be indoors and close-up, while "photo" is outdoors and more likely with more distant focus. That's good to know.

### Batch conversion

With that in mind, I can convert a pile of screenshots that have been collecting on my computer to refer to later. One kind of screenshots I sometimes take is of video meetings with mostly indoor views of people. I will use the "picture" preset for those.

A simple `bash` script works well to process many images in a row:

```bash
for infile in Screenshot*.png
do
    echo $infile
    base=$(basename "$infile" .png)
    cwebp -preset picture -v "$infile" -o "$base".webp
done
```

If you have many images to convert to WebP and want to do several at the same time to get done faster, you can use [GNU parallel](https://www.gnu.org/software/parallel/).

**My screenshots when converted from PNG to WebP consistently take about 3% of the original space, 33–35× smaller! And the quality looks about the same. Amazing.**

These screenshots are 2880×1800 pixels, mostly of Google Meet low-bandwidth video streams. The originals of these screenshots don't look particularly good to begin with, with some blurriness. But exactly because of this, there is no reason for me to keep a larger high-quality original here. The much smaller WebP is fine.

### Competitors to WebP

Other newer image formats have also been in the works for years, chasing some of the same goals. Should we skip WebP and use one of them instead?

#### HEIC

The [HEIC (High-Efficiency Image Container)](https://en.wikipedia.org/wiki/High_Efficiency_Image_File_Format#HEIC:_HEVC_in_HEIF) subset of the HEIF (High Efficiency Image File Format) standard uses High Efficiency Video Coding (HEVC, H.265) for storing images with a `.heic` suffix.

Compared to JPEG, HEIC offers the nice advantages of smaller file sizes for the same quality level (roughly half the size of an equivalent JPEG), and animation support (to replace GIF).

On the downside, HEIC is encumbered by patents that limit its use for major commercial projects, even on devices licensed for consumer use. It is also slower to encode/​decode. And, concerning for archivists, HEIC shows severe visual damage to the entire image if part of the file is corrupted. In contrast, with corrupted JPEG files the visual damage is typically localized to particular smaller square regions, not the entire image.

HEIC has been used in Apple's operating systems since the 2017 release of the iPhone 7 and iOS 11 and macOS 10.13 (High Sierra). Support was later added to Windows 10, Android 9, and Ubuntu 20.04.

As of this writing, no major browsers [support HEIC natively](https://caniuse.com/heif), not even Apple's own Safari.

So for now, HEIC is primarily used by Apple to store photos more efficiently on its mobile devices.

#### AVIF

The [AVIF (AV1 Image File Format)](https://en.wikipedia.org/wiki/AVIF) competes with HEIC and, confusingly, uses the same HEIF container file format that HEIC does. That confusion is reduced in practice by its use of the separate file extension `.avif`.

[AVIF is supported](https://www.caniuse.com/avif) in current Chrome, Firefox, and Opera. Support was added to WebKit in 2021, but it still has not made its way into Safari. It also works in newer VLC, GIMP, Windows, Android, etc.

Netflix has a [very detailed blog post](https://netflixtechblog.com/avif-for-next-generation-image-coding-b1d75675fe4) comparing AVIF to JPEG and showing AVIF's many advantages.

#### JPEG XL

A semi-compatible successor to JPEG has long been in the works, and JPEG XL seems likely to eventually fill that role.

Whereas the other new image formats mentioned above usually lose some quality when recompressing JPEG and other images that were already lossy-compressed, according to the [Joint Photographic Experts Group (JPEG)](https://jpeg.org/jpegxl/):

> Existing JPEG files can be losslessly transcoded to JPEG XL, significantly reducing their size.

It has been reported that JPEG XL is expected to become available in its final standard form in 2022, and support is already available in preliminary form in some software (see the [Wikipedia JPEG XL article](https://en.wikipedia.org/wiki/JPEG_XL)).

That of course means that for now, no major browsers [support JPEG XL natively](https://caniuse.com/jpegxl).

### Use WebP now

So all the other new options are not yet usable for general web images. WebP is the current obvious choice, whether you want a lossy replacement for JPEG photos, a lossless replacement for PNG images, or a replacement for GIF animations.

Our developers have set up automatic server-side app conversion of high-quality PNG originals to WebP or JPEG on the fly, with the image size dependent on the browser viewport size. And we have worked with Cloudinary, Cloudflare, and other CDNs to use their image conversion services. We are available to help with your projects too.

### Reference

The Mozilla Development Network (MDN) has excellent documentation of web image format details, filename suffixes, and support in the major browsers in its [Image file type and format guide](https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types).
