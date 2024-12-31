---
title: "Introduction to Nuxt3 and Rendering Modes"
author: Bimal Gharti Magar
date: 2024-07-12
github_issue_number: 2063
description: An overview of Nuxt3, a free and open-source JS meta-framework for Vue.
featured:
  image_url: /blog/2024/07/introduction-to-nuxt3-and-rendering-modes/cloud-cover.webp
tags:
- javascript
- vue
- frameworks
---

![Billowing clouds tower over a tree-covered mountain range. Their texture is oddly smooth, and they are slightly tinged by orange light. On the right side of the image, vertically centered, is a light pole which arches to the left.](/blog/2024/07/introduction-to-nuxt3-and-rendering-modes/cloud-cover.webp)

<!-- Photo by Seth Jensen, 2024. -->

Nuxt is a free and open-source framework which helps us build performant full-stack web applications and websites with Vue.js. Nuxt is built on top of Vue, so it is also called a meta-framework. Nuxt uses conventional style directory structure to streamline repetitive tasks and allow developers to focus on more important operational tasks. The configuration file can be used to customize the default behaviors.

### Nuxt3 features

1. **File-based routing**. Nuxt generates routes based on the Vue files and folder structure within the `pages/` directory. For example, if we have a `pages/contact.vue` file, Nuxt will generate a corresponding route at `/contact`. It also supports dynamic routing: `pages/product/[sku].vue` includes the route `/product/APPLE`, giving the `[sku].vue` single-file component access to the value `APPLE`.

