---
author: Greg Davidson
title: Enhancing Your Sites with Vue.js
github_issue_number: 1360
tags:
- javascript
- html
- frameworks
- vue
date: 2017-12-26
---

<img src="/blog/2017/12/enhancing-your-sites-with-vue/vuejs-logo.png" width="250" alt="Vue.js Logo" style="margin: 1em auto; display: block" />

### Framework Fatigue

When developers consider and evaluate front-end frameworks they often think in terms of writing *or rewriting* their entire project in Framework X. “Should we use Vue, React, Preact?” or “I heard about [Sapper](https://twitter.com/Rich_Harris/status/942493962857787392) the other day, has anyone tried that?” The running joke response (back-end developers especially **love** this one) is to the effect of: “If we wait a couple weeks there will be ten more choices!”

All joking aside, frameworks like [Vue](https://vuejs.org/ "Vue.js Project") and [React](https://reactjs.org/) offer many great benefits and can be *incrementally* adopted to enhance existing sites. There is no need to rewrite your entire project as a [Single Page Application](https://en.wikipedia.org/wiki/Single-page_application) to take advantage of what frameworks like Vue offer. I have taken this approach on a couple of my projects recently and been very happy with the results.

### Start Small

One of the benefits of using a framework in this way is that you’re not forced to adopt its entire toolchain and specific workflow immediately, such as using ES6/2015, [webpack](https://webpack.js.org/), and [Babel](https://babeljs.io/) right off the bat. I simply loaded the minified, minimal version of Vue I needed on my page and I was off to the races.

If you are familiar with [Angular](https://angular.io/), Vue has a similar concept of [custom directives](https://vuejs.org/v2/guide/custom-directive.html). I used this to build a small countdown timer directive for a customer who wanted to dynamically display the time left before promotions ended. By offloading the DOM updates and rendering to Vue, I was able to create a useful feature very quickly with lean and readable JavaScript code.

Here’s what the widget I delivered to the client looked like:

```html
<countdown-timer start="{start date/time}" end="{end date/time}" />
```

They were able to drop this snippet onto their pages *and* use multiple instances of the widget on their product listing page with ease.

### Wishlist Pagination

For another project I needed to display wishlists in the cart, below the items the customer had previously added. The wishlist feature is very popular and used by a large number of customers. Many customers have dozens (some hundreds!) of products in their wishlist at any given time.

For this project I was already using [gulp](https://gulpjs.com/) to handle the front-end automation so I simply added Vue and [vuejs-paginate](https://github.com/lokyoung/vuejs-paginate) to the project config and loaded those scripts asynchronously on the cart page. The vuejs-paginate plugin has a simple API that emitted the pagination related events I could tap into.

With a small Vue template and less than 100 lines of code I was able to create a dynamic and very responsive (read: fast!) pagination feature without any DOM manipulation code (e.g. updates, insertions, deletions, etc.).

With Vue (React and friends as well) you simply manage the state of your application (wishlist items in this case) and let the framework handle the rendering step. Give it a try—​I think you’ll like it!
