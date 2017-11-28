---
author: Steph Skardal
gh_issue_number: 399
tags: ecommerce, rails, sinatra
title: 'Ruby Ecommerce with Sinatra: Admin and Products'
---



Last week, I [wrote about creating a very simple ecommerce application on Ruby with Sinatra](/blog/2011/01/17/sinatra-ecommerce-tutorial). This week, we continue on the yellow brick road of ecommerce development on Ruby with Sinatra.

<a href="http://www.flickr.com/photos/airdiogo/4640440092/" title="yellow brick road by airdiogo, on Flickr"><img alt="yellow brick road" height="238" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-0.jpeg" width="500"/></a>

A yellow brick road.

### Part 2: Basic Admin Authentication

After you've got a basic application running which accepts payment for a single product as described in the previous tutorial, the next step is to add admin authorization to allow lookup of completed orders. I found several great resources for this as well as a few Sinatra extensions that may be useful. For the first increment of implementation, I followed the instructions [here](http://www.gittr.com/index.php/archive/sinatra-basic-authentication-selectively-applied/), which uses Basic::Auth. The resulting code can be viewed [here](https://github.com/stephskardal/sinatrashop/blob/part2/lib/authorization.rb). I also introduce [subclassing of Sinatra::Base](http://www.sinatrarb.com/blog.html), which allows us to keep our files a bit more modular and organized.

And if we add an "/admin" method to display orders, we can see our completed orders:

<a href="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565769827342544482" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 237px; height: 299px;"/></a>

Completed orders.

### Part 3: Introducing Products

Now, let's imagine an ecommerce store with different products! **Whoa!** For this increment, let's limit each order to one product. A migration and model definition is created to introduce products, which contains a name, description, and price. For this increment, product images match the product name and live ~/public/images. The orders table is modified to contain a reference to products.id. The orders model is updated to belong_to :products. Finally, the frontend authorization method is modified to use the order.product.price in the transaction.

<table width="100%">
<tbody><tr><td>
<pre class="brush:ruby">
# Products ActiveRecord migration
require 'lib/model/product'
class CreateProducts < ActiveRecord::Migration
  def self.up
    create_table :products do |t|
      t.string :name,
        :null => false
      t.decimal :price,
        :null => false
      t.string :description,
        :null => false
    end
  end

  def self.down
    drop_table :products
  end
end
</pre>
</td><td valign="top">
<pre class="brush:ruby"> 
# Products model class
class Product < ActiveRecord::Base
  validates_presence_of :name
  validates_presence_of :price
  validates_numericality_of :price
  validates_presence_of :description

  has_many :orders
end
</pre>
</td></tr>
<tr><td valign="top">
<pre class="brush:ruby">
# Order migration update
class CreateOrders < ActiveRecord::Migration
  def self.up
    create_table :orders do |t|
+      t.references :product,
+        :null => false
    end
  end

  def self.down
    drop_table :orders
  end
end
</pre>
</td><td valign="top">
<pre class="brush:diff">
# Order model changes
class Order < ActiveRecord::Base
...
+ validates_presence_of :product_id
+
+  belongs_to :product
end
</pre>
</td></tr>
<tr><td valign="top">
<pre class="brush:diff">
# in main checkout action
# Authorization amount update
- response = gateway.authorize(1000,
-   credit_card)
+ response = gateway.authorize(order.product.price*100,
+   credit_card)
</pre>
</td><td>
<p style="text-align:center;">
<a href="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565517523065098626" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 253px; height: 400px;"/></a><br/>Our new data model.</p>
</td></tr>
</tbody></table>

And let's use Sinatra's simple and powerful routing to build resource management functionality that allows our admin to list, create, update, and delete items, or in this case orders and products. Here's the sinatra code that accomplishes this basic resource management:

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td valign="top">
<pre class="brush:ruby">
# List items
app.get '/admin/:type' do |type|
  require_administrative_privileges
  content_type :json

  begin
    klass = type.camelize.constantize
    objects = klass.all
    status 200
    objects.to_json
  rescue Exception => e
    halt 500, [e.message].to_json 
  end
end
</pre>
</td><td valign="top">
<pre class="brush:ruby">
# Delete item
app.delete '/admin/:type/:id' do |type, id|
  require_administrative_privileges
  content_type :json

  begin
    klass = type.camelize.constantize
    instance = klass.find(id)
    if instance.destroy
      status 200
    else
      status 400
      errors = instance.errors.full_messages
      [errors.first].to_json
    end
  rescue Exception => e
    halt 500, [e.message].to_json
  end
end
</pre>
</td></tr><tr><td valign="top">
<pre class="brush:ruby">
# Create new item
app.post '/admin/:type/new' do |type|
  require_administrative_privileges
  content_type :json
  input = json_to_hash(request.body.read.to_s)
 
  begin
    klass = type.camelize.constantize
    instance = klass.new(input)
    if instance.save
      status 200
      instance.to_json
    else
      status 400
      errors = instance.errors.full_messages
      [errors.first].to_json
    end
  rescue Exception => e
    halt 500, [e.message].to_json
  end
