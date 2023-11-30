---
author: Matt Galvin
title: Unable to Bcc in mail, Spree 2.0 Stable Rails 3.2.14
github_issue_number: 991
tags:
- email
- spree
date: 2014-06-09
---

Hello again all.  As usual, I was working on a [Spree Commerce](https://spreecommerce.org/) website.  I recently encountered an issue when trying to bcc order confirmation emails.  Others have been asking about this on [Github](https://github.com/spree/spree/issues/4484) and also on the [Spree mailing list](https://groups.google.com/forum/#!msg/spree-user/50yjID6znOE/QSr51V1xgrUJ), so it was time to write about the problem and the solution that worked for me.

First, I’d like to briefly describe the use case here.  As with any typical e-commerce site, a user visits the site, adds some items to their cart, and checks out.  After which, an order confirmation (order summary) email is sent to the user with their order details and any extra information provided by the seller.

Spree pretty much handles all this for you automatically.  What about if you as the business owner would like a copy of this e-mail?  Easy enough.  If you review the [Spree documentation](https://web.archive.org/web/20160606002703/http://guides.spreecommerce.org/user/configuring_mail_methods.html) you will see simple instructions for the  “Mail Method Settings” to set up in the Spree Admin Interface.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/06/unable-to-bcc-in-mail-spree-20-stable/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/06/unable-to-bcc-in-mail-spree-20-stable/image-0.png"/></a></div>

Ok, so let’s say you follow all the instructions and start placing test orders (or receiving real ones), and you’re not getting bcc’d?  This is where it gets tricky, so let’s check out a few things:

1. Check the logs
    
    Check to see if Spree/Rails is attempting to send the confirmation email to your Bcc recipient
1. Try development, test, & production modes
    
    If the Bcc email is not getting sent, keep following along for the solution
1. Ensure the interceptor works by adding a value into “INTERCEPT EMAIL ADDRESS” via the admin.  If emails are being intercepted you know the the interceptor is working.  Why is that important? Because, that is also where the bcc code is.
    
    core/lib/spree/mail_interceptor.rb
    
    ```
    module Spree
      module Core
        class MailInterceptor
          def self.delivering_email(message)
            return unless MailSettings.override?
    
            if Config[:intercept_email].present?
              message.subject = "#{message.to} #{message.subject}"
              message.to = Config[:intercept_email]
            end
    
            if Config[:mail_bcc].present?
              message.bcc ||= Config[:mail_bcc]
            end
          end
        end
      end
    end
    ```
1. You can ensure that more than one email can be sent by updating `mail(to: @order.email, from: from_address, subject: subject)` to be an array of emails, like `mail(to: [@order.email, "some_other_email@somewhere.com"], from: from_address, subject: subject)`
    
    core/app/mailers/spree/order_mailer.rb
    
    ```ruby
    module Spree
      class OrderMailer < BaseMailer
        def confirm_email(order, resend = false)
          @order = order.respond_to?(:id) ? order : Spree::Order.find(order)
          subject = (resend ? "[#{Spree.t(:resend).upcase}] " : '')
          subject += "#{Spree::Config[:site_name]} #{Spree.t('order_mailer.confirm_email.subject')} ##{@order.number}"
          mail(to: @order.email, from: from_address, subject: subject)
        end
    
        def cancel_email(order, resend = false)
          @order = order.respond_to?(:id) ? order : Spree::Order.find(order)
          subject = (resend ? "[#{Spree.t(:resend).upcase}] " : '')
          subject += "#{Spree::Config[:site_name]} #{Spree.t('order_mailer.cancel_email.subject')} ##{@order.number}"
          mail(to: @order.email, from: from_address, subject: subject)
        end
      end
    end
    ```

At this point, you’ve verified the interceptor works, and the mailer can definitely send more than one email.  Here is the final piece that is not mentioned anywhere on the Spree site, or any resolutions for any posts I had found: you may need to contact your hosting provider and ask them to make any necessary adjustments to allow for the bcc messages.  I saw that several people have gotten hung up on this and I hope this post has saved you some time.  If you are still having trouble, please feel free to reach out in the comments.  You can refer to the [Spree issue](https://github.com/spree/spree/issues/4484) I created on this topic some time ago.
