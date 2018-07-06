---
author: David Christensen
gh_issue_number: 180
tags: mobile
title: Look Ma, I made an iPhone Enterprise Application!
---



One of our clients recently came to us for help with implementing an iPhone Enterprise application. This particular application involved deploying specific signed mail configurations for customers with iPhones. This was primarily a server-side application, although the front-end interface was created using the DashCode development tools from Apple. Although this was a web application, the DashCode integration enabled us to create the interface in a way that it appeared to be a native application on the iPhone. Client-side validation was performed in a way that for all intents and purposes appeared native.

The backend was a traditional CGI script which generated the .mobileconfig configuration payloads to easily integrate the customer’s mail server information into the iPhone’s Mail application. The backend was written to support any number of accounts deployed per customer, and the resulting payload was signed and verified by the customer’s PEM key.

We integrated openssl’s pkcs12 support to transparently sign the generated dynamic mobileconfig. This was keyed off of the client’s deployment key, so all of the generated keys were automatically indicated as trusted and registered by the client when installed on the iPhone.

Action shots:

<a href="https://4.bp.blogspot.com/_eLhk5Eevkf8/Snckmvx40MI/AAAAAAAAAAw/QD6fsoAIHSA/s1600-h/Picture+3.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5365797729114575042" src="/blog/2009/08/03/iphone-enterprise-application/image-0.png" style="margin:0 10px 10px 0;cursor:pointer; cursor:hand;width: 176px; height: 320px;"/></a>

<a href="https://2.bp.blogspot.com/_eLhk5Eevkf8/Snck1wTNpWI/AAAAAAAAAA4/7AfXR4efyuQ/s1600-h/Picture+4.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5365797986952389986" src="/blog/2009/08/03/iphone-enterprise-application/image-0.png" style="margin:0 10px 10px 0;cursor:pointer; cursor:hand;width: 173px; height: 320px;"/></a>


