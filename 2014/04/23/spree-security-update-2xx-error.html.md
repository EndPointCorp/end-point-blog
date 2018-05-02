---
author: Matt Galvin
gh_issue_number: 969
tags: ecommerce, ruby, rails, security, spree, update
title: Spree Security Update 2.x.x Error, undefined method ‘assume_from_symbol’ for Money:Class (ActionView::Template::Error)
---



On March 25, 2014 Spree Commerce posted an announcement that there was a security vulnerability for all Spree 2.x.x versions. As reported on [Spree’s website](https://spreecommerce.org/pages/blog/security-update-spree-2), 

> "The exploit would require the attacker to randomly guess valid order numbers, but once achieved, the technique would reveal private customer information associated with the order. **Credit card details are never stored in Spree and were never at risk by this exploit.**"

So, this update is pretty typical and as usual, you should make sure nothing has broken with any changes that were made. I wanted to note a couple of "gotchas" with this most recent update however.

The first of which is probably obvious and really more of a reminder as sometimes people forget. Further, the [instructions](https://spreecommerce.org/pages/blog/security-update-spree-2) for this update in the Spree docs don’t mention it, so, as a reminder - after updating be sure to run

```shell
$ bundle exec rake railties:install:migrations
$ bundle exec rake db:migrate
```

Now, here is the tricky one. After updating and installing/running your migrations you may find that you are getting an error:

```
undefined method `assume_from_symbol' for Money:Class (ActionView::Template::Error)
```

I have been unable to find anything on this in the Spree documentation but the problem is that in the update the money gem version 6.1.1 breaks the product display. The work around is to lock the money gem at 6.0.1. So, specify version 6.0.1 for the money gem in your Gemfile

```ruby
gem 'money', '=6.0.1'
```

Updating Spree versions can sometimes be a little tense if things start breaking and you don’t know why. I hope that if this error brought you here this article has saved you some time.


