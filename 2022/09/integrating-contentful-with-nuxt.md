---
author: "Juan Pablo Ventoso"
title: "Integrating Contentful with NuxtJS"
tags:
- nuxtjs
- vue
- cms
- saas
date: 2022-06-20
---

![Fishing on a sunset at Rio de la Plata](/blog/2022/06/integrating-contentful-with-nuxt/fishing-rio-de-la-plata-sunset.jpg)

<!-- Photo by Juan Pablo Ventoso -->

Some time ago, I had the opportunity to collaborate on a cool [NuxtJS](https://nuxtjs.org/) project. I'm still somewhat new to [Vue.js](https://vuejs.org/) and its frameworks, meaning I'm discovering exciting new tools and third-party services that can be integrated with them every time a new requirement appears. And there is a particular concept that I heard of theorically, but never worked with until this project. I'm talking about using a [Headless CMS](https://en.wikipedia.org/wiki/Headless_content_management_system) to deliver content.

Essentially, a headless CMS allows creating a custom content model and make it accesible through one (or several) APIs, allowing to choose whatever presentation layer we prefer to handle the display. This approach decouples the content management part (the "body") from the design, templates and frontend logic (the "head"), becoming particularly useful when we have several application types that will interact with the same data, such as a website, a mobile app, or an [IoT](https://en.wikipedia.org/wiki/Internet_of_things) device.

With that in mind, let's talk about [Contentful](https://www.contentful.com/): It's a headless CMS, under the concept of content-as-a-service ([CaaS](https://www.contentful.com/r/knowledgebase/content-as-a-service/)), meaning the content is delivered on-demand from a cloud platform to the consumer by implementing an API or web service.

--
--

--
--

### Pricing

For individual or small websites, the free option should be sufficient. It has a limit of 5 users and a size limit of 50MB for assets, and the technical support area is disabled. The next option (Medium, $489/month) also includes an additional role (author), additional locales, and you can create up to 10 different users. The asset size is also extended up to 1000MB.

![Contentful pricing](/blog/2022/06/integrating-contentful-with-nuxt/contentful-pricing.jpg)

You can review the full pricing details [here](https://www.contentful.com/pricing/).

--
--


When you make a request for an image, you can instruct the Cloudinary API to [retrieve it with a given size](https://cloudinary.com/documentation/resizing_and_cropping), which will trigger a transformation on their end before delivering the content. You can also use a cropping method: fill, fill with padding, scale down, etc.

### Gravity position

When we specify a [gravity position](https://cloudinary.com/documentation/resizing_and_cropping#control_gravity) to crop an image, the service will keep the area of the image we decide to use as the focal point. We can choose a corner (for example, top left), but also—and this is probably one of the most interesting capabilities on this service—we can specify ["special positions"](https://cloudinary.com/documentation/transformation_reference#g_special_position): By using machine learning, we can instruct Cloudinary to use face detection, or even focus on other objects, like an animal or a flower in the picture.

### Automatic format

Another cool feature is the [automatic format](https://cloudinary.com/documentation/transformation_reference#f_auto), which will use your request headers to find the most efficient picture format for your browser type and version. For example, if the browser supports it, Cloudinary will return the image in WebP format, which is generally more efficient than standard JPEG, as End Point CTO Jon Jensen demonstrates on his recent [blog post](https://www.endpointdev.com/blog/2022/02/webp-heif-avif-jpegxl/).

![Screenshot of Chrome browser dev tools showing network response for a WebP image](/blog/2022/03/optimizing-image-delivery-with-cloudinary/image-response.jpg)<br>
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


--
--

### Alternatives

There are several alternatives to Contentful out there: [Prismic CMS](https://prismic.io/) or [GraphCMS](https://graphcms.com/) -based entirely in GraphQL- are the most popular. There are also downloadable products, like [SilverStrap CMS](https://www.silverstripe.org/). Their pricing plans are varied, but all of them offer a free community plan for starters or small websites.

Have you used any other headless CMS not listed here? We would love to hear your comments!