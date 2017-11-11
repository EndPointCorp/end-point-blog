---
author: Jeff Boes
gh_issue_number: 641
tags: django, rails, conference, clients
title: RailsAdmin & Django
---

Steph Skardal and Greg Davidson presented on RailsAdmin and Django (in the context of two of our clients, Musica Russica and Providence Plan).

<a href="http://www.flickr.com/photos/80083124@N08/7186728287/" title="IMG_0796.JPG by endpoint920, on Flickr"><img alt="IMG_0796.JPG" height="240" src="/blog/2012/06/14/railsadmin-django/image-0.jpeg" width="320"/></a>

Clients need a browser interface to administrate their Rails apps' assets and configuration. RailsAdmin is an “engine” (an embedded miniature Rails app) for developing an admin interface, and a relatively young open-source project. It offers a CRUD-capable interface. It provides data export, filtering, pagination, and support for file attachments and a popular plug-in called “PaperTrail”. Musica Russica uses this as their site administration. This admin interface can be configured with many different customizable options: formatting, help text, sorting, etc.

RailsAdmin also provides authorization to limit certain actions (“delete”, “read”, “manage”) to objects (“User”, “Order”) by user.

<a href="http://www.flickr.com/photos/80083124@N08/7371962564/" title="IMG_0798.JPG by endpoint920, on Flickr"><img alt="IMG_0798.JPG" height="320" src="/blog/2012/06/14/railsadmin-django/image-0.jpeg" width="240"/></a>

In contrast, Django, written in Python, dates back to 2005 and is aimed at complex web applications. It provides an automatic admin interface which of course you can extend and customize, and mostly the same feature set (pagination, filtering, etc). Several high-profile web applications (Instagram, Pinterest, and Mozilla's add-ons site) are powered by Django. Our own work here is represented by the client site for Providence Plan.

Django's admin interface is (mostly) free of effort, once you have developed models for your application. In addition, there are many open-source apps that can be plugged into a project to manage specific things, such as permissions. Filters and searching can be configured, too: this helps limit the data that a user must consider during an administration operation.
