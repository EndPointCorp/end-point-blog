---
author: David Christensen
title: Remove specific CGI variables using Apache
github_issue_number: 486
tags:
- ecommerce
- sysadmin
- tips
- tools
date: 2011-08-10
---



Sometime you need to remove a single CGI variable from a query string in your published URLs; for instance, one of our client’s site had gotten spidered with a session id in the generated links, so we wanted to ensure that those URLs would be appropriately updated when re-spidered. Apache’s mod_rewrite to the rescue!

The following snippet serves to rewrite any URL which has a query string parameter named id to one the exact same without that CGI variable. Since mod_rewrite uses PCRE, we can use this to our advantage by using \b word break anchors to ensure we’re only picking up a CGI variable named **exactly** the same, so (say) id=bar will be removed but tid=foo will pass on through the rewrite unaltered.

```nohighlight
# already assume RewriteEngine on

RewriteCond %{QUERY_STRING} ^(.*)\bid=(\w*)\b(.*)
RewriteRule (.*) $1?%1%3 [R=301,L]
```

Note in the above example that we know the range of values that was present for the id variable, so \w is sufficient to determine the full value to remove in this case. $*N* is the replacement from the *N*th RewriteRule group and %*N* is the replacement from the *N*th RewriteCond group. We use [R=301] to trigger an external 301 redirect, which search engines should see as redirecting to the now canonical rewritten URL.

To validate this covered all cases, I tested against URLs without the id variable defined at all, ones with id=*foo* at the beginning, middle, end, and as the sole item in the query string and verified it worked as expected in all cases. I’d earlier had multiple cases to handle each of the above scenarios, but mod_rewrite is smart enough to handle the query string merging so you don’t end up with URLs like http://example.com/?**&**foo=1 (note ampersand) when the query string portion is ?id=2&foo=1.

We put this rule in front of everything else so if the request matches, it’ll trigger before any other special handling is considered. Hope this helps someone else!


