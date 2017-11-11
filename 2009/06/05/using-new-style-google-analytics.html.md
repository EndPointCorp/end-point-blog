---
author: Richard Templet
gh_issue_number: 158
tags: interchange, analytics
title: Using the new-style Google Analytics pageTracker functions in Interchange
---

For a while now there have been two different ways to setup the JavaScript calls to report traffic back to Google Analytics.  The older method uses functions names that mention "urchin," while the newer method uses a function named "pageTracker".  This post describes an approach for using the new method at a standard Interchange store.

You can see an example of the new method of reporting a page view [here](https://gist.github.com/124271).  Nothing Interchange-related is required for normal page tracking, but you may want to use a variable for the Google Account Number, of which more below.

If you have your Google Analytics account setup to treat the website as an E-commerce site, then you can also add the order tracking tags to your receipt page, so that it sends order data over to Google Analytics at the time of conversion.  The order tracking tags can be viewed [here](https://gist.github.com/123987). This gist shows the typical Interchange tags you might want to use to transmit the order specifics.  Of course you might need to change the field used for the category for the products since not everyone uses the prod_group field from the products table to hold this information.

As you can see, both normal and the order-conversion scripts need to be modified to contain the individual Google Analytics account number for the website.  I tend to set up an Interchange variable such as GOOGLE_ANALYTICS_ID in the variable.txt file or catalog.cfg.
