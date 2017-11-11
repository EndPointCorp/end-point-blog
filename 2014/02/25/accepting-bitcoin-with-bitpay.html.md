---
author: Mark Johnson
gh_issue_number: 932
tags: cryptocurrency, ecommerce, interchange, payments
title: Accepting Bitcoin with BitPay
---

End Point recently began discussions with long-time Interchange client [FrozenCPU](http://www.frozencpu.com/) about their desire to accept bitcoin payments. Because of the newness of bitcoin, as well as its non-traditional nature as a [cryptocurrency](http://en.wikipedia.org/wiki/Cryptocurrency), traditional payment gateways do not support it. While ideally suited to function as an exchange medium for ecommerce, we had to seek solutions that allowed for its integration into the checkout process.

### BitPay Payment Gateway

After investigating their options, FrozenCPU elected to partner with [BitPay](https://bitpay.com/) to handle bitcoin payments. BitPay provides merchants with a solution similar in function to PayPal, where users are either redirected to the BitPay servers to complete payment, or the interaction with BitPay can be embedded directly into the merchant site via an iframe. In either case, all communication between customer and payment processor is direct.

Customers with a digital wallet then approve a transfer for the converted amount of bitcoin. Merchants need not display or maintain conversion rates; they can continue to use their native currency and BitPay will manage the exchange rate directly.

The payment negotiation is managed by the creation of an *invoice* which tracks the state of the payment through a sequence of status updates. Each status update can be thought of as analogous to a credit card transaction, but instead of a number of independent transactions related through references, the same invoice and identifier are used throughout.

### The BitPay Process

At the point to finalize an order, a number of steps must be taken to complete the transaction using bitcoin. Again, the general process is most similar to PayPal, although no component of address management is included.

- At the point where an authorization is normally issued for a credit card payment, instead the merchant generates a new invoice from BitPay, which starts in the status "new".
- Upon successful invoice generation, the merchant can either redirect the customer to BitPay's server to present the payment screen, or embed the same through an iframe to keep the customer on site, if preferred.
- Customer authorizes payment to transfer bitcoin from their digital wallet at the exchange rate provided from BitPay.
- Once transferred, the invoice status moves to "paid" and the customer can then be presented with the order receipt, or in the case of redirect can click back on the merchant-provided backlink to the site to produce the receipt.
- BitPay then negotiates a validation process over the bitcoin network, where the payment is "complete" after 6 block confirmations. Merchants can choose how quickly they want to accept the payment as valid, where a higher speed increases the odds of failing validation later in the process:

        - High speed: immediately consider the payment "confirmed" once customer authorizes payment.
        - Medium speed: consider payment "confirmed" once BitPay receives 1 block confirmation. Typically 5-10 minutes.
        - Low speed: wait for all 6 block confirmations before considering the payment "confirmed". Typically 45-60 minutes.

- All payments must ultimately receive 6 block confirmations within 1 hour to complete. If this threshold cannot be met, the invoice status becomes "invalid" and the merchant must decide how to proceed.- Once the invoice status is "complete", the transaction cannot be reversed. No chargebacks. Funds can be received by the merchant in the local currency or in bitcoin.

- Invoices can be created with flags to either send notifications to an API the merchant creates, a designated email address, or both. This allows the merchant to keep on top of the transaction lifecycle in real time and minimize delays or disruptions on fulfillment.

### Bumps in the Road

This was our first venture into an emerging field with a young technology. We hit a few difficulties on our path to implementation:

- Not every status change on the invoice generates a notice, even when the fullNotifications flag is set to true. Customers have 15 minutes to pay an invoice, and if that time elapses the invoice status moves to "expired". That left us with a dangling order because the IPN does not fire on that status update. We had to compensate by developing a monitoring script to look for those dangling orders older than 15 minutes, make an API call to BitPay to confirm the invoice status of "expired", and cancel the order.
- We initially received no update messages on status changes to the invoice that sourced back to problems in BitPay's proxy software. However, BitPay was diligent in their efforts to troubleshoot the issue with us and they were able to upgrade the packages causing the problem. Their responsiveness in this matter certainly separates BitPay from other payment processors who are either entirely unresponsive to system bugs or are content to allow problems to persist through their regular release schedule.
- Development and testing was complicated by the lack of a development environment at BitPay.

We are looking forward to the anticipated success of accepting bitcoin for payment on FrozenCPU and the opportunity to explore this offering with our many other ecommerce clients.
