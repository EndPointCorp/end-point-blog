---
author: Jeff Boes
title: Determining dominant image color
github_issue_number: 441
tags:
- graphics
date: 2011-04-21
---



This grew out of a misunderstanding of a client’s request, so it never saw the light of day, but I thought it was an interesting problem.

The request was to provide a “color search” of products, i.e., “show me all the orange products”. Finding the specific products was not a challenge since it was just a database query. Instead I was interested in how to choose a “representative image” from among the available images for that product. (And as it turns out, the image filename gave me that information, but let’s assume you don’t have that luxury: how do you tell, from a group of images, which one is “more orange” than the others?)

Of course, this depends on the composition of the image. In this case, I knew that the majority were of solid-color (or two- or three-color at most) products on a white background. The approach that was settled on was to severely pixellate the image into something like 20x20 (arbitrary; this could be very dependent on the images under study, or the graphics library in use). If you also supply a color palette restricted to the colors you are interested in matching (e.g., primary, and secondary colors, plus perhaps black, white, and gray), you would have a roster of the colors represented.

Another approach makes use of the powerful ImageMagick library. There’s a huge list of examples and instructions at [https://www.imagemagick.org/Usage/quantize/](https://www.imagemagick.org/Usage/quantize/), but for my purposes this short sample will do:

<img height="117px;" src="/blog/2011/04/determining-dominant-image-color/image-0.jpeg" width="156px;"/>

```nohighlight
$ convert Waffle.jpg -scale 1x1\! -format '%[pixel:u]' info:-
rgb(219,166,94)
```

<img height="37px;" src="/blog/2011/04/determining-dominant-image-color/image-1.png" width="48px;"/>

Here we reduce an image to a single pixel, then report the RGB value of that color. After that it’s just a matter of determining how close this “average” is to your desired color.


