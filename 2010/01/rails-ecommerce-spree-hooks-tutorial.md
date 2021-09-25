---
author: Steph Skardal
title: 'Rails Ecommerce with Spree: Customizing with Hooks Tutorial'
github_issue_number: 252
tags:
- ecommerce
- rails
- spree
date: 2010-01-12
---

In the last couple months, there’s been a bit of buzz around theme and hook implementation in [Spree](https://spreecommerce.org/). The Spree team hasn’t officially announced the newest version 0.9.5, but the [edge code is available](https://github.com/spree/spree) and developers have been encouraged to work with the edge code to check out the new features. Additionally, there is decent [documentation about theme and hook implementation](https://guides.spreecommerce.org/developer/view.html). In this article, I’ll go through several examples of how I would approach site customization using hooks in the upcoming Spree 0.9.5 release.

**Background**

I’ve been a [big](https://groups.google.com/forum/#!topic/spree-user/V7K7mkj5qL0) [proponent](https://groups.google.com/forum/#!topic/spree-user/AE4D2jcvdlI) of how WordPress implements themes, plugins, and hooks in the [spree-user Google group](https://groups.google.com/forum/#!forum/spree-user). The idea behind WordPress themes is that a theme includes a set of PHP files that contain the display logic, HTML, and CSS for the customer-facing pages:

- index
- a post page
- archive pages (monthly, category, tag archives)
- search result page
- etc.

In many cases, themes include sections (referred to as partial views in Rails), or  components that are included in multiple template pages. An example of this partial view is the sidebar that is likely to be included in all of the page types mentioned above. The WordPress theme community is abundant; there are many free or at-cost themes available.

The concept behind WordPress plugins is much like Spree extension functionality—​a plugin includes modular functionality to add to your site that is decoupled from the core functionality. Judging from the popularity of the WordPress plugin community, WordPress has done a great job designing the [Plugin API](https://codex.wordpress.org/Plugin_API). In most cases, the Plugin API is used to extend or override core functionality and add to the views without having to update the theme files themselves. An example of using the WordPress plugin API to add an action to the wp_footer hook is accomplished with the following code:

```ruby
/* inside plugin */
function add_footer_text() {
    echo '<p>Extra Footer Text!!</p>';
}
add_action('wp_footer', 'add_footer_text');
```

WordPress themes and plugins with hooks are the building blocks of WordPress: with them, you piece together the appearance and functionality for your site. I reference WordPress as a basis of comparison for Spree, because like WordPress users, Spree users aim to piece together the appearance and functionality for their site. One thing to note is that the hook implementation in Spree is based on hook implementation in [Redmine](https://www.redmine.org/).

**Spree Code**

I grabbed [the latest code](https://github.com/spree/spree). After examining the code and reviewing the Spree documentation, the first thing I learned is that there are four ways to work with hooks:

- insert before a hook component
- insert after hook component
- replace a hook component’s contents
- remove a hook component

The next thing I researched was the hook components or elements. Below are the specific locations of hooks. The specific locations are more meaningful if you are familiar with the Spree views. The hooks are merely wrapped around parts of pages (or layouts) like the product page, product search, homepage, etc. Any of the methods listed above can act on any of the components listed below.

- layout: inside_head, sidebar
- homepage: homepage_sidebar_navigation, homepage_products
- product search: search_results
- taxon: taxon_side_navigation, taxon_products, taxon_children
- view product: product_description, product_properties, product_taxons, product_price, product_cart_form, inside_product_cart_form
- etc.

After I spent time figuring out the hook methods and components, I was ready to **do stuff**. First, I got Spree up and running (refer to the [Spree Documentation](https://guides.spreecommerce.org/) for more information):

<a href="http://2.bp.blogspot.com/_wWmWqyCEKEs/S0fnymK64uI/AAAAAAAADAY/3A18BO3Vk0E/s1600-h/image1.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424559132616876770" src="/blog/2010/01/rails-ecommerce-spree-hooks-tutorial/image-0.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 172px;"/></a>

Spree startup with seed data and images.

Next, I updated the product list with a few pretend products. Let’s take a quick look at the site with the updated products:

<a href="http://3.bp.blogspot.com/_wWmWqyCEKEs/S0fny_9mZ8I/AAAAAAAADAg/U4MjLcE75Kk/s1600-h/image2.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424559139540330434" src="/blog/2010/01/rails-ecommerce-spree-hooks-tutorial/image-1.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 165px;"/></a>

Spree with new product data for test site.

**Example #1: Replace the logo and background styling.**

First, I created an extension with the following code. Spree’s extensions are roughly based off of [Radiant’s](http://radiantcms.org/) extension system. It’s relatively simple to get an extension up and running with the following code (and server restart).

```plain
script/generate extension StephsPhotos
```

Next, I wanted to try out the insert_after method to append a stylesheet to the default theme inside the <head> html element. I also wanted to remove the sidebar because my test site only has 8 products (lame!) and I don’t need sidebar navigation. This was accomplished with the following changes:

- First, I added the insert_after hook to add a view that contains my extra stylesheet. I also added the remove hook to remove the sidebar element:

```ruby
# RAILS_ROOT/vendor/extensions/stephs_photos/stephs_photos_hooks.rb
insert_after :inside_head, 'shared/styles'
remove :sidebar
```

- Next, I added a new view in the extension to include the new stylesheet.

```plain
# RAILS_ROOT/vendor/extensions/stephs_photos/app/views/shared/_styles.erb
<link type="text/css" rel="stylesheet" href="/stylesheets/stephs_photos.css">
```

- Next, I created a new stylesheet in the extension.

```css
/* RAILS_ROOT/vendor/extensions/stephs_photos/public/stylesheets/stephs_photos.css */
body { background: #000; }
body.two-col div#wrapper { background: none; }
a, #header a { color: #FFF; text-decoration: none; }

ul#nav-bar { width: 280px; line-height: 30px; margin-top: 87px; font-size: 1.0em; }
ul#nav-bar li form { display: none; }

.container { width: 750px; }
#wrapper { padding-top: 0px; }

.product-listing li { background: #FFF; height: 140px; }
.product-listing li a.info { background: #FFF; }

body#product-details div#wrapper { background: #000; }
body#product-details div#content, body#product-details div#content h1 { color: #FFF; margin-left: 10px; }
#taxon-crumbs { display: none; }
#product-description { width: 190px; border: none; }
.price.selling { color: #FFF; }
#product-image #main-image { min-height: 170px; }

/* Styling in this extension only applies to product and main page */

div#footer { display: none; }
```

One more small change was required to update the logo via a Rails preference. I set the logo preference variable to a new logo image and uploaded the logo to RAILS_ROOT/vendor/extensions/stephs_photos/public/images/.

```ruby
# RAILS_ROOT/vendor/extensions/stephs_photos/stephs_photos_extension.rb
def activate
 AppConfiguration.class_eval do
   preference :logo, :string, :default => 'stephs_photos.png'
 end
end
```

After restarting the server, I was happy with the new look for my site accomplished using the insert_after and remove methods:

<a href="http://1.bp.blogspot.com/_wWmWqyCEKEs/S0fnzRAmApI/AAAAAAAADAo/WHtsOGCc_0s/s1600-h/image3.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424559144116290194" src="/blog/2010/01/rails-ecommerce-spree-hooks-tutorial/image-2.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 148px;"/></a>

New look for Spree acomplished with several small changes.

*Note: You can also add a stylesheet with the code shown below. However, I wanted to use the hook method described above for this tutorial.*

```ruby
def activate
  AppConfiguration.class_eval do
    preference :stylesheets, :string, :default => 'styles'
  end
end
```

**Example #2: Use insert_before to insert a view containing Spree core functionality.**

The next requirement I imagined was adding promo functionality to the product listing page. I wanted to use core Spree logic to determine which promo image to use. The first promo image would be a 10% off discount to users that were logged in. The second promo image would be a 15% off discount offered to users who weren’t logged in and created an account. I completed the following changes for this work:

- First, I added the insert_before method to add the promo view before the homepage_products component, the component that lists the products on the homepage.

```ruby
# RAILS_ROOT/vendor/extensions/stephs_photos/stephs_photos_hooks.rb
insert_before :homepage_products, 'shared/stephs_promo'
```

- Next, I added the view using core Spree user functionality.

```plain
# RAILS_ROOT/vendor/extensions/stephs_photos/app/views/shared/_stephs_promo.erb
<% if current_user -%>
<img src="http://www.blogger.com/images/promo10.png" alt="10 off" />
<% else -%>
<img src="http://www.blogger.com/images/promo15.png" alt="15 off" />
<% end -%>
```

- Finally, I uploaded my promo images to RAILS_ROOT/vendor/extensions/stephs_photos/public/images/

After another server restart and homepage refresh, I tested the logged in and logged out promo logic.

<a href="http://2.bp.blogspot.com/_wWmWqyCEKEs/S0fnzmk6OsI/AAAAAAAADAw/ASys_VeRS8w/s1600-h/image4.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424559149905754818" src="/blog/2010/01/rails-ecommerce-spree-hooks-tutorial/image-3.png" style="display: block; cursor: pointer; width: 400px; height: 175px;"/></a>

vs.

<a href="http://4.bp.blogspot.com/_wWmWqyCEKEs/S0fnz-pL2hI/AAAAAAAADA4/QuJR5NvI_1A/s1600-h/image5.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424559156366137874" src="/blog/2010/01/rails-ecommerce-spree-hooks-tutorial/image-4.png" style="display: block; cursor: pointer; width: 400px; height: 175px;"/></a>

Spree core functionality used to display two different promo images inside a partial view.

*Note: The promo coupon logic that computes the 10% or 15% off was not included in this tutorial.*

**Example #3: Use replace method to replace a component on all product pages.**

In my third example, I imagined that I wouldn’t have time to manage product descriptions when I was rich and famous. I decided to use the replace hook to replace the product description on all product pages. I completed the following steps for this change:

- First, I added the replace method to replace the :product_description component with a rails partial view.

```ruby
# RAILS_ROOT/vendor/extensions/stephs_photos/stephs_photos_hooks.rb
replace :product_description, 'shared/generic_product_description'
```

- Next, I created the view with the generic product description.

```plain
# RAILS_ROOT/vendor/extensions/stephs_photos/app/views/shared/_generic_product_description.erb
all prints are 4x6 matte prints.<br />
all photos ship in a folder.
```

After yet another server restart and product refresh, I tested the generic product description using the replace hook.

<a href="http://1.bp.blogspot.com/_wWmWqyCEKEs/S0fn6-Dcd3I/AAAAAAAADBA/OjFhnOhI7bQ/s1600-h/image6.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424559276466927474" src="/blog/2010/01/rails-ecommerce-spree-hooks-tutorial/image-5.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 135px;"/></a>

The replace hook was used to replace product descriptions on all product pages.

**Intermission**

OK, so hopefully you see the trend:

1. Figure out which component you want to pre-append, post-append, replace, or remove.
1. Modify extension_name_hooks.rb to include your hook method (and pass the view, if necessary).
1. Create the new view in your extension.
1. Restart server and be happy!

I’ll note a couple other examples below.

**Example #4: Bummer that there’s no footer component**

In the next step, I intended to add copyright information to the site’s footer. I was disappointed to find that there was no hook wrapped around the footer component. So, I decided not to care for now. But in the future, my client (me) may make this a higher priority and the options for making this change might include:

- Clone the default template and modify the template footer partial view.
- Clone the default template, create a hook to wrap around the footer component, add the changes via a hook in an extension.
- Add a view in the extension that overrides the theme footer view.

**Example #5: Add text instead of partial view.**

Since I couldn’t add copyright information below the footer, I decided to add it using after the inside_product_cart_form component using the insert_after hook. But since it’s a Friday at 5:30pm, I’m too lazy to create a view, so instead I’ll just add text for now with the following addition to the extension hooks file:

```ruby
# RAILS_ROOT/vendor/extensions/stephs_photos/stephs_photos_hooks.rb
insert_after :inside_product_cart_form, :text => '<p>© stephpowell. all rights reserved.</p>'
```

Server restart, and I’m happy, again:

<a href="http://3.bp.blogspot.com/_wWmWqyCEKEs/S0fn7AEhscI/AAAAAAAADBI/kxAk6KzZaas/s1600-h/image7.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5424559277008335298" src="/blog/2010/01/rails-ecommerce-spree-hooks-tutorial/image-6.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 140px;"/></a>

Text, rather than a partial view, was appended via a hook.

Hopefully my examples were exciting enough for you. There’s quite a lot you can do with the hook methods, and over time more documentation and examples will become available through the Spree site, but I wanted to present a few very simple examples of my approach to customization in Spree.

Tomorrow, I’m set to publish closing thoughts and comments on the hook implementation. Stay tuned.
