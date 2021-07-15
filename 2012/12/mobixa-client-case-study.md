---
author: Steph Skardal
title: 'Mobixa: A Client Case Study'
github_issue_number: 729
tags:
- clients
- php
- rails
- case-study
date: 2012-12-05
---

<a href="http://www.mobixa.com/"><img border="0" height="122" src="/blog/2012/12/mobixa-client-case-study/image-0.png" width="324"/></a>

A few weeks ago we saw the official (and successful!) website launch for one of our clients, [Mobixa](http://www.mobixa.com/). Mobixa will buy back your used iPhones and/or provide you with information about when you should upgrade your existing phone and sell it back. Right now, Mobixa is currently buying back iPhones and advising on iPhones and Androids. End Point has been working with Mobixa for several months now. This article outlines some of the interesting project notes and summarizes End Point’s diverse skillset used for this particular website.

### Initial Framework

Mobixa initially wanted a an initial proof of concept website without significant investment in development architecture because the long-term plan and success was somewhat unknown at the project unset. The initial framework comprised of basic HTML combined with a bit of logic driven by PHP. After a user submitted their phone information, data was sent to [Wufoo](http://www.wufoo.com/) via a Wufoo provided PHP-based API, and data was further handled from Wufoo. Wufoo is an online form builder that has nice export capabilities, and painlessly integrates with MailChimp.

This initial architecture was suitable for collecting user information, having minimal local database needs and allowing external systems (e.g. Wufoo, MailChimp) to handle much of the user logic. However, it became limiting when the idea of user persistence came into play – the long-term goal will be to allow users to modify previous submissions and look up their order information, essentially a need for basic user account management functionality. For that reason, we made a significant switch in the architecture, described below.

### Framework #2: Rails 3

Because of the limiting nature of a database-less application with externally managed data and as business needs for users increased, we decided to make the move to Rails. End Point has a large team of Rails developers, Rails is a suitable framework for developing applications efficiently, and we are experienced in working with Rails plugins such as [RailsAdmin](https://github.com/sferik/rails_admin), [Devise](https://github.com/plataformatec/devise), and [CanCan](https://github.com/ryanb/cancan), which immediately provide a configurable admin interface, user authentication, and user authentication to the application. In the process of moving to Rails, we eliminated the middle-man Wufoo to integrate with the shipping fulfillment center and MailChimp directly.

The current Mobixa site runs on Rails 3, [Nginx](http://nginx.org/) and [Unicorn](http://unicorn.bogomips.org/) backed by PostgreSQL, leverages End Point’s [DevCamps](http://www.devcamps.org/) to allow multiple developers to simultaneously add features and maintain the site painlessly, and uses RailsAdmin, Devise, and CanCan. It features a responsive design and uses advanced jQuery techniques. The focus of the site is still a simple HTML page that passes user-entered information to the local database, but several user management features have been added as well as the ability to sell back multiple phones at a time.

### MailChimp Integration

In my search for a decent Rails MailChimp integration gem, I found [gibbon](https://github.com/amro/gibbon). Gibbon is fairly simple - it’s an API wrapper for interacting with MailChimp. Any API capabilities and methods available in MailChimp can be called via Gibbon. The integration looks something like this:

```ruby
# user model
def update_mailchimp
  gb = Gibbon.new(*api_key*, { :timeout => 30 })

  info = gb.list_member_info({ :id => *list_id*, :email_address => self.email })

  if info["success"] == 1
    gb.listUpdateMember({ :id => *list_id*,
                          :email_address => self.email,
                          :merge_vars => self.mailchimp_data })
  else
    gb.list_subscribe({ :id => *list_id*,
                        :email_address => self.email,
                        # additional new user arguments #
                        :merge_vars => self.mailchimp_data })
  end
end
```

The above method instantiates a connection to Mailchimp and checks if the user is already subscribed to the Mailchimp list. If the user is subscribed, the listUpdateMember method is called to update the user subscription information. Otherwise, list_subscribe is called to add the user to the Mailchimp list.

### What’s Next?

In addition to expanding the product buyback capabilities, we expect to integrate additional features such as external-API driven address verification, social media integration, referral management, and more advanced user account management features. The project will continue to involve various members of our team such as [Richard](/team/richard-templet), [Greg D.](/team/greg-davidson), Tim Case, [Kamil](/blog/authors/kamil-ciemniewski), [Josh W.](/team/josh-williams) and me.
