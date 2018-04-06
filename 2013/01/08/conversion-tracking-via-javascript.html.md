---
author: Steph Skardal
gh_issue_number: 747
tags: analytics
title: Conversion Tracking via JavaScript
---

Most analytics conversion tracking is done these days with JavaScript or invisible pixel requests on the page that indicates a user has reached a conversion event, such as the receipt page. For example, Google Analytics conversion code might look like this on the receipt page:

```javascript
_gaq.push(['_setAccount', 'UA-XXXXX-X']);
_gaq.push(['_trackPageview']);
_gaq.push(['_addTrans',
   '1234',           // transaction ID - required
   'Womens Apparel', // affiliation or store name
   '28.28',          // total - required
   '1.29',           // tax
   '15.00',          // shipping
   'San Jose',       // city
   'California',     // state or province
   'USA'             // country
]);
_gaq.push(['_addItem',
   '1234',           // transaction ID - necessary to associate item with transaction
   'DD44',           // SKU/code - required
   'T-Shirt',        // product name
   'Olive Medium',   // category or variation
   '11.99',          // unit price - required
   '1'               // quantity - required
]);
_gaq.push(['_trackTrans']);
```

But what happens when a single page with various JavaScript-driven UI updates drives a user to a conversion event via AJAX? All of the conversion events have to be triggered via JavaScript after the conversion event. After some experimentation and verification with Google’s Developer Tools (Network) or Firebug’s Net Tool, I’ve implemented the following tracking services and code in JavaScript upon a conversion event for our Ruby on Rails client [Mobixa](https://web.archive.org/web/20130112044344/http://www.mobixa.com:80/):

### MSN Conversion

```javascript
tagid = /* tag id */
domainid = /* domain id */
actionid = /* action id */
jQuery('<iframe src="//flex.atdmt.com/mstag/tag/' + tagid
  + '/analytics.html?dedup=1&domainId=' + domainid + '&type=1&actionid='
  + actionid + '" frameborder="0" scrolling="no" width="1" height="1"
  style="visibility:hidden;display:none"><0/iframe>')
  .appendTo('#hidden_tracking');
```

### Google Ad Services

```javascript
google_conversion_id = /*conversion id*/
google_conversion_label = /* conversion label */
var image = new Image(1,1);
image.src = 'http://www.googleadservices.com/pagead/conversion/' +
  google_conversion_id + '/?label=' + google_conversion_label +
  '&value=1&guid=ON&script=0';
```

### Floodlight Conversion

```javascript
jQuery('<img height="1" width="1" src="http://sa.jumptap.com/a/conversion?
  event=Purchase" />').appendTo('#hidden_tracking');
```

### AdParlor Conversion

```javascript
adid = /* Ad Parlor id */
jQuery('<img height="1" width="1" alt="AP_pixel"
  src="http://fbads.adparlor.com/conversion.php?adid="'
  + adid + '  />').appendTo('#hidden_tracking');
```

### AdKnowledge

```javascript
adknowledgeid = /* adknowledge id */
jQuery('<iframe src="https://www.lynxtrack.com/track.frame.php?g='
  + adknowledgeid + '&o=' + /* order number */ + '&s=' + /* total */
  + '" height="1" width="1" frameborder="0">  <script
  language="JavaScript" src="https://www.lynxtrack.com/trackjs/g-'
  + adknowledgeid + '/o-' + /* order number */ + '/s-' + /* total */
  + '/track.js"> </script><noscript>
  <img src="https://www.lynxtrack.com/track.php?g=' + adknowledgeid
  + '&o=' + /* order number */ + '&s=' + /* total */ + '" width="1"
  height="1" border="0"></noscript></iframe>')
  .appendTo('#hidden_tracking');
```

### Google Analytics Ecommerce Conversion

```javascript
_gaq.push(['_addTrans',
    /* order number */,
    /* affiliation */,
    /* total */,
    /* tax */,
    /* shipping */,
    /* city */,
    /* state */,
    /* country */
]);
$.each(purchased_items, function(i, item) {
    gaq.push(['_addItem',
        /* order number */,
        /* item sku */,
        /* item name */,
        /* item category */,
        /* item price */,
        /* item quantity */
    ]);
});
_gaq.push(['_trackTrans']);
```

### Conclusion

Here are a few important takeaways in working with conversion tracking via JavaScript:

- Most of the above conversion tracking calls have a specific ID that is provided by the marketing service.
- Images and iframes are appended to a div with an id of hidden_tracking on the page to trigger the conversion request. Tracking did not appear to work if the images or iframes were appended to the body element. Also in the case of Google Ad Services conversion, the image itself did not have to be appended to the page; a request alone was enough.
- It’s important and extremely helpful to use Google Developer Tools or Firebug to verify these requests go through during development.
- Google Analytics tracking does not look much different from non-AJAX conversion tracking, but much of the other tracking code differs from what you might see in on-page tracking events.
