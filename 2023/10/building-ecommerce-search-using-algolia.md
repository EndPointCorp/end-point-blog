---
author: Dylan Wooters
title: 'Building Ecommerce Search Using Algolia'
tags:
- search
- vue
- typescript
date: 2023-10-12
github_issue_number: 2015
featured:
  image_url: /blog/2023/10/building-ecommerce-search-using-algolia/east-bay-hills.webp
description: This post shows readers how to add intelligent search to their website using the search-as-a-service offering Algolia.
---

![Looking east from the top of the Berkeley hills over the Briones Reservoir. Rolling hills are seen in the distance with the sun setting to the west.](/blog/2023/10/building-ecommerce-search-using-algolia/east-bay-hills.webp)

<!-- Photo by Dylan Wooters, 2020 -->

A common request that developers receive when embarking on a new website project is for the website to have "Google-like search." For many years, this meant writing custom code to replicate the intelligent and user-friendly aspects of Google search, which was no easy feat. However, now we have many search-as-a-service offerings that do the hard work for us and make this process much easier.

In this blog post, we’ll dive into one of these search-as-a-service platforms, [Algolia](https://www.algolia.com/). We recently worked on an ecommerce website and used Algolia in an interesting way, both as a search engine and as a lightweight backend database to hold product data managed in Salesforce. Algolia worked beautifully, offering users fast and accurate search results, and also allowing us to launch the site within a relatively short time frame.

We will look at how to load Algolia with data, configure search options, and connect the search to the frontend using Algolia’s Vue library.

### Loading the index with data

To start using Algolia’s search, you need to load up an index with data. You have the option of manually uploading a JSON file, or using Algolia’s API to programmatically load records. For our backend, we chose to use Algolia's [JavaScript API client](https://www.npmjs.com/package/algoliasearch) in some lightweight Typescript scripts that are triggered by cron. These scripts allowed us to sync inventory data between Salesforce and the index in Algolia.

Using the Algolia JavaScript client is quite simple. Regardless of where your data comes from—be it in a database, a platform like Salesforce, or elsewhere—once it is in JSON format, you can load it into Algolia with a few lines of code:

```javascript
import * as algolia from "algoliasearch";

const products = [{
    name: "Fender F-5 Acoustic",
    make: "Fender",
    model: "F-5",
    category: "Guitars",
    status: "Used",
    objectID: "Fender-001"
  }, {
    name: "Fender Player Jaguar",
    make: "Fender",
    model: "Jaguar (Player)",
    category: "Guitars",
    status: "New",
    objectID: "Fender-002"
  }];


const index = algolia.default(process.env.ALGOLIA_APP_ID, process.env.ALGOLIA_API_KEY).initIndex("store_products");
await index.saveObjects(products);
```

Note the `objectID` property, which is used by Algolia as a primary key. If the `objectID` does not exist, a new record will be created. If it does exist, the record will be updated. This makes it easy to run a data sync process using a single `saveObjects` command, without having to worry about differentiating between create and update operations.

### Configuring the index

Once you have your index loaded, you’ll want to configure it. Algolia does a good job of walking you through this process using a built-in tutorial when you first load your index. Basically, you will be selecting the [searchable properties/​attributes](https://www.algolia.com/doc/guides/sending-and-managing-data/prepare-your-data/how-to/setting-searchable-attributes/) from your JSON data, setting how results are ranked and sorted, and adjusting more advanced aspects of search like typo tolerance, stop words, etc.

An important feature we utilized on our recent project is [faceting](https://www.algolia.com/doc/guides/managing-results/refine-results/faceting/). Faceting allows users to easily drill down and refine search by categories, and is also easy to develop using the handy frontend libraries that Algolia provides (more on that in the next section). This feature is powerful and can be used to both refine search and drive homepage category/​subcategory links. When you configure your index, you can select which attributes of your data should be used for faceting.

### Setting up search on the frontend

We used [Nuxt](https://nuxt.com/) to build the frontend of the website, and we leveraged Algolia’s [Vue InstantSearch](https://www.algolia.com/doc/guides/building-search-ui/what-is-instantsearch/vue/) library for the UI. This library really speeds along development, as it wraps all of the search-related functionality in simple widgets, providing the search bar, results, refinements, filtering, and more.

The [`ais-instant-search`](https://www.algolia.com/doc/api-reference/widgets/instantsearch/vue/) widget is the parent widget. It serves the search state to its children, which allows you to show the search bar, search hits, hierarchical menus, etc. Here is a simple example of the `ais-instant-search` widget with a search bar and hits (pulled directly from [Algolia’s Vue docs](https://www.algolia.com/doc/guides/building-search-ui/getting-started/vue/)):

```html
<template>
  <ais-instant-search :search-client="searchClient" index-name="demo_ecommerce">
    <ais-search-box />
    <ais-hits>
      <template v-slot:item="{ item }">
        <h2>{{ item.name }}</h2>
      </template>
    </ais-hits>
  </ais-instant-search>
</template>


<script>
import algoliasearch from 'algoliasearch/lite';
import 'instantsearch.css/themes/algolia-min.css';


export default {
  data() {
    return {
      searchClient: algoliasearch(
        '[Your app ID]',
        '[Your API key]'
      ),
    };
  },
};
</script>


<style>
body {
  font-family: sans-serif;
  padding: 1em;
}
</style>
```

### Using faceting for search refinement and filtering

I mentioned faceting above when discussing how to configure your index. Once you have selected the attributes in your JSON data that can be used for faceting (e.g., category, subcategory), you can feed those attributes to the [`ais-hierarchical-menu`](https://www.algolia.com/doc/api-reference/widgets/hierarchical-menu/vue/) widget for display on the frontend.

Here is a bit of sample code from the website we built, which offers expandable category refinement via `ais-hierarchical-menu`.

```html
<div class="sidebar-segment">
  <p class="sidebar-segment-title">Category</p>
  <ais-hierarchical-menu
    :limit="100"
    :attributes="categoryAttrs"
    :sort-by="hierarchicalMenuSort"
  >
    <div slot-scope="{ items, refine, createURL }">
      <hierarchical-menu-list
        :items="items"
        :refine="refine"
        :create-url="createURL"
      />
    </div>
  </ais-hierarchical-menu>
</div>
```

Above, we are using the `limit` property to set the maximum number of items to 100. The `attributes` property, which targets the JSON attributes in your index data that represent your categories, is set to the following:

```javascript
categoryAttrs: ['categories.lvl0', 'categories.lvl1', 'categories.lvl2'],
```

These represent the three levels of categories in our data (zero-based), and are used to build the hierarchical menu.

Finally, the `sort-by` attribute points to a simple function that uses the JavaScript `localeCompare` method to provide alphanumeric sorting:

```javascript
function hierarchicalMenuSort(a, b) {
  return a.name.localeCompare(b.name, undefined, {
    numeric: true,
    sensitivity: 'base',
  })
}
```

### Wrapping up: seeing Algolia in action

If you’d like to see Algolia in action on the site that we built, head over to [eiffeltrading.com](https://www.eiffeltrading.com/). If you search the site, you’ll see autocomplete, fast results (thanks to both Algolia and Nuxt), and other aspects of good search that we have all come to expect from modern ecommerce sites.

Next time you are faced with a build involving full-text search, consider search-as-a-service offerings like Algolia. They could save you time and headaches over rolling your own search functionality. Sometimes it’s good to let others do the hard work!

Have questions or feedback on the topic? Let us know in the comments section below.
