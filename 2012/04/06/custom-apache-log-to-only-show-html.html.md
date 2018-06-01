---
author: Ron Phipps
gh_issue_number: 584
tags: javascript, apache, ecommerce, jquery
title: Custom apache log to only show html requests
---

Today while working on an AJAX issue for [CollegeDistrict.com](http://www.collegedistrict.com) I came across a need to only see HTML requests to Apache while leaving out all of the many requests for images, css, and js files. This would make it quite easy to see when AJAX requests were making it through properly.

I found the following solution which worked well:
[https://www.serverwatch.com/tutorials/article.php/10825_3376671_2/Advanced-Logging-Techniques-With-Apache.htm](https://www.serverwatch.com/tutorials/article.php/10825_3376671_2/Advanced-Logging-Techniques-With-Apache.htm)

I used these settings in our development httpd.conf:

```nohighlight
SetEnvIf Request_URI "(\.html|\.shtml)$" html
CustomLog logs/html.log common env=html
```
