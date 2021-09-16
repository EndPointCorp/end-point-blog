---
author: James Bennett
title: 'Learning Spree: 10 Intro Tips'
github_issue_number: 342
tags:
- ecommerce
- rails
- spree
date: 2010-08-26
---

In climbing the learning curve with Spree development here are some observations I’ve made along the way:

1. **Hooks make view changes easier** — I was surprised at how fast I could implement certain kinds of changes because Spree’s hook system allowed me to inject code without requiring overriding a template or making a more complicated change. Check out Steph’s blog entries on hooks [here](/blog/2010/01/rails-ecommerce-spree-hooks-tutorial) and [here](/blog/2010/01/rails-ecommerce-spree-hooks-comments), and the [Spree documentation on hooks and themes](https://web.archive.org/web/20091231114016/http://spreecommerce.com/documentation/theming.html).

1. **Core extensions aren’t always updated** — One of the biggest surprises I found while working with Spree is that some Spree core extensions aren’t maintained with each release. My application used the Beanstream payment gateway. Beanstream authorizations (without capture) and voids didn’t work out of the box with Spree 0.11.0.

1. **Calculators can be hard to understand** — I wrote a custom shipping calculator and used calculators with coupons for the project and found that the data model for calculators was a bit difficult to understand initially. It took a bit of time for me to be comfortable using calculators in Spree. Check out the [Spree documentation on calculators](https://web.archive.org/web/20091231113503/http://spreecommerce.com/documentation/calculators.html) for more details.

1. **Plugins make the data model simpler after learning what they do** — I interacted with the plugins [resource_controller](http://jamesgolick.com/2007/10/19/introducing-resource_controller-focus-on-what-makes-your-controller-special.html), [state_machine](https://web.archive.org/web/20160619151126/http://www.pluginaweek.org/2009/03/08/state_machine-one-machine-to-rule-them-all/), and [will_paginate](https://github.com/mislav/will_paginate/wiki) in Spree. All three simplified the models and controllers interface in Spree and made it easier to identify the core behavior of Spree models and controllers.

1. **Cannot revert migrations** — Spree disables the ability to revert migrations due to complications with extensions which makes it difficult to undo simple database changes. This is more of a slight annoyance, but it complicated some aspects of development.

1. **Coupons are robust, but confusing** — Like calculators, the data model for coupons is a bit confusing to learn but it seems as though it’s complicated to allow for robust implementations of many kinds of coupons. [Spree’s documentation on coupons and discounts](https://web.archive.org/web/20091231113934/http://spreecommerce.com/documentation/coupons_and_discounts.html) provides more information on this topic.

1. **Solr extension works well** — I replaced Spree’s core search algorithm in the application to allow for customization of the indexed fields and to improve search performance. I found that the [Solr extension for Spree](https://github.com/romul/spree-solr-search) worked out of the box very well. It was also easy to customize the extension to perform indexation on additional fields. The only problem is that the Solr server consumes a large amount of system resources.

1. **Products & Variants** — Another thing that was a bit strange about Spree is that every product has at least one variant referred to as the master variant that is used for baseline pricing information. Spree’s data model was foreign to me as most ecommerce systems I’ve worked with have had a much different product and variant data model.

1. **Routing** — One big hurdle I experienced while working with Spree was how Rails routing worked. This probably stemmed from my inexperience with the resource_controller plugin, or from the fact that one of the first times I worked with Rails routing was to create routes for a nested resource. Now that I have learned how routing works and how to use it effectively, I believe it was well worth the initial struggle.

1. **Documentation & Community** — I found that the [documentation for Spree](https://web.archive.org/web/20091231114006/http://spreecommerce.com/documentation/index.html) was somewhat helpful at times, but the [spree-user Google group](https://groups.google.com/forum/#!forum/spree-user) was more helpful. For instance, I got a response on Beanstream payment gateway troubleshooting from the Spree extension author fairly quickly after asking on the mailing list.

I believe that Spree is an interesting project with a somewhat unusual approach to providing a shopping cart solution. Spree’s approach of trying to implement 90% of a shopping cart system is very different from some other shopping cart systems which overload the code base to support many features. The 90% approach made some things easier and some things harder to do. Things like hooks and extensions makes it far easier to customize than I expected it would be, and it also seems like it helps avoid the build up of spaghetti code which comes from implementing a lot of features. However, allowing for a "90%" solution seems to make some things like calculators a bit harder to understand when getting started with Spree, since the implementation is general and robust to allow for customization.
