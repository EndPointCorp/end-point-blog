---
author: Ryan Masters
gh_issue_number: 123
tags: rails, seo
title: Rails and SEO advantages
---

In today's climate, search engine optimization is a must to be competitive. Rails routing provides this advantage and much more.

Descriptive, content packed URLs afford your website better search rankings because they provide a clear context as to what the page is about. Using keywords in the filename goes even further. Under normal circumstances, without advanced configuration, a web page filename is rigid and fixed. This isn't a problem in itself, except for that it doesn't help with SEO one bit.

Having multiple URLs linking to the same page opens more doors to search engine crawlers. Generally, once indexed correctly, this means more access paths in to your site which in turn a result in a greater variety and volume of traffic.

Normally in most other programming languages, you would need to use an Apache rewrite rule to accomplish this. This rule will detect a digit in a file name and pass it along as a parameter to another dynamically generated page.

```nohighlight
RewriteRule ^/.*([0-9]+).*$ /index.php?i=$1 [R=301,L]
```

This rule is definitely probably too greedy of a match, however, it serves to illustrate the point. With that rule in place, any request containing at least one number will be forwarded along to the index.php handler. Then by using a site map or just by modifying existing link structure, you can spell out multiple, descriptive, relevant URLs and increase the number of ways into your site. Not only will the quantity of links improve, but more importantly, the quality will too.

Rails does it a little different. Apache generally deals with files and for the most part isn't aware of application dynamics. This is where rails routing comes in. Rails is MVC oriented; each controller is comprised of one or many methods or actions in rails terminology. The URI is typically broken down into constituent parts in the following fashion.

```ruby
map.connect ":controller/:action/:id"
```

With rails routing, you can specify that the elements in the URL are passed along to the correct controller and corresponding method along with variables that are used in your code.

```ruby
map.connect "music/:category/:year/:month",
            :controller   => "events",
            :action       => "show",
            :requirements => {
                :year  => /(19|20)\d\d/,
                :month => /[01]\d/,
            },
```

As you can see as reflected in these examples, rails is powerful tool for building websites, well beyond SEO advantages. The point is though, for SEO, you can specify as many alternate pathways into your site utilizing keyword rich linkage. By using apache you can accomplish a lot, but with rails, you can accomplish so much more. If your application has dynamic category set that you wanted to have accessible via URI, rails would be ideal for this. With rails, not only could categories be represented, but products and product descriptions can be easily translated into the URI and then propagated out to the search engines indexes.
