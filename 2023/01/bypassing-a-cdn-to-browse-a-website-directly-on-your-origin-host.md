---
title: "Bypassing a CDN to browse a website directly on your origin host"
author: Seth Jensen
date: 2023-01-20
github_issue_number: 1934
tags:
- hosting
- cdn
description: Sometimes you need to bypass your CDN and test your website directly on its origin server. This has gotten harder with newer browser features like Secure DNS in Chrome and Firefox. Here's how to do it on Windows, macOS, and Linux.
featured:
  endpoint: false
  image_url: /blog/2023/01/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/winter-mountains.webp
---

![A pale winter morning, looking out over a valley from a mountainside](/blog/2023/01/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/winter-mountains.webp)

<!-- Photo by Seth Jensen, 2023 -->

Using a content distribution network (CDN) has many advantages over serving a website directly, and for any reasonably large website, you should use one. Those advantages include:

* Caching at each of the CDN's PoPs (points of presence).
* Often thousands of PoPs around the world, so traffic will be quick for everyone regardless of how far away they are from your origin server.
* Blocking of some Bad Guys automatically at the edge, including DDoS (distributed denial of service attacks) mitigation help.
* Origin IP address insulation. Hiding the origin IP address is useful to protect against DDoSes, since CDNs are generally well-defended against DDoS and your origin server probably is not as much.

You should generally be cautious about revealing your websites' origin IP address. We serve other sites from our origin directly, so we don't worry too much about sharing it here.

### Straight to the source

Sometimes, though, you need to bypass your CDN and test your website directly on its origin server. For example, if you need to test that your website would still work if the CDN goes down, or to sidestep CDN caching or content modification when troubleshooting a problem.

It can be surprisingly confusing to bypass the CDN by yourself and not for the rest of your visitors, especially with newer features like Secure DNS in Chrome and Firefox muddying up traditional DNS resolution behaviors.

We'll use a browser extension called IPvFoo (available for Chrome and Firefox) to see which IP address our hostname resolves to. Install IPvFoo from the [Chrome Web Store](https://chrome.google.com/webstore/detail/ipvfoo/ecanpcehffngcegjmadlcijfolapggal) or Firefox's [addons.mozilla.org](https://addons.mozilla.org/en-US/firefox/addon/ipvfoo-pmarks/) and then click on its indicator next to the search bar.

Before we change anything, www\.endpointdev.com resolves to 104.21.30.147:

![IPvFoo showing Cloudflare's IP address](/blog/2023/01/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/cloudflare.webp)

After a quick `whois` search, we see that this IP address belongs to Cloudflare, our CDN:

```plain
$ whois 104.21.30.147

✀
OrgName:        Cloudflare, Inc.
✀
```

We can also check the certificate issuer by clicking on the padlock icon in our browser's search bar, then clicking on "Connection is secure" or similar to see all the details about the certificate issuer.

![Chrome showing Cloudflare as the certificate-issuing authority, before sidestepping the CDN.](/blog/2023/01/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/cert-issuer-chrome-before.webp)

Before we change anything, we see the TLS/SSL certificate presented is issued by Cloudflare, as expected.

### Make the hosts file point directly to our server

Common desktop and server operating systems typically come with a "hosts file" that can be used to provide hostname to IP address translation that happens before your designated DNS servers are consulted.

This is useful to test a hostname without ever adding it to DNS, or to override a DNS entry with your own IP address.

We want to change our hosts file so that www\.endpointdev.com points directly to our site's origin server. How to do this depends on your operating system:

* Linux/macOS: Open /etc/hosts as root (using `sudo` or `su`) in your favorite editor such as vim or nano.
* Windows: Open C:\Windows\System32\drivers\etc\hosts as administrator in a decent plain text editor, not a word processor — I used Notepad++.

Once you have your hosts file open, add a line to point your domain name directly to your origin server. For www\.endpointdev.com:

```plain
23.239.26.161 www.endpointdev.com
```

### Disable DNS-over-TLS & DNS-over-HTTPS

You may also need to disable any "secure DNS" in your browser, such as DNS-over-TLS or DNS-over-HTTPS.

#### Chrome

In Chrome, this is called Secure DNS, and you can disable it by going to Settings > Privacy and Security > Security > Use secure DNS, and disabling it.

![Chrome settings, navigated to Settings > Privacy and Security > Security > Use secure DNS with a radio button disabling Secure DNS](/blog/2023/01/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/secure-dns-chrome.webp)

#### Firefox

In Firefox, go to Network Settings, then disable DNS over HTTPS.

![Firefox preferences, navigated to Network Settings > Enable DNS over HTTPS, with a check box unchecked.](/blog/2023/01/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/dns-over-https-firefox.webp)

Then close any open tabs in your browser and quit it completely. Then start it again.

### Browse the website directly

Now go to www\.endpointdev.com.

![IPvFoo showing the origin's IP address](/blog/2023/01/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/origin.webp)

IPvFoo is now showing the origin IP address we gave it, so we know that we're being served data directly from that server.

We can also run `whois` on our origin server, for good measure:

```plain
$ whois 23.239.26.161

✀
OrgName:        Linode
✀
```

Now we're getting the Linode IP address, not Cloudflare's. This is expected, since our origin site is hosted on a server at Linode.

### Check certificate issuer

You can also check that the certificate issuer changed. Keep in mind that sometimes your certificate issuer might be the same when serving directly as when serving through a CDN, if you got a certificate signed by the CDN, or if you gave your CDN your TLS key & certificate to use.

But if there *is* a different certificate being served, we will likely see it was signed by a different certificate authority (CA):

![Chrome showing Sectigo as the certificate-issuing authority, after sidestepping the CDN.](/blog/2023/01/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/cert-issuer-chrome-after.webp)

After sidestepping Cloudflare our certificate is issued by Sectigo, so this is more proof our changes are working.

### Clean up

When you're all done, open /etc/hosts again and either delete the line you added or comment it out by putting a # at the beginning of the line.

```plain
# 23.239.26.161 www.endpointdev.com
```

Save.

Then close all browser windows, quit, and restart, and when you go to www\.endpointdev.com, Cloudflare should be in the middle again.

### Mobile

Note that there is no easy way to do something like this on iOS with an iPhone or iPad, as far as I can tell. And on Android, you either need a rooted phone, or a fancy VPN that lets you change your hostname mapping. I tried [Hosts Go](https://play.google.com/store/apps/details?id=dns.hosts.server.change&hl=en_US&gl=US) and it worked, despite some annoying ads which you don't have to deal with in an /etc/hosts file 😁.

If you need to test on mobile, or on multiple devices, you could also use a DNS server on your local network, and configure any device to point to your local DNS. [Pi-hole](https://pi-hole.net/) is a great option for this; see our [blog post](https://www.endpointdev.com/blog/2020/12/pihole-great-holiday-gift/) from a couple years ago for some of its other features.
