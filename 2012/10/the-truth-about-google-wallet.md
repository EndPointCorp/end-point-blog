---
author: Marina Lohova
title: The truth about Google Wallet integration
github_issue_number: 711
tags:
- ecommerce
- payments
- php
- api
date: 2012-10-19
---

Google Wallet integration is quite a bumpy ride for every developer. I would like to describe one integration pattern that actually works. It is written in PHP for Google Wallet 2.5 API.

### Google Merchant account settings

First, one must [sign up](https://developers.google.com/checkout/developer/Google_Checkout_Buy_Now_Button_How_To#signup) for Google Merchant account. Once this is done, it is very important to configure the service properly on the Settings > Integration tab

<a href="/blog/2012/10/the-truth-about-google-wallet/image-0.png" imageanchor="1"><img border="0" src="/blog/2012/10/the-truth-about-google-wallet/image-0.png"/></a>

### Buy now button

[Buy Now buttons](https://developers.google.com/checkout/developer/Google_Checkout_Buy_Now_Button_How_To) are the simplest form of integration. The code for the button can be obtained on the Tools > Buy Now Buttons tab.

<img border="0" src="/blog/2012/10/the-truth-about-google-wallet/image-1.jpeg"/>

I modified the code provided by Google to transfer information to Google Wallet server via the hidden fields on the form.

```php
<form method="POST" action="https://sandbox.google.com/checkout/api/checkout/v2/checkoutForm/Merchant/<merchant_id>" accept-charset="utf-8">
<input type="hidden" name="item_name_1" value=""/>
<input type="hidden" name="item_description_1" value="Subscription Fees"/>
Enter Amount to Deposit:<input type="text" class="normal" size="5" name="item_price_1" value=""/>
<input type="hidden" name="item_currency_1" value="USD"/>
<input type="hidden" name="item_quantity_1" value="1"/>
<input type="hidden" name="shopping-cart.items.item-1.digital-content.display-disposition" value="OPTIMISTIC"/>
<input type="hidden" name="shopping-cart.items.item-1.digital-content.description" value="It may take up to 24 hours to process your deposit. Check your account balance and notify the Commissioner if it's not updated within 24 hours."/>
<input type="hidden" name="_charset_" />
<!-- Button code -->
<input type="image" name="Google Checkout" alt="Fast checkout through Google" src="http://sandbox.google.com/checkout/buttons/checkout.gif?merchant_id=<merchant_id>&w=180&h=46&style=white&variant=text&loc=en_US" height="46" width="180" />>
</form></merchant_id></merchant_id>
```

### Tweaking Google Merchant Libraries for PHP

The business logic for my website includes:

- People enter amount they wish to deposit via Google Wallet and click "Buy Now" button.
- Google sends back confirmation that card is pre-authorized and ready to charge
- The script tells Google: Go ahead and charge it.
- Google tells the site that charge went through.
- Table "orders" in the database adds entry of transaction.

The good news is that we have a very good PHP library for Google Wallet integration in place. The source code can be found [here](http://code.google.com/p/google-checkout-php-sample-code/source/browse/trunk/).

The bad news is that the sample code provided with the library does not entirely work with the newest 2.5 Google Wallet API. The library does have functions like SendChargeAndShipOrder (charge-and-ship-order) from 2.5 API implemented, but the demo example still uses the old function SendChargeOrder (charge-order).

I will tweak the sample code in responsehandlerdemo.php for my specific business requirements and 2.5 API version.

Customization is implemented with the help of useful Google Wallet [callbacks](https://developers.google.com/checkout/developer/Google_Checkout_Custom_Processing_How_To) sent at various stages of order processing. First, my script will wait for the "authorization-amount-notification" notification that is sent after credit card data was verified and authorized. When the notification is received, I will issue the "charge-and-ship-order" command. The "charge-order" command used in the library's sample code no longer works in 2.5 API, because charging and shipping is now done at once.

```php
switch ($root) {
  case "authorization-amount-notification": {
    $google_order_number = $data[$root]['google-order-number']['VALUE'];
    $GChargeRequest = new GoogleRequest($merchant_id, $merchant_key, $server_type);
    $GChargeRequest->SendChargeAndShipOrder($google_order_number);
    $Gresponse->sendAck($data[$root]['serial-number']);
    break;
  }
  default:
    $Gresponse->sendAck($data[$root]['serial-number']);
    break;
}
```

I should receive the "charge-amount-notification" notification after the order is successfully charged. If we go to the Google Wallet dashboard, we will notice that the order is marked as charged and shipped. When the notification is received, the record is created in the "orders" table.

```php
case "charge-amount-notification": {
  $items = get_arr_result($data[$root]['order-summary']['shopping-cart']['items']['item']);
  $googleid = $data[$root]['google-order-number']['VALUE'];
  foreach( $items as $item ) {
    $userid =$item['item-name']['VALUE'];
    if(isset($userid)){
      $amount = $data[$root]['total-charge-amount']['VALUE'];
      $date = $data[$root]['timestamp']['VALUE'];
      $tmpsql = "INSERT into orders(google_id,amount,userid) VALUES('". $googleid."','".$amount."','".$userid."')";
      if(! $sqlresult=mysql_query($tmpsql)) {
        $Gresponse->log->LogError(mysql_error());
      }
    }
  }
  $Gresponse->sendAck($data[$root]['serial-number']);
  break;
}
```

### Debugging tools

Google provides a very useful Google Wallet [Sandbox](http://support.google.com/checkout/sell/bin/answer.py?hl=en&answer=134469), that the developers can use while testing their features. No actual orders are placed and no credit cards are charged.

All the low level warnings and exceptions are recorded to the Tools > Integration Console tab.

<img border="0" src="/blog/2012/10/the-truth-about-google-wallet/image-2.jpeg"/>

Finally, it can be very useful to check googlemessage.log file defined in the sample code.

```php
define('RESPONSE_HANDLER_LOG_FILE', 'googlemessage.log');
```

### Full source code

The full source code for the modified responsedemohandler.php can be found [here](https://gist.github.com/eb63b05ab465c672c6ae).
