---
author: Greg Davidson
gh_issue_number: 639
tags: ecommerce, payments
title: Handling Ecommerce Transactions with PayPal
---



<a href="https://www.flickr.com/photos/80083124@N08/7186533985/" title="IMG_0782.JPG by endpoint920, on Flickr"><img alt="IMG_0782.JPG" height="375" src="/blog/2012/06/14/handling-ecommerce-transactions-with/image-0.jpeg" width="500"/></a>

### Options

PayPal has several options for payment processing and Mark Johnson just shared his experiences working with saved credit cards using PayPal’s [Express Checkout](https://www.paypal.com/us/webapps/mpp/express-checkout).

### Order Types

There are a couple of order types of transaction in Express Checkout:

- Standard: everything purchased in a single transaction
- Custom: handles multiple shipments and multiple charges

### What’s in a name?

PayPal generates something they call an “order” that is distinct from the order for a given merchant. This is typically confusing to merchants because their concept of an order simply refers to the order a customer has just placed in their ecommerce application. The PayPal “order” is created prior to any other transaction. If the authorization fails, the “order” is not removed (which would be nice) but lingers around for 29 days by default. When merchants ask about this, the response PayPal offers is to void the “order”.
For standard on API call (authorization) if that fails you have to do a second API call to void the order.

The “order” has little value except to specify a charge ceiling for a given ecommerce transactions. Although the ceiling is set by the “order”, there is the notion of an “order allowance”. By default this allowance or ceiling is set to 115% of the original charge but this can be negotiated and changed if required.

Merchants desire to have the “order” removed when it is no longer needed but this isn’t always possible. One of the limitations of PayPal from a developer’s perspective is that you cannot initiate any activity unless you are the customer. For example a customer service rep cannot enter an order on behalf of a customer. Also, telephone orders are not possible due to this limitation.

It is not possible to remove “order” if you might have subsequent changes to the order. This is common scenario in ecommerce apps where customers would like to add to or modify their order after it has been shipped. If the PayPal “order” is closed, subsequent transactions like this are not possible.

### API Calls for Express Checkout

When a customer initiates the check out process, a “Set Request” API call is made to PayPal to establish a session. The response includes a session ID. With Set Request, URLs need to be submitted which specify resources to redirect the customer to for either success for failure.

Get Request is another API method offered and the response will include the user id, shipping address and email of the customer. You can also force them to include a phone number and billing address if you like. PayPal by default likes to offer less information while ecommerce clients often like to have more information.

For standard orders, there is a “Do payment” call which combines the order setup and authorization into a single requests. For custom orders, the setup and authorization are performed separately. The developer has the option to either complete the order or leave it open. If you choose to leave it open, you can perform multiple capture or charges up to the ceiling amount that has been specified.

### PCI Compliance

The payment card industry has a set of regulations including:

- The full account number must be encrypted
- The CVC cannot be written to permanent media
- PAN displays must be masked

Mark noted that Secure decryption is a challenge and he has worked on a secure decryption service for one of our ecommerce clients.

### Saved Cards

Authorize.net has a customer information manager (CIM) which supports “profiles”. These profiles are referenced by tokens and the data storage includes PANs. There are three types of profiles: customer, payment and address. The default behaviours is to use them for “on-demand” transactions.

### Pity the fool...

```
-->>:[]}}}}-O
```

Mr. T made several cameo appearances during the talk to keep us all engaged and interested!


