---
author: Jon Jensen
title: Apache accidental DNS hostname lookups
github_issue_number: 854
tags:
- devops
- hosting
- linux
- networking
date: 2013-09-18
---

Logging website visitor traffic is an interesting thing: Which details should be logged? How long and in what form should you keep log data afterward? That includes questions of log rotation frequency, file naming, and compression. And how do you analyze the data later, if at all?

Allow me to tell a little story that illustrates a few limited areas around these questions.

### Reverse DNS PTR records

System administrators may want to make more sense of visitor IP addresses they see in the logs, and one way to do that is with a reverse DNS lookup on the IP address. The network administrators for the netblock that the IP address is part of have the ability to set up a PTR (pointer) record, or not. You can find out what it is, if anything.

For example, let’s look at DNS for End Point’s main website at www.endpoint.com using the standard Unix tool “host”:

```plain
% host www.endpoint.com
www.endpoint.com has address 208.43.132.31
www.endpoint.com has IPv6 address 2607:f0d0:2001:103::31
% host 208.43.132.31
31.132.43.208.in-addr.arpa domain name pointer 208.43.132.31-static.reverse.softlayer.com.
% host 2607:f0d0:2001:103::31
1.3.0.0.0.0.0.0.0.0.0.0.0.0.0.0.3.0.1.0.1.0.0.2.0.d.0.f.7.0.6.2.ip6.arpa domain name pointer 2607.f0d0.2001.0103.0000.0000.0000.0031-static.v6reverse.softlayer.com.
```

The www.endpoint.com name points to both an IPv4 and an IPv6 address, so there are two answers. When each of those IP addresses is looked up, each shows a PTR record pointing to a subdomain of softlayer.com, which gives a clue about where our site is hosted.

(As an aside: Why don’t we use a prettier or more specific PTR record? We could set it to almost whatever we want. Well, there are dozens of websites hosted on those IP addresses, so which one should be in the PTR record? There’s no obvious choice, and it doesn’t matter for normal network functioning, so we just left it the way it was.)

So, is a PTR record like these useful to know about visitors to your website? Sometimes. Let’s take a look at a random sample of visitors to a different website we manage. How much can you tell about each of the visitors based on their reverse DNS PTR records? Is it a bot, someone at home or the office, in which country, and who is their Internet provider? How common is it for a visitor’s IP address to have no PTR record? And keep in mind that most of the visitors have no idea what their IP address or its PTR record is.

```plain
% host 93.137.189.55
55.189.137.93.in-addr.arpa domain name pointer 93-137-189-55.adsl.net.t-com.hr.
% host 66.249.73.121
121.73.249.66.in-addr.arpa domain name pointer crawl-66-249-73-121.googlebot.com.
% host 88.134.68.31
31.68.134.88.in-addr.arpa domain name pointer 88-134-68-31-dynip.superkabel.de.
% host 67.49.156.20
20.156.49.67.in-addr.arpa domain name pointer cpe-67-49-156-20.hawaii.res.rr.com.
% host 123.211.36.234
234.36.211.123.in-addr.arpa domain name pointer CPE-123-211-36-234.lnse3.cha.bigpond.net.au.
% host 91.75.70.162 
Host 162.70.75.91.in-addr.arpa. not found: 3(NXDOMAIN)
% host 209.82.97.10
10.97.82.209.in-addr.arpa domain name pointer mail02.westjet.com.
% host 76.70.117.223
223.117.70.76.in-addr.arpa domain name pointer bas1-toronto26-1279686111.dsl.bell.ca.
% host 101.160.207.115 
Host 115.207.160.101.in-addr.arpa. not found: 3(NXDOMAIN)
% host 184.198.177.214
214.177.198.184.in-addr.arpa domain name pointer 184-198-177-214.pools.spcsdns.net.
% host 84.199.97.130
130.97.199.84.in-addr.arpa domain name pointer 84-199-97-130.iFiber.telenet-ops.be.
% host 182.19.87.24 
Host 24.87.19.182.in-addr.arpa. not found: 3(NXDOMAIN)
% host 62.34.219.216
216.219.34.62.in-addr.arpa domain name pointer i01v-62-34-219-216.d4.club-internet.fr.
216.219.34.62.in-addr.arpa domain name pointer lns-c10k01-v-62-34-219-216.dsl.sta.abo.bbox.fr.
% host 187.86.213.190
Host 190.213.86.187.in-addr.arpa. not found: 3(NXDOMAIN)
% host 15.211.201.84
84.201.211.15.in-addr.arpa domain name pointer zccy01cs104.houston.hp.com.
% host 161.69.46.150
150.46.69.161.in-addr.arpa domain name pointer miv-scan015.scanalert.com.
% host 77.182.146.99
99.146.182.77.in-addr.arpa domain name pointer essn-4db69263.pool.mediaWays.net.
% host 107.0.160.152 
152.160.0.107.in-addr.arpa domain name pointer 107-0-160-152-ip-static.hfc.comcastbusiness.net.
```

Did you notice that one IP address returned two different PTR records? That is allowed, though uncommon, as I mentioned in my blog post [Multiple reverse DNS pointers per IP address](/blog/2008/11/multiple-reverse-dns-pointers-per-ip) a few years back. Many reverse DNS control panels provided by commodity hosting providers won’t allow you to assign multiple PTR records, but if you get your reverse DNS delegated to a real nameserver you control, you can do it.

### Finding the IP address owner: whois

