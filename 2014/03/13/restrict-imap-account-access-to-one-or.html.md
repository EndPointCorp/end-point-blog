---
author: Emanuele “Lele” Calò
gh_issue_number: 945
tags: email, iptables, security
title: Restrict IMAP account access to one (or more) IP address
---



If you’re in need of some extra layer of security on your mail server and know in advance who is going to access your IMAP account and from where (meaning which IP), then the following trick could be the perfect solution for you.

In order to use this feature you’ll have to use *Dovecot 2.x+* and then just add a comma separated list of addresses/subnets to the last field of your dovecot passwd auth file:

```bash
user:{plain}password::::::allow_nets=192.168.0.0/24,10.0.0.1,2001:abcd:abcd::0:0/80
```

After a quick reload Dovecot will start to enforce the specified new settings.

An additional neat aspect is that from an attacker perspective the given error will always be the same one got from a “wrong password” attempt, making basically impossible to discover this further protection.

Stay safe out there!
