---
author: Carl Bailey
gh_issue_number: 939
tags: ecommerce, payments
title: Amazon Payments — Caveat Developer
---



A client of ours needed me to install Amazon Payments for them. Now there are several shopping carts for which Amazon Payments can be installed as an option, and I assume they work just fine. This client was not so lucky, and I had to roll my own.

Amazon starts with a JavaScript widget that asks you to log in or create an Amazon account. The widget returns an order reference ID:

```nohighlight
<div id="payWithAmazonDiv" style="padding-top: 1.2em;">
  <br />
   <img src="https://payments.amazon.com/gp/widgets/button?sellerId=[Amazonseller id]&size=large&color=orange" 
        style="cursor: pointer;"/>
</div>

<script type="text/javascript">
 var amazonOrderReferenceId;
 new OffAmazonPayments.Widgets.Button ({
   sellerId: '[Amazon seller id]',
   useAmazonAddressBook: true,
   onSignIn: function(orderReference) {
     amazonOrderReferenceId = orderReference.getAmazonOrderReferenceId();
      window.location = 'https://www.yoursite.com/nextpage.html?session=' +
                        amazonOrderReferenceId;
   },
   onError: function(error) {
     // your error handling code
     alert('Amazon error');
    }
 }).bind("payWithAmazonDiv");
</script>
```

The Id returned looks like “P##-#######-#######.” and must be saved for future screens. It’s know as the Amazon Order Reference Id. In my case, I simply passed it to the next page in the session variable of the query string.

Amazon next wants you specify a shipping address and that’s when the fun begins: Amazon provides a way to specify a callback function that gets invoked when an address has been selected. You use this function to ask Amazon to provide the details of the order so that you can calculate a shipping cost. To do this part you first need to provide the order reference, your Amazon access key id and sellerId (both provided to you by Amazon), Then you must compute a signature using the SignatureMethod specified. Also be sure to format your time stamp in the way Amazon requires it (%Y-%m-%dT%H:%M.000Z).

```nohighlight
https://mws.amazonservices.com/OffAmazonPayments
?AWSAccessKeyId=[Amazon ACCESS KEY]
&Action=GetOrderReferenceDetails
&AmazonOrderReferenceId=[Amazon Order Reference]
&SellerId=[Amazon Seller ID]
&SignatureMethod=HmacSHA256
&SignatureVersion=2
&Timestamp=2014-03-01T17%3A49.000Z
&Version=2013-01-01
&Signature=[Computed Signature]'
```

For this I used a Perl module: *use Digest::SHA qw( hmac_sha256_base64 )*. This routine successfully encodes the data and converts it to base64, as Amazon requires. Another little bit of fun comes from having to sort the options before the signature in case-sensitive alphabetical order. Only this results in the Signature being generated properly. Another little gotcha is to make sure your timestamp is set to the future. I set it for six hours ahead, and it seems to work properly.

I followed these guidelines for the remainder of Amazon’s steps, and at last resulted in an order where the charge had been properly approved or declined.

The thing is, that unlike PayPal and traditional credit card gateways, Amazon does not necessarily return an immediate yes or no answer as to whether the transaction is approved. The order is placed in a “Pending” state, and you need to poll them from time to time to get the final approval status of such orders. They attribute this to extra fraud protection that they perform. At the worst case, they say that it could take them up to a full day to return a formal decision, though most transactions (95%+) will be resolved within an hour. This unexpected development caused me to have to handle Amazon orders differently from other orders placed at the site. In my case, Amazon orders got their own order acknowledgement page and email, and we changed the way that the company determines which orders are approved and ready to be filled.

In short Amazon Payments it not any sort of “drop-in” alternative to PayPal. Rather it’s a fairly complex system that may require you to change the way orders are processed.


