---
author: Jeff Boes
title: Improve SEO URLs for Interchange search pages
github_issue_number: 1198
tags:
- interchange
- seo
date: 2016-01-27
---

This is an article aimed at beginner-to-intermediate Interchange developers.

A typical approach to a hierarchical Interchange site is:

```nohighlight
Categories -> Category -> Product
```

I.e., you list all your categories as links, each of which opens up a search results page filtering the products by category, with links to the individual product pages via the flypage.

Recently I upgraded a site so the category URLs were a bit more SEO-friendly. The original category filtering search produced these lovely specimens:

```nohighlight
/search.html?fi=products&st=db&co=1&sf=category&se=Shoes&op=rm
   &sf=inactive&se=yes&op=ne&tf=category&ml=100
```

but what I really wanted was:

```nohighlight
/cat/Shoes.html
```

Such links are easier to communicate to users, more friendly to search engines, less prone to breakage (e.g., by getting word-wrapped in email clients), and avoid exposing details of your application (here, we've had to admit publicly that we have a table called “products” and that some items are “inactive”; a curious user might decide to see what happens if they change “sf=inactive&se=yes” to some other expression).

Here's how I attacked this.

###  Creating a category listing page 

First, I copied my “results.html” page to “catpage.html”. That way, my original search results page can continue to serve up ad hoc search results.

The search results were displayed via:

```nohighlight
[search-region]
...
[/search-region]
```

I converted this to a database query:

```nohighlight
[query sql="SELECT * FROM products WHERE NOT inactive AND category = [sql-quote][cgi category][/sql-quote]"
 type=list prefix=item]
...
[/query]
```

I chose to use a prefix other than the default since it would avoid having to change so many tags in the page, and now both the original search page and new catpage would look much the same internally (and thus, if desired, I could refactor them in the future).

Note that I've defined part of the API for this page: the category to be searched is set in a CGI variable called “category”.

In my specific case, there was additional tinkering with this tag, because I had nested [query] tags already in the page within the search-region.

###  Creating a “cat” actionmap 

In order to translate a URL containing SEO-friendly “/cat/Shoes.html” into my search, I need an actionmap. Here's mine; it's very simple.

```perl
Actionmap cat <<"CODE"
sub {
  my $url = shift;
  my @url_parts = split '/' => $url;
  shift @url_parts if $url_parts[0] eq 'cat';

  $CGI->{mv_nextpage} = 'catpage.html';
  $CGI->{category} = shift @url_parts;
  return 1;
}
CODE
```

Actionmaps are called when Interchange detects that a URL begins with the actionmap's name; here “cat”. They are passed a parameter containing the URL fragment (after removing all the site stuff). Here, that would be (e.g.) “/cat/Shoes”. We massage the URL to get our category code, and set up the page to be called along with the CGI parameter(s) it expects.

###  Cleaning up the links 

At the start of this article I noted that I may have a page listing all my categories. In my original setup, this generated links using a construction like this:

```html
<a href="[area href=search form=|fi=products
         st=db
         sf=category
         se=Shoes
         tf=category
         ml=100|]">
  Shoes
</a>
```

Now my links are the much simpler:

```html
<a href="[area cat/Shoes]">Shoes</a>
```

In my specific case, these links were generated within a [query] loop, but the approach is the same. 

Note: the [Strap demo](http://demo.icdevgroup.org/demo1/) supports SEO-friendly URLs out-of-the-box, and that it is included with the latest [Interchange 5.10](http://www.icdevgroup.org/i/dev/news?mv_arg=00060) release.
