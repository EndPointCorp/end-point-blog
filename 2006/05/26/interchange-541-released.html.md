---
author: Jon Jensen
gh_issue_number: 11
tags: interchange
title: Interchange 5.4.1 released
---

Interchange 5.4.1 was released today. This is a maintenance update of the web application server End Point has long supported.

There were a few important bugfixes:

- Dan Collis-Puro fixed bugs in the ITL (Interchange Tag Language) parser that can cause an infinite loop when malformed ITL opening tags are encountered.

- Stefan Hornburg fixed a regression in the htmlarea widget (word processor-style editing in web browsers) which kept it from working with Microsoft Internet Explorer and browsers claiming to be compatible.

- Brian Miller fixed an obscure profile parsing bug that kicked in when a comment immediately precedes the __NAME__ identifier.

- Kevin Walsh changed the default robot detection settings to check for "GoogleBot", rather than just "Google", to prevent false positive matches with other user agent values such as "GoogleToolbar".

- Josh Lavin and Mike Heins made improvements to the Linkpoint and VeriSign payment modules.

- Ryan Perry added support for recent versions of mod_perl 2 to Interchange::Link.

- UPS shipping rates were updated in the Standard demo.

There were also numerous other minor bugfixes in core code, tags, the admin, and the Standard demo.

We invite you to [learn more about Interchange](/technology/perl-interchange) if you're not familiar with it.
