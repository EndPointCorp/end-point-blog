---
author: Matt Galvin
gh_issue_number: 991
tags: email, spree
title: Unable to Bcc in mail, Spree 2.0 Stable Rails 3.2.14
---

Hello again all.  As usual, I was working on a [Spree Commerce](http://spreecommerce.com/) website.  I recently encountered an issue when trying to bcc order confirmation emails.  Others have been asking about this on [Github](https://github.com/spree/spree/issues/4484) and also on the [Spree mailing list](https://groups.google.com/forum/#!msg/spree-user/50yjID6znOE/QSr51V1xgrUJ), so it was time to write about the problem and the solution that worked for me.

First, I'd like to briefly describe the use case here.  As with any typical e-commerce site, a user visits the site, adds some items to their cart, and checks out.  After which, an order confirmation (order summary) email is sent to the user with their order details and any extra information provided by the seller.

Spree pretty much handles all this for you automatically.  What about if you as the business owner would like a copy of this e-mail?  Easy enough.  If you review the [Spree documentation](http://guides.spreecommerce.com/user/configuring_mail_methods.html) you will see simple instructions for the  "Mail Method Settings" to set up in the Spree Admin Interface.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/06/09/unable-to-bcc-in-mail-spree-20-stable/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/06/09/unable-to-bcc-in-mail-spree-20-stable/image-0.png"/></a></div>

Ok, so let's say you follow all the instructions and start placing test orders (or receiving real ones), and you're not getting bcc'd?  This is where it gets tricky, so let's check out a few things:

1. Check the logs

    - Check to see if Spree/Rails is attempting to send the confirmation email to your Bcc recipient

1. Try development, test, & production modes

    - If the Bcc email is not getting sent, keep following along for the solution

1. Ensure the interceptor works by adding a value into "INTERCEPT EMAIL ADDRESS" via the admin.  If emails are being intercepted you know the the interceptor is working.  Why is that important? Because, that is also where the bcc code is.

    - core/lib/spree/mail_interceptor.rb ~~~ruby
5 module Spree
  6   module Core
  7     class MailInterceptor
  8       def self.delivering_email(message)
  9         return unless MailSettings.override?
 10
 11         if Config[:intercept_email].present?
 12           message.subject = "#{message.to} #{message.subject}"
 13           message.to = Config[:intercept_email]
 14         end
 15
 16         if Config[:mail_bcc].present?
 17           message.bcc ||= Config[:mail_bcc]
 18         end
 19       end
 20     end
 21   end
 22 end
```

1. You can ensure that more than one email can be sent by updating

mail(to: @order.email, from: from_address, subject: subject)

to be an array of emails, like

mail(to: [@order.email, "some_other_email@somewhere.com"], from: from_address, subject: subject)

    - core/app/mailers/spree/order_mailer.rb ~~~ruby
1 module Spree
  2   class OrderMailer < BaseMailer
  3     def confirm_email(order, resend = false)
  4       @order = order.respond_to?(:id) ? order : Spree::Order.find(order)
  5       subject = (resend ? "[#{Spree.t(:resend).upcase}] " : '')
  6       subject += "#{Spree::Config[:site_name]} #{Spree.t('order_mailer.confirm_email.subject')} ##{@order.number}"
  7       mail(to: @order.email, from: from_address, subject: subject)
  8     end
  9
 10     def cancel_email(order, resend = false)
 11       @order = order.respond_to?(:id) ? order : Spree::Order.find(order)
 12       subject = (resend ? "[#{Spree.t(:resend).upcase}] " : '')
 13       subject += "#{Spree::Config[:site_name]} #{Spree.t('order_mailer.cancel_email.subject')} ##{@order.number}"
 14       mail(to: @order.email, from: from_address, subject: subject)
 15     end
 16   end
 17 end
```

At this point, you've verified the interceptor works, and the mailer can definitely send more than one email.  Here is the final piece that is not mentioned anywhere on the Spree site, or any resolutions for any posts I had found: you may need to contact your hosting provider and ask them to make any necessary adjustments to allow for the bcc messages.  I saw that several people have gotten hung up on this and I hope this post has saved you some time.  If you are still having trouble, please feel free to reach out in the comments.  You can refer to the [Spree issue](https://github.com/spree/spree/issues/4484) I created on this topic some time ago.
