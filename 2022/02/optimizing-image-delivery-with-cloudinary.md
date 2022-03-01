---
author: "Juan Pablo Ventoso"
title: "Optimizing media delivery with Cloudinary"
tags:
- compression
- graphics
- browsers
- optimization
date: 2022-02-21
---

![Mountain and clouds](/2022/02/optimizing-image-delivery-with-cloudinary/la-cumbrecita-202201.jpg)

<!-- Photo by Juan Pablo Ventoso -->

I remember how we needed to deal with different image formats and sizes years ago: From using the Wordpress-style approach of automatically saving different resolutions on the server when uploading a picture, to using a PHP script to resize or crop images on the fly and return the result as a response to the frontend. Of course, many of those approaches were expensive, and not fully optimized for different browsers or device sizes.

With those experiences in mind, it was a nice surprise for me to discover [Cloudinary](https://cloudinary.com/) when working on a new project a couple of months ago. It's basically a cloud service that saves and delivers media content with a lot of transformations and management options for us to use. [There is a free version](https://cloudinary.com/pricing) with a usage limit: Up to 25K transformations or 25 GB of storage/bandwidth, which should be enough for most non-enterprise websites. The cheapest paid service is $99 per month.

Here's a list of the image features we used on that project. I know they offer many other things that can be used as well, but I think this is a good start for anyone who hasn't used this service yet:

### Resizing and cropping

When you make a request for an image, you can instruct the Cloudinary API to [retrieve it with a given size](https://cloudinary.com/documentation/resizing_and_cropping), which will trigger a transformation on their end before delivering the content. You can also use a cropping method (fill, fill with padding, scale down, etc.).

### Gravity position

When we specify a [gravity position](https://cloudinary.com/documentation/resizing_and_cropping#control_gravity) to crop an image, the service will keep the area of the image we decide to use as the focal point. We can choose a corner (i.e. top left), but also -and this is probably one of the most interesting capabilities on this service- we can specify ["special positions"](https://cloudinary.com/documentation/transformation_reference#g_special_position): By using machine learning, we can instruct Cloudinary to use facial detection, or even focus on other objects, like an animal or a flower on the picture.

### Automatic format

Another cool feature is the [automatic format](https://cloudinary.com/documentation/transformation_reference#f_auto), which will use your request headers to find the most efficient picture format for your browser type and version. For example, if the browser supports it, Cloudinary will return the image in WebP format, which is generally more efficient than standard JPG, as End Point CTO Jon Jensen demonstrates on his recent [blog post](https://www.endpointdev.com/blog/2022/02/webp-heif-avif-jpegxl/).

![Automatic format in action: Returning a WebP image in Chrome](/2022/02/optimizing-image-delivery-with-cloudinary/image-response.jpg)<br>
Automatic format in action: Returning a WebP image in Chrome

### Other features

There are many other options for us to choose when querying their API, like setting up a default placeholder when we don’t have an image, applying color transformations, removing red eyes, among other things. The [Transformation reference page](https://cloudinary.com/documentation/transformation_reference) on their documentation section is a great resource.

### NuxtJS integration

The project I mentioned above was a [NuxtJS](https://nuxtjs.org/) application with a [Node.js](https://nodejs.org/) backend. And since there's a [NuxtJS module for Cloudinary](https://cloudinary.nuxtjs.org/), it made sense to use it instead of building the queries to the API from scratch.

The component works great, except for one bug that we found that didn't allow us to fully use their image component with server-side rendering enabled. Between that drawback and some issues trying to use the lazy loading setting, we ended up creating a Vue component ourselves that used a standard image tag instead. But we still used their component to generate most of the API calls and render the results.

Below is an example of using the Cloudinary Image component on a Vue template:

```html
<template>
  <div>
    <cld-image
      :public-id="publicId"
      width="200"
      height="200"
      crop="fill"
      gravity="auto:subject"
      radius="max"
      fetchFormat="auto"
      quality="auto"
      alt="An image example with Cloudinary"
    />
  </div>
</template>
```

### Alternatives

Of course, Cloudinary is not the only image processing and CDN company out there: There are other companies offering similar services, like [Cloudflare images](https://www.cloudflare.com/products/cloudflare-images/), [Cloudimage](https://www.cloudimage.io/), or [imagekit.io](https://imagekit.io/).

Do you know any other good alternatives, or have you used any other Cloudinary feature that is not listed here? Feel free to add a comment below!