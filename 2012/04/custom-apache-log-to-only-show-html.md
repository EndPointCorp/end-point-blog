---
author: Ron Phipps
title: Custom Apache log to only show HTML requests
github_issue_number: 584
tags:
- apache
- sysadmin
date: 2012-04-06
---

Today while working on an AJAX issue for [CollegeDistrict.com](https://www.collegedistrict.com) I came across a need to only see HTML requests to Apache while leaving out all of the many requests for images, CSS, and JavaScript files. This would make it quite easy to see when AJAX requests were making it through properly.

I found [a solution which worked well](https://web.archive.org/web/20120428121948/https://www.serverwatch.com/tutorials/article.php/10825_3376671_2/Advanced-Logging-Techniques-With-Apache.htm) and used these settings in our development `httpd.conf`:

```nohighlight
SetEnvIf Request_URI "(\.html|\.shtml)$" html
CustomLog logs/html.log common env=html
```
