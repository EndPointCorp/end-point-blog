---
author: Jon Jensen
title: Multiple reverse DNS pointers per IP address
github_issue_number: 77
tags:
- networking
date: 2008-11-28
---

I recently ran across an IP address that had two PTR (reverse DNS) records in DNS. I’ve always thought that each IP address is limited to only a single PTR record, and I’ve seen this rule enforced by many ISPs, but I don’t remember ever seeing it conclusively stated.

I was going to note the problem to the responsible person but thought it’d be good to test my assumption first. Lo and behold, it’s not true. The [Wikipedia “Reverse DNS lookup” page](https://en.wikipedia.org/wiki/Reverse_DNS_lookup) and a source it cites, an [IETF draft on reverse DNS](https://tools.ietf.org/html/draft-ietf-dnsop-reverse-mapping-considerations-06), note that multiple PTR records per IP address have always been allowed.

There is apparently plenty of software out there that can’t properly deal with more than one PTR record per IP address, and with too many PTR records, a DNS query response will no longer fit inside a single UDP packet, forcing a TCP response instead, which can cause trouble of its own. And as I noted, many ISPs won’t allow more than one PTR record, so in those cases it’s an academic question.

But it’s not invalid, and I saved myself and someone else a bit of wasted time by doing a quick bit of research. It was a good reminder of the value of checking assumptions.
