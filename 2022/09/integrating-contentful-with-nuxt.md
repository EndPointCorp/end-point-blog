---
author: "Juan Pablo Ventoso"
title: "Integrating Contentful with NuxtJS"
tags:
- nuxtjs
- vue
- cms
- saas
date: 2022-09-05
---

![Fishing on a sunset at Rio de la Plata](/blog/2022/09/integrating-contentful-with-nuxt/fishing-rio-de-la-plata-sunset.jpg)

<!-- Photo by Juan Pablo Ventoso -->

Some time ago, I had the opportunity to collaborate on a cool [NuxtJS](https://nuxtjs.org/) project. I'm still somewhat new to [Vue.js](https://vuejs.org/) and its related frameworks, meaning I'm still discovering exciting new tools and third-party services that can be integrated with them every time a new requirement appears. And there is a particular concept that I heard of, but never worked with... until this project: I'm talking about using a [Headless CMS](https://en.wikipedia.org/wiki/Headless_content_management_system) to deliver content.

Essentially, a headless CMS permits creating a custom content model and make it accesible through one (or several) APIs that we can query, allowing to choose whatever presentation layer we prefer to handle the display. This approach decouples the content management part (the "body") of a project from the design, templates and frontend logic (the "head"), becoming particularly useful when we have several application types that will interact with the same data, such as a website, a mobile app, or an [IoT](https://en.wikipedia.org/wiki/Internet_of_things) device.

With that in mind, let's have a quick look at [Contentful](https://www.contentful.com/): It's a headless CMS that is offered under the concept of content-as-a-service ([CaaS](https://www.contentful.com/r/knowledgebase/content-as-a-service/)), meaning the content is delivered on-demand from a cloud platform to the consumer by implementing an API or web service.

### Pricing

For individual or small websites, the free option should be sufficient. It has a limit of 5 users and a size limit of 50MB for assets, and the technical support area is disabled. The next option (Medium, $489/month) also includes an additional role (author), additional locales, and you can create up to 10 different users. The asset size is also extended up to 1000MB.

![Contentful pricing](/blog/2022/09/integrating-contentful-with-nuxt/contentful-pricing.jpg)

You can review the full pricing details [here](https://www.contentful.com/pricing/).

### Creating content

In order to start creating content, there are two essencial steps:

* We will need to [set up a new space](https://www.contentful.com/help/contentful-101/#step-2-create-a-space). A space is an area where the content will be grouped into a single project.

* We need to define the [model for our content](https://www.contentful.com/help/contentful-101/#step-3-create-the-content-model). The model is the type and structure that our content will have. For the integration below, we will need a new "Page" model, that will contain two fields to save the basic information for a static page: `title` and `content`. We could also add a publish date field, just for us to keep track of when the content was created.

![Page content model](/blog/2022/09/integrating-contentful-with-nuxt/page-content-model.jpg)

### Integration

With our space created and our content model ready, it's time to add Contentful to our NuxtJS app. The integration process is quite simple, thanks to the [JavaScript client library](https://www.npmjs.com/package/contentful) provided by Contentful. The library is based on the [axios](https://github.com/axios/axios) client, allowing it to run on the client as well as on the server, for [SSR](https://nuxtjs.org/docs/concepts/server-side-rendering/). If we have [npm](https://www.npmjs.com/) set up, we can add it to our project by running:

```bash
npm install --save contentful
```

The most efficient way to use it across our app and have it ready for both client and server rendering, is to declare a new plugin. All we need to do is create a new file named `contentful.js` under our project's `plugins` folder:

```js
const contentful = require('contentful')

const config = {
  space: process.env.CONTENTFUL_SPACE_ID,
  accessToken: process.env.CONTENTFUL_API_ACCESS_TOKEN,
}

module.exports = {
  createClient() {
    return contentful.createClient(config)
  },
}
```

Next, we need to add the new environment variables to our project's .env file. The values that we need to provide are our [space ID](https://www.contentful.com/help/find-space-id/) and the [access token](https://www.contentful.com/developers/docs/references/authentication/) for querying the API:

```
CONTENTFUL_SPACE_ID={our_space_id}
CONTENTFUL_API_ACCESS_TOKEN={our_access_token}
```

We're all set! Now, we have our plugin ready to use. One neat extra step that we did for this particular project, is creating a `ContentfulPage` component that will automatically pull the contents from Contentful based on the given entry ID. By doing that, we can simple use the component in all the static pages that we have in our website.

First, let's create the component, containing a simple wrapper for the template section, and an `entryId` property that we will use to query the API. We can save it under `~/components/ContentfulPage.vue`:

```html
<template>
  <div :id="entryId">
    <p v-if="$fetchState.pending">Loading...</p>
    <div v-else>
      <h1>
        {{ page.fields.title }}
      </h1>
      <div class="page-content" v-html="$md.render(page.fields.content)" />
    </div>
  </div>
</template>

<script>
  import { createClient } from '~/plugins/contentful'
  const contentful = createClient()

  export default {
    name: 'ContentfulPage',
    props: {
      entryId: {
        type: String,
        required: true,
      },
    },

    data() {
      return {
        page: {},
      }
    },

    async fetch() {
      this.page = await contentful.getEntry(this.entryId)
    },
  }
</script>
```

This component will load fetch the entry from Contentful asynchronously, and display a "loading" legend while it does so. Once the query is complete, the content will be shown inside the `div` element with the `page-content` class. The component expects the returned page to have at least two attributes: `title` and `content`.

With the new component added to our project, we are ready to create a page (for example, `index.vue`) that uses it to render our content like this:

```html
<template>
  <div>
    <contentful-page entry-id="{index_entry_id}" />
  </div>
</template>

<script>
  import ContentfulPage from '~/components/ContentfulPage'
  export default {
    components: {
      ContentfulPage,
    },
  }
</script>
```

All we need to do, is to get the entry ID from the content we created in Contentful, and pass it to the entry-id parameter of the component, and that's it! Our content will be fetched from the API and displayed to the user. It will also work when rendering on the client, as well as for SSR.

### Alternatives

There are several alternatives to Contentful out there: [Prismic CMS](https://prismic.io/) or [GraphCMS](https://graphcms.com/) -based entirely in GraphQL- are the most popular. There are also downloadable products, like [SilverStrap CMS](https://www.silverstripe.org/). Their pricing plans are varied, but all of them offer a free community plan for starters or small websites.

Have you used any other headless CMS not listed here? We would love to hear your comments!