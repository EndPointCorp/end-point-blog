---
author: Ron Phipps
title: Dropped sessions when Ask.com Toolbar is installed
github_issue_number: 225
tags:
- community
- ecommerce
- interchange
- tips
date: 2009-11-18
---

We’ve been dealing with an issue on a client’s site where customers were reporting that they could not login and when they added items to their cart the cart would come up empty. This information pointed towards a problem with the customer’s session being dropped, but we were unable to determine the common line across these customer’s environments and came up empty handed. This was a case of being unable to reproduce a problem which made it nearly impossible to fix.

This morning on the Interchange users list there was a post from Racke discussing a similiar issue. His customer had the Ask.com toolbar installed and Interchange’s robot matching code was mistakenly matching the Ask.com toolbar as a search spider. The user agent of the browser with Ask.com installed appeared as so:

`Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; msn OptimizedIE8;ENUS; AskTB5.6)`

A quick look at the current robots.cfg that Steven Graham linked showed that ‘AskTB’ had been added to the NotRobotUA directive which instructs Interchange to not consider AskTB a search spider, thus allowing proper use of sessions on the site.

Updating the robots.cfg on our client’s site allowed users with Ask.com to browse, login and checkout as expected. Those with Interchange sites who see reports of similiar issues should consider a false positive spider match a possibility and update their robots.cfg.
