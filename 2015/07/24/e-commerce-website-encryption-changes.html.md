---
author: Jon Jensen
gh_issue_number: 1141
tags: ecommerce, hosting, security
title: E-commerce website encryption changes
---

### The big picture

Computer security is a moving target, and during the past few years it’s been moving faster than ever.

In the e-commerce world, the [PCI Security Standards Council](https://www.pcisecuritystandards.org/) sets the rules for what merchants and vendors must do to have what they consider to be a sufficiently secure environment to handle cardholder data such as credit card numbers, expiration dates, and card security codes.

[PCI DSS 3.1, released on 15 April 2015](https://www.pcisecuritystandards.org/pdfs/15_04_15%20PCI%20DSS%203%201%20Press%20Release.pdf) puts us all on notice that TLS 1.0 is considered unfit to use for e-commerce website encryption (HTTPS), and will be disallowed soon. The new rules specify that new software implementations must not use TLS versions prior to 1.1. Existing implementations must require TLS 1.1 or 1.2 no later than 30 June 2016.

They provide some guidance on [Migrating from SSL and early TLS](https://www.pcisecuritystandards.org/documents/Migrating_from_SSL_Early_TLS_Information%20Supplement_v1.pdf) and explain what is expected in more detail.

Long ago we were required to disable SSL 2, and last year we were expected to disable SSL 3, the predecessor to TLS 1.0. That turned out to not be particularly hard or cause too many problems, because almost all systems that supported SSL 3 also supported TLS 1.0.

This time we are not so lucky. Many clients (such as browsers) and servers did not support TLS beyond version 1.0 until fairly recently. That means much more work is involved in meeting these new requirements than just changing some settings and restarting servers.

Almost every client (browser) and server that supports TLS 1.1 also supports TLS 1.2, and almost everything that doesn’t support TLS 1.2 doesn’t support TLS 1.1 either. So to keep things simpler here I’ll just talk about TLS 1.0 vs. TLS 1.2 below, and TLS 1.1 can be assumed to apply as well where TLS 1.2 is mentioned.

At End Point we deploy, support, and host e-commerce sites for many customers, so I’ll talk about the server side of this first. Note that servers can act as both server and client in TLS connections, since servers often make outgoing HTTPS connections as well as accepting incoming requests. Let’s review the situation with each of the major Linux server operating systems.

### Debian

Debian 8 is the current version, and supports TLS 1.2. It is scheduled to be supported until April 2020.

Debian 7 supports TLS 1.2, and has planned support until May 2018.

Debian’s support lifetime has historically depended on how quickly future releases come, but recently the project began to offer long-term support (LTS) for Debian 6, which was supposed to be at end of life, so it will be supported until February 2016. It also only supports TLS 1.0.

### Ubuntu

Ubuntu’s long-term support (LTS) server versions are supported for 5 years. Currently supported versions 12.04 and 14.04 both handle TLS 1.2.

Some sites are still using Ubuntu 10.04, which supports only TLS 1.0,  but its support ended in April 2015, so it should not be used any longer in any case.

### Red Hat Enterprise Linux (RHEL) and CentOS

Red Hat and CentOS are “enterprise” operating systems with a very long support lifetime of 10 years. Because that is so long, the oldest supported versions may become practically unusable due to changes in the world such as the deprecation of TLS 1.0.

RHEL/CentOS 7 is the current version, supported until June 2024. It supports TLS 1.2.

RHEL/CentOS 6 is supported until November 2020. It is mostly ok for TLS 1.2. One exception is that the bundled version of curl doesn’t support TLS > 1.0 for some reason, so if you have applications making curl client calls to other systems, they may break without workarounds.

RHEL/CentOS 5 is the oldest version still supported, until March 2017, and it is very widely used, but it does not supprt TLS > 1.0.

### Old server remediation

If you’re on an older server that doesn’t support TLS 1.2, the best thing to do is upgrade or migrate to a newer operating system, as soon as possible.

The common versions of OpenSSL that don’t support TLS 1.2 also do not support [Server Name Indication](https://en.wikipedia.org/wiki/Server_Name_Indication) used for hosting multiple HTTPS sites on the same IP address. That is now becoming more commonly used since the thing holding back acceptance was old versions of Windows XP that didn’t support it, and they are now are mostly dead. You can control whether you need SNI on the server side, avoiding it by continuing to get a separate IP address for each HTTPS site you host. But when you are a client of someone else’s service that requires SNI, you’ll wish you had it.

So migrate. That’s easier said than done, of course. Moving to a new OS version involves a lot of new system library versions, language versions, web server version, etc. Some things aren’t compatible. It takes work and time. That’s life, so accept it and move ahead. Advocate it, schedule it, do it. But in the meantime, if you must cope with old servers, there are some not entirely terrible options.

You could use plain HTTP on a local private network to talk to a newer server running [stunnel](https://www.stunnel.org) or an nginx proxy to do the TLS layer, or use a VPN if you have no private network.

You can use CDN in front of your site, which will certainly support TLS 1.2, and covers the path between the end user and the CDN, at least.

You can build your own versions of OpenSSL, any libraries that link to OpenSSL such as curl or wget, Apache or nginx, etc. This is tempting but is a terrible option, because you are almost certain to not update this hand-crafted stack often enough in the future to protect against new vulnerabilities in it. Sidestepping the operating system’s native package management for core infrastructure software like this is usually a mistake.

You could avoid that problem by using someone else’s backported parallel-install packages of all that, if you can find some, and if you think they’re trustworthy, and if they’re going to maintain them so you can get later updates. I’m not familiar with anyone doing this, but it may be out there and could be hired for the right ongoing price.

But the best bet is to start planning your upgrade or migration as soon as possible.

### Browser support for TLS 1.2

Of course the other half of the connection is the client, primarily end-users’ web browsers. On Wikipedia is a very detailed table showing various browsers’ support of various features, broken down by version, here: [TLS support history of web browsers](https://en.wikipedia.org/wiki/Transport_Layer_Security#Web_browsers). My summary follows:

**Google Chrome and Mozilla Firefox** have been automatically updating themselves for a long time, so unless you or your system administrator have disabled the auto-update, they will work with TLS 1.2.

**Internet Explorer** 8, 9, and 10 support TLS 1.2, but it is disabled by default. Not until IE 11 can TLS 1.2 be counted on to work.

**Apple Safari** 7, 8, and 9 for Mac OS X support TLS 1.2.

The built-in browser on **Android** < 4.4 doesn’t support TLS > 1.0, and Android 4.4 has TLS > 1.0 disabled by default, which is the same thing for most users. So anyone with Android < 5.0 will not be able to connect to your site unless they’re using a separate and newer mobile browser such as Chrome and Firefox.

### Browser support for TLS 1.0

I have not heard of any timelines being announced for browsers to disable TLS 1.0 yet. I suspect that’s because there are still so many servers that only support TLS 1.0. But before too long we may start to see servers catch up and then I expect browsers will eventually disable TLS 1.0.

### Other clients

There are too many non-browser clients to list here. We’ve already mentioned curl; there is also wget, and the web client libraries in Perl, Python, Ruby, and Java. PHP uses libcurl. NodeJS and Go are likely not from the operating system and newer than it, so may be more current. At any rate, some of those clients will be old and won’t support TLS 1.2, so when other sites stop allowing TLS 1.0 connections, whatever you were talking to them for will stop working.

PCI DSS will require client applications to stop using TLS 1.0 also, which may mean that applications need to be configured to require TLS 1.2 for outgoing HTTPS connections.

### Summary

**Your systems need to stop supporting TLS 1.0 by June 2016 at the latest.** Start planning the migration now! [We are available to help](/contact) our current and new clients test, assess needs, and plan upgrades and migrations.

### Reference

- “SSL and early TLS are no longer considered to be strong cryptography and cannot be used as a security control after June 30, 2016. Prior to this date, existing implementations that use SSL and/or early TLS must have a formal Risk Mitigation and Migration Plan in place. Effective immediately, new implementations must not use SSL or early TLS.” ―Sections 2.2.3, 2.3, 4.1 of [PCI DSS 3.1](https://www.pcisecuritystandards.org/documents/PCI_DSS_v3-1.pdf)
- [How’s My SSL?](https://www.howsmyssl.com/) — tells you how secure your TLS client is
- [Qualys SSL Labs client test](https://www.ssllabs.com/ssltest/viewMyClient.html) — a different client test
- [Qualys SSL Labs server test](https://www.ssllabs.com/ssltest/index.html) — very useful, and shows client compatibility with a server’s configuration
- [linuxlifecycle.com — Support Life Cycles for Enterprise Linux Distributions](http://linuxlifecycle.com/)
