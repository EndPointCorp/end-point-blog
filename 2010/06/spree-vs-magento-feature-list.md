---
author: Steph Skardal
title: 'Spree vs Magento: A Feature List Comparison'
github_issue_number: 314
tags:
- ecommerce
- ruby
- rails
- spree
- cms
- magento
date: 2010-06-07
---

Note: This article was written in June of 2010. Since then, there have been several updates to Spree. Check out the current [Official Spree Extensions](https://web.archive.org/web/20111027123306/http://www.spreecommerce.com/extensions?is_official=true) or review a list of all the [Spree Extensions](https://web.archive.org/web/20111010012147/http://spreecommerce.com/extensions).

This week, a client asked me for a list of Spree features both in the core and in available extensions. I decided that this might be a good time to look through Spree and provide a comprehensive look at features included in Spree core and extensions and use Magento as a basis for comparison. I’ve divided these features into meaningful broader groups that will hopefully ease the pain of comprehending an extremely long list :) Note that the Magento feature list is based on their documentation. Also note that the Spree features listed here are based on recent 0.10.* releases of Spree.

### Features on a Single Product or Group of Product

<table cellpadding="2" cellspacing="0" width="100%"><tbody>
<tr class="alt header"><td width="60%">Feature</td><td width="20%">Spree</td><td>Magento</td></tr>
<tr><td>Product reviews and/or ratings</td><td>Y, extension</td><td>Y</td></tr>
<tr class="alt"><td>Product qna</td><td>N</td><td>N</td></tr>
<tr><td>Product seo (url, title, meta data control)</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Advanced/flexible taxonomy</td><td>Y, core</td><td>Y</td></tr>
<tr><td>Seo for taxonomy pages</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Configurable product search</td><td>Y, core</td><td>Y</td></tr>
<tr><td>Bundled products for discount</td><td>Y, extension</td><td>Y</td></tr>
<tr class="alt"><td>Recently viewed products</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Soft product support/downloads</td><td>Y, extension</td><td>Y, I think so</td></tr>
<tr class="alt"><td>Product comparison</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Upsell</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Cross sell</td><td>N</td><td>Y</td></tr>
<tr><td>Related items</td><td>Y, extension</td><td>Y</td></tr>
<tr class="alt"><td>RSS feed of products</td><td>N</td><td>Y</td></tr>
<tr><td>Multiple images per product</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Product option selection (variants)</td><td>Y, core</td><td>Y</td></tr>
<tr><td>Wishlist</td><td>Y, extension</td><td>Y</td></tr>
<tr class="alt"><td>Send product email to friend</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Product tagging / search by tagging</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Breadcrumbs</td><td>Y, core</td><td>Y</td></tr></tbody></table>

### CMS Features

<table cellpadding="2" cellspacing="0" width="100%"><tbody>
<tr class="alt header"><td width="60%">Features</td><td width="20%">Spree</td><td>Magento</td></tr>
<tr><td>Blogging functionality</td><td>Y, extension</td><td>Y *extension</td></tr>
<tr class="alt"><td>Static page management</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Media management</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Contact us form</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Polls</td><td>Y, extension</td><td>Y</td></tr></tbody></table>

### Checkout Support

<table cellpadding="2" cellspacing="0" width="100%"><tbody>
<tr class="alt header"><td width="60%">Feature</td><td width="20%">Spree</td><td>Magento</td></tr>
<tr><td>One page checkout</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Guest checkout</td><td>Y, core</td><td>Y</td></tr>
<tr><td>SSL Support</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Discounts</td><td>Y, core</td><td>Y</td></tr>
<tr><td>Gift Certificates</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Saved Shopping Cart</td><td>N</td><td>Y</td></tr>
<tr><td>Saved Addresses</td><td>Y, extension</td><td>Y</td></tr></tbody></table>

### Shipping Support

<table cellpadding="2" cellspacing="0" width="100%"><tbody>
<tr class="alt header"><td width="60%">Feature</td><td width="20%">Spree</td><td>Magento</td></tr>
<tr><td>Real time rate lookup (UPS, USPS, Fedex)</td><td>Y, extension</td><td>Y</td></tr>
<tr class="alt"><td>Order tracking</td><td>N</td><td>Y</td></tr>
<tr><td>Multiple shipments per order</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Complex rate lookup</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Free shipping</td><td>Y, extension</td><td>Y</td></tr></tbody></table>

