---
author: Kirk Harr
gh_issue_number: 979
tags: ecommerce, drupal, cms
title: Drupal Commerce for Fun and Profit
---

Drupal has for years been known as open source content management system (CMS) for creating easy content-driven websites for any topic. In addition to the CMS, there are a whole host of tools built upon this foundation to extend the features using modules. One module in particular I worked with recently for a client was Drupal Commerce, which helps to augment the CMS with an eCommerce platform.

Within Drupal for normal content items, you would create distinct articles, which have a predefined model of fields that would reflect the different aspects of an article, author, title, tags, etc. While Drupal Commerce uses these same functions, it will also give you the capability to also define SKUs, product categories, and rules and procedures to be carried when adding a particular item to your cart. In much the same way as articles are published to the Drupal taxonomy to allow users to browse through the articles, product categories, and individual products are published, and allow the administrator to customize the layout of how those products would display.

**Getting Started with Drupal Commerce**

One tool that is extremely helpful on getting a Drupal Commerce setup up for yourself is using the Drupal [Commerce Kickstart](https://drupal.org/project/commerce_kickstart).

This tool, which is maintained by a group of Drupal consultants/enthusiasts who created an embedded install of Drupal with some modules installed and configured to get both a working Drupal install and a copy of the Commerce plugin as well. The installation is quite simple, you extract the install archive into your web server document root, and then you follow an install procedure to configure your database, the name of the site, and any other information needed.

Once the install is complete, you will have a copy of Drupal Commerce installed, and will have a basic product display model on the front page with a few example products available. From here the next steps would be to define your own products and categories and input those model objects.

**Creating Products**

Internally to Drupal, when referring to articles, there are distinct units for each article and category known as nodes, and a hierarchical taxonomy that is defined by the administrator for how these items fit together. Within Drupal Commerce there is a similar designation, but the items are known as 'entities' and could refer to a whole host of possible objects in Drupal Commerce. Here is a chart to show the relationships:

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2014/05/06/drupal-commerce-for-fun-and-profit/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="233" src="/blog/2014/05/06/drupal-commerce-for-fun-and-profit/image-0.png" width="320"/></a></div>

These "entities" extend the original concept of a Drupal node to allow for different products, attributes of products and customers and their attributes. The product reference is a pointer object that allows a product to be added to a node article to be displayed on the front end of the site. This reference refers back to the products that were added, and if those product objects are updated, the content to display those products will stay static, but will be dynamically updated. In this way, the content templates for display products is abstracted from the actual product SKUs themselves.

When defining each product there are a number of relationships that are created which relate to the possible categories that a product would live in, as well as fields and properties implied by that product. Here is a visual representation of these relationships:

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2014/05/06/drupal-commerce-for-fun-and-profit/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="281" src="/blog/2014/05/06/drupal-commerce-for-fun-and-profit/image-1.png" width="320"/></a></div>

Every product entity would by definition be part of the "Product" bundle, and also would fall into a custom bundle for the "T-shirt" product category. In this way, you can create as complex or as simple of relationships between products and categories to reflect the actual state of the business using the tool, and will allow for the product definitions to remain in place, even if you were to redefine the layout for those products to display.

**Conclusions**

Drupal Commerce is a hulking tool, with a number of learning curves and a bit of terminology to get straight, but once in place and working will give a user a very robust commerce platform. Any Drupal developer familiar with creating custom taxonomies for article display and categorization will be able to use the same skills to create a slick eCommerce site.
