---
title: "Introduction to Nuxt3 and rendering modes"
date: 2024-06-03
---
### Introduction

Nuxt is a free and open source framework which helps us build performant full-stack web applications and websites with Vue.js. Nuxt is built on top of Vue.js, so it is also called a meta framework. Nuxt uses conventional style directory structure to streamline repetitive tasks and allow developers to focus on more important operational tasks. The configuration file can be used to customize the default behaviors.

#### Nuxt3 features:

1. File-based routing
Nuxt generates routes based on the vue files and folder structure within the `pages/` directory. For example, if we have a file `pages/contact.vue`, it will generate a corresponding route at `/contact`. It also supports dynamic routing which can be defined in a folder structure like `pages/product/[sku].vue`, which supports the route `/product/APPLE`, where `[sku].vue` SFC will have access to value `APPLE`.

1. Auto-imports
Components, composables and helper functions have their respective directories, which can be used across the project without importing them. This feature enhances the developer experience by removing the long list of imports. Nuxt also supports auto importing of [Vue.js APIs](https://vuejs.org/api). It can be configured to import third party packages using `nuxt.config` file. Auto import can also be disabled using `nuxt.config` 

1. Server-side rendering: Nuxt has built-in SSR support, without having to configure server. It has many benefits such as loading pages quickly, improved search engine optimization, caching and many more. We will talk more about other rendering methods later below.

1. Data-fetching utilities: Nuxt provides composables to handle SSR-compatible [data fetching](https://nuxt.com/docs/getting-started/data-fetching) as well as different strategies.

1. TypeScript support: Nuxt3 fully supports typescript

1. Modules: Nuxt provides a [module system](https://nuxt.com/modules) to extend the framework core and simplify integrations.

### Rendering Modes
The process of interpreting JavaScript code to convert Vue.js components to HTML elements is called rendering. This can happen both in the browser and the server. Nuxt supports the following rendering modes and we will discuss them more in detail :

#### 1. Universal Rendering (SSR + CSR)
This is the default rendering mode which provides a better user experience, performance and optimized search engine indexing. The Rendering mode can be switched by changing [ssr](https://nuxt.com/docs/api/nuxt-config#ssr) value in `nuxt.config` file.

In this mode, the server returns a fully rendered HTML page to the browser on request. Nuxt runs the Vue.js code in the server, which produces HTML content. Users get the content of web application which can be displayed in browser.

After the page is loaded from the server, the browser loads the JS code to make content interactive and dynamic. The browser again interprets the Vue.js code to enable interactivity. This process of making a page interactive in the browser is called `Hydration`.

Universal rendering provides quick page load times while preserving the benefits of client-side rendering and also enhancing SEO because HTML content is already present for crawling.

Pros:
- Performance: Browsers display static content faster hence users can see the page content immediately. Nuxt also preserves the interactivity of the web application using hydration.
- SEO: Web crawlers can index the page's content easily as universal rendering delivers the entire HTML content of the page to the browser.

Cons:
- Development constraints: Some of the APIs don't work both in the browser and and the server side like a `window` object. It can be time consuming to write code that runs on both sides. Nuxt does provide guidelines and variables to help with this.
- Cost: Unlike hosting a static files, this requires running a server to generate the full HTML content. Using a server adds a cost.

#### 2. Client-Side Rendering (CSR)
A traditional Vue.js application loads the Javascript code on the browser first then interprets the code to generate the HTML elements and interface.

Pros:
- Development speed: Writing client side only code improves development speed as we don't have to worry about supporting server side compatibility.
- Cheaper: The code can be hosted on a simple web server just for hosting the files, and can run on the browser so it can reduce the cost.
- Offline: The code only runs on the browser, so the web application can keep working even if there is no internet.

Cons:
- Performance: Because the browser has to first download files and then run JavaScript files to generate the HTML document, the process can be slow depending on the network speed for downloading files and also depending on the performance of the user's device for executing the JS code. This can reduce the performance and impact user's experience.
- SEO: Crawlers takes more time indexing and updating the content delivered using client-side rendering. Based on the above performance drawback, the crawler may not wait for the interface until the interface is fully rendered.

Client-side rendering is preferred choice for interactive heavy web applications such as SaaS, back-office applications that don't require indexing.

Enabling client-side only rendering with Nuxt can be done by updating `nuxt.config`
```typescript nuxt.config.ts
export default defineNuxtConfig({
  ssr: false
})
```

#### 3. Hybrid Rendering

Hybrid rendering allows different caching rules per route using Route Rules which can dictate the server response for each new request.

Without hybrid rendering all the routes/pages of the application used the same rendering mode either universal or client-side.
With hybrid rendering, there may be various cases where some pages which have static content can be generated at build time while pages which have dynamic content like dashboard and orders page can be generated client side.

Nuxt3 provides a way to support hybrid rendering using `routeRules` config in `nuxt.config` file which looks like below:

```typescript
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
})
```
Routes can have various properties like:

##### a. `ssr`
This is used to disable or enable server side rendering for the given route. It can be used to make SPA app like dashboard and orders page for serving dynamic content with `ssr: false` 

##### b. `swr`
SWR means state-while-revalidate caching technique, this enables the server to provide cached data for configurable Time To Live(TTL). We can define a time value in seconds, which is used to set TTL or just pass true which sets the TTL with max age. Without TTL, the response is cached until there is change in the content. With TTL, the response is cached until the TTL expires. The response of the page upon first request is generated and cached.

##### b. `isr`
This is similar to `swr` with main difference being that the response is cached on the CDN. It also can be configured with TTL and without TTL.

##### c. `prerender`
This generates pages based on routes at build time and serves them as static pages.

There are many more [properties](https://nuxt.com/docs/guide/concepts/rendering#route-rules) that we can use to define how each route will act.


Demo [app](https://ep-nuxt-render.vercel.app/) showing hybrid rendering.
This app shows list of countries and universites and their details page. The app is deployed to vercel with hybrid rendering configuration.
- `/country` and `/university` routes are defined as client side rendering (SPA), where we can see the server time and client time are almost same with the differnce being hydration time.
- `/prerender/country` and `/prerender/university` routes are defined as prerendered or SSG, which means the pages are generated at build time. The server time shows the time when the build was run to generate the pages.
- `/prerender/country/{countries starting from a to m}` routes are defined as prerendered which means the countries whose name starts with `a` to `m` are generated at build time. We can browse any of the prerendered countries page like `/prerender/country/Canada`, we see server times are the same as build times, however if we browse non prerendered countries page like `/prerender/country/Nigeria` we see server times are just the same as browser times, the time we use to browse the page.
- `/isr/country`, `/isr/country/**`, `/swr/country/**` and `/swr/country` routes are defined as isr and swr set as max TTL which served cached content until the response changes.
- `/isr/university`, `/isr/university/**`, `/swr/university/**` and `/swr/university` routes are defined as isr and swr having TTL as 120 seconds. This means the pages when first browsed with the matching routes, will serve the initial response and cache it for 2 minutes.


Github [repo](https://github.com/bimalghartimagar/EPNuxtRender).