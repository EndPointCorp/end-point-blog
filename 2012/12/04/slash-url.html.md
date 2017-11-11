---
author: Jeff Boes
gh_issue_number: 728
tags: apache, interchange, perl, seo
title: Slash URL
---



There's always more to learn in this job. Today I learned that [Apache web server](http://www.jampmark.com/web-scripting/5-solutions-to-url-encoded-slashes-problem-in-apache.html) is smarter than me.

A typical SEO-friendly solution to Interchange pre-defined searches (item categories, manufacturer lists, etc.) is to put together a URL that includes the search parameter, but looks like a hierarchical URL:

/accessories/Mens-Briefs.html

/manufacturer/Hanes.html

Through the magic of [actionmaps](http://interchange.rtfm.info/icdocs/config/ActionMap.html), we can serve up a search results page that looks for products which match on the "accessories" or "manufacturer" field. The problem comes when a less-savvy person adds a field value that includes a slash:

accessories: "Socks/Hosiery"

or

manufacturer: "Disney/Pixar"

Within my actionmap Perl code, I wanted to redirect some URLs to the canonical actionmap page (because we were trying to short-circuit a crazy Web spider, but that's beside the point). So I ended up (after several wild goose chases) with:

```perl
my $new_path = '/accessories/' .
   Vend::Tags-&gt;filter({body =&gt; (join '%2f' =&gt; (grep { /\D/ } @path)),
       op =&gt; 'urlencode', }) .
   '.html';
```

By this I mean: I put together my path out of my selected elements, joined them with a URL-encoded slash character (%2f), and then further URL-encoded the result. This was counter-intuitive, but as you can see at the first link in this article, it's necessary because Apache is smarter than you. Well, than me anyway.


