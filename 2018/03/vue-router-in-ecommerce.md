---
author: Steph Skardal
title: 'Vue in Ecommerce: Routing and Persistence'
github_issue_number: 1387
tags:
- ecommerce
- vue
- javascript
- open-source
date: 2018-03-01
---

<img src="/blog/2018/03/vue-router-in-ecommerce/vue-shop.png" alt="Vue Shop created by Matheus Azzi" /><br />

I recently wrote about [Vue in Ecommerce](/blog/2018/02/vue-in-ecommerce/) and pointed to a handful of references to get started. Today, I’ll talk about using [vue-router](https://router.vuejs.org/en/) in a small ecommerce application, combined with [vuex-persist](https://www.npmjs.com/package/vuex-persist) for state storage.
 
I forked this [Vue Shop on GitHub](https://github.com/matheusazzi/shop-vue) from Matheus Azzi. It was a great starting point for to see how basic component organization and state management might look in a Vue ecommerce application, but it is a single page ecommerce app with no separate page for a product detail, checkout, or static pages, so here I go into some details on routing and persistence in a Vue ecommerce application.

### Vue Router

In looking through the documentation, I don’t see a great elevator pitch on what it is that Vue Router does. If you are new to routing, it’s a tool to map the URL request to the Vue component. Since I’m coming from the Rails perspective, I’m quite familiar with the Ruby on Rails routing from URL pattern matching, constraints, resources to Ruby on Rails controllers and actions. Vue routing via vue-router has some similar elements.

When you create a basic Vue application via vue-cli, you are given the option to include vue-router:

```
vue init webpack myapp

? Project name myapp
? Project description A Vue.js project
? Author Steph <steph@endpoint.com>
? Vue build standalone
? Install vue-router? (Y/n) 
```

If you select Yes here, the main differences you’ll see are that an application with vue-router installed will call `<router-view/>` to render the view for the current router, instead of a `<HelloWorld/>` component, and that a vue-router app will include src/router/index.js with basic routing configuration to your `<HelloWorld/>` component.

#### Without Routing
```
// App.vue without vue-router
<template>
  <div id="app">
    <img src="./assets/logo.png">
    <HelloWorld/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

```

#### With Routing

```
// App.vue with vue-router
<template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>


// src/router/index.js
import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
```

Moving on, building out an ecommerce app with some basic page set up, not including user accounts, might look like the setup below, which includes basic components and routes for the Home, Cart, Checkout, Receipt, and About page. This simplified set-up doesn’t even include a product detail page, but one could accomplish that with a bit of URL matching via parameters.

```
// src/router/index.js
import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/components/pages/Home'
import Receipt from '@/components/pages/Receipt'
import About from '@/components/pages/About'
import Cart from '@/components/pages/Cart'
import Checkout from '@/components/pages/Checkout'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', component: Home },
    { path: '/receipt', component: Receipt },
    { path: '/about', component: About },
    { path: '/cart', component: Cart },
    { path: '/checkout', component: Checkout }
  ]
})
```

##### History Mode

One thing you also might notice is the ‘history’ mode setting above, overriding the default hash mode. You can read about that [here](https://router.vuejs.org/en/essentials/history-mode.html), but it leverages `history.pushState` to URL navigation. The history mode override must be combined with server configuration to ensure that non-static asset URL requests (i.e. all of our routes) hit the Vue index.html app in our Vue application, and then renders the component associated with the requested route. I’m using Apache for my Vue application, so I followed the instructions on that documentation for vue-router history mode configuration.

##### Using \<router-link/\>

One thing you also will want to use throughout your templates is `<router-link/>`, instead of hard-coding rigid URL paths. For example, instead of linking to the cart via `<a href="/cart">Cart</a>`, you’ll want to link via `<router-link to="cart">Cart</router-link>`. This will be resolve to the proper link upon rendering depending on your routing configuration. 


### Vuex PersistedState 

If you are still reading, you’ve now seen the basic configuration for vue-router in an ecommerce application running on Vue. The ecommerce application I forked uses [vuex](https://vuex.vuejs.org/en/intro.html), a state management pattern and library to store the state of our application. What you’ll notice with a shopping cart application, though, is that you need to persist the state of your cart for sessions. Without further setup, every page refresh on your application will result in losing the state of the cart.

To address this behavior, there are a few options to persist your state in Vue. I chose [vuex-persist](https://www.npmjs.com/package/vuex-persist), which stores the state (for all modules or specific modules) in localStorage. After installing vuex-persist, I modified the following to include the shoppingCart module in my stored state:

```
// src/store/index.js
import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
// import other stuff

Vue.use(Vuex)
const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
  reducer: state => ({
    shoppingCart: state.shoppingCart
  })
})

export default new Vuex.Store({
  // ...
  plugins: [vuexLocal.plugin]
})
```

It’s as simple as that to persist the state of your shopping cart using all the vuex-persist defaults, and there are some alternative Promise-based stores supported if you are interested.

### What’s Next?

What’s next in building out your ecommerce application? From here, one might consider adding user authentication & authorization support, as well as support for retrieving and rendering products in the product list view. I hope to address those in upcoming blog posts in this series on Vue in ecommerce.
