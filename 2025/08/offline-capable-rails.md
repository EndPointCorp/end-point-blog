---
author: "Couragyn Chretien"
title: "Building Offline-Capable Rails Apps Using Service Workers and Turbo"
description: "How to cache pages and assets, handle Turbo form submissions offline, and provide a fallback UI for a Rails app."
featured:
  image_url: /blog/2025/08/offline-capable-rails/red-flowers.webp
github_issue_number: 2133
date: 2025-08-07
tags:
- rails
- javascript
---

![The left half of the image is dominated by out-of-focus pink-red flower petals close to the camera, which give way to petals on branches which are in focus, with sunlight shining through the back.](/blog/2025/08/offline-capable-rails/red-flowers.webp)

<!-- Photo by Seth Jensen on Karmir 160 film, 2025. -->

Users today expect web apps to continue working even when their internet connection is unstable or temporarily lost. Out of the box, Rails applications do not handle this well. In this blog post, we will walk through how to add offline support to a Rails app using Service Workers, Workbox, and Turbo. This approach gives users a smoother experience and better reliability when network conditions are not ideal.

This guide focuses on a real-world setup. You will learn how to cache pages and assets, handle Turbo form submissions offline, and provide a fallback UI when needed.

### Why Offline Support Matters

Turbo makes Rails applications fast and responsive by replacing traditional client-side JavaScript with HTML over the wire. However, if the network drops out, those Turbo requests fail silently. Adding a Service Worker allows us to intercept those requests and provide a better experience.

Offline support improves performance, enhances user experience on mobile devices, and adds resilience in situations where network access is intermittent.

### Creating a Manifest File

Start by adding a manifest file to your Rails app. This file lets the browser know your app supports offline behavior.

Create a file at `app/assets/manifest.json` with the following content:

```json
{
  "name": "Offline Rails App",
  "short_name": "OfflineRails",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#222222"
}
```

Then, in your application layout, reference the manifest file:

```erb
<%= tag.link rel: "manifest", href: asset_path("manifest.json") %>
```

This enables progressive web app features and prepares your app for Service Worker support.

### Creating the Service Worker

Rails does not ship with a Service Worker, so you need to create one. You can either output the compiled Service Worker file directly into the `public` folder or configure your JavaScript build system to handle it.

Here is a minimal Service Worker example using Workbox, saved as `public/service-worker.js`:

```javascript
import { precacheAndRoute } from 'workbox-precaching'
import { registerRoute } from 'workbox-routing'
import { NetworkFirst, CacheFirst } from 'workbox-strategies'

precacheAndRoute(self.__WB_MANIFEST || [])

registerRoute(
  ({ request }) => request.mode === 'navigate',
  new NetworkFirst()
)

registerRoute(
  ({ request }) => ['style', 'script', 'image'].includes(request.destination),
  new CacheFirst()
)
```

This configuration tells the browser to try the network first for page navigation, but to fall back to cache if offline. Static assets such as stylesheets, scripts, and images are cached after the first visit.

### Registering the Service Worker in Your Rails App

To register the Service Worker, add this code to your Rails JavaScript entry point. In Rails 7 with import maps or jsbundling, this is usually found in `application.js` or `app/javascript/application.js`:

```javascript
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js')
      .then(reg => console.log('Service worker registered', reg))
      .catch(err => console.error('Registration failed', err))
  })
}
```

Once registered, the browser begins managing network requests through the Service Worker.

### Pre-Caching Essential Pages

To ensure key pages are available offline before a user visits them, you can pre-cache them during the install phase of the Service Worker.

Add the following to your Service Worker file:

```javascript
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('static-pages-v1').then(cache => {
      return cache.addAll([
        '/',
        '/important_things',
        '/offline.html'
      ])
    })
  )
})
```

These pre-cached pages are useful for first-time offline users and can be extended as needed.

### Handling Offline Turbo Form Submissions

Turbo uses fetch to submit forms. If the network is down, the request will fail and the user may not even notice. To improve this, you can intercept Turbo form submissions using Stimulus and queue them locally.

Here is an example Stimulus controller:

```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  connect() {
    this.element.addEventListener("turbo:submit-start", event => {
      if (!navigator.onLine) {
        event.preventDefault()
        const formData = new FormData(this.element)
        const payload = Object.fromEntries(formData)
        queueOfflineSubmission(payload)
        alert("You are offline. Your submission has been saved.")
      }
    })
  }
}
```

You will need to define `queueOfflineSubmission` to save the data to IndexedDB or localStorage. Later, you can sync the data when the connection is restored.

### Adding an Offline Fallback Page

If a request fails because the user is offline and the response is not cached, it is helpful to show a fallback page.

Add this to your Service Worker:

```javascript
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match('/offline.html')
    })
  )
})
```

Place a simple `offline.html` file in the `public` folder. This helps users understand what happened instead of seeing a generic browser error.

### Summary

Adding offline support to a Rails application is very achievable using Turbo, Service Workers, and a small amount of JavaScript. With this setup, your app can handle dropped connections without frustrating your users.

You now have a working foundation that includes:
* A browser manifest and Service Worker registration  
* Cached pages and assets for offline use  
* Form submission queuing while offline  
* A fallback UI for missing network responses
