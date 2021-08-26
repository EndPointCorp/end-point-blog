---
author: Ron Phipps
title: SearchToolbar and dropped Interchange sessions
github_issue_number: 389
tags:
- ecommerce
- interchange
date: 2010-12-22
---



A new update to Interchange’s robots.cfg can be found [here](https://raw.githubusercontent.com/interchange/interchange/master/dist/robots.cfg). This update adds “SearchToolbar” to the NotRobotUA directive which is used to exclude certain user agent strings when determining whether an incoming request is from a search engine robot or not. The SearchToolbar addon for IE and FireFox is being used more widely and we have received reports that users of this addon are unable to add items to their cart, checkout, etc. You may remember a similiar issue with the Ask.com toolbar that we discussed [in this post](/blog/2009/11/dropped-sessions-when-askcom-toolbar-is). If you are using Interchange you should download the latest robots.cfg and restart Interchange.