2. **Auto-imports**. Components, composables, and helper functions have their respective directories which can be used across the project without importing them. This feature enhances the developer experience by removing the long list of imports. Nuxt also supports automatic importing of [Vue APIs](https://vuejs.org/api/). It can be configured to import third-party packages using the `nuxt.config` file. Auto import can also be disabled using `nuxt.config`.

3. **Server-side rendering**. Nuxt has built-in server-side rendering (SSR) support, without having to configure the server. It has benefits such as loading pages quickly, improved search engine optimization, caching, and many more. We will talk more about other rendering methods later.

4. **Data-fetching utilities**. Nuxt provides composables to handle SSR-compatible [data fetching](https://nuxt.com/docs/getting-started/data-fetching) as well as different strategies.

5. **TypeScript support**. Nuxt3 fully supports TypeScript.

6. **Modules**. Nuxt provides a [module system](https://nuxt.com/modules) to extend the framework core and simplify integrations.

### Rendering Modes
The process of interpreting JavaScript code to convert Vue components to HTML elements is called rendering. This can happen both in the browser and the server. Nuxt supports the following rendering modes and we will discuss them more in detail:

#### 1. Universal Rendering (SSR + CSR)

This is the default rendering mode which provides a great user experience, good performance, and optimized search engine indexing. The rendering mode can be switched by changing the [`ssr`](https://nuxt.com/docs/api/nuxt-config#ssr) value in `nuxt.config`.

In this mode, the server returns a fully rendered HTML page to the browser on request. Nuxt runs the Vue code in the server, which produces HTML content. Users get the content of web application which can be displayed in browser.

After the page is loaded from the server, the browser loads the JS code to make content interactive and dynamic. The browser re-interprets the Vue code to enable interactivity. This process of making a page interactive in the browser is called "[hydration](https://nuxt.com/docs/api/composables/use-hydration)".

Universal rendering provides quick page load times while preserving the benefits of client-side rendering. It enhances SEO because HTML content is already present for crawling.

Pros:

- **Performance**. Browsers display static content faster, hence users can see the page content almost immediately. Nuxt also preserves the interactivity of the web application using hydration.
- **SEO**. Web crawlers can index the page's content easily as universal rendering delivers the entire HTML content of the page to the browser.

Cons:

- **Development constraints**. Some APIs don't work in both the browser and the server; for example, the `window` object is only available in the browser, so it can't be accessed on the server. It can be time consuming to write code that runs on both sides. Nuxt does provide guidelines and variables to help with this.
- **Cost**. Unlike hosting static files, universal rendering requires a server to generate the full HTML content. Using a server adds cost.

#### 2. Client-Side Rendering (CSR)

A traditional Vue application loads the JavaScript code on the browser first, then interprets the code to generate the HTML elements and interface.

Pros:

- **Development speed**. Writing client-side-only code improves development speed as we don't have to worry about supporting server-side compatibility.
- **Cheaper**. The code can be hosted on a simple web server without the need for a application server, and can run in the browser, reducing the server-side cost.
- **Offline**. Once the JavaScript has been sent to the client, the code only runs in the browser. This means the web application can keep working even if there is no internet.

Cons:

- **Performance**. Because the browser has to first download files and then run JavaScript files to generate the HTML document, the page can be slow to load initially. This depends on the network download speed as well as the performance of the user's device for executing the JS code. This negatively affect page load times and user experience.
- **SEO**. Crawlers takes more time indexing and updating the content delivered. Based on the above performance drawback, the crawler may not wait until the interface is fully rendered, and will report slower load speeds.

Client-side rendering is the preferred choice for heavy interactive web applications such as SaaS and back-office applications that don't require indexing.

Enabling client-side only rendering with Nuxt can be done by updating `nuxt.config`:

```ts
export default defineNuxtConfig({
  ssr: false
})
```

#### 3. Hybrid Rendering

Hybrid rendering allows different caching rules per route using Route Rules which can dictate the server response for each new request.

Without hybrid rendering all the routes/pages of the application use the same rendering mode—either universal or client-side.

With hybrid rendering, some pages which have static content can be generated at build time while pages which have dynamic content (e.g. dashboard or orders pages) can be generated client-side.

Nuxt3 provides a way to support hybrid rendering using `routeRules` in `nuxt.config`:

```ts
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true }, // Pre-render or SSG
    '/country': { ssr: false }, // CSR (SPA)
    '/university': { ssr: false }, // CSR (SPA)
    '/isr/country': { isr: true }, // ISR without TTL
    '/isr/university': { isr: 60 }, // ISR with TTL
    '/swr/country': { swr: true }, // SWR without TTL
    '/swr/university': { swr: 60 }, // SWR with TTL
    '/prerender/country': { prerender: true }, // Pre-render or SSG
    '/prerender/university': { prerender: true }, // Pre-render or SSG
  }
)
```
Routes can have various properties such as:

* `ssr`.  This is used to disable or enable server-side rendering for the given route. It can be used to make SPA app like dashboard and orders page for serving dynamic content with `ssr: false`.
* `swr`. SWR means state-while-revalidate. This is a caching technique which enables the server to provide cached data for a configurable Time to live (TTL). We can define a time value in seconds, which is used to set TTL, or just pass `true`, which sets the TTL with maximum age. Without TTL, the response is cached until there is change in the content. With TTL, the response is cached until the TTL expires. The response of the page upon first request is generated and cached.
* `isr`. This stands for "incremental static regeneration." It is similar to `swr`, with the main difference being that the response is cached on the CDN. It can also be configured with TTL and without TTL.
* `prerender`. This generates pages based on routes at build time and serves them as static pages.

There are many more [properties](https://nuxt.com/docs/guide/concepts/rendering#route-rules) that we can use to define how each route will act.

I've created a demo [app](https://ep-nuxt-render.vercel.app/) showing hybrid rendering. This app shows list of countries and universities with details pages.

- The `/country` and `/university` routes are defined as single-page applications (SPA—this means they use client-side rendering). We can see that the time on the server and the time on the client are almost same, with the difference being hydration time.
- The `/prerender/country` and `/prerender/university` routes are defined as prerendered or static-site generated (SSG), which means the pages are generated at build time. The server time shows the time when the build was run to generate the pages, and does not change.
- The `/prerender/country/{countries starting from a to m}` routes are defined as prerendered, which means the countries whose name starts with `a` to `m` are generated at build time. We can browse any of the prerendered country pages, like `/prerender/country/Canada`, where we see that the server times are build times. However, if we browse a country page which isn't prerendered, like `/prerender/country/Nigeria`, we see that server times are the same as browser times.
- The `/isr/country`, `/isr/country/**`, `/swr/country/**`, and `/swr/country` routes are defined as ISR and SWR respectively, with the maximum TTL set. These pages will serve cached content until the response changes.
- The `/isr/university`, `/isr/university/**`, `/swr/university/**` and `/swr/university` routes are defined as ISR and SWR with a TTL of 120 seconds. This means that when first browsed, the pages will serve the initial response and cache it for 2 minutes.

You can see the code for the demo app on [GitHub](https://github.com/bimalghartimagar/EPNuxtRender).
