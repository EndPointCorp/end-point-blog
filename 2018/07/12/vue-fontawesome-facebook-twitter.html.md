---
title: Vue, Font Awesome, and Facebook/​Twitter Icons 
author: David Christensen
tags: vue, javascript
gh_issue_number: 1443
---

<img src="/blog/2018/07/12/vue-fontawesome-facebook-twitter/fontawesome-screenshot.png" alt="some Font Awesome fonts" />

### Overview

[Font Awesome](https://fontawesome.com) and [Vue](https://www.vuejs.org/) are both great technologies. Here I detail overcoming some issues when trying to get the Facebook and Twitter icons working when using the `vue-fontawesome` bindings in the hopes of saving others future debugging time.

### Detail

Recently, I was working with the `vue-fontawesome` tools, which have recently been updated to version 5 of Font Awesome. A quick installation recipe:

```shell
$ yarn add @fortawesome/fontawesome
$ yarn add @fortawesome/fontawesome-svg-core
$ yarn add @fortawesome/free-solid-svg-icons
$ yarn add @fortawesome/free-brands-svg-icons
$ yarn add @fortawesome/vue-fontawesome
```

A best practice when using Font Awesome is to import only the icons you need for your specific project instead of the thousand+, as this just contributes to project bloat. So in our `main.js` file, we import them like so:

```js
// Font Awesome-related initialization
import { library } from '@fortawesome/fontawesome-svg-core'
import { faEnvelope, faUser } from '@fortawesome/free-solid-svg-icons'
import { faFacebook, faTwitter } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Add the specific imported icons
library.add(faEnvelope)
library.add(faUser)
library.add(faFacebook)
library.add(faTwitter)

// Enable the FontAwesomeIcon component globally
Vue.component('font-awesome-icon', FontAwesomeIcon)
```

This allows you to include icons in your view components like so:

```html
<template>
  <div class="icons">
    <font-awesome-icon icon="user"/>
    <font-awesome-icon icon="envelope"/>
  </div>
</template>
```

This worked fine for me until I tried to use the `facebook` and `twitter` icon:

```html
<template>
  <div class="icons">
    <font-awesome-icon icon="user"/>
    <font-awesome-icon icon="envelope"/>
    <font-awesome-icon icon="twitter"/>  <!-- broken -->
    <font-awesome-icon icon="facebook"/> <!-- broken -->
  </div>
</template>
```

Only blank spots and errors in the browser console like so:

```plaintext
[Error] Could not find one or more icon(s) (2)
{prefix: "fas", iconName: "twitter"}
{}
[Error] Could not find one or more icon(s) (2)
{prefix: "fas", iconName: "facebook"}
{}
```

After turning up dry from a run to the Google well and scanning the docs, I determined that this must come down to a difference in the prefix; since the icons that worked were being imported from the `free-solid-svg-icons` library, it would seem that that was the source of the `fas` prefix. Since the non-working icons were coming from the `free-brands-svg-icons` library it stood to reason that somehow passing in a prefix parameter of `fab` would work.

I tested modifying things like follows, just to exercise potentially obvious answers. Sadly, this did not result in workage.

```html
<template>
  <div class="icons">
    <font-awesome-icon icon="user"/>
    <font-awesome-icon icon="envelope"/>
    <font-awesome-icon icon="twitter" prefix="fab"/>  <!-- still broken -->
    <font-awesome-icon icon="fab-facebook"/>          <!-- also still broken -->
  </div>
</template>
```

I finally took to the original source for the `FontAwesomeIcon` component (every engineer’s favorite thing, aside from brown paper packages tied up with string), and noted the following:

```js
function normalizeIconArgs (icon) {
  if (icon === null) {
    return null
  }

  if (typeof icon === 'object' && icon.prefix && icon.iconName) {
    return icon
  }

  if (Array.isArray(icon) && icon.length === 2) {
    return { prefix: icon[0], iconName: icon[1] }
  }

  if (typeof icon === 'string') {
    return { prefix: 'fas', iconName: icon }
  }
}
```

AHA! The `icon` parameter is what was passed in in the `<font-awesome-icon>` component, so I immediately attempted to utilize an object to pass the `prefix` and the `iconName` parameter (since this is the name in the object referenced here, it should be the key).

So I ended up trying:

```html
<template>
  <div class="icons">
    <font-awesome-icon icon="user"/>
    <font-awesome-icon icon="envelope"/>
    <font-awesome-icon :icon="{ prefix: 'fab', iconName: 'twitter' }"/>
    <font-awesome-icon :icon="{ prefix: 'fab', iconName: 'facebook' }"/>
  </div>
</template>
```

(I am omitting the part where I stupidly left out the leading `:` to pass in an explicit object instead of a string equivalent.)

Everything worked! And there was much rejoicing! Hope this helps someone else who had the same issue as me.