### Payment Support

<table cellpadding="2" cellspacing="0" width="100%"><tbody>
<tr class="alt header"><td width="60%">Feature</td><td width="20%">Spree</td><td>Magento</td></tr>
<tr><td>Multiple Payment Gateways</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Authorize.net</td><td>Y, core</td><td>Y</td></tr>
<tr><td>Authorize and capture versus authorize only</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Google Checkout</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Paypal Express</td><td>Y, extension</td><td>Y</td></tr></tbody></table>

### Admin Features

<table cellpadding="2" cellspacing="0" width="100%"><tbody>
<tr class="alt header"><td width="60%">Feature</td><td width="20%">Spree</td><td>Magento</td></tr>
<tr><td>Sales reporting</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Sales Management Tools</td><td>N</td><td>Y</td></tr>
<tr><td>Inventory management</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Purchase order management</td><td>N</td><td>Y</td></tr>
<tr><td>Multi-tier pricing for quantity discounts</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Landing page tool</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Batch import and export of products</td><td>Y, extension</td><td>Y</td></tr>
<tr class="alt"><td>Multiple Sales reports</td><td>Y, core</td><td>Y</td></tr>
<tr><td>Order fulfillment</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Tax Rate Management</td><td>Y, core</td><td>Y</td></tr></tbody></table>

### User Account Features

<table cellpadding="2" cellspacing="0" width="100%"><tbody>
<tr class="alt header"><td width="60%">Feature</td><td width="20%">Spree</td><td>Magento</td></tr>
<tr><td>User addresses</td><td>Y, extension</td><td>Y</td></tr>
<tr class="alt"><td>Feature rich user preferences</td><td>N</td><td>Y</td></tr>
<tr><td>Order tracking history</td><td>Y, core</td><td>Y</td></tr></tbody></table>

### System Wide Features

<table cellpadding="2" cellspacing="0" width="100%"><tbody>
<tr class="alt header"><td width="60%">Feature</td><td width="20%">Spree</td><td>Magento</td></tr>
<tr><td>Extensibility</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Appearance Theming</td><td>Y, core</td><td>Y</td></tr>
<tr><td>Ability to customize appearance at category or browsing level</td><td>N</td><td>Y</td></tr>
<tr class="alt"><td>Localization</td><td>Y, core</td><td>Y</td></tr>
<tr><td>Multi-store, single admin support</td><td>Y, extension</td><td>Y</td></tr>
<tr class="alt"><td>Support for multiple currencies</td><td>N</td><td>Y</td></tr>
<tr><td>Web Service API</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>SEO System wide: sitemap, google base, etc</td><td>Y, extension</td><td>Y</td></tr>
<tr><td>Google Analytics</td><td>Y, core</td><td>Y</td></tr>
<tr class="alt"><td>Active community</td><td>Y, N/A</td><td>Y</td></tr></tbody></table>

The configurability and complexity of each feature listed above varies. Just because a feature is provided within a platform does not guarantee that it will meet the desired business needs. Magento serves as a more comprehensive ecommerce platform out of the box, but the disadvantage may be that adding custom functionality may require more resources (read: more expensive). Spree serves as a simpler base that may encourage quicker (read: cheaper) customization development simply because it’s in Rails and because the dynamic nature of Ruby allows for elegant extensibility in Spree, but a disadvantage to Spree could be that a site with a large amount of customization may not be able to take advantage of community-available extensions because they may not all play nice together.

Rather than focus on the platform features, the success of the development depends on the developer and his/her skillset. Most developers will say that **any** of the features listed above are doable in Magento, Spree, or Interchange (a Perl-based ecommerce platform that End Point supports) with an unlimited budget, but a developer needs to have an understanding of the platform to design a solution that is easily understood and well organized (to encourage readability and understandability by other developers), develop with standard principles like DRY and MVC-style separation of concerns, and elegantly abstract from the ecommerce core to encourage maintainability. And of course, be able to understand the business needs and priorities to guide a project to success within the given budget. Inevitably, another developer will come along and need to understand the code and inevitably, the business will often use an ecommerce platform longer than planned so maintainability is important.

Please feel free to comment on any errors in the feature list. I’ll be happy to correct any mistakes. Now, off to rest before RailsConf!
