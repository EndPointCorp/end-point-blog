---
author: Kürşat Kutlu Aydemir
title: Our Vue Storefront “Proof of Concept” Experience
github_issue_number: 1654
tags:
- vue
- javascript
- ecommerce
- interchange
- magento
date: 2020-08-10
---

Recently we experimented internally with integrating [Vue Storefront](https://www.vuestorefront.io/) and [Magento](https://business.adobe.com/products/magento/open-source.html) 2.3. Vue Storefront is an open source Progressive Web App (PWA) that aims to work with many ecommerce platforms.

What initially piqued our interest was the possibility of integrating Vue Storefront with the venerable ecommerce back-end platform [Interchange](https://www.interchangecommerce.org/i/dev), which many of our clients use. Vue Storefront’s promise of ease of integration with any ecommerce backend made us curious to see whether it would make a good modern front-end for Interchange.

Since Vue Storefront seems to be most commonly used with Magento, we decided to start our experiment with a standard Vue Storefront/​Magento 2.3 proof-of-concept integration. 

### PoC of Vue Storefront/​Magento 2.3

OK, to be honest, at the beginning we blindly expected that Vue Storefront would be a copy/​paste front-end template solution that would fairly easily be made to work with its standard integration to a Magento backend. Sadly, this was not the case for us.

Before beginning our journey here, to summarize the Vue Storefront integration with Magento let’s have a look at this diagram to see what components are included:

![VS Architecture](/blog/2020/08/vue-storefront-magento-integration/GitHub-Architecture-VS.png)

*Figure 1*

At first, we wanted to see how all these components can be installed and run on a single server with modest resources.

I walked through the [Vue Storefront documentation](https://docs.vuestorefront.io/guide/) and a few [blog posts](https://medium.com/the-vue-storefront-journal/proof-of-concept-how-to-run-pwa-for-magento-in-a-week-c0fa04fadd3d) to figure out Vue Storefront and Magento integration.

### Preparing the Environment

I downloaded and installed the following:

* OS: CentOS Linux 7 (64-bit)
* PHP 7.2.26
* Magento 2.3 with sample data
* Elasticsearch 5.6
* Redis
* Docker
* Vue Storefront API
* Vue Storefront
* mage2vuestorefront bridge

Installation of those components is fairly easy. We started our virtual server with 4 GB of memory, which we thought should be plenty for a toy setup.

### Indexing Elasticsearch with mage2vuestorefront

PHP and Magento 2.3 had a series of memory usage issues. While running the mage2vuestorefront indexer Magento used most of the memory and caused Elasticsearch to go down each time I tried to index Elasticsearch. Then I configured PHP and Apache httpd server to use a very modest amount memory and made Magento 2.3 work on this server without making it crash due to unavailable memory but the performance became a nightmare on the PHP & Magento 2.3 side. mage2vuestorefront ran without issue, but very slowly.

I am not very familiar with the Magento 2 API, but while indexing Elasticsearch with mage2vuestorefront it makes several individual API calls. Especially if you have several products in Magento 2, mage2vuestorefront calls the Magento API for almost all products. Due to PHP and Magento’s high memory usage available memory might become a problem during indexing.

The Vue Storefront developers [explain](https://docs.vuestorefront.io/guide/cookbook/elastic.html#_0-introduction) a big reason why they chose Elasticsearch as one of the essential components of this integration:

> *Vue Storefront* defines itself backend-agnostic PWA e-commerce solution where *Vue Storefront* is a storefront as the name dictates, and *Elasticsearch* works as a datastore for *catalog* and its sibling data such as *taxrule*, *products* and so on.

I am unsure if the backend-agnostic approach even really applies to the suggested implementation of Vue Storefront with Magento 2, or if does apply with significant headaches. I’ll detail my concerns about this later.

### Viewing the Vue Storefront Application

The responsive and offline supportive design of Vue Storefront is elegant. It uses Elasticsearch via vue-storefront-api as its indexing search engine to provide a seamless user experience. Although the overall integration and the produced data structure looks complex there are only a few catalog data stores that need to be indexed on Elasticsearch. Also, since this is an ecommerce integration, you can expect that only products and product-related data are going to be available in such an integration.

In the Vue Storefront and Vue Storefront API app home directories (`vue-storefront/` and `vue-storefront-api/`) I ran `npm start` to start the Node.js apps, then navigated to the Vue Storefront homepage to view its default template:

![](/blog/2020/08/vue-storefront-magento-integration/storefront_temphost_net.jpg)

*Figure 2*

There is a hamburger menu in the top-left which opens the categories menu of Vue Storefront:

![](/blog/2020/08/vue-storefront-magento-integration/storefronttemphostnet_cats_menu.jpg)

*Figure 3*

As I mentioned, the data being viewed is relatively simple according to the count of the catalog types (essentially Products, Categories, Attributes, and Tax Rules) which are already categorized and these are a bunch of specific sets of data.

By searching through the categories Women &gt; Tops &gt; Jackets, the search output list is shown by Vue Storefront:

![](/blog/2020/08/vue-storefront-magento-integration/storefronttemphostnet_cats_search.jpg)

*Figure 4*

### Designing a New Approach for Interchange

When exploring the features and components of Vue Storefront we discussed how we can adapt Interchange to use Vue Storefront. We ended up with two main options:

1. Keep the same approach of Vue Storefront’s current integration with Magento and other ecommerce backends using Elasticsearch and vue-storefront-api as the backend gateways
2. Remove the Elasticsearch and vue-storefront-api dependencies and create a new API in Interchange producing similar API outputs to the ones vue-storefront-api & Elasticsearch are creating. I also found a similar approach where they integrated SAP Hybris with Vue Storefront. I thought that this way would fit our intention.

#### Inspired By A Similar Approach of Vue Storefront + SAP Commerce

[Vue Storefront + SAP Commerce: Open-source PWA Storefront Integration (+DEMO)](https://hybrismart.com/2019/02/13/vue-storefront-sap-commerce-open-source-pwa-storefront-integration-demo/)

This article discusses several approaches, including [Vue Storefront developers’ boilerplate integration](https://github.com/DivanteLtd/storefront-integration-sdk) and their custom solutions. In the following table they show different options and comments on their resolutions.

![](/blog/2020/08/vue-storefront-magento-integration/t1-1.png)

*Figure 5*

As you can see in Figure 5, they decided to go with the 4th option as their most suitable and least problematic solution. Here is their statement of why:

*After some analysis, we have come to believe that using custom middleware only for a bunch of simple requests is an additional burden and thick layer of complexity. We decided to get rid of it as well.*

*So, option #4 turned out to be the best choice. For the option #4, we need to parse Magento and Elasticsearch APIs and generate the compatible responses.*

Here is how their solution looks according to option #4:

![](/blog/2020/08/vue-storefront-magento-integration/p2.png)

*Figure 6*

Using this approach, they decided to remove the Elasticsearch and Vue Storefront API components from the Vue Storefront boilerplate integration and developed their SAP Commerce custom Vue Storefront API to produce responses similar to the responses taken from Elasticsearch through Vue Storefront API to pretend that Vue Storefront is taking its responses from Elasticsearch API + Magento API.

We decided to discard Elasticsearch when integrating Interchange with Vue Storefront for simplicity, and to cut down on the cost such additional search solutions create.

After our discussions, I was inspired by this SAP Commerce + Vue Storefront integration demo. We finally decided to move forward with creating an Interchange API to produce the similar responses to those from the Elasticsearch & Magento APIs, so we could make the Interchange API pretend to be the Elasticsearch API + Magento API.

We need to mention the Magento 2 API, or at least the Magento 2 data structure, because the Vue Storefront API and Vue Storefront boilerplate code is heavily designed to be taking ecommerce data (Products, Categories, Product Attributes, Tax Rules etc.) almost identical to the Magento API’s provided data.

So our Interchange + Vue Storefront integration looks like this:

![](/blog/2020/08/vue-storefront-magento-integration/Vsinterchange_arch.png)

*Figure 7*

Compare Figure 1 with Figure 7 to see the difference between this approach and Vue Storefront’s suggested solution.

#### Interchange API Prototype Design

In order to achieve the API prototyping for our Interchange/​Vue Storefront integration, I cloned vue-storefront and vue-storefront-api, which I had previously integrated with Magento 2.3, into a new user, keeping all settings the same. This cloned Vue Storefront application started initially with the same configuration as vue-storefront-api and Elasticsearch were not excluded yet. So I decided to replace the vue-storefront-api endpoints that vue-storefront is calling with endpoints from the new Interchange API.

As the default SAP Commerce/​Vue Storefront integration suggests, I walked through the outputs of search results in “product”, “category”, and “attributes”. Product data JSON output has some universal attributes like name or title, description, or price, but it also has some custom product attributes adapted from the Magento 2 API (specifically, the data structure of Magento is applied).

At this point I started questioning if Vue Storefront is not really platform agnostic, or if it is, but with some headaches. The next section will detail these headaches but to summarize, adapting the data structure of new ecommerce backends to Vue Storefront is a real pain. It forces you to use its data structure since that’s a part of core development, and they rely mainly on Elasticsearch, and I guess because of that the developers of Vue Storefront believe that Elasticsearch is an essential part of this “agnostic” approach. Refer to [Getting data from Elasticsearch](https://docs.vuestorefront.io/guide/data/elastic-queries.html#getting-data-from-elasticsearch) for custom implementations using the [core Elasticsearch lib](https://github.com/vuestorefront/vue-storefront/tree/master/core/lib).

Anyway, I moved on and produced product and product categories outputs that Vue Storefront expects as the search results at the homepage and the search box output results.

Documentation is another pain. This is discussed further in the next section, but briefly, it’s hard to say that you could clearly pick the data structure that all kind of output results from the documentation. You need to dig into the TypeScript code, and the exact search output result is what is actually being expected.

One conflict was that the identifiers are required to be numeric, not strings. If your ecommerce data structure doesn’t provide its identifiers as numbers you’ll need to alter and add a new numeric unique identifier along with the existing one, which is what I did.

Product attributes also need to be adapted to Vue Storefront (really to Magento’s data structure). The attribute names, attribute lists, attributes’ assigned values, and categories attached to the products and configurable child products all come along with the product list on a search output. If your ecommerce data is not structured similarly to Magento’s data structure, you need to dig and restructure even for minimal changes like product attributes and configurable child products. For example, if your data structure doesn’t allow configurable child products then you can probably only provide each option (such as product color or size options) as a new product, which will be a real pain.

Most of Vue Storefront’s app endpoints are defined in `config/default.json` which is the default config on a new install. On the other hand, the ecommerce catalog data (which is indexed in Elasticsearch) is available through the Elasticsearch implementation which is by default defined in `lib/search/adapter/api/searchAdapter.ts`. In my case I needed to alter this implementation, which is generating the Elasticsearch (actually the Vue Storefront API) endpoints dynamically by looking up the related catalog index (product, category, attributes, taxes, etc.), and change the Elasticsearch definition in the Vue Storefront config file to the new Interchange API, adapted to emulate the Vue Storefront API and Elasticsearch:

```json
...
  "elasticsearch": {
    "httpAuth": "",
    "host": "/api/catalog",
    "index": "vue_storefront_catalog",
...
```

I needed to set the Interchange API URL to the host property and not necessarily set an API-defining URL sub-path name to the index property above. This way our API would pretend to be the Elasticsearch endpoint as long as it can generate the JSON output that Vue Storefront expects.

These configuration changes generally satisfied Vue Storefront’s expectations.

### Common and Exceptional Issues

Many concerns and challenges are discussed in [this article on Vue Storefront + SAP Commerce integration](https://hybrismart.com/2019/02/13/vue-storefront-sap-commerce-open-source-pwa-storefront-integration-demo/#h.4jhhd7ba1u4i) which I mentioned earlier.

A review of some issues I detailed earlier:

- Required numeric unique IDs for all catalogs (products, categories, etc.)
- Poor documentation
- Catalog data structure is managed on the Vue Storefront side, heavily relying on its own data types and models. Your backend may need to be adapted to meet Vue Storefront’s expectations, even if you are using Elasticsearch.
- A structure which is constantly being reorganized, creating a big maintenance concern.

### Conclusion

Despite my concerns, I thought we could still implement our Interchange API with a front-end framework, but I hadn’t asked the question: Is it reusable enough to mantain? Each of our clients would have different UI and UX expectations. One UI template model could never be enough, which would mean continuous front-end template design and enough maintenance to match the operational cost of existing Interchange front-end solutions. Adapting existing data to Vue Storefront’s new data model would bring more costs along with it.

While Vue Storefront’s offline working model is well designed, for the purpose of integrating with a non-Magento backend, this is overshadowed by its many issues. You would be better off looking elsewhere for a more modular, truly platform-agnostic, easier-maintained, component- and data model-independent front-end.
