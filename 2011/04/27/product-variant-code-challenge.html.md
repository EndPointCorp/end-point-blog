---
author: Steph Skardal
gh_issue_number: 445
tags: ecommerce, ruby
title: A Product Variant Code Challenge
---



A while ago, I came across a [cute little Ruby challenge](http://norbauer.com/notebooks/code/notes/code-challenge-combinations) that looked interesting:

*

Given an array of arrays of possible values, enumerate all combinations that can occur, preserving order. For instance:

Given: [[1,2,3], [4,5,6], [7,8,9]], calculate the same result as the code below, but do so with an arbitrary size array:

```ruby
combos = []
[1,2,3].each do |v1|
  [4,5,6].each do |v2|
    [7,8,9].each do |v3|
      combos << [v1, v2, v3]
    end
  end
end
combos
```

Entries can be written using one or more functions, and may optionally be written as a class extension (i.e. Array)....

*

And now some context to why I thought this was applicable to ecommerce: Let's imagine you have a product. Then, let's imagine that the product has variations, or variants. We'll say we have an arbitrary size array of "option types", each with an arbitrary number of items in the array. Here, we have option types of size, color, and printed logo, which yields multiple variations, variants or combinations of a single product:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr>
<th align="center" width="33%">Size</th>
<th align="center" width="33%">Color</th>
<th align="center" width="33%">Logo</th>
</tr>
<tr>
<td align="center" width="33%">
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5598028811643117810" src="/blog/2011/04/27/product-variant-code-challenge/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width:200px;"/>
Large</td>
<td align="center" width="33%">
<div style="background:red;height:100px;width:100px;"> </div>
Red</td>
<td align="center" width="33%">
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5598030265473204450" src="/blog/2011/04/27/product-variant-code-challenge/image-1.jpeg" style="display:block; margin:0px auto 10px;width:200px;"/>
</td>
</tr>
<tr>
<td align="center">
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5598028811643117810" src="/blog/2011/04/27/product-variant-code-challenge/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width:150px;"/>
Medium</td>
<td align="center">
<div style="background:blue;height:100px;width:100px;"> </div>
Blue</td>
<td align="center">
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5598031461272555154" src="/blog/2011/04/27/product-variant-code-challenge/image-3.jpeg" style="display:block; margin:0px auto 10px;width:200px;"/>
</td>
</tr>
<tr>
<td align="center">
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5598028811643117810" src="/blog/2011/04/27/product-variant-code-challenge/image-0.jpeg" style="display:block;margin:0px auto 10px;width:100px;"/>
Small</td>
<td></td>
<td align="center"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5598030258808542178" src="/blog/2011/04/27/product-variant-code-challenge/image-5.png" style="display:block; margin:0px auto 10px;width:200px;"/></td>
</tr>
<tr>
<td></td>
<td></td>
<td align="center"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5598030266039686082" src="/blog/2011/04/27/product-variant-code-challenge/image-6.jpeg" style="display:block; margin:0px auto 10px;width:200px;"/></td>
</tr>
</tbody></table>

And let's give a real-life example data model, this one from a [previous article on Spree's product data model](http://blog.endpoint.com/2010/07/spree-sample-product-data.html):

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5598028813657050850" src="/blog/2011/04/27/product-variant-code-challenge/image-7.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 537px; height: 279px;"/>

Given this context, we can say that the outer array dimension represents product option types with individual values and that this challenge is asking for a simple method to create a list of all possible variants or variations of the product. In our t-shirt example, the solution to the example is:

```ruby
[["large", "blue", "twitter"],
["large", "blue", "facebook"],
["large", "blue", "tumblr"],
["large", "blue", "blogger"],
["large", "red", "twitter"],
["large", "red", "facebook"],
["large", "red", "tumblr"],
["large", "red", "blogger"],
["medium", "blue", "twitter"],
["medium", "blue", "facebook"],
["medium", "blue", "tumblr"],
["medium", "blue", "blogger"],
["medium", "red", "twitter"],
["medium", "red", "facebook"],
["medium", "red", "tumblr"],
["medium", "red", "blogger"],
["small", "blue", "twitter"],
["small", "blue", "facebook"],
["small", "blue", "tumblr"],
["small", "blue", "blogger"],
["small", "red", "twitter"],
["small", "red", "facebook"],
["small", "red", "tumblr"],
["small", "red", "blogger"]]
```

Unfortunately, the original contest only received 2 submissions, so I wanted to open the door here to allow people to submit more submissions in Ruby and any other language. Please include a link to the gist or code solution and in a few weeks, I'll update the post with several submissions and links to the submissions, including my own solution. It's a nice little puzzle to take on in your desired language.


