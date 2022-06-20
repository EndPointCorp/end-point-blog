---
author: Steph Skardal
title: 'Spree and Authorize.Net: Authorization and Capture Quick Tip'
github_issue_number: 295
tags:
- ecommerce
- rails
- spree
date: 2010-04-26
---

Last week I did a bit of reverse engineering on payment configuration in Spree. After I successfully setup Spree to use Authorize.net for a client, the client was unsure how to change the Authorize.Net settings to perform an authorize and capture of the credit card instead of an authorize only.

<a href="/blog/2010/04/spree-authorizenet-authorization/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5464601012045345282" src="/blog/2010/04/spree-authorizenet-authorization/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 184px;"/></a>

The requested settings for an Authorize.Net payment gateway on the Spree backend.

I researched in the Spree documentation for a bit and then sent out an email to the End Point team. [Mark Johnson](/team/mark-johnson/) responded to my question on authorize versus authorize and capture that the Authorize.Net request type be changed from “AUTH-ONLY” to “AUTH_CAPTURE”. So, my first stop was a grep of the activemerchant gem, which is responsible for handling the payment transactions in Spree. I found the following code in the gem source:

```ruby
# Performs an authorization, which reserves the funds on the customer's credit card, but does not
# charge the card.
def authorize(money, creditcard, options = {})
  post = {}
  add_invoice(post, options)
  add_creditcard(post, creditcard)
  add_address(post, options)
  add_customer_data(post, options)
  add_duplicate_window(post)

  commit('AUTH_ONLY', money, post)
end

# Perform a purchase, which is essentially an authorization and capture in a single operation.
def purchase(money, creditcard, options = {})
  post = {}
  add_invoice(post, options)
  add_creditcard(post, creditcard)
  add_address(post, options)
  add_customer_data(post, options)
  add_duplicate_window(post)

  commit('AUTH_CAPTURE', money, post)
end
```

My next stop was the Spree payment_gateway core extension. This extension is included as part of the Spree core. It acts as a layer between Spree and the payment gateway gem and can be swapped out if a different payment gateway gem is used without requiring changing the transaction logic in the Spree core. I searched for purchase and authorize in this extension and found the following:

```ruby
def purchase(amount, payment)
  #combined Authorize and Capture that gets processed by the ActiveMerchant gateway as one single transaction.
  response = payment_gateway.purchase((amount * 100).round, self, gateway_options(payment))
  ...
end
def authorize(amount, payment)
  # ActiveMerchant is configured to use cents so we need to multiply order total by 100
  response = payment_gateway.authorize((amount * 100).round, self, gateway_options(payment))
  ...
end
```

My last stop was where I found the configuration setting I was looking for, Spree::Config[:auto_capture], by searching for authorize and purchase in the Spree application code. I found the following logic in the Spree credit card model:

```ruby
def process!(payment)
  begin
    if Spree::Config[:auto_capture]
      purchase(payment.amount.to_f, payment)
      payment.finalize!
    else
      authorize(payment.amount.to_f, payment)
    end
  end
end
```

The auto_capture setting defaults to false, not surprisingly, so it can be updated with one of the following changes.

```ruby
# *_extension.rb:
def activate
  AppConfiguration.class_eval do
    preference :auto_capture, :boolean, :default => true
  end
end

# EXTENSION_DIR/config/initializers/*.rb:
if Preference.table_exists?
  Spree::Config.set(:auto_capture => true)
end
```

After I found what I was looking for, I googled “Spree auto_capture” and found a few references to it and saw that it was briefly mentioned in the [Spree documentation payment information](https://web.archive.org/web/20101128005539/http://spreecommerce.com/documentation/payments.html). Perhaps more documentation could be added around how the Spree auto_capture preference setting trickles down through the payment gateway processing logic, or perhaps this article provides a nice overview of the payment processing layers in Spree.
