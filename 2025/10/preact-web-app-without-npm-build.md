---
author: Dmitry Kiselev
title: A Preact Web App Without npm Build
description: A simple way to use Preact and Signals directly in the browser—no npm, no bundlers, just HTML, CSS, and JS.
date: 2025-10-15
github_issue_number: 2154
featured:
  image_url: /blog/2025/10/preact-web-app-without-npm-build/nyc-skyline-orange-sunset.webp
tags:
- nodejs
- javascript
---

![An orange sun sets over New York City, viewed from the top of a building in Manhattan. A water tower is visible in front of buildings which reflect bright light on the left side, with shadows on the right side.](/blog/2025/10/preact-web-app-without-npm-build/nyc-skyline-orange-sunset.webp)

<!-- Photo by Seth Jensen, 2025. -->

Modern JavaScript frameworks such as React and Preact usually require a full “build pipeline” with Node.js, npm, and bundlers like Webpack or Vite. That’s fine for large web apps, but sometimes you just need a small, self-contained browser interface inside a project that isn’t mainly about the web — say, a Java program that processes transit data and simply needs a page to display results.

This post explores how to use Preact and its companion library @preact/signals *without any npm build process at all*. By taking advantage of browser-native import maps and writing a bit of code directly in JavaScript instead of JSX, it shows how to build a lightweight, modern UI that runs straight from static HTML, CSS, and JS files — no build tools required.

### The Scenario

This might look like a strange problem to solve but sometimes the web UI part just isn’t a main character in your project.

For instance, I have a GTFS data processor whose main goal is to preprocess public transport stop timetables. It’s written in Java and I want a simple browser UI to check its output. So I want the web UI part of the project to be just static HTML, CSS, and JavaScript files.

I also don’t want to run npm or yarn inside what would otherwise be a pure Maven-managed project. But at the same time, I would like to use a modern JS UI framework such as Preact.

### The Main Issues

To pull off this trick, there are two main challenges:

* JSX
* Imports

### JSX

JSX is basically JavaScript templates. When you write something like:

```javascript
function Greeting() {
  return (
    <div className="greeting">
      Hello world
    </div>
  )
}

function App() {
  return (<Greeting/>)
}
```

During project build Babel will transform it into:

```javascript
function Greeting() {
  // Particular function for creating elements may vary.
  return h('div', {className: "greeting"}, 'Hello world')
}

function App() {
 return h(Greeting, null);
}
```

This is a pretty straightforward transformation, and no one is stopping you from importing the element creation function (h in the example above) and composing what would be Babel output yourself.

### Imports

Now for the more interesting issue: imports.

Normally, with a build process, you could just write:

```javascript
import { h } from 'preact'
import { signal } from '@preact/signals'
```

What’s more, some packages will try to resolve their own dependencies by importing them by global name. For instance, `@preact/signals` will try to import `@preact/signals-core`, and there isn’t a ready-made UMD (Universal Module Definition) version of `@preact/signals-core` available.

### The Solution: Browser Import Maps

I would like to be able to just map library names to URLs of ES modules.

There is a relatively new browser feature that does exactly this: an *import map*. It’s a special type of `<script>` block containing a JSON object with your mapping.

```react
<script type="importmap">
  {
    "imports": {
      "preact": "https://unpkg.com/preact@latest/dist/preact.mjs",
      "preact/hooks": "https://unpkg.com/preact@latest/hooks/dist/hooks.mjs",
      "preact/compat": "https://unpkg.com/preact@latest/compat/dist/compat.mjs",
      "@preact/signals-core": "https://unpkg.com/@preact/signals-core@latest/dist/signals-core.mjs",
      "@preact/signals": "https://unpkg.com/@preact/signals@latest/dist/signals.mjs"
    }
  }
</script>
```

And that’s it!

With the import map in place, your browser can resolve all those imports directly from a CDN like [unpkg.com](https://unpkg.com/). You can then use Preact, hooks, and signals exactly as if you were running a fully bundled app.

### Conclusion

This approach is ideal for small, embedded, or hybrid projects where a full JavaScript toolchain would be overkill. It lets you:

* Build modern UI components with Preact
* Avoid npm, yarn, Babel, and bundlers entirely
* Keep your project clean and language-native (e.g., Maven for Java, without extra layers)
* Run everything as plain static assets, right from your browser

Everything works, and nothing extra gets in the way.