The reverse DNS PTR can be set misleadingly, such that a forward lookup on the name does not point back to the same IP address. In the end the way to really know who controls that IP address (or at least a network provider who supplies the ultimately responsible person) is with a “whois” lookup. We can check that the 208.43.132.31 IP address really is hosted at SoftLayer, and for which customer, like this:

```plain
% whois 208.43.132.31
[Querying whois.arin.net]
[Redirected to rwhois.softlayer.com:4321]
[Querying rwhois.softlayer.com]
[rwhois.softlayer.com]
%rwhois V-1.5:003fff:00 rwhois.softlayer.com (by Network Solutions, Inc. V-1.5.9.5)
network:Class-Name:network
network:ID:NETBLK-SOFTLAYER.208.43.128.0/19
network:Auth-Area:208.43.128.0/19
network:Network-Name:SOFTLAYER-208.43.128.0
network:IP-Network:208.43.132.0/27
network:IP-Network-Block:208.43.132.0-208.43.132.31
network:Organization;I:End Point Corporation
network:Street-Address:920 Broadway, Suite 701
network:City:New York
network:State:NY
network:Postal-Code:10010
network:Country-Code:US
network:Tech-Contact;I:sysadmins@softlayer.com
network:Abuse-Contact;I:abuse@endpoint.com
network:Admin-Contact;I:IPADM258-ARIN
network:Created:2007-06-18 12:15:54
network:Updated:2010-11-21 18:59:43
network:Updated-By:ipadmin@softlayer.com

%referral rwhois://root.rwhois.net:4321/auth-area=.
%ok
```

So you can see that’s really End Point’s IP address, at SoftLayer.

Use your local whois tool or search for a web-based one and look up a few of the IP addresses that didn’t have reverse DNS PTR records in our log cross-section above. The results are interesting.

### Reverse lookups in Apache httpd

Now let’s say that as a system administrator you would like to see the PTR records for visitor IP addresses on your Apache httpd website. It may be tempting to use the [HostnameLookups](http://httpd.apache.org/docs/2.2/mod/core.html#hostnamelookups) configuration directive to do real-time lookups and put them in the log alongside the IP address. It’s easy but not wise to put the PTR record *instead* of the IP address, because it may not point back to the IP address, and even if it does, it can change over time, and will not provide a complete picture of the connection later on.

However, if you read the [HostnameLookups documentation](http://httpd.apache.org/docs/2.2/mod/core.html#hostnamelookups), you’ll see the authors recommend it not be enabled on busy production servers because of the extra network traffic and delay for visitors, especially for any netblocks with slow DNS servers (and there are many out there). This is important! It really should almost never be enabled for any public site.

Most web server administrators learn this early on and wouldn’t dream of enabling HostnameLookups.

However, I recently came across a situation where we inadvertently were doing the equivalent without explicitly enabling HostnameLookups. How? By limiting access based on the remote hostname! Read the documentation on the [Allow directive](http://httpd.apache.org/docs/2.2/mod/mod_authz_host.html#allow), under the section “A (partial) domain-name”:

> 
> This configuration will cause Apache to perform a double reverse DNS lookup on the client IP address, regardless of the setting of the HostnameLookups directive. It will do a reverse DNS lookup on the IP address to find the associated hostname, and then do a forward lookup on the hostname to assure that it matches the original IP address. Only if the forward and reverse DNS are consistent and the hostname matches will access be allowed.
> 

This makes perfect sense, but it is a pretty big likely unexpected side effect to using something like:

```
Allow from .example.com
```

In our case it was an even less obvious case that didn’t make us think of hostnames at all:

```
Allow from localhost
```

Here localhost was written, perhaps to save some effort or maybe increase clarity vs. writing out 127.0.0.1 (IPv4) and ::1 (IPv6). Mentally it’s so easy to view “localhost” is a direct alias for 127.0.0.1 and ::1 that we can forget that the name “localhost” is just a convention, and requires a lookup like any other name. Those familiar with the MySQL database may know that it actually assigns special confusing meaning to the word “localhost” to make a UNIX socket connection instead of a TCP connection to 127.0.0.1 or whatever “localhost” is defined as on the system!

You may also be thinking that looking up 127.0.0.1 is fast because that is usually mapped to “localhost” in /etc/hosts. True, but every other visitor who is not in /etc/hosts gets the slow DNS PTR lookup instead! And depending on the operating system, you may see “ip6-localhost” or “ip6-loopback” (Debian 7, Ubuntu 12.04), “localhost6” (RHEL 5/6, Fedora 19) in /etc/hosts, or something else. So it’s important to spell out the addresses:

```
Allow from 127.0.0.1
Allow from ::1
```

Doing so immediately stops the implicit HostnameLookups behavior and speeds up the website. In this case it wasn’t a problem, since it was for a private, internal website that couldn’t be visited at all by anyone not first allowed through a firewall, so traffic levels were relatively low. That access control is part of why localhost needed to be allowed in the first place. But it would have been very bad on a public production system due to the slowdown in serving traffic.

### The right way

If you really want to see PTR records for every visitor IP address, you can use Apache’s [logresolve](http://httpd.apache.org/docs/2.2/programs/logresolve.html) log post-processing program. Or you can let an analytics package do it for you.

So, lesson learned: It’s not just HostnameLookups you need to keep turned off. Also watch out for the Apache Allow directive and don’t use it with anything other than numeric IP addresses!