end
</pre>
</td><td valign="top">
<pre class="brush:ruby">
# Edit item
app.post '/admin/:type/:id' do |type, id|
  require_administrative_privileges
  content_type :json
  input = json_to_hash(request.body.read.to_s)
  
  begin
    klass = type.camelize.constantize
    instance = klass.find(id)
    if instance.update_attributes(input)
      status 200
      instance.to_json
    else
      status 400
      errors = instance.errors.full_messages
      [errors.first].to_json
    end
  rescue Exception => e
    halt 500, [e.message].to_json
  end
end
</pre>
</td></tr></tbody></table>

Note that in the code shown above, the request includes the class (product or order in this application), and the id of the item in some cases. The [constantize](http://api.rubyonrails.org/classes/ActiveSupport/Inflector.html#method-i-constantize) method is used to get the class constant, and ActiveRecord methods are used to retrieve and edit, create, or delete the instance. This powerful routing now allows us to easily manage additional resources with minimal changes to our server-side code.

Next, I use jQuery to call these methods via AJAX, also in such a way that it'll be easy to manage new resources with minimal client side code. That base admin code can be found [here](https://github.com/stephskardal/sinatrashop/blob/part3/public/javascripts/admin/base.js). With this jQuery admin base, we now define our empty resource, content for displaying that resource, and content for editing that resource. Examples of this are shown below:

<table width="100%">
<tbody><tr><td valign="top">
<pre class="brush:ruby">
functions.product = {
  edit: function(product) {
    return '<h4>Editing Product: '
      + product.id
      + '</h4>'
      + '<p><label for="name">Name</label>'
      + '<input type="text" name="name" value="'
      + product.name
      + '" /></p>'
      + '<p><label for="price">Price</label>'
      + '<input type="text" name="price" value="'
      + parseFloat(product.price).toFixed(2)
      + '" /></p>'
      + '<p><label for="description">Description</label>'
      + '<textarea name="description">'
      + product.description
      + '</textarea></p>';
  },
  content: function(product) {
    var inner_html = '<h4>Product: '
      + product.id
      + '</h4>'
      + 'Name: '
      + product.name
      + '<br />Price: $'
      + parseFloat(product.price).toFixed(2)
      + '<br />Description: '
      + product.description
      + '<br />';
    return inner_html;
  },
  empty: function() {
    return { name: '',
      price: 0, 
      description: '' };  
  }
};
</pre>
</td><td valign="top">
<p style="text-align:center;">
<a href="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565131584641759378" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 164px;"/></a>
<br/>Product listing.<br/>
<a href="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565131588529278818" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 204px;"/></a>
<br/>Creating a new product.<br/>
<a href="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-4-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565131574311871250" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 170px;"/></a>
<br/>Editing an existing product.</p>
</td></tr><tr><td>
<pre class="brush:ruby">
functions.order = {
  edit: function(order) {
    return '<b>Order: '
      + order.id
      + '</b><br />'
      + '<input name="email" value="'
      + order.email
      + '" />'
      + ' – '
      ...
      //Order editing is limited
  },
  content: function(order) {
    return '<b>Order: '
      + order.id
      + '</b><br />'
      + order.email
      + ' – '
      + order.phone
      + '<br />'
      ...
  },
  empty: function() {
    return { 
      email: '',
      phone: '',
      ...
    };  
  }
};
</pre>
</td><td valign="top">
<p style="text-align:center;"><a href="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-5-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565131571665096178" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-5.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 283px;"/></a><br/>For this example, we limit order editing to email and phone number changes.</p>
</td></tr></tbody></table>

With a final touch of frontend JavaScript and CSS changes, the following screenshots show the two customer-facing pages from our example store. Like the application described in the [previous article](/blog/2011/01/17/sinatra-ecommerce-tutorial), this ecommerce application is still fairly lightweight, but it now allows us to sell several products and manage our resources via the admin panel. Stay tuned for the next increment!

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td valign="top" width="50%">
<a href="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-6-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565134342843290130" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-6.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 300px;"/></a></td><td valign="top">
<a href="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-7-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565134348504692946" src="/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin/image-7.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 300px;"/></a>
</td></tr></tbody></table>

The cupcake images shown in this article are under the Creative Commons license and can be found [here](http://www.flickr.com/photos/quintanaroo/1761452945/), [here](http://www.flickr.com/photos/rachelpatterson/4572080699/), and [here](http://www.flickr.com/photos/dn/3304329740/). The code shown in this article can be found [here](https://github.com/stephskardal/sinatrashop) (branches part2 and part3).


