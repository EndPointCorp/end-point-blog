---
author: Carl Bailey
title: 'Gift Certificates: Easy to Say, Hard to Do'
github_issue_number: 357
tags:
- ecommerce
date: 2010-09-29
---



A recent [blog article](/blog/2010/07/spree-gift-certificates-and-coupons/) by Steph goes through the steps taken to handle implementation of gift certificates using Spree’s coupon/discount model. At the end of the article, she rightly concludes that gift certificates are not that well suited to the discount model and need to be handled separately. Gift certificates are rightly handled as a method of payment—​they should have no effect on the amount of the sale, sales tax or shipping charges. This is an attempt to further that discussion.

Some people want to put rules on to how gift certificates can be used: Minimum purchase, expiration dates, etc. However, these are rules that apply to qualification: Does the person or the sale qualify to get a lower price? To my mind, these are not rules that can be applied to true gift certificates. A gift certificate is a business liability. The merchant has the money, and the customer should be allowed to spend it as she sees fit, without having to pass any qualifications separate from those that apply to everyone else. So gift certificates should be treated by the system as a form of payment, and customers should not have to qualify just to use them.

To implement a gift certificate system, we need to be able to sell them, record them, and redeem them.

Selling Gift Certificates:

The first thing to tackle is selling a gift certificate. The key thing here is that the sales tax is charged later, when the certificate is used to pay for merchandise. So we need to set up a non-taxable category of merchandise and put our certificate in it. If the site is selling a physical certificate, shipping can be charged, but this would typically be a flat rate for postage that does not vary with the amount of the certificate. No shipping should be charged on virtual gift certificates. This may not fit easily into standard shipping calculators, so something custom may be needed here.

I am assuming here that certificates sell at face value (a $50 certificate sells for $50). If not, we need a way to get the certificate value different from the amount paid for it. In any case the sale price needs to be at least the value of the certificate ($100 certificate costs $105) or we can get an runaway escalation effect, where one certificate is used to buy another ad infinitum. For that same reason, our gift certificates should be non-discountable. Otherwise a slick customer can use one to buy another, eventually getting free certificates. No thanks! Alternatively, we could prevent people from using one gift certificate to pay for another. For now, let’s just say that certificates are non-discountable. Anyway, discounts apply to merchandise, and a gift certificate is not merchandise.

Recording Gift Certificates:

Having been sold, the gift certificate needs to go on file so it can be used. The record needs to include the purchaser, (who may not be the eventual redeemer) and the the original value of the certificate. In the database we need a table like “giftcerts,” to which we can insert a row with the certificate number, the order number it was purchased from, and the certificate value. Ideally, having certificate numbers be pulled randomly from a large space, and taking care to ensure no duplicates are issued is sufficient. Usually a certificate just needs to be too hard to guess or to brute-force, but certainly, knowing one valid number, it should not be possible to guess another.

To redeem a card, a customer just needs to enter its number. Once it is presented for the first time, we can associate it with the logged-in username if we desire. Some merchants may want to ensure that a customer is registered to spend a gift certificate. This has two benefits: (1) we get better tracking of gift certificate sales, and (2) we can use the registration info to ensure that the person who spends the certificate is the one to whom it belongs.

Redeeming Gift Certificates:

When a certificate is used for purchase, the system needs to determine whether the code is eligible or not. To us, that means simply does the card have an available balance?

When applied to the purchase total, a valid certificate will either cover the entire purchase amount, or leave a balance due. If a balance is due, the system should require a credit card, possibly even another gift certificate, or other payment mode be provided to cover the remaining amount of the sale. To avoid race conditions, the system needs to implement special handling to make sure that no overspend takes place. If the certificates used cover the entire amount of the sale, we need to then bypass credit card processing.

If the customer edits the cart contents once a certificate is applied, we need to re-apply the certificate, adjusting the applied value. Likewise, when the order is finally submitted, we need to check each certificate again, and report failure and request new payment details if any part of the submitted payments does not go though. If our database is one that can handle transactions, we are in good shape—​we can process the payments one by one, handling the gift certificates first, and roll back if any part fails.

Of course we will need to record gift certificate usage, so that for each certificate, we are able to see how it has been spent and when. So, once a sale is placed that uses a certificate for payment, we need to insert rows into “giftcert_use” indicating the order number, certificate number and amount charged, one row for each certificate used by the customer.

Other thoughts:

In the case of returns for merchandise paid for by gift certificate, it may be best to issue a new gift-certificate as a store credit for the amount of the return. In fact this can be done for any return! The customer gets credit that can only be used at the store. This requires an admin capability to add new gift certificates with a comment or flag to indicate that the certificate was added as a refund of store credit.

Comments?

So we see it’s not so easy to handle gift certificates!. This simple discussion involves customizations to sales tax, shipping, and payment processing. There are race conditions to be handled and avoided, and and admin interface for issuing store credits. All that, and we did not cover auditing of gift certificates or providing reports to users.

What have I left out? Are there other important elements to be considered? Your comments are welcome!


