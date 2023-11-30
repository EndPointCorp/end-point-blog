---
author: Steph Skardal
title: 'Spree: Working with Sample Product Data'
github_issue_number: 327
tags:
- ecommerce
- rails
- spree
date: 2010-07-21
---

It’s taken me a bit of time to gain a better understanding of working with Spree sample data or [fixtures](http://api.rubyonrails.org/v2.3.8/classes/Fixtures.html), but now that I am comfortable with it I thought I’d share some details. The first thing you might wonder is why should you even care about sample data? Well, in our project, we had a few motivations for creating sample data:

1. **Multiple developers, consistent sample data provides consistency during development.** End Point offers [SpreeCamps](http://www.spreecamps.com/), a hosting solution that combines the open source Spree technology with devcamps to allow multiple development and staging instances of a Spree application. In a recent project, we had a two developers working on different aspects of the custom application in SpreeCamps; creating meaningful sample data allowed each developer to work from the same data starting point.
1. **Unit testing**. Another important element of our project includes adding unit tests to test our custom functionality. Consistent test sample data gave us the ability to test individual methods and functionality with confidence.
1. **Application testing**. In addition to unit testing, adding sample data gives the ability to efficiently test the application repeatedly with fresh sample data.

Throughout development, our standard practice is to repeatedly run rake db:bootstrap SKIP_CORE=1 AUTO_ACCEPT=1. Running bootstrap with these arguments will not create Spree’s core sample data set, but it will set the core’s default data that includes some base zones, zone members, countries, states, and roles, data that is essential for the application to work.

### Product Data Model

<a href="/blog/2010/07/spree-sample-product-data/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5496461407635652018" src="/blog/2010/07/spree-sample-product-data/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 292px;"/></a>

Product data relationship in Spree

The first data I create is the product data. As you can see from the image above, products data may have relationships with other tables including option_types, option_values, and taxons, or the tables that create has and belongs to many relationships between products and these elements.

The most simple form of sample data might include one test product and its master variant, shown below. If you do not define a master variant for a product, the product page will crash, as a master variant is required to display the product price.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top" width="50%">
<pre class="brush:ruby">
<b>products.yml</b>
test_product:
  id: 1
  name: Test Product
  description: Lorem ipsum...
  available_on: <%= Time.zone.now.to_s(:db) %>
  count_on_hand: 10
  permalink: test-product
</pre>
</td>
<td valign="top">
<pre class="brush:ruby">
<b>variants.yml</b>
test_variant:
  product: test_product
  price: 10.00
  cost_price: 5.00
  count_on_hand: 10
  is_master: true
  sku: 1-master
</pre>
</td>
</tr>
</tbody></table>

### Option Types and Option Values

To expand on this, you might be interested in adding option types and values to allow for sizes to be assigned to this variant, shown below. The option type and option value data structure provides a flexible architecture for creating product variants, or multiple *varieties* of a single product such as different sizes, colors, or combinations of these option values.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top" width="50%">
<pre class="brush:ruby">
<b>option_types.yml</b>
size:
  name: size
  presentation: Size
</pre>
</td>
<td valign="top">
<pre class="brush:ruby">
<b>option_values.yml</b>
small:
  name: Small
  presentation: Small
  option_type: size
large:
  name: Large
  presentation: Large
  option_type: size
</pre>
</td></tr><tr><td valign="top">
<pre class="brush:ruby">
<b>product_option_types.yml</b>
test_product_size:
  product: test_product
  option_type: size
</pre>
</td><td valign="top">
<pre class="brush:ruby">
<b>variants.yml</b>
# ...  master variant
small_variant:
  product: test_product
  option_values: small
  price: 10.00
  cost_price: 5.00
  count_on_hand: 10
  sku: 1-small
large_variant:
  product: test_product
  option_values: large
  price: 20.00
  cost_price: 10.00
  count_on_hand: 10
  sku: 1-large
</pre>
</td></tr></tbody></table>

### Taxonomies and Taxons

Another opportunity for expansion on sample product data is the taxonomy structure, which is very flexible. A root taxonomy can be thought of as a tree trunk with branches; products can be assigned to any number of branches. If we assume you have multiple test products, you might set up the following test data:

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td valign="top" width="50%">
<pre class="brush:ruby">
<b>taxonomies.yml</b>
category:
  name: Category
brand:
  name: Brand
</pre>
</td><td valign="top">
<pre class="brush:ruby">
<b>taxons.yml</b>
category_root:
  id: 1
  name: Category
  taxonomy: category
  permalink: c/
jackets:
  id: 2
  name: Jackets
  taxonomy: category_root
  permalink: c/jackets/
  parent_id: 1
  products: test_product, test_product2, test_product3
pants:
  id: 3
  name: Pants
  taxonomy: category_root
  permalink: c/pants/
  parent_id: 1
  products: test_product4, test_product5, test_product6
brand_root:
  id: 4
  name: Brand
  taxonomy: brand
  permalink: b/
brand_one:
  id: 5
  name: Brand One
  taxonomy: brand
  permalink: b/brand-one/
  parent_id: 4
  products: test_product, test_product3, test_product5
brand_two:
  id: 6
  name: Brand Two
  taxonomy: brand
  permalink: b/brand-two/
  parent_id: 4
  products: test_product2, test_product4, test_product6
</pre>
</td></tr></tbody></table>

I also needed to include the taxons.rb (used in the Spree core sample data) to assign products to taxons correctly.

```ruby
<b>taxons.rb</b>
Taxon.rebuild!
Taxon.all.each{|t| t.send(:set_permalink); t.save}
```

<a href="/blog/2010/07/spree-sample-product-data/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5496461414727904594" src="/blog/2010/07/spree-sample-product-data/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 372px; height: 400px;"/></a>

Example taxonomies created with Spree sample data

### Product Images

My last step in creating Spree sample data is to add product images. I’ve typically added the image via the Spree backend first, and then copied the images my site extension directory.

```plain
# upload Spree images

# create sample image directory
mkdir RAILS_ROOT/vendor/extensions/site/lib/tasks/sample/

# copy the uploaded images to the sample image directory
cp -r RAILS_ROOT/public/assets/products/ RAILS_ROOT/vendor/extensions/site/lib/tasks/sample/
```

After uploading and copying the images over, I include the image information in assets.yml. The ID for each asset must be equal to the directory containing the multiple image sizes. For example, the directory RAILS_ROOT/vendor/extensions/site/lib/tasks/sample/1/ contains directories original, large, product, small, and mini with images sized respectively.

```ruby
<b>assets.yml</b>
i1:
  id: 1
  viewable: test_product
  viewable_type: Product
  attachment_content_type: image/jpg
  attachment_file_name: blue_sky.jpg
  attachment_width: 1024
  attachment_height: 683
  type: Image
  position: 1
```

And finally, I use a modified version of the Spree’s core products.rb file to copy over product images during bootstrap:

```ruby
<b>products.rb</b>
require 'find'
# make sure the product images directory exists
FileUtils.mkdir_p "#{RAILS_ROOT}/public/assets/products/"

# make product images available to the app
target = "#{RAILS_ROOT}/public/assets/products/"
source = "#{RAILS_ROOT}/vendor/extensions/site/lib/tasks/sample/products/"

Find.find(source) do |f|
  # omit hidden directories (SVN, etc.)
  if File.basename(f) =~ /^[.]/
    Find.prune
    next
  end

  src_path = source + f.sub(source, '')
  target_path = target + f.sub(source, '')

  if File.directory?(f)
    FileUtils.mkdir_p target_path
  else
    FileUtils.cp src_path, target_path
  end
end
```

With my sample data defined in my Spree site extension, I run rake db:bootstrap SKIP_CORE=1 AUTO_ACCEPT=1 to create the above products, variants, and taxonomy structure. I commit my changes to the git repository, and other developers can work with the same set of products, variants, taxonomies including product images. During development, I also add unit tests to test model methods that interact with our sample data. An alternative to setting up Spree sample data described in this article is to dump entire databases and reimport them and manage the sample images manually, but I find that the approach described here forces you to understand the Spree data model better.

<a href="/blog/2010/07/spree-sample-product-data/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5496461422974810018" src="/blog/2010/07/spree-sample-product-data/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 209px;"/></a>

Sample product image created with the sample data above.

In addition to setting up sample product data, I’ve worked through creating sample orders, shipping configuration, and tax configuration. I hope to discuss these adventures in the future.
