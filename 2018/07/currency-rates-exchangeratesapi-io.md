---
title: Currency exchange rates with exchangeratesapi.io
author: Jon Jensen
github_issue_number: 1444
tags:
- saas
- ecommerce
date: 2018-07-14
---

<img src="/blog/2018/07/currency-rates-exchangeratesapi-io/38037392525_3501fee918_o-sm.jpg" alt="city street with currency exchange signs" />

Several of our clients run ecommerce sites, built on custom software, that allow customers to pay in their choice of a few different currencies.

Some have set up separate merchant bank accounts for each currency and use separate payment gateway accounts to accept payments natively in each currency. But more commonly they use a payment gateway that allows them to accept payment in several currencies, but receive funds converted into their specified native currency in their merchant bank account.

In either case, it is common to store prices for products, shipping, etc. in one base currency (say, USD for companies based in the U.S.) and dynamically convert prices for customers. Non-native prices may need to be marked up to cover the cost of conversion into the native currency, depending on the terms of the agreement with the payment gateway or bank.

Because currency exchange rates change often, and because payment gateways generally do not offer a way to retrieve the exchange rates in advance, we need our own source for ongoing retrieval and storage of our exchange rates (also known as forex rates).

For a while we were very pleased with [Fixer.io](https://fixer.io/), which was a free service that collected exchange rates from the European Central Bank (ECB) and provided current or historical rates via a simple JSON API. We were sad to find that in March 2018 they deprecated that API and in June 2018 they discontinued it entirely, as [described to their users](https://github.com/fixerAPI/fixer#readme). Fixer.io has transitioned to a paid service and they appear to have improved their operation to retrieve exchange rate data from at least a dozen more sources than the ECB, and to store far more frequent rate updates. Those are nice features, but not something our clients need.

Fixer.io still offers a free plan that allows 1000 API calls per month but in that plan the exchange rates are all based on the Euro. You need to sign up for at least the $10/month plan to retrieve exchange rates from the other currencies as base. As our customers needed exchange rates based on USD and CAD, the free plan wouldn’t work for us. They offer a limited-time Legacy Plan which would work, but that would just be “kicking the can down the road” until that plan too is discontinued. Their lowest paid plan is inexpensive, but with one of our clients retrieving exchange rates just once per week for only 4 currencies, it felt like overkill to track another paid service and API key, deal with renewals and updated credit card payment details, etc.

We quickly found another service called [Exchange Rates API](https://exchangeratesapi.io/), run by [Madis Väin](https://github.com/madisvain), which is free to use without any account setup or API key needed. It is also based on the published ECB exchange rates, and uses the same API that Fixer.io did. The [server side is open source](https://github.com/madisvain/exchangeratesapi) written in Python using the [Sanic](https://github.com/channelcat/sanic) web server library (similar to Flask, but focused on speed and async request handlers).

The ExchangeRatesAPI.io service runs on [Heroku](https://www.heroku.com/) and the open source code is easy to deploy to your own Heroku instance if you want to run your own private service.

Thanks to Madis Väin for providing it, and to Fixer.io for the good service in the past!
