---
author: Matt Galvin
gh_issue_number: 880
tags: ecommerce, javascript, ruby, rails, spree
title: How to Dynamically Update A Spree Product's Price Based on Volume Pricing
---

I was recently working on a Spree Commerce site that utilizes Spree's Volume Pricing extension. For those who may not be familiar, the [Spree Commerce Volume Pricing extension](https://github.com/spree/spree_volume_pricing) allows a user to offer a variety of 'price ranges'. These price ranges represent discounted prices per unit for larger quantity orders. For example (we will use this t-shirt pricing table for the remainder of the post) from the  **[Spree Volume Pricing Github](https://github.com/spree/spree_volume_pricing)**

```nohighlight
   Variant                Name               Range        Amount         Position
   -------------------------------------------------------------------------------
   Rails T-Shirt          1-5                (1..5)       19.99          1
   Rails T-Shirt          6-9                (6...10)     18.99          2
   Rails T-Shirt          10 or more         (10+)        17.99          3
```

I would like to mention that these ranges, although resembling traditional ranges,  are expressed as Strings as this will become more important later. Again from the **[Spree Volume Pricing](https://github.com/spree/spree_volume_pricing)** project page at Github,

>   "All ranges need to be expressed as Strings and must include parentheses. '(1..10)' is considered to be a valid range. '1..10' is not considered to be a valid range (missing the parentheses.)"

Now that the intent of Volume Pricing has been discussed I would like to bring your attention to what is likely a very common use case.  Often on an e-commerce website when placing an order for an item the price and quantity is seen as so,

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/11/08/how-to-dynamically-update-spree/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/11/08/how-to-dynamically-update-spree/image-0.png"/></a></div>

Which is generated from relatively typical Spree models and functions in erb and the HTML5 number input:

```ruby
#price per shirt
  &lt;%= display_price(@product) %&gt; per shirt

  #number field
  &lt;%= number_field_tag (@product.variants_and_option_values.any? ? :quantity : "variants[#{@product.master.id}]"),
    1, :class =&gt; 'title', :min =&gt; 1 %&gt;
  &lt;%= button_tag :class =&gt; 'large primary', :id =&gt; 'add-to-cart-button', :type =&gt; :submit do %&gt;
    &lt;%= Spree.t(:add_to_cart) %&gt;
  &lt;% end %&gt;
```

However, without any additional coding when a customer increases their order quantity to the next range, the price per unit (shirt) should be decremented as noted in the table above.  However, as we can see here rather than the price being lowered to 18.99 per shirt, it continues to indicate 19.99 even though volume pricing has taken effect and the shirts are actually 18.99 each.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/11/08/how-to-dynamically-update-spree/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/11/08/how-to-dynamically-update-spree/image-1.png"/></a></div>

So, how would one accomplish this?  JavaScript is the first thing that comes to most people's mind.  I spent some time looking around the Spree docs thinking that certainly there must be something quick to drop in, but there was not.  I did a little Googling and found the same thing to be true- not much info out there on how best to proceed with this task.  I was very surprised to find no notes on anyone doing what I would think is a very common issue.  So, here we are and I hope that anyone who reads this finds it helpful.

### **Step 1a: Create an array of the prices**

This is the most challenging part of the task.  After discussing the issue with some colleagues I believed the easiest method was to create an array of all the possible volume prices.  Then, this price could be referenced by just taking the selected quantity of an order, subtracting 1 (to account for the zero-indexing of arrays) and getting the value of the complete volume price array via that index.  In this example, using the data from the table above, the array would look like this:

[19.99, 19.99, 19.99, 19.99, 19.99,18.99,18.99,18.99,18.99]

In case that isn't clear from above, volume price (1..5) is 19.99 so the first 5 items in the array are 19.99. Volume price 18.99 is in effect for range (6..9) so the 6th through 9th item in the array are 18.99. If a user were to indicate a quantity of 5, 5-1 = 4.  Index 4 of the array is 19.99, the correct price for five shirts. **Note, for now I've left off the (10+) range and associated pricing and the reason will be clear in a few moments.**

Alright, so now on how to create this array. Those of you who are familiar with Spree know that we use the Spree Model decorator, in this case, the Product decorator which should be created in app/models/product_decorator.rb

```ruby
Spree::Product.class_eval do

  def all_prices
    price_ranges = Spree::Variant.where(product_id: self.id).first.volume_prices[0...-1].map(&amp;:range)
    volume_prices = Spree::Variant.where(product_id: self.id).first.volume_prices[0...-1].map(&amp;:amount).map(&amp;:to_f)
    price_ranges.map(&amp;:to_range).map{|v| v.map{|i| volume_prices[price_ranges.map(&amp;:to_range).index(v)]}}.flatten
  end

end
```

### **Step 1b: Create to_range function for Strings &amp; create a function to return lowest possible price per unit**

Now here you may note the to_range call in pink above.  As mentioned in this post and in the Volume Pricing docs, Spree expresses these ranges as Strings and not true ranges, so I used this to_range method in lib/range.rb to easily convert the String ranges into true Ranges, which I found on the "Master Ruby/Rails Programming" post at [athikunte blog](http://athikunte.blogspot.com/2008/02/convert-string-to-range.html). I would also like to draw your attention to the fact that I am taking all but the last item of the volume prices array ([0...-1]).  Why?  Because '10+' will not be converted into a range and any quantity of 10 or greater can just get the lowest volume price. Perhaps most importantly, if some product's last range is 10+ while another is say 25+, this method of obtaining the lowest discounted price will avoid any problems related to that variance.  In lib/string.rb,

```ruby
class String
  def to_range
    case self.count('.')
      when 2
        elements = self.split('..')
        return Range.new(elements[0].to_i, elements[1].to_i)
      when 3
        elements = self.split('...')
        return Range.new(elements[0].to_i, elements[1].to_i-1)
      else
        raise ArgumentError.new("Couldn't convert to Range: #{str}")
    end
  end
end
```

app/models/product_decorator.rb

```ruby
def lowest_discounted_volume_price
  Spree::Variant.where(product_id: self.id).first.volume_prices[-1].to_f
end
```

### **Step 2:  Load Your New Volume Pricing Array and Lowest Possible Price**

I did this by creating some script tags in the product show page (or wherever you wish to have this price per unit showing) to make the data from the backend available in a JavaScript file that will update the price dynamically as a user adds or subtracts from the desired quantity. I just called the functions I created in the product decorator here and stored the result in variables for the JavaScript file, app/views/product_show_page.html.erb

```ruby
var all_prices = &lt;%= @product.all_prices %&gt;;
var lowest_discounted_volume_price = &lt;%= @product.lowest_discounted_volume_price %&gt;;
```

### **Step3: Write JavaScript Code to Handle Quantity Changes**

In your Spree app just follow typical rails protocol and create a new JavaScript file in app/assets/javascripts/volume_pricing.js and of course require it in your manifest file.  Here, just plug your variables in and update your view with the change event (I also added keyup so the price changes if/when a user types in a new quantity)

```javascript
$(function() {
  $('.title').on('keyup change', function(e){
    var qty = parseInt( $(this).val());
    var prices_array = all_prices;
    var per_shirt = ' per shirt'
    if (qty &lt;= prices_array.length)
      {
        $('span.price.selling').text('$'+prices_array[qty -1] + per_shirt);
      }
    else
      {
        $('span.price.selling').text('$'+lowest_discounted_volume_price + per_shirt);
      }
   });
```

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/11/08/how-to-dynamically-update-spree/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/11/08/how-to-dynamically-update-spree/image-2.png"/></a></div>

And now you have dynamically updating price based on selected quantity!  I hope you have found this informative and useful, thank you for reading.
