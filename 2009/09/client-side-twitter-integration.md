---
author: Steph Skardal
title: Client Side Twitter Integration
github_issue_number: 199
tags:
- ecommerce
- javascript
date: 2009-09-14
---

I recently was assigned a project that required an interesting solution, [Crisis Consultation Services](http://www.crisis-consultation.com/). The site is essentially composed of five static pages and two dynamic components.

The first integration point required PayPal payment processing. Crisis Consultation Services links to PayPal where payment processing is completed through PayPal. Upon payment completion, the user is bounced back to a static receipt page. This integration was quite simple as PayPal provides the exact form that must be included in the static HTML.

The second integration point required a unique solution. The service offered by the static brochure site is dependent on the availability and schedule of the company employees, so the service availability remains entirely dynamic. The obvious solution was to include dynamic functionality where the employees would update their availability. Some thoughts that crossed our minds of how to update the availability were:

- Could we build an app for the employees to update the availability given the budget constraints?
- Could the employees use ftp or ssh to upload a single file containing details on their availability?
- Are there other dynamic tools that we could use to track the availability of the consultant such as SMS or Twitter?

Initially, we investigated using Google App Engine with a Python app that retrieved the availability information from an existing tool. To keep the budget down and try to stick with a purely static site on the server, we decided to investigate using Twitter for integration. I reviewed the [Twitter API](https://developer.twitter.com/) and found some code snippets for integrating Twitter via JavaScript. Below are snippets and explanations of the resulting code.

First, a script that retrieves the Twitter feed is appended to the document body. In this case, the endpoint Twitter account is pinged to get the most recent comment (count=1), and the resulting callback ‘twitterAfter’ is made after the JSON feed has been retrieved.

```javascript
var url = 'http://twitter.com/statuses/user_timeline/endpoint.json?callback=twitterAfter&count=1';
var script = document.createElement('script');
script.setAttribute('src', url);
document.body.appendChild(script);
```

Next, the callback ‘twitterAfter’ function is called. The callback function includes logic to determine if the consultant is available based on the most recent twitter message. If the datetime is in the future, the consultant is not available and will be available at that future datetime. If the datetime is in the past, the consultant is available and has been available since that datetime.

```javascript
var twitterAfter = function(obj) {
   var now = new Date();
   var available = new Date(obj[0].text.replace(/-/g, '/'));
   if (now >= available) {
       alert('Consultant is available!');
       // do other whizbang stuff here
   }
   return;
};
```

In another example of a more complex callback, the availability of the consultant is calculated.

```javascript
var twitterAfter_advanced = function(obj) {
   var now = new Date();
   var available = new Date(obj[0].text.replace(/-/g, '/'));
   mins_available = parseInt((available.getTime() - now.getTime())/60000);
   if (mins_available < 1) {
       alert('Consultant is available!');
       // do other whizbang stuff here
    } else {
       alert('Consultant is not available. The consultant will be available in ' + mins_available + ' minute(s).');
       // do other whizbang stuff here
    }
    return;
};
```

Here is an example Twitter feed to be used with this client side code:

```nohighlight
2009-09-13 9:00 - 6:00pm Sept 12th from web
2009-09-12 8:30 - 7:00pm Sept 11th from web
2009-09-10 22:00 - 5:00pm Sept 10th from web
```

The above example Twitter feed would yield the following availability:

```nohighlight
Sept 10th 5pm - Sept 10th 10pm: Not Available
Sept 10th 10pm - Sept 11th 7pm: Available
Sept 11th 7pm - Sept 12th 8:30am: Not Available
Sept 12th 8:30am - Sept 12th 6pm: Available
Sept 12th 6pm - Sept 13th 9am: Not Available
Sept 13th 9am - now: Available
```

In both the basic and advanced callback methods above, content on the page is updated to inform users of service or consultant availability. In the application of the advanced callback method, the user is notified when the consultant will be available.

The client side Twitter integration solution fit our budget and server constraints—​the functionality lives entirely on the client side, so we weren’t concerned about server installation, setup, or requirements. Additionally, Twitter is such a popular app that there are many convenient ways to tweet availability from a mobile environment.
