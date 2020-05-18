---
author: Ron Phipps
gh_issue_number: 109
tags: hosting, seo
title: Apache RewriteRule to a destination URL containing a space
---

Today I needed to do a 301 redirect for an old category page on a client’s site to a new category which contained spaces in the filename. The solution to this issue seemed like it would be easy and straight forward, and maybe it is to some, but I found it to be tricky as I had never escaped a space in an Apache RewriteRule on the destination page.

The rewrite rule needed to rewrite:

```nohighlight
/scan/mp=cat/se=Video Games
```

to:

```nohighlight
/scan/mp=cat/se=DS Video Games
```

I was able to get the first part of the rewrite rule quickly:

```nohighlight
^/scan/mp=cat/se=Video\sGames\.html$
```

The issue was figuring out how to properly escape the space on the destination page. A literal space, %20 and \s all failed to work properly. Jon Jensen took a look and suggested a standard Unix escape of ‘\ ’ and that worked. Some times a solution is right under your nose and it’s obvious once you step back or ask for help from another engineer. Googling for the issue did not turn up such a simple solution, thus the reason for this blog posting.

The final rule:

```nohighlight
RewriteRule ^/scan/mp=cat/se=Video\sGames\.html$ http://www.site.com/scan/mp=cat/se=DS\ Video\ Games.html [L,R=301]
```
