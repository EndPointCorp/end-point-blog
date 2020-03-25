---
author: Matt Galvin
gh_issue_number: 1071
tags: ecommerce, rails, spree
title: "Spree Commerce “invalid value for Integer(): \"09\"” in Spree​::Checkout​/update"
---

Hello again all. I like to monitor the orders and exceptions of the Spree sites I work on to ensure everything is working as intended. One morning I noticed an unusual error: “invalid value for Integer(): \"09\"” in Spree::Checkout/update on a Spree 2.1.x site.

### The Issue

Given that this is a Spree-powered e-commerce site, a customer’s inability to checkout is quite alarming. In the backtrace I could see that a **string** of “09” was causing an invalid value for an **integer**. Why hadn’t I seen this on every order in that case?

I went into the browser and completed some test orders. The bug seemed to affect only credit cards with a leading “0” in the expiration month, and then only certain expiration months. I returned to the backtrace and saw this error was occurring with Active Merchant. So, Spree was passing Active Merchant a string while Active Merchant was expecting an integer.

Armed with a clearer understanding of the problem, I did some Googling. I came across [this post](https://github.com/Shopify/active_merchant/issues/919). This post describes the source of this issue as being the behavior of sprintf which I will describe below. This [topic](https://www.ruby-forum.com/topic/77946) was discussed in the [Ruby Forum](https://www.ruby-forum.com).

### Octal Numbers 

As per Daniel Martin on the aforementioned post:
 
- sprintf("%d",'08')   ==>  ArgumentError
- sprintf("%d",'8')    ==>  "8"
- sprintf("%d",'08'.to_i) ==>  "8"
- sprintf("%f",'08')   ==>  "8.000000"

As you can see, sprintf cannot convert ‘08’ or ‘09’ to a decimal. Matthias Reitlinger notes, 

> “%d tells sprintf to expect an Integer as the corresponding argument. Being given a String instead it tries to convert it by calling Kernel#Integer”

In the same post, we can review some documentation of Kernel#Integer

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/14/spree-commerce-invalid-value-for/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/01/14/spree-commerce-invalid-value-for/image-0.png"/></a></div>

We can see here that if the argument being provided is a string (and it is since that is what Spree is sending), the “0” will be honored. Again, we know 
 

<table>
    <tbody><tr>
      <td>sprintf("%d",'01') => "1"</td>
      <td> | </td>
      <td>sprintf("%d", 01) => "1"</td>
    </tr>

    <tr>
      <td>sprintf("%d",'02') => "2"</td>
      <td> | </td>
      <td>sprintf("%d", 02) => "2"</td>
    </tr>

    <tr>
      <td>sprintf("%d",'03') => "3"</td>
      <td> | </td>
      <td>sprintf("%d", 03) => "3"</td>
    </tr>

    <tr>
      <td>sprintf("%d",'04') => "4"</td>
      <td> | </td>
      <td>sprintf("%d", 04) => "4"</td>
    </tr>

    <tr>
      <td>sprintf("%d",'05') => "5"</td>
      <td> | </td>
      <td>sprintf("%d", 05) => "5"</td>
    </tr>

    <tr>
      <td>sprintf("%d",'06') => "6"</td>
      <td> | </td>
      <td>sprintf("%d", 06) => "6"</td>
    </tr>

    <tr>
      <td>sprintf("%d",'07') => "7"</td>
      <td> | </td>
      <td>sprintf("%d", 07) => "7"</td>
    </tr>

    <tr>
      <td>sprintf("%d",'08') => error</td>
      <td> | </td>
      <td>sprintf("%d", 08) => error</td>
    </tr>

    <tr>
      <td>sprintf("%d",'09') => error</td>
      <td> | </td>
      <td>sprintf("%d", 09) => error</td>
    </tr>

  </tbody></table>

 By pre-prepending the “0” to the numbers, they are being marked as ‘octal’. [Wikipedia](https://en.wikipedia.org/wiki/Octal) defines octal numbers as

> “The octal numeral system, or oct for short, is the base-8 number system, and uses the digits 0 to 7. Octal numerals can be made from binary numerals by grouping consecutive binary digits into groups of three (starting from the right).”
> 

So, 08 and 09 are not octal numbers.

### Solution

This is why this checkout error did not occur on every order whose payment expiration month had a leading “0”, only August (08) and September (09) were susceptible as the leading ‘0’ indicates we are passing in an octal of which 08 and 09 are not valid examples of. So, I made Spree send integers (sprintf("%d",8) #=> "8" and sprintf("%d",9) #=> "9") so that the leading “0” would not get sent (thereby not trying to pass them as octals). I created a app/models/spree/credit_card_decorator.rb file with the contents

```ruby
Spree::CreditCard.class_eval do
  def expiry=(expiry)
    if expiry.present?
      self[:month], self[:year] = expiry.delete(' ').split('/')
      self[:year] = "20" + self[:year] if self[:year].length == 2
      self[:year] = self[:year].to_i
      self[:month] = self[:month].to_i
    end
  end
end
```

After adding this, I tested it in the browser and there were no more checkout errors! I hope you’ve found this interesting and helpful, thanks for reading!


