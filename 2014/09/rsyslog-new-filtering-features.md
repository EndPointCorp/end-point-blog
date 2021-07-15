---
author: Emanuele “Lele” Calò
title: Rsyslog property based filtering features
github_issue_number: 1027
tags:
- linux
- sysadmin
date: 2014-09-04
---



Do you need something more powerful than the usual, clunky selectors based Rsyslog filtering rules but still you don’t see the benefit of going full throttle and use RainerScript?

Perhaps you weren’t aware, but there is an additional filtering rule you may not have used, which is a great alternative to the classic selector-based one, called **property-based filtering**.

This kind of filtering lets you create rules like:

```bash
:msg, contains, "firewall: IN=" -/var/log/firewall
```

There’s a few more properties that you can use like *hostname*,*fromhost*,*fromip* and the number (and variety) is growing over time.

Instead of just verifying that a specific string is contained in the highlighted property, you could also be interested in operators like *isempty*, *isequal* or the powerful *regex* and *ereregex* which could be used to compare the string content against regexes, that we all love so much.

```bash
:fromhost, regex, ".*app-fe\d{2}" -/data/myapp/frontend_servers.log
:fromhost, regex, ".*app-db\d{2}" -/data/myapp/DB_servers.log
```

Also remember that you can always use the *!* to negate the condition and the *discard operator* to block Rsyslog from further rules parsing for that specific content:

```bash
:msg, !contains, "firewall: IN=" -/data/myapp/all_logs_but_firewall_related.log
:fromhost, regex, ".*appfe\d{2}" ~ -/data/myapp/frontend_servers.log
:fromhost, regex, ".*appdb\d{2}" ~ -/data/myapp/DB_servers.log
*.* /data/myapp/all_logs_but_firewall_related_and_not_from_appfe_and_appdb_servers.log
```

In case you don’t know what the **-** (dash) sign stands for, that’s used to put the log writing process in async mode, so that Rsyslog can proceed with other filtering and won’t wait for disk I/O to confirm a successful write before proceeding to something else.

Now go back to your logging system and let us know what nice set up you came up with!

Link-ography:

- [Rsyslog Filters documentation](http://www.rsyslog.com/doc/rsyslog_conf_filter.html)
- [Rsyslog Properties documentation](http://www.rsyslog.com/doc/property_replacer.html)
- [Rsyslog RegEx support documentation](http://www.rsyslog.com/doc/expression.html)


