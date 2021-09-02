---
author: Steph Skardal
title: Sunsetting Piggybak, A Ruby on Rails Ecommerce Gem
github_issue_number: 1382
tags:
- ecommerce
- ruby
- rails
- open-source
date: 2018-02-14
---

<img src="/blog/2018/02/sunsetting-piggybak/piggybak.jpg" alt="Screenshot of website for Piggybak: Open Source Ruby on Rails Ecommerce" /><br />

Hi there! I’m Steph, the original creator and not-very-good maintainer
of [Piggybak](https://github.com/piggybak/piggybak), a modular ecommerce
platform written in Ruby on Rails. With the help of End Point, I created
Piggybak after building a custom Ruby on Rails ecommerce application
for one of our clients here at End Point.

My goal with Piggybak was to create a lightweight, modular ecommerce
platform in the form of a Ruby on Rails gem that could be combined with
other Ruby on Rails gems for quick setup. Over the years, End Point has
had much success working in [Interchange](http://www.icdevgroup.org/), an
ecommerce framework written in Perl.  The web stack has evolved greatly
over the years, as has the capacity for modularity and the ability to
decouple front-end and back-end architecture.

Fast forward about 4 years after Piggybak was released, and we’ve
decided to retire it. Not only did I leave the maintenance up to End Point
after I left to work as an in-house software engineer for the last couple
of years, but I was also in a position to evaluate using Piggybak as
the base for a custom solution.

While I think there are some great Ruby on Rails gems to help support
your ecommerce application (see below), one of the main things I realized
was that the modularity in Piggybak often doesn’t suit the needs for the
target audience of custom Ruby on Rails ecommerce platforms.

These days, here’s my oversimplified categorization of those looking
for ecommerce solutions, divided into two audiences:

<b>Audience #1: Boilerplate Saas with Theme Customization</b><br />
Those sellers where boilerplate ecommerce solutions work, with simple
product and variant modeling. Shopify, Magento, BigCommerce, WooCommerce
can be decent popular options for that audience, but there are so many
other options out there.
  
<b>Audience #2: Custom Ecommerce in Ruby on Rails</b><br />
Companies going this route have custom enough needs where a small
team can develop and maintain a custom solution, using Ruby on Rails
efficiently that don’t require them to depend on a pre-existing data
model or business rule.
 
Not only did Piggybak suffer from a lack of community involvement, but it
also didn’t suit the needs of the two audiences listed above. Because
it was complex enough written in the form of a Rails gem (engine),
it required a developer with some knowledge to install and customize
further. And because it defined assumptions around the product-variant
data model and business rules for inventory and payment management,
it wasn’t necessarily a good fit for custom ecommerce needs.

### Other Ruby on Rails Gems

While I’m sad to sunset Piggybak, I still believe Rails offers great
options for ecommerce needs, including these popular Ruby on Rails gems:

* [Rails_admin](https://github.com/sferik/rails_admin), active_admin (no longer maintained), [administrate](https://github.com/thoughtbot/administrate)
* [Carrierwave](https://github.com/carrierwaveuploader/carrierwave): File attachment management. Has decent third party support.
* [Devise](https://github.com/plataformatec/devise). User authentication marches on.
* [Cancancan](https://github.com/CanCanCommunity/cancancan). User authorization.
* [Kaminari](https://github.com/kaminari/kaminari). Pagination.
* [RSpec](http://rspec.info/), [FactoryBot](https://github.com/thoughtbot/factory_bot), [Capybara](https://github.com/teamcapybara/capybara), the testing stack I am most familiar with.
* [ActiveShipping](https://github.com/Shopify/active_shipping). Shipping for ecommerce.
* [ActiveMerchant](https://github.com/activemerchant/active_merchant). Payment gateways for ecommerce.

If you are wondering if there are any Ruby on Rails ecommerce gems still
out there, you can look at [Solidus](https://solidus.io/),
[Spree](https://spreecommerce.org/), and [RoR-E](http://www.ror-e.com/).
End Point has a long history with Spree, and experience with the other
two platforms, but again, the audience of those businesses choosing
a custom path may not want to be tied to the data models and business
rules adopted by these existing platforms.
