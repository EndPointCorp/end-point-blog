---
author: "Ardyn Majere"
title: "A great gift for the holidays: No ads!"
tags: linux, security, networking
gh_issue_number: 1701
---

![Pi-hole logo](/blog/2020/12/03/pihole-great-holiday-gift/pihole-logo.png)

Many people will bring home a pie during the holiday season, but perhaps you’ll find a place in your home network for a [Raspberry Pi](https://www.raspberrypi.org/) instead?

With more people than ever working from home, many more people are using their personal infrastructure to conduct business, and aren’t able to rely on a crack team of network engineers to make sure their system is secure. While there are many things one can do to improve network security, from using a VPN to ensuring you update your system, a Pi-hole is one quick, inexpensive way to help keep your network a little safer not just on your phone or laptop, but on every device that connects to your router.

It’s great not only for technical types, but for everyone who connects to your network. You can even set it up with remote access and gift it to a relative, as long as you’re willing to fix it if it breaks. With the holiday season coming up, it’s surely something to consider.

### Shut the door with Pi-hole

[Pi-hole](https://pi-hole.net/) is an open source DNS server for your local network which blocks advertising and, after adding some extra block lists, some malicious websites.

This is done before the data even gets downloaded, by redirecting requests for ads and garbage to a blank page, which means your internet will be faster as well as safer—this is especially important if you’re sharing networks with spouses and kids. It doesn’t rely on any client-side software, either, so it works regardless of platform, even on some smart TVs and apps. (Remember to support the websites and apps you use by other means if possible, though!)

In addition to securing your network by allowing you to block malware, there’s an optional step that you can take to secure your DNS entirely: [Encrypted DNS](https://docs.pi-hole.net/guides/dns-over-https/). With this, you can stop your ISP or any other entity from not only tampering with your DNS results, but seeing them at all. It won’t stop state actors, but it should help keep your browsing data from being sold.

Here’s some example stats from the author’s home. This is one (rather heavy) day’s worth of traffic!

![Example stats](/blog/2020/12/03/pihole-great-holiday-gift/example-display.png)

### Installing Pi-hole

What sort of knowledge do you need in order to be able to install Pi-hole? Well, it does require some minimal command line knowledge. However, if you don’t already have this, then this is a great first project to learn with.

The Pi-hole website offers [great instructions](https://docs.pi-hole.net/main/prerequisites/) for installing the software. While you may want to use it as initially intended—on a $35 Raspberry Pi board—you don’t have to purchase new hardware. You can run Pi-hole on any Linux server, or even on a Docker instance or using a virtual machine on many different services. 

> If you’re an End Point fan, our brand [Open Hosting](https://www.openhosting.com/) can provide you with an inexpensive Linux container machine for under $5 a month that will easily handle a large household’s DNS requirements.

Just make sure that whatever system you install Pi-hole on is always turned on and stable (unplug the Pi-hole and your internet may stop working for the house, something I know my own family hates to have happen).

### Adding blocklists

Adding blocklists is as simple as putting in a link to a text file with the offending hostnames. There are quite a few blocklists curated on the page. The trick is to choose blocklists that will meet your requirements—Some of the block lists can generate false positives. If you’re using Pi-hole for yourself, that’s probably not an issue since you can manually whitelist things as you go, but if you have a larger household, you may want to stick with the more conservative whitelists. Same if you’re setting this up for a relative or family member where you won’t be on site to fix things.

> [Firebog.net](https://firebog.net/) has a good list of block lists, sorted by category. Green checkmarks are best for minimal maintenance situations; the other categories may incur false positives that require whitelisting.

### Encrypted DNS

While blocking ads is a great start, to add further security to your DNS, you have several options.

You can enable DNSSEC, which doesn’t encrypt your DNS but does validate it, assuming the domain owner actually enabled it. This is a good thing to enable, but it doesn’t replace true encrypted DNS. 

[Cloudflare](https://www.cloudflare.com/) is the service that Pi-hole officially recommends using, via the tool [cloudflared](https://docs.pi-hole.net/guides/dns-over-https/#configuring-dns-over-https). This routes all DNS traffic over https to Cloudflare’s DNS servers by default. There are also several other options, such as [DNSCrypt](https://www.dnscrypt.org/). There’s a debate going on about DNS over HTTPS vs DNS over TLS, which is summed up nicely by this [IEEE spectrum article](https://spectrum.ieee.org/tech-talk/telecom/security/the-fight-over-encrypted-dns-boils-over).

Do you need to do this? No. But taking this step is relatively easy and protects you and your family from slippery man-in-the-middle attacks as well as your ISP snooping on what websites you go to and selling this to advertisers.

### What can’t it do?

For now, it won’t block **all** advertising. YouTube ads aren’t blocked, nor are most streaming services that display ads from their internal servers. It won’t block ads hosted directly on the website you’re visiting. 

To keep things running smoothly, there is some maintenance required: the OS and Pi-hole need to be updated periodically, and the blocklists as well, though these tasks are easily automated.

The Pi-hole also won’t protect you from concerted attempts to get into your system. This isn’t a replacement for a good firewall or antivirus/​malware protection software, and you should of course remember to practice good browsing habits. But as a relatively simple project to set up, it’s a good way to make your browsing experience at least a little less annoying.

