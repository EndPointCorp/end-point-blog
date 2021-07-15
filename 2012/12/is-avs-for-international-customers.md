---
author: Jeff Boes
title: Is AVS for International Customers Useless?
github_issue_number: 732
tags:
- ecommerce
- payments
date: 2012-12-13
---

Any ecommerce site that sells "soft goods", some digitally delivered product, has to deal with a high risk of credit card fraud, since their product is usually received instantly and relatively easily resold. Most payment processors can make use of [AVS](http://en.wikipedia.org/wiki/Address_Verification_System) (Address Verification System). It usually works well for cards issued by United States banks with customers having a U.S. billing address, but its track record with international customers and banks has been less than stellar.

AVS compares a buyer's address information with what the bank has on file for the card's billing address. To reduce false negatives, that comparison is limited to the postal code and the numeric part of the street address. The lack of consistent AVS implementation by non-U.S. banks, and the variety of postal codes seen outside the U.S., Canada, and the U.K., mean problems creep in for most international orders.

Any time you reject an order, whether it's for a legitimately incorrect billing address, a bank/AVS problem, or any other reason, you're increasing the likelihood of losing the customer's business, having them retry and cost you more in payment processing fees, or having them call your customer service line in frustration.

Also note that the AVS result is only available *after* a transaction is authorized or processed (and the payment processor has thus charged a fee), not before.

So what can you do as a conscientious developer? There are a number of approaches, all with drawbacks as you'll see:

### Don't use AVS for foreign cards

That's the simple approach. Skip AVS altogether, at least for international orders, and let the chips fall where they may. By "international order", I mean "one that has a non-US billing address". Merchants tend to think in terms of "foreign" and "domestic" credit cards, and it's true that it's possible to determine the country of the bank based on the card number. See the Wikipedia articles on [Bank card number](http://en.wikipedia.org/wiki/Bank_card_number) and [List of Issuer Identification Numbers](http://en.wikipedia.org/wiki/List_of_Issuer_Identification_Numbers) for some mostly-accurate information. However, you really need a current "BIN" (Bank Identification Number) database, and those cost money and must be massaged into the format your ecommerce system needs. Oh, and usually your ecommerce system won't know anything about BIN numbers and you'll need custom programming to consult a BIN database.

So for most merchants, actually knowing whether a credit card number is from a U.S. or foreign bank isn't possible to determine, so they fall back to rough estimates such as assuming that a non-U.S. billing address means a non-U.S. bank, and then skipping or weakening the AVS check for those orders.

It seems like that would work, but it's wrong so often that it's not very useful. Customers with a U.S. billing address may have a card issued by a foreign bank that doesn't support AVS, and strict AVS checks for them will mean they can't complete the order. Customers with a foreign billing address may have a card issued by a U.S. bank that does support AVS. And some foreign banks *do* support AVS, just to keep things interesting.

In any case, disabling or weakening AVS may allow more fraudulent transactions than the merchant is willing to stomach. But this minimizes the grief you incur because of false positives (and the ensuing held funds and customer service calls).

### AVS on the whole amount

A charge that fails an AVS check will result in the funds being held on the customer's card until removed, which can cause unease or downright hostility on the part of that customer, especially if you are charging something large compared to the customer's available credit.

Furthermore, many people's cards have a very low credit limit, and there are a [lot more people](http://mymoneycounselor.com/credit-card-debt-trends) with low remaining balances than you might first think.

In addition, customers using debit cards will be especially cranky if their funds are held because of a failed AVS check. They use that same account for writing checks, withdrawing cash from the ATM, etc., so when you tie up their real money in an account (not just some credit), it feels to them like you have stolen their money.

### AVS on a "test charge"

You can submit a "test charge" (usually just $1) against the card to retrieve the the AVS information, to "fish out" the AVS response before making the full charge. This is quite useful if the full charge would be significant; it's less handy for small amounts.

This approach has a serious drawback: it means you are making an additional authorization request for *each sale*, which doubles transaction fees, and may bump the seller into a higher tier of transaction costs because of the total number of requests.

It is also increasingly noticed by customers in the era of computer banking. Many banks will show pending transactions including these little $1 charges, even after the full charge has come in, inducing over-anxious customers to call your customer service line and waste everyone's time.

### Tragic calculus

There's really no magic bullet to correct the issues involved in AVS processing: you can sanitize the data, and cushion the shock for a customer when your website declines their card due to a failed AVS check, but in the end you have to resolve the tragic calculus of whether you lose more to fraud or to abandoned carts, and how many customer service calls you can afford to handle. It is not amusing for customer service reps to have to explain many times per day to anxious customers how the credit card processing system works, often directly contradicting the customers' banks' own explanations that may be so dumbed-down as to be simply incorrect.

Certainly the value of AVS as fraud prevention depends a lot on how you implement it. Perhaps it's time for you to consider whether additional customization of your order processing is in order to maximally balance customer satisfaction, processing charges, and keep fraud at a minimum.

### Acknowledgments

This post was extensively edited and extended by [Jon Jensen](/team/jon-jensen), who has seen plenty of this pain first-hand as well.
