---
author: "David Christensen"
title: "Cloudflare and Vue SSR; Client Hydration Failures"
tags: vue, cloudflare, javascript
gh_issue_number: 1529
---

<img src="/blog/2019/06/11/cloudflare-vue-ssr-significant-comments/banner.jpg" alt="Camera and instant photos" />

[Photo](https://www.flickr.com/photos/freestocks/29163583261) by [freestocks](https://www.flickr.com/photos/freestocks), used under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)

I recently worked on getting a client’s Vue application converted to use Server Side Rendering (SSR). SSR works by generating the app’s initial HTML structure using a server-side process and then using client-side JavaScript to initialize or “hydrate” the application state on the client-side.

This worked out well in development and testing, however when it came time to roll things out to production, we ended up with a non-functioning application. While the server-rendered content was displaying inline, the client hydration piece was failing, and I was seeing browser console errors that I had never encountered before:

The error in Chrome:

```error
chunk-vendors.342a7610.js:21 Uncaught DOMException: Failed to execute 'appendChild' on 'Node': This node type does not support this method.
...
```

The error in Safari:

```error
[Error] HierarchyRequestError: The operation would yield an incorrect node tree.
	get (chunk-vendors.342a7610.js:27:30686)
	er (chunk-vendors.342a7610.js:27:30565)
	Le (chunk-vendors.342a7610.js:27:27806)
	xe (product-listing.0773c46e.js:1:18553)
[Error] TypeError: undefined is not an object (evaluating 't.$scopedSlots') — chunk-vendors.342a7610.js:27:27998
	on (chunk-vendors.342a7610.js:27:12025)
	rn (chunk-vendors.342a7610.js:27:11937)
	nn (chunk-vendors.342a7610.js:27:11584)
	(anonymous function) (chunk-vendors.342a7610.js:27:12759)
	fn (chunk-vendors.342a7610.js:27:12135)
	promiseReactionJob
```

Since the client hydration was failing, this resulted in a non-functioning front-end application which we had to quickly roll back. I’d scratched my head over this quite a bit, as this had been well-tested in development and staging.

After testing direct access to the origin server via `/etc/hosts` modification, we determined that the server itself was returning content that was working fine, so this pointed to something about the caching layer.

The errors being generated were similar to errors I’d encountered before during development where the generated DOM in the SSR content was mismatched with the version of the client-side Vue application.

One of the big differences here was that production was being served via Cloudflare (CF), however we had not run into any issues with stale versions (i.e., older versions of code being returned) and the like in the past. Our resources were stamped hashes via Webpack, so per-application version shouldn’t have been utilizing cached old versions of the generated resources in question.

Because we could not really debug this issue on production and this was still just a theory that CF was the issue, we ended up setting up a development environment behind Cloudflare.

Sure enough, the same issue started occurring in the development environment with Cloudflare fronting it; now, however, we had time to debug/diagnose without affecting production users.

After comparing the static JS for the app returned through CF against the raw source files, I noticed that they were slightly smaller. We had already minified the source as part of our production build, but CF was further minifying things, removing newlines and JS comments that had been left in the prod build. This made me realize that something on the CF side was minifying resources further.

After some research, it turns out the CF has an `AutoMin` setting to allow the automatic minification of served resources (JS, CSS, and HTML). This setting was contributing to the minification that I was seeing. However, this could not explain what I was seeing on the JS minification alone; these were verified non-functional changes that should not affect how the app ran.

I turned my attention to the HTML of the page itself. Comparing the CF-returned version with the version returned by the app, I quickly saw that minification was affecting this returned HTML as well, cleaning up spacing/formatting and HTML comments as well.

And herein lay the issue; Vue SSR sticks in HTML comments as placeholders for nodes which are non-visible at server render time. So for example, if you had a Vue component like so:

```vue
<template>
  <div>
    My component!
    <div v-if="display">
      <p v-for="l in list">
        {{ l }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MyComponent',
  data () {
    return {
      list: [1, 2, 3]
    }
  }
  props: {
    display: {
      type: Boolean,
      default: false
    }
  }
}
</script>
```

This would render in Vue SSR as the following HTML (assuming the component was not shown by the calling app):

```html
<div>My component!<!-----></div>
```

Here, the `<!----->` placeholder is a *significant* HTML comment, standing in for a non-visible component in the virtual DOM (the false condition in the `v-if` directive). Rehydration requires this to be in place for proper handling, so when CF stripped out HTML comments from the returned page output this disrupted the generated server-side DOM. This meant that the server-side DOM no longer matched what Vue was expecting and the client-side hydration failed and the app failed to init properly.

I tested disabling `AutoMin` for the test site, which resulted in a functioning application, verifying this was the issue. We did not want to turn off `AutoMin` globally, so I looked around for ways to narrow this down to only the affected pages (all of which had a common URL prefix).

I came across CF’s `Page Rules` settings, which let you modify its handling of specific URLs. I added an exception for the pages in question, turning off only the `AutoMin` setting for these pages, and voilà, the app worked while leaving this setting on for the rest of the site.

TL;DR:

Cloudflare’s `AutoMin` setting can interfere with Vue SSR output by removing significant HTML comments. The fix is to disable `AutoMin` on the relevant pages using `Page Rules`.

