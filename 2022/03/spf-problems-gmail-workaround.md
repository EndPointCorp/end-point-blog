---
author: "Jon Jensen"
title: "Working around SPF problems delivering to Gmail"
date: 2022-03-30
tags:
- email
- sysadmin
- hosting
github_issue_number: 1847
---

![Hand-drawn signs reading "Someplace", "Any pla…", "No place", with arrows pointing variously, attached to a leaning signpost in front of a high mountain desert scene with snow-topped peaks and sagebrush](/blog/2022/03/spf-problems-gmail-workaround/20220321_194242-sm.webp)
Photo by Garrett Skinner

### Email deliverability

Legitimate email delivery keeps getting harder. Spammers and phishers never stop flooding everyone's inboxes with unwanted and harmful email, so automated defenses against junk mail are necessary. But they are not perfect, and good email sometimes gets flagged as spam.

When sending important "transactional" email such as for account confirmations, password resets, and ecommerce receipts, it is often worth using a paid email delivery service to increase deliverability. Those typically cost a flat amount per month for up to a certain quota of outgoing email, with overage charges for messages beyond that.

Many of our clients use one of those services and generally they have all worked well and differ mostly in pricing and feature set. Popular choices include SendGrid, Mandrill, Postmark, Mailgun, and Amazon SES.

We continue to have many cases where we want to be able to send potentially large amounts of automated email to ourselves, our clients, or our systems. This is usually for testing, notifications, or internal delivery to special mailboxes separate from our main mailboxes.

These other uses for sending email keep us involved in the fight for good email deliverability from our own servers, which we have worked at over many years, long predating these paid email delivery services.

### Sender Policy Framework

One of the longest-running tools to fight spam is SPF, the Sender Policy Framework.

SPF is an open standard that provides a way for a receiving mail server to verify that the sending server is authorized to send email for the message's "envelope" sender domain. The envelope sender address or "return-path" is not normally seen by email recipients, but is used behind the scenes by servers. It may or may not be the same as the sender seen in the "From" header.

The SPF policy for each domain is set in a special DNS TXT record for that domain.

The important thing is that each sender's email belongs to a domain with a valid SPF record showing that the sending servers are allowed to send for that domain, and that all other servers should *not* be allowed to send email for that domain.

For example, our endpointdev\.com domain currently has this TXT record to define its SPF policy:

```plain
v=spf1 a:maildrop.endpointdev.com include:_spf.google.com include:servers.mcsv.net -all
```

Let's look at each of those space-separated elements:

* `v=spf1` designates this TXT record as an SPF policy, version 1 (the only one so far).
* `a:maildrop.endpointdev.com` means to allow the A (IPv4) and/or AAAA (IPv6) IP address(es) of hostname maildrop.endpointdev\.com as a valid source.
* `include:_spf.google.com` means to look up another DNS TXT record at \_spf.google.com (for Gmail, our main email provider here) and add its SPF policy to ours.
* `include:servers.mcsv.net` is the same thing, but for servers.mcsv\.net (for Mailchimp, to allow it to deliver email newsletters for our domain).
* `-all` means to disallow any other senders.

With such a policy, receiving mail servers can immediately reject any incoming email claiming to be sent by us for our domain if it didn't come from one of our designated servers.

This obviously doesn't stop all spam, but it stops a whole class of forged senders, which is very helpful.

The key point to note is that SPF applies to the sending email server at the moment it connects to the receiving email server. It doesn't deal with anything else.

One other point to note is that SPF policies are limited to a fairly small total number of DNS lookups via `include` elements, so we can't endlessly add new valid sending servers to our list.

### Email server trails

Based on the above SPF policy, if we want to send email from address `notifier@endpointdev.com`, it will have to be sent through `maildrop.endpointdev.com`, Gmail, or Mailchimp. Messages coming from any other sending server should be rejected by the receiving server. They don't have to behave that way, but it is in their interest to do so if they don't like spam.

We have an internal server we'll call `dashboard.endpointdev.com`, which sends email notifications from address `notifier@endpointdev.com`.

Since we don't want to bloat our SPF policy, we'll have our server `dashboard.endpointdev.com` route its outgoing email through our mail forwarding service called maildrop, which lives on two or more servers behind the DNS name `maildrop.endpointdev.com`.

This is a good idea for several reasons:

* It keeps all our outgoing email flowing through a few places so we can easily monitor them for any problems.
* We don't need to have SMTP daemons running on all our servers just to send outbound email.
* We don't need to worry about the quotas or pricing of commercial emailing services when sending less-important or internal-only email.

Since SPF is designed for a receiving email server to check that the server connecting to it to send email is authorized to do so for that email address's domain, it shouldn't matter what server the email originated on.

### Gmail misuses header information in SPF checks

We recently discovered that Gmail has been misusing email header information in its SPF checks.

