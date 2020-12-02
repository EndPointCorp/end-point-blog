---
author: "Ardyn Elisabeth Majere"
title: "A Great Gift for the Holidays: No ads!"
tags: Raspberry Pi, linux, dns, security, network
---

Many people will bring home a pie during the holiday season- but perhaps you'll find a place in your home network for a Raspberry Pi instead?

With more people than ever working from home, many more people are using their personal infrastructure to conduct business, and aren't able to rely on a crack team of network engineers to make sure their system is secure.

While there are many things one can do to improve network security, from using a VPN to ensuring you update your system, one quick, inexpensive trick can help keep your network a little safer not just on your phone or laptop, but on every device that connects to your router.

It’s great not only for technical types- but for everyone who connects to your network- You can even set it up with remote access and gift it to a relative- As long as you’re willing to fix it if it breaks - And with the holiday season coming up, it’s surely something to consider.

## Shut the door with Pi-Hole

Pi-Hole is an open source DNS server for your local network which blocks advertising and, by adding some extra block lists, some malicious websites.

This is done before the data even gets downloaded, by redirecting requests for ads and garbage to a blank page, which means your internet will be faster as well as safer- especially important if you're sharing networks with spouses and kids. It doesn't rely on any client side software, either, so it works irregardless of platform- even on smart TVs and inside apps. (Remember to support the websites and apps you use by other means, if you can, though!)

In addition to securing your network by allowing you to block malware- there's an additional step that you can take to secure your DNS entirely- Encrypted DNS.

With this, you can stop your ISP or any other entity from not only tampering with your DNS results, but seeing them at all. (It won't stop state actors, but it should help keep your browsing data from being sold.)

![Here's some example stats from the Author's home. This is one (rather heavy) day's worth of traffic!](/2020/12/03/pihole_great_holiday_gift/example_display.png)

## Installing Pi-Hole

What sort of knowledge do you need in order to be able to install Pi-Hole? Well, it does require some minimal command line knowledge- If you don't already know this, then this is a great first project to learn with.

The [Pi-Hole website](https://pi-hole.net/) offers great instructions for installing the software. While you may want to use it as initially intended- on a $35 Raspberry Pi board- you don't have to purchase new hardware. You can run Pi-Hole on any linux server, or even on a [Docker instance] or using a Virtual Machine on many different services. 
s
> If you’re an End Point fan, Our brand, Open Hosting, can provide you with an inexpensive linux container machine for under $5 a month that will easily handle a large household’s DNS requirements- check out Open Hosting here: [https://www.openhosting.com/](https://www.openhosting.com/) 

Just make sure that whatever system you install Pi-Hole on is always up and stable- unplug the pi-hole and your internet may stop working for the house- Something I know my own family hates to have happen.

## Adding blocklists

Adding blocklists is as simple as putting in a link to a text file with the offending URLs. There are quite a few blocklists curated on the page . The trick is to choose blocklists that will meet your requirements- Some of the block lists can generate false positives. 

If you’re using Pi-hole for yourself, that’s probably not an issue if you can manually whitelist things as you go, but if you have a large family, you may want to stick with the more conservative whitelists. Same if you’re setting this up for a relative or family member where you won’t be on site to fix things.

>**_[Firebog.net](https://firebog.net/)_** has a good list of block lists, sorted by category- Green checkmarks are best for minimal maintenance situations- the other categories may incur false positives that require whitelisting.


## Encrypted DNS

While blocking ads is a great start, To add further security to your DNS, you have several options.

You can enable DNSSEC, which doesn't encrypt your DNS but does validate it- assuming the website owner actually enabled it. This is a good thing to enable, but it doesn't replace true encrypted DNS. 

[Cloudflared](https://docs.pi-hole.net/guides/dns-over-https/) is the service that Pi-Hole officially recommends, which routes all DNS traffic over https to Cloudflare's DNS servers by default- but there are several other options, such as [DNSCrypt](https://www.dnscrypt.org/) (a DNSCrypt proxy can be used here instead of Cloudflared) There's a debate going on over DNS over HTTPS vs DNS over TLS which is summed up nicely by this [IEEE spectrum article](https://spectrum.ieee.org/tech-talk/telecom/security/the-fight-over-encrypted-dns-boils-over)

Do you need to do this? No. But taking this step is relatively easy and protects yourself and your family from slippery man in the middle attacks- and from your ISP snooping on what websites you go to and selling this to advertisers.

## What can’t it do?

For now, it won’t block ALL advertising. YouTube ads aren’t blocked- same for most streaming services that display ads from their internal servers. It won’t block ads hosted directly on the website you're visiting. 

To keep things running smoothly, there is some maintenance required- the OS and Pi-Hole need to be updated, and the blocklists as well- though these tasks are easily automated .

The Pi-Hole also won’t protect you from concerted attempts to get into your system. This isn’t a replacement for a good firewall or antivirus/malware protection software, and you should of course remember to practice good browsing habits.

But as a relatively simple project to set up, it’s a good way to make your browsing experience at least a little less annoying.

