---
author: Steph Skardal
title: 'Vue and Ecommerce: An Introduction'
github_issue_number: 1386
tags:
- ecommerce
- vue
- javascript
- open-source
date: 2018-02-19
---

<img src="/blog/2018/02/vue-in-ecommerce/vue-shop.png" alt="Vue Shop created by Matheus Azzi" /><br />

I speak the domain specific language of ecommerce, Ruby on Rails, JavaScript, and jQuery. Lately, I’ve been getting up to speed on [Vue.js](https://vuejs.org/). I’ve been working on writing a small ecommerce site using Vue.js, because for me, creating an application addressing familiar paradigm in a new technology is a great way to learn.

Vue.js, initially released about 3 years ago, is a lightweight JS framework that can be adopted incrementally. In the case of my small example site, Vue.js serves the frontend shop content and connects to a decoupled backend that can be run on any platform of choice. On my path to get up to speed on Vue, I found great resources that I wanted to write about before I get into the details of my ecommerce app. Here they are:

* First, I started with the [Vue.js documentation](https://vuejs.org/v2/guide/). The documentation is great as a starting point to understand some of the terminology. I often don’t love the documentation that comes with technologies, but I found the <b>Essentials</b> section in the Vue documentation to be a great launching point.
* After I worked through some of the Vue.js documentation, I did a simple search for “[vue jsfiddle](https://www.google.com/search?q=vue+jsfiddle)” and experimented with a few of those fiddles. Having come from a jQuery background (with [mustache](https://mustache.github.io/)), I was familiar with how templating and logic inside a template might work, but less familiar with [the vue instance](https://vuejs.org/v2/guide/instance.html) and [binding](https://vuejs.org/v2/guide/class-and-style.html), so I targeted jsfiddles with this in mind.
* Next, I looked for resources with Vue + ecommerce specifically. Here’s where I found some good stuff:
    * [Scotch.io Course on Vue + Ecommerce](https://scotch.io/courses/build-an-online-shop-with-vue/introduction): This online course has a great amount of overlap with the main documentation of Vue, but some of the examples are ecommerce specific, which serves as a good introduction.
    * [Vue + Third Party Integration for Ecommerce](https://medium.com/@connorleech/standing-on-the-shoulders-of-giants-node-js-vue-2-stripe-heroku-and-amazon-s3-c6fe03ee1118): This Medium article talks about integrating third party tools used with Vue (Stripe, AWS S3, Heroku) to build an ecommerce site. While this post doesn’t go into the nitty gritty details of a Vue application, it does provide many code examples for checkout and payment integration, although noting that [vue-stripe-elements](https://github.com/fromAtoB/vue-stripe-elements) is now the module of choice for Stripe integration in Vue.
    * [Vue API App + Magento Backend](https://vuejsfeed.com/blog/vue-js-storefront-pwa-for-ecommerce): This is a front-end open source Vue application designed to pair with a Magento backend, capitalizing on the popularity of Magento.
    * [Moltin](https://moltin.com/): This company is providing backend microservices for ecommerce, with Vue.js support (and other technologies) to build out your store.
    * [Vue + Ecommerce with Vuex](https://travishorn.com/vue-online-store-with-shopping-cart-c072433f8d9e): Here’s another Medium article which features [vuex](https://vuex.vuejs.org/en/), the state management library in Vue, essentially going through examples of state management to manage a shopping cart.
    * [CodePen Vue + Ecommerce Example](https://codepen.io/mjweaver01/pen/yerzox): Here’s a standalone CodePen example of a Vue shopping cart. While I find this a little hard to parse because there’s a significant amount of code in the example, you can download and experiment with it.
    * [Stripe Integration Example](https://github.com/sdras/sample-vue-shop): Here’s a GitHub repo that demonstrates Stripe integration in serverless Vue shop. 
    * [Basic Vue Shop on GitHub](https://github.com/matheusazzi/shop-vue): Why reinvent the wheel when someone has already built out product listing and cart functionality? After reviewing all the examples above, this was my choice for a starting point in building out a Vue shop, but it is a basic starter point, without the use of [vue-router](https://router.vuejs.org/en/).

### Vue Libraries / Dependencies 

You might have noticed I mentioned a few Vue libraries and tools. Here are additional resources for getting up to speed on those dependencies:

* Installing Node.js and npm, if you aren’t already familiar with it. [Here](https://www.quora.com/How-does-npm-compare-to-other-packaging-systems-like-Ruby-gems-and-Pythons-pip) is a great comparison if you are coming from the Rails space.
* Already mentioned, [vuex](https://vuex.vuejs.org/en/intro.html) state management in Vue.
* [vue-router](https://router.vuejs.org/en/). In an ecommerce site, you would possibly have routing for the index, product detail, cart, checkout, user account, order detail pages.
* [vue-cli](https://github.com/vuejs/vue-cli): simple command line interface for scaffolding Vue projects. Think “rails generate ...” for Vue.
* [vue-resource](https://github.com/pagekit/vue-resource), or a comparable module ([vue-axios](https://alligator.io/vuejs/rest-api-axios/)) for making API and AJAX requests.

### Incremental Adoption

While I am writing a Vue ecommerce shop based on the shop-vue GitHub repo mentioned above, in the ecommerce space, we commonly take on incremental ecommerce updates rather than “The Big Rewrite”, as noted in [Greg’s article](/blog/2017/12/enhancing-your-sites-with-vue/). Components that could be introduced incrementally into existing ecommerce applications might include:

* Dynamic marketing elements on homepage or product listing page, e.g. promo tools, “Customers Also Looked at”, “Products Recently Viewed”
* Cart + Checkout process (standalone component)
* Admin elements for data management and processing
* User account section
