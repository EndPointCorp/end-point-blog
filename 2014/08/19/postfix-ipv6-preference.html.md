---
author: Jon Jensen
gh_issue_number: 1023
tags: email, ipv6, linux, sysadmin
title: Postfix IPv6 preference
---



On a Debian GNU/Linux 7 (“wheezy”) system with both IPv6 and IPv4 networking setup, running Postfix 2.9.6 as an SMTP server, we ran into a mildly perplexing situation. The mail logs showed that outgoing mail to MX servers we know have IPv6 addresses, the IPv6 address was only being used occasionally, while the IPv4 address was being used often. We expected it to always use IPv6 unless there was some problem, and that’s been our experience on other mail servers.

At first we suspected some kind of flaky IPv6 setup on this host, but that turned out not to be the case. The MX servers themselves are fine using only IPv6. In the end, it turned out to be a Postfix configuration option called [smtp_address_preference](http://www.postfix.org/postconf.5.html#smtp_address_preference):

> 
> smtp_address_preference (default: any)
> 
> The address type (“ipv6”, “ipv4” or “any”) that the Postfix SMTP client will try first, when a destination has IPv6 and IPv4 addresses with equal MX preference. This feature has no effect unless the inet_protocols setting enables both IPv4 and IPv6. With Postfix 2.8 the default is “ipv6”.
> 
> Notes for mail delivery between sites that have both IPv4 and IPv6 connectivity:
> 
> The setting “smtp_address_preference = ipv6” is unsafe. It can fail to deliver mail when there is an outage that affects IPv6, while the destination is still reachable over IPv4.
> 
> The setting “smtp_address_preference = any” is safe. With this, mail will eventually be delivered even if there is an outage that affects IPv6 or IPv4, as long as it does not affect both.
> 
> This feature is available in Postfix 2.8 and later.
> 

That documentation made it sound as if the default had changed to “ipv6” in Postfix 2.8, but at least on Debian 7 with Postfix 2.9, it was still defaulting to “any”, thus effectively randomly choosing between IPv4 and IPv6 on outbound SMTP connections where the MX record pointed to both.

Changing the option to “ipv6” made Postfix behave as expected.


