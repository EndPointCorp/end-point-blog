---
author: Steph Skardal
title: 'RailsConf 2010: Spree and The Ecommerce Smackdown, Or Not'
github_issue_number: 316
tags:
- conference
- ecommerce
- ruby
- rails
- spree
date: 2010-06-09
---

Spree has made a good showing at RailsConf 2010 so far this year, new site and logo released this week:

<a href="https://spreecommerce.org/"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5480830761567477442" src="/blog/2010/06/railsconf-2010-ecommerce-smackdown/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 176px; height: 82px;"/></a>

It started off in yesterday’s Ecommerce Panel with Sean Schofield, a former End Point employee and technical lead on Spree, Cody Fauser, the CTO of [Shopify](https://www.shopify.com/) and technical lead of [ActiveMerchant](http://activemerchant.org/), Nathaniel Talbott, co-founder of [Spreedly](https://www.spreedly.com/), and Michael Bryzek, the CTO and founder of [Gilt Groupe](https://www.gilt.com/boutique/).

The panel gave a nice overview on a few standard ecommerce questions:

- **My client needs a store—​what technology should I use? Why shouldn’t I just reinvent the wheel?**
The [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) reps evangelized their technologies well, explaining that a hosted solution is good as a relatively immediate solution that has minimum cost and risk to a business. A client [of SaaS] need not be concerned with infrastructure or transaction management initially, and a hosted solution comes with *freebies* like the use of a CDN that improve performance. A hosted solution is a good option to get the product out and make money upfront. Also, both SaaS options offer elegant APIs.
- **How do you address client concerns with security?**
Again, the SaaS guys stressed that there are a few mistakes guaranteed to kill your business and one of those things includes dropping the ball on security, specifically credit card security. The hosted solutions worry about credit card security so the client doesn’t have to. One approach to PCI compliance is to securely post credit card information to a 3rd party secure payment request API as the external requests minimizes the risk to a company. Michael (Gilt) discussed The Gilt Groupe’s intricate process in place for security and managing encryption keys. Nathaniel (Spreedly) summarized that rather than focus on PCI compliance specifically, it’s more important to have the right mindset about financial data security.
- **What types of hosting issues should I be concerned about?**
Next, the SaaS guys led again on this topic by explaining that they worry about the hosting—​that a monthly hosted solution cost (Shopify.com starts at $24/month) is less than the cost of paying a developer who knows your technology in an emergency situation when your site goes down on subpar hosting. Michael (Gilt) made a good point by considering that everything is guaranteed to fail at some point—​how do you (client) feel about taking the risk of that? do you just trust that the gateway is always up? One interesting thing mentioned by the SaaS guys is that technically, you should not be able to host any solution in the cloud if you touch credit card data, although you may likely be able to “get away with it”—​I’m not sure if this was a scare tactic, but it’s certainly something to consider. One disadvantage to hosting in the cloud are that you can’t do forensic investigation after a problem if the machine has disappeared.

The remaining panel time was spent on user questions that focused on payment and transaction details specifically. There were a few bits of valuable transaction management details covered. Cody (Shopify) has no plans of developing or expanding on alternative payment systems because there isn’t a good ROI. The concept of having something like OIDs for credit cards to shop online would likely not receive support from credit card companies, but PayPal [kinda] serves this role currently. Nathaniel (Spreedly) covered interesting details on how user transaction information is tracked: From day one, everything that is stacked on a users account is a transaction model object that mutate the user transaction state over time. The consensus was that a transaction log is the way to track user transaction information—​you should never lose track of any dollarz. On the topic of data, Shopify and Spreedly collect and store all data—​the first client step is to sell stuff, then later the client can come back to analyze data for business intelligence such as ROI per customer demographic, the average lifespan of a customer, or the computed value of a customer.

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5480830768195378674" src="/blog/2010/06/railsconf-2010-ecommerce-smackdown/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 750px;"/>
Now I take a break for an image, because it’s important to have images in blog articles. Here is my view from the plane as I traveled to Baltimore.

After the panel, Spree had a Birds of a Feather session in the evening, which focused more on Spree. Some topics covered:

- **What is the current Spree road map to work on Rails 3? Extension development in Rails 3?**

As Rails 3 stabilizes over time, Spree will begin to transition but no one’s actively doing Rails 3 work at this point. I spoke with Brian Quinn, a member of the Spree core team, who mentioned that he’s recently spent time on investigating [resource controller](https://github.com/jamesgolick/resource_controller) versus inherited resources or something else. The consensus was that people don’t like Resource Controller (one attendee mentioned they used the Spree data model, but ripped out all of the controllers), but that a sensible alternative will need to be implemented at some point. [Searchlogic](https://github.com/binarylogic/searchlogic), the search gem used in Spree search functionality, has no plans to upgrade to Rails 3, so Spree will also have to make sensible decisions for search. The Rails 3 generators have a reputation to be good, so this may trickle down to have positive effects on Spree extension development. Rails 3 also encourages more modular development, so the idea with Spree is that things will gradually be broken into more modular pieces, or gems, and the use of [Bundler](https://github.com/bundler/bundler) will tie the Spree base components together.
- **How’s test coverage in Spree?**
Bad. Contributors appreciated.
- **I got scared after I went to the Ecommerce Panel talk—​what’s PCI compliance and security like in Spree?**
Spree is PCI compliant with the assumption that the client doesn’t store credit cards—​there is (was?) actually a Spree preference setting that defaults to not store credit cards in the database, but it will result in unencrypted credit cards being stored in the database if set to true. The Spree core team [recently mentioned](https://groups.google.com/forum/#!topic/spree-user/F-Xp15e64k0) that this might be removed from the core. Offsite credit card use such as Authorize.Net CIM implementation is included in the Spree core.

The Spree Birds of a Feather session was good: the result of the session was likely a comprehension of the short and long term road map of Spree is as it transitions to Rails 3. This blog post was going to end here, but luckily I sat next to a Shopify employee this morning and learned more about Shopify. My personal opinion of the ecommerce panel was that advantages of the hosted solutions were appropriately represented, but there wasn’t much focus on Spree and the disadvantages of SaaS weren’t covered much. I learned that one major disadvantage to Shopify is that they don’t have user accounts, however, user accounts are in development. Shopify is also [obviously] not a good choice for sites that have customization but there is a large community of applications. One example of a familiar customization is building a site with a one-deal-at-a-time business model ([SteepAndCheap.com](https://www.steepandcheap.com/), [JackThreads.com’s](https://jackthreads.com/) former business model)—​this would be difficult with Shopify. Some highlights of Shopify include it’s template engine, based on [Liquid](https://shopify.github.io/liquid/), it has a great API, where you can do most things except place an order, and that it scales really well.

Obviously, I [drink](/blog/2010/05/spree-multi-store-architecture/) [the](/blog/2010/03/spree-software-development/) [Spree](/blog/2010/01/rails-ecommerce-spree-hooks-tutorial/) [kool-aid](/blog/2010/03/spree-heroku-development-environment/) [often](/blog/2010/06/spree-vs-magento-feature-list/), so I learned more from the panel, BOF, and hallway talk on the subject of SaaS, or hosted Rails ecommerce solutions. The BOF session covered details on the Spree to Rails 3 (hot topic!) transition nicely.
