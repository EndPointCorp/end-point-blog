---
author: Adam Vollrath
title: Interchange Caching Implementation Under Fire
github_issue_number: 648
tags:
- ecommerce
- interchange
- performance
- security
date: 2012-06-15
---



Richard and David presented a recent case study on an e-commerce hosting client.

<a href="http://www.flickr.com/photos/80083124@N08/7189648287/" title="IMG_0856.JPG by endpoint920, on Flickr"><img alt="IMG_0856.JPG" height="375" src="/blog/2012/06/interchange-caching-implementation/image-0.jpeg" width="500"/></a>

Several [Interchange](http://www.icdevgroup.org/) catalogs drive their individually branded storefronts, on top of a standard single-server LAMP stack boosted by an SSD drive.

Last year the sites came under an intense Distributed Denial of Service attack which lasted nearly two weeks. End Point responded immediately and soon engaged third-party DDoS mitigation firms. This experience later prompted an Interchange caching implementation.

Cache population and expiration is difficult for any dynamic web application using sessions, and doubly so for e-commerce sites. Every shopping cart needs a session, but delaying session creation until the first POST submission enables efficient caching for most of the sitemap. Other Interchange caching improvements made it back into the upstream code.


