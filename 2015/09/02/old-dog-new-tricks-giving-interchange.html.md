---
author: Greg Hanson
gh_issue_number: 1155
tags: css, design, html, interchange, javascript
title: Old Dog &amp; New Tricks - Giving Interchange a New Look with Bootstrap
---

### Introduction

So your [Interchange](http://www.icdevgroup.org) based website looks like it walked out of a disco... but you spent a fortune getting the back end working with all those custom applications.... what to do?

Interchange is currently being used in numerous very complex implementations. Trying to adapt another platform to replace Interchange is a formidable task, and in many cases the "problem" that users are trying to "solve" by replacing Interchange, can be remedied by a relatively simple face lift to the front end. One of the main attractions to Interchange in the past was its ability to scale from a small mom &amp; pop eCommerce application, to a mid level support system for a larger company and its related back end systems. Once the connection to those back end systems has been created, and for as long as you use those related systems, Interchange will continue to be the most economic choice for the job. But that leaves the front end, the one that your customers see and use (with their phones and tablets) that becomes the most immediate target for "modernization".

Granted, there are new and alternate ways of accessing and presenting data and views to users, but many of those alternatives are also accessible and inter-operable with Interchange. So while there are several topics that can be investigated at length, we will focus first on a popular front end framework that can help Interchange present a modern responsive theme to the end users. That framework is [Bootstrap](http://getbootstrap.com/).  Bootstrap is a good basic start for breathing new life into your Interchange application. Bootstrap uses a reasonably generic approach to HTML, CSS, and Javascript frameworking. This blends nicely with the Interchange application approach: providing a basic, repeatable, broad based and well supported foundation that can then be crafted into whatever the developer and their client may need.

My intent in this post, is to give you links to the tools available to implement Bootstrap into your Interchange application, and in subsequent posts explain our development process which may help you in how you use the tools.  Like any development, there are many ways to accomplish various tasks, and knowing why certain things were done, can help.

Alternatively, you may simply want to just download the "strap" catalog, and get started. At the time of this writing, Josh Lavin has been reviewing and refining the package, and the most recent version can be found at his Github account: [Bootstrap template for Interchange](https://github.com/jdigory/strap). It will soon become the standard catalog template in Interchange. So, if you are not really interested in why and how this template was developed, feel free to go to the git repository in the link, clone a copy and get busy!  The [README](https://github.com/jdigory/strap/blob/master/README.md) is very informative, and if you are an Interchange developer you probably won't have much trouble implementing this.

If you are interested in some of the major changes that we made to the old "standard" templating approach, and how you can apply those changes to an existing catalog without having to start from scratch, stay tuned in for my next post.
