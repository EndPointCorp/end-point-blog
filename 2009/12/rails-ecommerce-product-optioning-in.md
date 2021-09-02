---
author: Steph Skardal
title: Rails Ecommerce Product Optioning in Spree
github_issue_number: 230
tags:
- ecommerce
- rails
- spree
date: 2009-12-02
---

A couple of months ago, I worked on an project for [Survival International](https://shop.survivalinternational.org/) that required two-dimensional product optioning for products. The shopping component of the site used Spree, an open source rails ecommerce project that End Point previously sponsored and continues to support. Because the Spree project is quickly evolving, we wanted to implement a custom solution that would “stand the test of time” and work with new releases. I worked with the existing data structures and functionality as much as possible. The product optioning implementation discussed in this article should translate to other ecommerce platforms as well.

<a href="https://1.bp.blogspot.com/_wWmWqyCEKEs/Sxbj4ANgHxI/AAAAAAAACvs/GgKcIvu918Y/s1600-h/ts.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5410762553601040146" src="/blog/2009/12/rails-ecommerce-product-optioning-in/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 320px; height: 205px;"/></a>

Here’s what I mean when I say “two dimensional product optioning”.

The first step to extending the core ecommerce functionality was to understand the data model. A single product “has many” option types (size, color). An option type “has many” option values (size: small, medium, large). Each product also “has many” variants. Each variant was tied to an option value for each product option type. For example, each variant would requires a corresponding size and color option value in the example above. Ideally, each variant represents a unique size and color combination.

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/Sxb1OBkX2JI/AAAAAAAACwM/5rK_oOi9gF8/s1600-h/data.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5410781623620196498" src="/blog/2009/12/rails-ecommerce-product-optioning-in/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 192px;"/></a>

An *awesome* database dependency diagram.

Using the Spree demo data, I set up the Apache Baseball Jersey to have option types “PO_Size” and “PO_Color”. PO_Size contains option values Red, Blue, and Green. PO_Color contains option values Small, Medium, and Large.

<a href="https://2.bp.blogspot.com/_wWmWqyCEKEs/Sxb1eKJ5HzI/AAAAAAAACwU/ESxvD0XSUkU/s1600-h/setup.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5410781900802957106" src="/blog/2009/12/rails-ecommerce-product-optioning-in/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 178px;"/></a>

Variants assigned to the Apache Baseball Jersey

The second step to producing a two dimensional product option table was to generate the required data in a before_filter method in the controller. Below are the contents of the module that generates the hash in the before_filter method with color and size information. The module retrieves active variants first, then verifies that the required option types are tied to the product. Then, size, color, and variant ids are collected from the active variants producing the data structure described above.

```ruby
  def self.included(target)
    target.class_eval do
      before_filter :define_2d_option_matrix, :only => :show
    end
  end
  def define_2d_option_matrix
    variants = Spree::Config[:show_zero_stock_products] ?
      object.variants.active.select { |a| !a.option_values.empty? } :
      object.variants.active.select { |a| !a.option_values.empty? && a.in_stock }
    return if variants.empty? ||
      object.option_types.select { |a| a.presentation == 'PO_Size' }.empty? ||
      object.option_types.select { |a| a.presentation == 'PO_Color' }.empty?
    variant_ids = Hash.new
    sizes = []
    colors = []
    variants.each do |variant|
      active_size = variant.option_values.select { |a| a.option_type.presentation == 'PO_Size' }.first
      active_color = variant.option_values.select { |a| a.option_type.presentation == 'PO_Color' }.first
      variant_ids[active_size.id.to_s + '_' + active_color.id.to_s] = variant.id
      sizes << active_size
      colors << active_color
    end
    size_sort = Hash['S', 0, 'M', 1, 'L', 2]
    @sc_matrix = { 'sizes' => sizes.sort_by { |s| size_sort[s.presentation] }.uniq,
 'colors' => colors.uniq,
 'variant_ids' => variant_ids }
  end
```

The code above produces a hash with three components:

- @sc_matrix['variant_ids']: a hash that maps size and color combinations to variant id
- @sc_matrix['sizes']: an array of sorted unique sizes of product variants
- @sc_matrix['colors']: an array of unique colors of product variants

In the view, the output of size and color arrays is used to generate a table. In this hardcoded view, sizes are displayed as the horizontal option across the top of the table, and colors as the vertical option along the left side of the table.

```nohighlight
...
<% if @sc_matrix -%>
<p>Choose your colour, size and quantity below.</p>
<table id="option-matrix">
    <tr>
        <th></th>
        <% @sc_matrix['sizes'].each do |s| %>
        <th class="size"><%= s.presentation %></th>
        <td class="spacer"></td>
        <% end -%>
    </tr>
    <% @sc_matrix['colors'].each do |c| -%>
    <tr>
        <th class="color"><%= c.presentation %></th>
        <% @sc_matrix['sizes'].each do |s| -%>
        <td>
            <% if @sc_matrix['variant_ids'][s.id.to_s + '_' + c.id.to_s] -%>
            <input type="radio" value="<%= @sc_matrix['variant_ids'][s.id.to_s + '_' + c.id.to_s] %>" name="products[<%= @product.id %>]" />
            <% else -%>
            <img src="/images/radio-notavailable.png" alt="X" width="20" height="20" />
            <% end -%>
        </td>
        <td class="spacer"></td>
        <% end -%>
    </tr>
    <% end -%>
</table>
<% elsif #check for other stuff
...
```

Here is a comparison of the current variant display method versus two dimensional variant display of the same product:

<a href="https://3.bp.blogspot.com/_wWmWqyCEKEs/Sxb2Rd9hiQI/AAAAAAAACwk/-FBN56TLNv0/s1600-h/vs2.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5410782782293117186" src="/blog/2009/12/rails-ecommerce-product-optioning-in/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 174px;"/></a>

Current variant display method.

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/Sxb2RMC7MaI/AAAAAAAACwc/uaBS3qii_FU/s1600-h/vs.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5410782777483932066" src="/blog/2009/12/rails-ecommerce-product-optioning-in/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 170px;"/></a>

Two dimensional variant display method. Two variants shown here are out of stock.

And here is another example of two dimensional optioning in use at Survival International (more glamorous styling):

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/Sxbj4M0Pf_I/AAAAAAAACv0/GbVlNPksOUU/s1600-h/ts2.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5410762556984754162" src="/blog/2009/12/rails-ecommerce-product-optioning-in/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 320px; height: 208px;"/></a>

Spree extensions are similar to WordPress plugins or Drupal modules that do not typically require you to edit core code. The primary components of the extension are a module with the before_filter functionality and a custom view that overrides the core product view. An extension was created for this functionality and it lives at [https://github.com/stephskardal/spree-product-options](https://github.com/stephskardal/spree-product-options).

Possibilities for future work include editing the extension to be more robust by eliminating the use of the hard-coded option types of “PO_Size” and “PO_Color” and removing the hard-coded size ordering hash. It would be ideal to be able to assign the two dimension option types (horizontal axis and vertical axis) in the Spree admin for each product or a set of products. Another option for future work with this extension includes extending the functionality to multi-dimensional product optioning that would allow you to select more than two option types per product (for example: size, color, and material), but this functionality is more complex and may be dependent on JavaScript to hide and show option types and values.