When one of our outgoing emails originated from server `dashboard.endpointdev.com` and was then forwarded to `maildrop.endpointdev.com` which then delivered it to Gmail, Gmail looked at the earliest sender server it could find in the `Received` headers of the email message, found `dashboard.endpointdev.com`, and flagged it as an SPF failure because our SPF policy didn't include `dashboard.endpointdev.com` [206.191.128.233].

This can be seen in this excerpt of relevant email headers. (Some specific details here were changed to protect the innocent.) Note that email headers appear in reverse chronological order, so the most recent events are at the top:

```plain
Received: from maildrop14.epinfra.net (maildrop14.epinfra.net. [69.25.178.35])
        by mx.google.com with ESMTPS id l20si5561179oos.78.2022.01.25.10.52.05
        for <notifications@endpointdev.com>
        (version=TLS1_3 cipher=TLS_AES_256_GCM_SHA384 bits=256/256);
        Tue, 25 Jan 2022 10:52:05 -0800 (PST)
Received-SPF: fail (google.com: domain of notifier@endpointdev.com does not designate 206.191.128.233 as permitted
    sender) client-ip=206.191.128.233;
Authentication-Results: mx.google.com;
       dkim=pass header.i=@endpointdev.com header.s=maildrop header.b=hR445V77;
       spf=fail (google.com: domain of notifier@endpointdev.com does not designate 206.191.128.233 as permitted
    sender) smtp.mailfrom=notifier@endpointdev.com
Received: from dashboard.endpointdev.com (dashboard.endpointdev.com [206.191.128.233])
    by maildrop14.epinfra.net (Postfix) with ESMTP id A2AA03E8A7
    for <notifications@endpointdev.com>; Tue, 25 Jan 2022 18:52:05 +0000 (UTC)
To: <notifications@endpointdev.com>
```

That is wrong! The SPF check should have been done against `maildrop14.epinfra.net` [69.25.178.35] because that is the IP address that actually connected to Gmail to send the email. That server is one of our infrastructure hostnames allowed to send email as part of the `maildrop.endpointdev.com` DNS record, so checking it would have led Gmail to give a passing SPF result.

Why did Gmail do this? I don't know, and at the time didn't find any public discussion that would explain it. I suspect it has something to do with Gmail's internal systems being comprised of many, many servers, and the SPF check being done long after the email was passed on from the initial receiving point through various other servers. Then Gmail parses the headers to find out who the sender was, and gets confused.

### Don't share TMI

We can avoid this problem by not having maildrop mention our original sending server `dashboard.endpointdev.com` at all.

Why should it mention it in the first place? It's helpful for tracing problems when debugging, but really is TMI (too much information) for normal email sending, and exposes internal infrastructure details that would be better omitted anyway.

Since `dashboard.endpointdev.com` is running the very flexible and configurable Postfix email server, we can direct it to remove any `Received` headers that mention our internal hostnames.

By default Postfix in `/etc/postfix/main.cf` has the `header_checks` directive set to look at a table to match regular expressions and take specified actions.

So we added a regular expression to match and designated the action `IGNORE`, to the file `/etc/postfix/header_checks`:

```plain
/^Received:\ (from|by)\ .*(epinfra\.net|endpointdev\.com|localhost|localdomain)/  IGNORE
```

Then we update the map database file so that it takes immediate effect for new email flowing through Postfix:

```sh
postmap /etc/postfix/header_checks
```

When we sent another notification email from `dashboard.endpointdev.com` and received it in Gmail we saw the email's headers look like this:

```plain
Received: from maildrop14.epinfra.net (maildrop14.epinfra.net. [69.25.178.35])
        by mx.google.com with ESMTPS id g72si1894187vke.271.2022.01.25.11.03.37
        for <notifications@endpointdev.com>
        (version=TLS1_3 cipher=TLS_AES_256_GCM_SHA384 bits=256/256);
        Tue, 25 Jan 2022 11:03:37 -0800 (PST)
Received-SPF: pass (google.com: domain endpointdev.com configured 69.25.178.35 as internal address)
Authentication-Results: mx.google.com;
       dkim=pass header.i=@endpointdev.com header.s=maildrop header.b=qkccUkkU;
       spf=pass (google.com: domain endpointdev.com configured 69.25.178.35 as internal address)
    smtp.mailfrom=notifier@endpointdev.com
To: <notifications@endpointdev.com>
```

There is no more mention of `dashboard` or its IP address, so Gmail runs its SPF check against the proper IP address 69.25.178.35 which belongs to server `maildrop14.epinfra.net` which is part of the `maildrop.endpointdev.com` DNS name. Gmail now validates that IP address is allowed to send for the endpointdev\.com domain and gives a "pass" result for its SPF check.

Perhaps this will help your legitimate email delivery too!

### Reference

* [SPF Introduction](http://www.open-spf.org/Introduction/)
* [Postfix mail server](https://www.postfix.org/)
