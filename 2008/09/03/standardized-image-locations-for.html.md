---
author: Jeff Boes
gh_issue_number: 56
tags: interchange
title: Standardized image locations for external linkage
---

Here's an interesting thought:
[https://boingboing.net/2008/09/01/publishers-should-al.html](https://boingboing.net/2008/09/01/publishers-should-al.html)

Nutshell summary: publishers should put cover images of books into a standard, predictable location (like http://www.acmebooks.com/covers/{ISBN}.jpg).

This could be extended for almost any e-commerce site where the product image might be useful for reviews, links, etc.

At very least, with [Interchange](http://www.icdevgroup.org/) action maps, a site could capture external references to such image requests for further study. (E.g., internally you might reference a product image as [image src="images/products/current{SKU}"], but externally as "/products/{SKU}.jpg"; the actionmap wouldn't be used for the site, but only for other sites linking to your images.)
