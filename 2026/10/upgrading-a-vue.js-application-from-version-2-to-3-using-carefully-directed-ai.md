---
author: "Kevin Campusano"
title: "Upgrading a Vue.js application from version 2 to 3 using carefully directed AI"
date: 2026-10-08
tags:
- vue
- javascript
- ai
- rails
---

I wouldn't go as far as saying that AI coding agents have made all programming problems shallow. But one area where they do excel is in well-specified but tedious tasks like upgrading a codebase to work with newer versions of their underlying frameworks and libraries.

Recently we inherited a legacy [Ruby on Rails](https://rubyonrails.org/) web application that had its frontend written with [Vue.js 2](https://v2.vuejs.org/). We were tasked with modernizing the entire codebase, and the frontend was of course a big part of that work. Version 2 of Vue has long been [deprecated](https://v2.vuejs.org/eol/), so we needed to upgrade it to [version 3](https://vuejs.org/).

Recently, with the advent of AI coding agents, the level of effort required for such tasks has been greatly reduced. However, in order to maintain ownership, control, and a thorough understanding of the codebase, and ensure high internal and functional quality, we couldn't simply throw the codebase to our agent and big-bang-prompt it: "Please upgrade this codebase to version 3 of Vue".

Instead, we took a deliberate, carefully planned approach where we owned the design decisions and relied on the agent for most of the grunt work and subsequent troubleshooting. In this blog post I'll explain how we did it.

## An overview of the project

First, let's describe the system. This application is a web-based B2B e-commerce site. The site allows customers to authenticate, browse a catalog of products, create a shopping cart, and place orders. In the catalog, they can filter products by category, price, and available inventory quantity. They can also filter them by name via a free-text search function. The system offers no capabilities for new user registration, as those come from an external system. It also does not have payment processing features. All captured orders are sent to an external system, where payment and fulfillment happen.

The frontend is a Vue 2 app hosted within a Ruby on Rails codebase. The code is managed, bundled, and served by the Rails framework itself and its supporting libraries. We will have to touch on that part a little bit, but for this article, we won't dive into too much detail where Rails is concerned. Our main topic here is the Vue 2 to 3 migration. Suffice it to say, this Vue migration was part of a bigger project of upgrading a Rails application from 5 to 8, and we would maintain this aspect of a Rails-managed frontend.

## The upgrade plan

Here are the general steps that we took to perform this migration:

1. Review and understand the code and the dependencies.
2. Develop a comprehensive test suite.
3. Design the new architecture and conventions.
4. Set up the new project.
5. Build the AI agent support files.
6. Transplant the frontend code files.
7. Final testing and troubleshooting.

We will describe each one in the following sections.

## 1. Review and understand the code and the dependencies

The first step for us is to review the codebase and gain a good understanding of it. Specifically, we need to know how the main features are implemented, the big building blocks, and which framework features and libraries are being used.

Once we had explored the functionality, which we've already discussed, we looked at the code and here's what we learned:

Overall, this was a pretty conventional Vue 2 app, all things considered. It implemented routing using [Vue Router](https://router.vuejs.org/), and made heavy use of global application state via [Vuex](https://vuex.vuejs.org/). It also used the Event Bus pattern and [Vue filters](https://v2.vuejs.org/v2/guide/filters.html), implemented using built-in Vue 2 features. All of these things had changed in Vue 3, so they would need to be upgraded or reimplemented using the available alternatives.

Having a Rails backend, this frontend also used the client side libraries for [Action Cable](https://guides.rubyonrails.org/action_cable_overview.html). Most notably, though, this backend did not implement a traditional [REST API](https://www.redhat.com/en/topics/api/what-is-a-rest-api). Instead, it used the [JSON API](https://jsonapi.org/) protocol, powered by [Graphiti](https://graphiti.dev/). So, in order to communicate with it, the frontend relied upon [Spraypaint](https://graphiti.dev/js/), a client side library for interacting with JSON API backends. Luckily, the library was still well maintained and compatible with the latest Vue.

Also, the frontend and backend lived together in the same codebase. This is usual for Rails apps. This meant that the Rails framework itself and supporting libraries took care of managing and bundling the frontend code. In other words, there were no direct calls to [Node.js](https://nodejs.org) commands for builds or anything else. It was all managed via the CLI offered by Rails and the related gems. In this case, this was a Rails 5 project, and the bundling was done by [Webpacker](https://github.com/rails/webpacker). This would also need to change, as the modern versions for Rails and Vue no longer support this, and have new recommended tools.

For visual styling, the app also used [Foundation for Sites](https://get.foundation/sites.html), [Font Awesome icons](https://fontawesome.com/icons) (via the [`Vue-Awesome` package](https://justineo.github.io/vue-awesome/demo/)), and several other smaller libraries for implementing GUI elements like carousels, site navigation breadcrumbs, notifications etc. Most of these had to be upgraded or replaced to work with Vue 3.

## 2. Develop a comprehensive test suite

Before moving forward, we had to create a safety net. Unfortunately, when we inherited the project, it was severely lacking in the automated tests department. For a migration such as this, having a good test suite was essential. For this frontend, we expected a lot of the inner workings of components to change, so we focused on higher-level end-to-end [Capybara](https://teamcapybara.github.io/capybara/) tests. Thankfully, in Rails, even back then, the framework came out of the box with support for such tests, so we didn't have to invest in setting them up; we only had to write them.

For this, we wrote a few test cases ourselves by hand to cover some of the basic scenarios like login or catalog browsing. Once that baseline was established, we wrote the rest using our AI agent. This method allowed the agent to have a clear example of code styling and patterns to follow closely. Our prompts ended up reading something like:

> Please write feature tests for the scenarios related to the catalog page. Follow the same patterns and style established by the other tests under `spec/features`. Focus on validating that visitors see key page content, exercising the search functionality and the category, price, quantity and name filters. Also validate that catalog items contain the expected rendered elements: a picture, the name and the price.

The important part here is being specific about what we want to test and how. We also did it in small increments, so that the amount of code generated at once was never overwhelming to review. We did this for each page and scenario and, without too much trouble and with minimal tweaking, eventually ended up with a reasonable test suite that carried us through the migration. This "first create an example for the agent to follow" strategy gave us good results without having to litter our project with agent skill files and whatnot.

```sh
spec/features/
├── authentication_spec.rb
├── categories_spec.rb
├── my_account_spec.rb
├── shop_catalog_spec.rb
└── shopping_cart_spec.rb
```

## 3. Design the new architecture and conventions

Within the code base, the frontend code was stored in a conventional Rails location: under `app/javascript`. Within it, we had the following structure:

```sh
app/javascript
├── app.vue
├── components
├── filters
├── layouts
├── models
├── packs
├── router
├── services
└── store
```

This is fine for the most part. But since we're modernizing this code base, we decided to change it. Taking inspiration from [Vite on Rails](https://vite-ruby.netlify.app/) and modern Vue setups like [Nuxt](https://nuxt.com/) and Vue's own `npm create vue@latest` default template, we arrived at the following structure under `app/frontend/`:

```sh
app/frontend
├── App.vue
├── assets
├── components
├── entrypoints
├── filters
├── layouts
├── models
├── router
├── services
├── stores
├── styles
└── views
```

Here's a breakdown of that directory structure:

- `App.vue`: This is our root Vue component. The one we pass to `createApp` in order to start up the application.
- `assets`: Here we store assets like images and icons.
- `components`: This is where we store the bulk of our reusable Vue components. These are all the bits and pieces like a button, a search box, a product catalog item template, a form for adding products to a cart, etc.
- `entrypoints`: The Vite entry points live here. These are the root files that Vite uses to construct the bundles. Since our app is a [SPA](https://en.wikipedia.org/wiki/Single-page_application), we have just one file here: `application.js`. This file initializes the Vue application and all its components and libraries.
- `filters`: This is where we store utility functions called [filters](https://v2.vuejs.org/v2/guide/filters.html). Their purpose is to format values in various ways, for presentation purposes.
- `layouts`: This directory will store special type of Vue components that define overall page layouts.
- `models`: Here we will put the Spraypaint models. These are used to call on the backend API to store and retrieve data. They also define the structure of the data that passes back and forth.
- `router`: This is where the application's frontend router lives. It maps URLs to particular components from the `views` directory.
- `services`: Here we put classes and functions that contain business logic that's worth separating from the Vue components.
- `stores`: We put the [Pinia](https://pinia.vuejs.org/) stores in this directory.
- `styles`: Here we put any CSS stylesheets that we might need.
- `views`: These are the Vue components that effectively represent the "pages" or "screens" that make up our site. The router links to these.

In addition to defining a new file structure, we also studied and took notes from the official migration guides from [Vue](https://v3-migration.vuejs.org/), [Vue Router](https://router.vuejs.org/guide/migration/) and [Pinia](https://pinia.vuejs.org/cookbook/migration-vuex.html). There were many changes to look out for. We also decided to adopt new naming conventions and file organization for components, and to adhere as much as possible to [Vue's style guide](https://vuejs.org/style-guide/).

We also identified the key third party libraries that were being used, investigated them and came up with strategies on how to replace them. Luckily, while most of them had been deprecated, they did have Vue 3 alternatives.

Also, on the Rails side, we wanted to modernize how the frontend code is managed and bundled. The original codebase used [Webpacker](https://github.com/rails/webpacker), and we decided to migrate that to [Vite](https://vite.dev/). In fact, we didn't have much of a choice, as Vite is the recommended toolchain for modern Vue projects, and Webpacker had long been deprecated.

Once we had learned all this, a set of design decisions, guidelines and steps for a migration plan began to emerge. In order to make effective use of AI agents, like we had planned to do, we had to put all that in writing. That would come a bit later though...

## 4. Set up the new project

Now we're ready to start building the new codebase. At this point we need to do a few things:

- Set up a new development environment.
- Set up a new Rails project.
- Set up frontend asset bundling with Vite.
- Install and configure Vue.js.

I won't go into too much detail on this here because I already wrote [another blog post about it](https://www.endpointdev.com/blog/2026/06/building-a-web-app-using-rails-8-and-vue-3-with-vite/).

But once we're done with that, we end up with a containerized development environment that has the latest versions of Ruby, Rails and Node.js, as well as the following files, among others:

```js
// vite.config.js
// This file configures Vite with the Vite Ruby and Vue plugins. This makes it
// so Vite integrates with Rails and can bundle Vue components.

import { defineConfig } from 'vite';
import RubyPlugin from 'vite-plugin-ruby';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [
    RubyPlugin(),
    vue()
  ],
});
```

```js
// app/frontend/entrypoints/application.js:
// This is our main frontend application entry point. The file that Vite's
// bundling process takes as the starting point to build our entire frontend
// app. It configures and initializes our Vue SPA.

import { createApp } from 'vue';
import App from '../App.vue';

const app = createApp(App);
// Finds an HTML element with id "app" and mounts the Vue app in it.
app.mount('#app');
```

```html
<!-- app/frontend/App.vue -->
<!-- A basic starter Vue component. -->

<script>
export default {
  data() {
    return {
      message: 'Hello Rails, Vue and Vite!'
    }
  }
}
</script>

<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<style scoped>
h1 {
  background: linear-gradient(to right, red, green, yellow);
}
</style>
```

And we also have to add that `#app` mounting point somewhere in our homepage, so that the call to `app.mount('#app');` has somewhere to put the app. For this Rails app, that would be the `app/views/home/index.html.erb` view template:

```html
<!-- app/views/home/index.html.erb -->

<div id="app"></div>
```

We also make sure that we have configured our application's backend routing so that the root path points to this page:

```rb
# config/routes.rb

Rails.application.routes.draw do
  # ...

  root to: "home#index"

  # ...
end
```

Now we are able to see our brand new empty Vue 3 frontend app running when we start the dev servers for the Rails backend and the Vite frontend:

```sh
bin/rails server

bin/vite dev
```

At this point we again employ the "first create an example for the agent to follow" strategy that we used for the tests. We begin installing and configuring some of the core libraries, and porting over some of the core components from the old codebase into the new one. We leveraged the official docs, and agents, for this, but we took a more hands-on approach, in order to establish solid patterns and styling for the rest of the work.

We installed and configured the following: Vue and Rails supporting libraries:

- [Pinia](https://pinia.vuejs.org/), the replacement of Vuex, which the frontend uses for managing global application state. Pinia is the recommended state management library for Vue 3.
- [Vue Router](https://router.vuejs.org/), which Vue uses for frontend routing.
- [Action Cable](https://www.npmjs.com/package/actioncable), which is Rails' [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)-powered real-time framework. It has a frontend component.
- [Mitt](https://github.com/developit/mitt), which we used to implement the Event Bus pattern. The old code used raw Vue instances for that, but this is no longer supported in Vue 3.
- [Spraypaint](https://graphiti.dev/js/), the library for interacting with the backend Graphiti JSON API.
- [Foundation for Sites](https://get.foundation/sites.html) and [Font Awesome icons](https://fontawesome.com/icons), for visual styling.

These are the main ones. As mentioned before, this frontend used other libraries for specific GUI widgets like carousels, and notifications. Most of these need to be replaced for Vue 3. We would leave that for later, to figure them out at the time of porting the parts of the application that need them.

So at this stage, we have an `application.js` file that looks like this:

```js
// app/frontend/entrypoints/application.js:

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from '../router';
import App from '../App.vue';

import ActionCableVue from 'actioncable-vue';

const actionCableVueOptions = {
  debug: true,
  debugLevel: 'error',
  connectionUrl: `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/cable`,
  connectImmediately: true,
  unsubscribeOnUnmount: true,
};

import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { far } from '@fortawesome/free-regular-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';
library.add(fas, far, fab);

import 'foundation-sites/dist/css/foundation.css';

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(ActionCableVue, actionCableVueOptions);

app.mount('#app');
```

And we also wrote a basic router that only knows the homepage:

```js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
  ],
});

export default router;
```

And that `HomeView.vue` component is precisely the first one that we ported manually as part of establishing our initial foundation. At this point we didn't migrate the entire homepage, but just enough to have a running shell, test our design decisions and assumptions, and establish the patterns and conventions of the project moving forward. We ended up porting the main layout, the header, and the containers for sidebars and main page content, as well as the overall visual styling. We began applying our new naming, structural and code styling conventions.

At this point we had a running application with exemplary code implementing the foundation. As far as the code was concerned, the stage was set for bringing in more heavy usage of AI agents. Now we needed to write some documentation to guide them.

## 5. Build the AI agent support files

Like humans, agents can really benefit from clear, well articulated and concise documentation. To that end, we created these two documents:

- A `MIGRATION_GUIDE.md` file that captured all we had learned during our previous investigations, all the design decisions that we made, and what we wanted the finalized codebase to look like.
- A `MIGRATION_PLAN.md` file that broke down the migration process into a checklist with discrete, manageable steps. The overall idea was to migrate the frontend files vertically, component by component, feature by feature, page by page.

AI agents were very helpful for creating these files, but we carefully reviewed and adjusted several aspects. We captured all of our learnings from the previous sections, designed a series of prompts to generate and adjust these documents, and then further refined them until we were satisfied with the result. You can see [the initial prompt we used to create the guide here](https://gist.github.com/megakevin/ae4c6964512b32124828d772d37070f6). And here is [the initial prompt we used to generate the plan](https://gist.github.com/megakevin/6d3f00daa6acd6553d96ea2768e61664). And these are the final [guide](https://gist.github.com/megakevin/ba3df673013f555242c66f0c34ffdb83) and [plan](https://gist.github.com/megakevin/ec17883e8df0f510a59a6e80aa337431) documents.

That's quite a lot of text, but I'm not asking you to read all of it. I only include them to illustrate the depth and breadth of these files, and what kinds of things got included. The key here was to put in as much detail as possible to clearly explain our intent, in both the prompts and the documents, in order to eliminate any guesswork on the part of the AI agent that would eventually be helping execute this plan and follow these guidelines. The objective was for the resulting code to look and feel just as if we had written everything ourselves by hand. We had to maintain control, intimate understanding and ownership.

## 6. Transplant the frontend code files

Now, when it comes to the actual work of porting the code, all we have to do is execute the plan, while respecting the guidelines. We don't just big-bang-prompt the AI agent and let it loose on the code base, though. Instead we instruct it to execute the plan step by step, always following the guidelines, and to always pause after it's done with a step so that we can manually review, test and give it the go ahead to continue to the next step. Because the plan's steps are discrete and manageable, every increment is reasonably sized, so we can review and test without being overwhelmed, maintaining control and ownership.

> Ok good. It's time to get started executing the plan. I've already completed steps 1.1 through 1.4. Please review.

> Ok yes, please mark the completed steps. Continue executing the plan. Do it in small enough steps so that I can review every step of the way.

With this approach, we leverage the tried and true practices of iterative and incremental software engineering, augment them with AI, and execute a process that accelerates our work, removes a considerable part of the tedium, and ensures a quality product at the end of it all.

When problems occur, the AI agent is invaluable for troubleshooting as well. The fact that the ecosystem of frontend JavaScript and Vue is built mostly on top of open source technologies is a great boon. The solutions to most configuration or API misuse issues become apparent without having to spend hours sifting through documents. The agent can read library code and documentation much much faster than us.

Another thing to note is that we copied over the entire old codebase into a directory within our new project. We called it `old_codebase` and pointed the agent to it to use as a reference. That just makes it easier as everything is in one single directory structure.

Something that was also useful was to give permissions to the agent to run the test suite, run the app, and write and run its own ad-hoc Playwright tests. These are great tools for the agent to use while it's doing its work because they give it more autonomy. That way it can accomplish more on its own without us having to intervene as much. We can focus on coming in for review and test at the end of each step. The harness we used for this was GitHub Copilot, so these tools come out of the box and we just have to give our consent for the agent to use them. Other harnesses specialized in programming would behave similarly.

Something that we also learned is that there are no free lunches. Even with the meticulous guide, plan, and process we had devised, the agent still made mistakes, or came up with solutions that we didn't like, or drifted from the established design and conventions, or ran into issues that took deeper troubleshooting. We also had to go back and refine the guide and the plan a couple of times. Still, the help was immense. This just shows that indeed, we do need to keep a close eye on the work as it progresses, and review and test diligently.

## 7. Final testing and troubleshooting

As we neared the end of the project, we moved our Capybara tests from the old codebase into the new one. We had to tweak the configuration to account for the differences between Rails versions. But all in all, they translated pretty cleanly and passed without too many complications.

~

Truly, the frontier AI models have advanced incredibly during the last couple of years, so much so that they can handle complex tasks. We found that they truly shine when meticulously directed to handle well specified projects with clear success criteria, such as a Vue 2 to 3 migration. This is no groundbreaking work; many of these types of projects have been completed by practitioners throughout the years, and many more will still have to be done. But each project is different from the others because each application is different, so it still needs to be done carefully. Luckily for us, with the help of AI, a big portion of what was tedious hard work in the past can now be successfully delegated to the computer.
