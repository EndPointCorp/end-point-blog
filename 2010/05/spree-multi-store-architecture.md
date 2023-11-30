---
author: Steph Skardal
title: Spree and Multi-site Architecture for Ecommerce
github_issue_number: 311
tags:
- ecommerce
- ruby
- rails
- spree
date: 2010-05-24
---

Running multiple stores from a single ecommerce platform instance seems to be quite popular these days. End Point has worked with several clients in developing a multi-store architecture running from one Interchange installation. In the case of our work with Backcountry.com, the data structure requires that a site_id column be included in product and navigation tables to specify which stores products and categories belong to. Frontend views are generated and “partial views” or “view components” are organized into a per-site directory structure and database calls request products against the current site_id. Below is a simplified view of the data structure used for Backcountry.com’s multi-site architecture.

<img src="/blog/2010/05/spree-multi-store-architecture/image-0.png" /><br />
Basic multi-store data architecture

A similar data model was implemented and enhanced for another client, College District. A site_id column exists in multiple tables including the products and navigation tables, and sites can only access data in the current site schema. College District takes one step further in development for appearance management by storing CSS values in the database and enabling CSS stylesheet generation on the fly with the stored CSS settings. This architecture works well for College District because it allows the owners to quickly publish new sites. Below is a simplified view of the data structure used for College District, where the table site_variables contains CSS values (text, background colors, etc.).

<a href="/blog/2010/05/spree-multi-store-architecture/image-1-big.png"><img src="/blog/2010/05/spree-multi-store-architecture/image-1.png" /></a>

Extended multi-store data architecture where site_variables table contains CSS settings. The store frontend can access data in the current store schema only.

In the past year, running a multi-site setup has been a popular topic in the user group for Spree, an open source Ruby on Rails platform. I’ve been happy to be involved in a couple of client multi-site projects. Here I’ll discuss some comments for my Spree multi-site implementation work.

### Basic Extension

First, the [Spree multi-domain extension](https://github.com/railsdog/spree-multi-domain) developed by the Spree core team serves as a strong starting point. The extension migrations produce the data structure shown below, by creating a new table stores and products_stores, and adding a store_id column to the tracker (Google Analytics data) and orders table.

<a href="/blog/2010/05/spree-multi-store-architecture/image-2-big.png"><img src="/blog/2010/05/spree-multi-store-architecture/image-2.png" /></a>

Code changes in addition to data model changes are:

- A before filter sets the current store by examining the current environment variable “SERVER_NAME”.
- Frontend product retrieval is modified to retrieve products in the current store only.
- Frontend navigation is generated based on products assigned to the current store.
- The Tracker (Google Analytics) retrieval method is modified to only retrieve the current store settings.
- Order processing assigns the store_id value to each order.

With this extension, a user can check out across multiple stores running from a single Spree application with the same account, products can be assigned to multiple stores, and a single default store is set to render if no domains match the current SERVER_NAME. The extension does not introduce the advanced schema behavior like College District’s data architecture, however, the extension could be customized to do so. The extension suits basic requirements for a multi-store architecture.

### Additional Customizations Required

In my project, there were additional changes required. I used the [Spree static pages extension](https://github.com/stephskardal/spree-static-content), which introduces functionality to present and manage static content pages. I modified this extension to create an additional stores_pages table that introduces a has and belongs to many relationship between stores and pages.

<table cellpadding="10" cellspacing="10" width="100%">
<tbody><tr>
<td><a href="/blog/2010/05/spree-multi-store-architecture/image-3-big.png"><img src="/blog/2010/05/spree-multi-store-architecture/image-3.png" /></a></td>
<td><a href="/blog/2010/05/spree-multi-store-architecture/image-4-big.png"><img src="/blog/2010/05/spree-multi-store-architecture/image-4.png" /></a></td>
</tr>
<tr><td>
Basic Spree static pages data model.
</td><td>
Expanded Spree static pages data model with multi-store design.
</td></tr>
</tbody></table>

Other custom requirements may include modifying the [spree-faq extension](https://github.com/joshnuss/spree-faq) to build a has and belongs to many relationship between questions and stores, or similar changes that create relationships between the stores table and other data.

### File Structure Organization

The next interesting design choice I faced was how to handle appearance management across multiple sites. As I mentioned before, a method was developed to retrieve and build views based on the current store in Backcountry.com’s multi-store solution. With College District, the database stored CSS values and generated new stylesheets on the fly for each site. I chose to implement a simplified version of the College District implementation, where a single stylesheet contains the rules for each site.

In the Spree implementation, the Spree::BaseController class is modified with a before filter to set the store and asset (images, javascript, stylesheet) location:

```ruby
module Spree::Fantegrate::BaseController
  def self.included(controller)
    controller.class_eval do
      controller.append_before_filter :set_store_and_asset_location
    end
  end
  def set_store_and_asset_location
    @current_store ||= Store.by_domain(request.env['SERVER_NAME']).first
    @current_store ||= Store.default.first
    @asset_location = @current_store.domains.gsub('.mydomain.com', '')
  end
end
```

The default layout includes the main and site specific stylesheets:

```plain
  <%= stylesheet_link_tag "style" %>
  <%= stylesheet_link_tag "#{@asset_location}/site" %>
```

The site specific stylesheet contains style rules and includes site specific image settings:

```css
body.site_a { background: #101a35 url(/images/site_a/bg.jpg) repeat-x 0 0; }
.site_a h1#logo { float: left; display: inline; width: 376px; height: 131px; position:relative; left: -15px; padding-bottom: 10px; }
.site_a h1#logo a { display: block; height: 131px; background: url(/images/site_a/logo.png); }
.site_a #top-right-info,
.site_a #top-right-info a,
.site_a #top-right-info b { color: #fff; }
...
```

This implementation acts on the assumption that there will be minimal design differences across stores. This is a simple and effective way to get an initial multi-store architecture in place that allows you to manage multiple site’s appearance in a single Spree application.

### Advanced Topics

Some advanced topics I’ve considered with this work are:

- Can we dynamically generate the migrations based on which extensions are installed? For example, a list of tables would be included in the main extension. This list of tables would be iterated through and if the table exists, a dynamic migration is generated to build a has many/belongs to, has one/belongs to, or has and belongs to many relationship between stores and the table.
- SSL setup for our Spree multi-store implementation was accomplished with a wildcard SSL certificate, where each store can be accessed from a different subdomain. Backcountry.com and College District implementation was accomplished with standard SSL certificates because the stores do not share domains. The Spree implementation methods described in this article do not vary for subdomain versus different domain design, but this is certainly something to consider at the start of a multi-site project.
- The multi-domain extension could be customized and enhanced to include a table that contains CSS settings similar to our College District implementation and allows you to generate new stylesheets dynamically to change the look of a site. The obvious advantage of this is that a user with site administrative permissions can change the appearance of the site via backend Spree management without involving development resources.
