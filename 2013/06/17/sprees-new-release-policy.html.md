---
author: Brian Buchalter
gh_issue_number: 822
tags: ecommerce, spree
title: Spree’s New Release Policy
---

Spree has recently updated its documentation regarding contributions and has included (maybe for the first time?) an official [Release Policy](https://web.archive.org/web/20130608210307/http://guides.spreecommerce.com/developer/contributing.html). This is an important step forward for the Spree community so that developers can communicate to clients the potential costs and benefits when upgrading Spree, understand how well Spree supports older releases, and gauge the overall speed of the “upgrade treadmill”.

### Deprecation Warnings

>
> Deprecation warnings are to be added in patch releases (i.e. 2.0.2) and the code being deprecated will only be removed in minor versions. For example, if a deprecation warning is added in 2.0.2, 2.0.3 will still contain the same deprecation warning but in 2.1.0 the deprecation warning and the code will be gone.
>

Deprecation warnings are very helpful for developers, but without a robust test suite exercising your application, it’s easy for deprecation warnings to go unnoticed. A strong test suite coupled with deprecation warnings helps you manage your client’s expectations about how upgrades can affect your Spree customizations and extensions.

### Master Branch Receives All Patches

>
> Master branch receives all patches, including new features and breaking API changes (with deprecation warnings, if necessary).
>

No surprises here; the master branch is for developers and should not be used for production. If you think you’ve encountered a bug in Spree, make sure to create a failing test against master to make sure it hasn’t be resolved by any existing patches. Read more about [filing an issue](https://web.archive.org/web/20130608210307/http://guides.spreecommerce.com/developer/contributing.html) for additional details.

### Current Stable Release Branch

>
> One branch “back” from master (currently 2-0-stable) receives patches that fix all bugs, and security issues, and modifications for recently added features (for example, split shipments). Breaking API changes should be avoided, but if unavoidable then a deprecation warning MUST be provided before that change takes place.
>

Continuing Spree’s history of very aggressive refactoring, breaking API changes are permitted in the current stable branch. If you’re looking for a truly stable release of Spree, you’ll need to look back two stable branches behind master.

### Two Releases Behind Master

>
> Two branches “back” from master (currently 1-3-stable) receives patches for major and minor issues, and security problems. Absolutely no new features, tweaking or API changes.
>

In my opinion, this is the only branch that should be considered for use in production. With the API locked down and a greater chance of most bugs worked out while it was the current release branch, the “two-back” stable branch is a safe bet that’s going to have the most up-to-date feature set.

### Three and Four Releases Behind Master

>
> Three branches back from master (currently 1-2-stable) receives patches for major issues and security problems. The severity of an issue will be determined by the person investigating the issue. Absolutely no features, tweaking or API changes. Four branches and more “back” from master (currently 1-1-stable and lesser) receive patches only for security issues, as people are still using these branches and may not be able to or wish to upgrade to the latest version of Spree.
>

It’s nice to see a fairly strong commitment to accepting security patches, although if we look at this in absolute terms, the 1.1.x release was put into security-patches-only mode after just 13 months. Considering that the 1-1-stable branch is 2,127 commits behind the 1-3-stable branch (!!), it’s clear that Spree is now formalizing it’s very aggressive release culture.

### Managing the Upgrade Treadmill

As stated previously, a strong test suite is the best tool available to be able to determine what upstream updates affect your Spree customizations. Coupled with deprecation warnings, it becomes a fairly straight-forward process for identifying breaking changes, creating estimates for fixes, and communicating these costs to clients. Following the stated guides for [customizing Spree](https://web.archive.org/web/20130708010221/http://guides.spreecommerce.com/developer/authentication.html) is also recommended. When visiting the Spree guides section on customization, you’ll first be taken to the sub-section for authentication. Make sure to expand the Customization menu on your left to see additional guidance for customizing [internationalization](https://web.archive.org/web/20130715044956/http://guides.spreecommerce.com/developer/i18n.html), [views](https://web.archive.org/web/20130709005650/http://guides.spreecommerce.com/developer/view.html), [JavaScript, stylesheet and image assets](https://web.archive.org/web/20130610052811/http://guides.spreecommerce.com/developer/asset.html), [business logic](https://web.archive.org/web/20160322070928/http://guides.spreecommerce.com:80/developer/logic.html), and [checkout](https://web.archive.org/web/20130715001359/http://guides.spreecommerce.com/developer/checkout.html).

Another important suggestion helpfully submitted by my colleague Mike Farmer was to never simply add gem ‘spree’ to your Gemfile. You should be very conscious about what version of Spree you want to use, and make sure you specify it in your Gemfile.
