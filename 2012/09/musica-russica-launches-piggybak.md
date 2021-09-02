---
author: Steph Skardal
title: Musica Russica Launches with Piggybak
github_issue_number: 687
tags:
- clients
- ecommerce
- piggybak
- rails
date: 2012-09-03
---

<a href="http://www.musicarussica.com/"><img border="0" src="/blog/2012/09/musica-russica-launches-piggybak/image-0.png" width="745"/></a>

The new home page for Musica Russica.

Last week, we launched a new site for [Musica Russica](http://www.musicarussica.com/). The old site was running on an outdated version of Lasso and Filemaker and was approximately 15 years old. Although it was still chugging along, finding hosting support and developers for an outdated platform becomes increasingly challenging as time goes on. The new site runs on [Ruby on Rails 3](http://rubyonrails.org/) with [Nginx](http://nginx.org/) and [Unicorn](http://unicorn.bogomips.org/) and uses open source Rails gems [RailsAdmin](https://github.com/sferik/rails_admin), [Piggybak](https://github.com/piggybak/piggybak), [CanCan](https://github.com/ryanb/cancan) and [Devise](https://github.com/plataformatec/devise). RailsAdmin is a great open source Rails Admin tool that I've blogged about before ([here](/blog/2011/08/railsadmin-gem-ecommerce), [here](/blog/2012/03/cancan-railsadmin), and [here](/blog/2012/02/railsadmin-import-part-2)). Piggybak is End Point's home grown light-weight ecommerce platform, also blogged about several times ([here](/blog/2012/01/piggybak-mountable-ecommerce-ruby-on), [here](/blog/2012/01/activerecord-callbacks-ecommerce-order), and [here](/blog/2012/06/rbenv-passenger-upgrade)). Below are a few more details on the site:

- The site includes Rails 3 goodness such as an elegant and thorough MVC architecture, advanced routing to encourage clean, user-friendly URLs, the ability to integrate modular elements (Piggybak, RailsAdmin) with ease, and several built-in performance options. The site also features a few other popular Rails gems such as [Prawn](http://prawn.majesticseacreature.com/) (for printing order and packing slip PDFs), [Rack-SSL-Enforcer](https://github.com/tobmatth/rack-ssl-enforcer) (a nice tool for enforcing SSL pages), [exception_notification](https://github.com/rails/exception_notification) (a small tool to configure sending emails on Rails exceptions), and [Paper Trail](https://github.com/airblade/paper_trail) (a gem to track changes on your models).
- The site features complex, feature-rich search run by [Sphinx](http://sphinxsearch.com/) with the popular Rails gem [ThinkingSphinx](http://pat.github.com/ts/en/). The search includes standard features such as selecting items listed per page, sort by various product attributes and wildcard text search. Although we've used Solr on several recent Rails projects, we wanted to go with Sphinx here to avoid the Tomcat and Java requirements. After working with both in depth, I'd conclude that both Sphinx and Solr offer very similar features.
- The site has a very custom data model. With the use of [Piggybak](https://github.com/piggybak/piggybak), any Rails model can become a sellable item, which gives us the ability to customize each data model without affecting all sellable products. This opportunity suits Musica Russica well because they offer very different product types such as books, sheet music, CDs, and sheet music collections. Additional features (taxonomy, cross-sell, upsell) in the application are not constrained to assumptions that traditional monolithic ecommerce applications make.
- The site introduces downloadable products, described more [in this article](/blog/2012/02/download-functionality-rails-ecommerce). A user purchasing downloadable products is required to register, and then has access to their purchased downloadables after purchase. Downloadable orders also include free shipping. Piggybak needed minor customization to support downloadable products.
- The site also features integration with the [Elavon](http://gateway.elavon.com/) payment gateway. This is the first time that End Point has worked with Elavon. Elavon is supported by ActiveMerchant, so adding support for Elavon simply required hooking into ActiveMerchant's Elavon module.

It was exciting to build a custom Rails ecommerce site from the ground-up, and the site certainly showcases End Point's wide range of ecommerce expertise ranging from hosting with modern cutting-edge servers to development of popular front-end ecommerce features with advanced open source tools.
