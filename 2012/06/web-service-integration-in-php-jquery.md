---
author: Ron Phipps
title: Web service integration in PHP, jQuery, Perl and Interchange
github_issue_number: 629
tags:
- company
- interchange
- javascript
- json
- perl
- php
- integration
date: 2012-06-13
---

Jeff Boes presented on one of his latest projects.

<a href="https://www.flickr.com/photos/80083124@N08/7369312150/" title="IMG_0732.JPG by endpoint920, on Flickr"><img alt="IMG_0732.JPG" height="375" src="/blog/2012/06/web-service-integration-in-php-jquery/image-0.jpeg" width="500"/></a>

CityPass.com decided on a project to convert their checkout from being served by Interchange to have the interface served by PHP, but continue to interact with Interchange for the checkout process through a web service.

The original site was entirely served by Interchange, the client then took on a project to convert the frontend to PHP while leveraging Interchange for frontend logic such as pricing and shipping as well as for backend administration for order fulfillment.

Technologies used in the frontend rewrite:

- PHP
- jQuery for jStorage, back-button support and checkout business logic
- AJAX web services for prices, discounts, click-tracking

The Interchange handler is conduit.am that handles the processing of the URL. From this ActionMap the URLs are decoded and passed to a Perl module, Data.pm, which handles processing the input and returning the results.

An order is just a JSON object so testing of the web service is easy. We have a known hash, we post to the proper URL and compare the results and verify they are the same. New test cases are also easy, we can capture any order (JSON) to a log file and add it as a test case.
