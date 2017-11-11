---
author: Tim Case
gh_issue_number: 925
tags: ecommerce, rails, spree, open-source
title: A Brief Retrospective of Spree
---

[SpreeConf NYC 2014](http://spreeconf.com/) starts on the 26th and its hard to believe that Spree is almost 7 years old! Here's a retrospective showing some notable Spree moments and major releases.

**July 15, 2007** RailsCart, the precursor to Spree, is created by Sean Schofield and gets its first commit as a Google Code project.

**February 1, 2008** Sean is hired by End Point Corporation to work on RailsCart along with its other Rails developers. End Point sponsors Spree for the next year and a half.

**February 15, 2008** RailsCart project moves from Google Code to GitHub and is renamed Spree.

**June 1, 2008** Spree 0.0.9 released: sophisticated data model for inventory.

**June 3, 2008** Product Properties added.

**June 5, 2008** Spree 0.2.0 released: adds Spree extensions.

**July 4, 2008** Zones introduced.

**Sept 8, 2008** Refactored to REST routing added state machine to order.

**October 1, 2008** New Taxonomy system introduced.

**October 2, 2008** Spree 0.4.0 released: Taxonomy, and VAT-inclusive pricing.

**November 26, 2008** Volume pricing introduced as an extension.

**November 24, 2008** Spree 0.5.0 released: new shipping framework.

**December 3, 2008** SEO friendly URLs.

**December 4, 2008** Switched from attachment_fu to paperclip for image attachments.

**February 3, 2009** Spree 0.6.0 released: friendly urls, attachment_fu to paperclip, paranoid deletion of products, standardized security model, rake tasks for translations.

**March 5, 2009** Searchlogic gem added.

**March 10, 2009** Spree 0.7.0 released: switches to ajax-based Magento-style single page checkout, order number as permalinks, French, Russian and Norwegian translations added.

**April 2, 2009** Authlogic gem added.

**April 23, 2009** Spreecommerce.com launched.

**May 4, 2009** Spree 0.8.0 released: CSS based layout using compass, sass, and blueprint, Authlogic, guest checkout, expanded functionality for prototype products, improved upgrade rake task, improved order security using tokens.

**May 18, 2009** Spree core team formalized.

**May 28, 2009** Sean Schofield leaves End Point and founds Rails Dog.

**September 22, 2009** Spree 0.9.0 released: Coupon and discount support, improved system of calculators, Thai, Hebrew, Dutch, Finish, and Mexican Spanish translations.

**September 5, 2009** Spree now 100% jQuery for all JavaScript functionality.

**March 13, 2009** Spree 0.10.0 released: Named scopes and product groups, pluggable search (Xapian, Sphinx, and Solr), theming, switch to multipage checkout, improved gateway configuration, multiple payment methods, refunds and credits, restful api.

**June 14, 2010** Spree 0.11.0 released: new look for Spree, Rails 2.3.8 compatibility.

**November 1, 2010** New extension registry.

**November 9, 2010** Spree 0.30.0 released: Rails 3 support, reorganization into multiple gems: spree_core, spree_auth, spree_api, spree_dash, spree_sample, Rails engines introduced, site extension removed, extensions become gems, improved payments with addition of state machine, simplification of adjustments, new promotion functionality, no more "vendor mode".

**December 10, 2010** Spree 0.40.0 released: switched from Authlogic to Devise for authentication.

**March 23, 2011** Spree 0.50.0 released: improved test coverage, replaced Searchlogic gem with Meta search gem.

**May 13, 2011** Spree 0.60.0 released: removal of Resource Controller.

**October 10, 2011** Announcement that Spree Commerce Inc. is formed and raised $1.5M in seed funding.

**November 7, 2011** Spree 0.70.0 Integration with rails asset pipeline, theming support, themes as engines, extension generator, promotions extended.

**January 31, 2012** Spree analytics with Jiraffe introduced.

**February 9, 2012** Spree 1.0 released, namespacing introduced, Spree referenced routes, mounting Spree engine in routes, Spree analytics, Spree dash gem, command line tool, default payment gateway Spree/Skrill Spree_usa_epay, moved gateways out of core to Spree gateway gem, Refactored preferences, polymorphic adjustments, removed helpers and JavaScript related to VAT, removed sales tax and VAT calculators.

**February 18, 2012** First SpreeConf held in New York City.

**April 30, 2012** Spree 1.1.0 released: support for Rails 3.2, Ransack replaces meta search, Spree product groups is a standalone extension, theme support deprecated in favor of deface, major rewrite of credit card model, API rewrite, stronger mass assignment protection, clearer separation between Spree components, easier Spree spec testing.

**August 31, 2012** Spree 1.2.0 released: Auth component completely removed from Spree and placed in separate Spree auth devise extension.  Customizing state machine no longer requires completely overriding it.

**December 19, 2012** Spree 1.3.0 released: Admin section redesigned, currency support.

**December 20, 2012** New Spree "Fancy" theme introduced.

**April 15, 2013** New documentation site launched.

**May 19, 2013** Spree 2.0.0 released: Removed support for Ruby 1.8.7, Backend and Frontend split from core, Split shipments introduced,  I18n names spaced translations, New API endpoints, instance level permission in API, Custom API templates, adjustment state changes, Order Populator in its own class, coupon applicator in its own class, product duplicator moved to its own class, new helpers to modify checkout flow steps, API supports "checking out" order, Auto-rotation of images, Unique payment identifier added to payments, removal of state call back in checkout controller, tracking URL for shipments, SSLRequirement deprecated in favor of ForceSSL, MailMethod model no longer exists,

**May 21, 2013** Second SpreeConf held in Washington DC.

**September 16, 2013** Spree 2.1.0 released: Rails 4 compatibility, breaking API changes, better Spree PayPal Express extension.
