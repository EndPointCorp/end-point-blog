---
title: "Bypassing a CDN to browse a website directly on your origin host"
author: Seth Jensen
date: 2022-12-29
tags:
- hosting
- cdn
---

![A pale winter morning, looking out over a valley from a mountainside](/blog/2022/12/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/winter-mountains.webp)

<!-- Photo by Seth Jensen, 2023 -->

Using a CDN has many advantages over serving a website directly, and for any reasonably large website, you should use one. Those advantages include:

* Thousands of PoPs (points of presence) around the world, so traffic will be quick for everyone regardless of how far away they are from our origin server.
* Caching at each PoP.
* DDoS mitigation help.
* Blocking of some Bad Guys automatically at the edge.
* Origin IP insulation. Hiding the origin IP is useful to protect against DDoSes, and you should generally be cautious about sharing your origin IP. We serve other sites from our origin directly, so we don't worry too much about sharing it here.

Sometimes, though, you need to bypass your CDN and test your website directly on its origin server; for example, if you need to test that your website would still work if the CDN goes down. It can be surprisingly confusing to do this, especially with newer features like Secure DNS in Chrome muddying up DNS.

We'll use a browser extension called IPvFoo (available for Chrome and Firefox) to see which IP our hostname resolves to. After installing IPvFoo, click on its indicator next to the search bar. Before we change anything, www\.endpointdev.com resolves to 104.21.30.147.

![IPvFoo showing Cloudflare's IP address](/blog/2022/12/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/cloudflare.webp)

After a quick `whois` search, we see that this IP belongs to Cloudflare, our CDN:

```plain
$ whois 104.21.30.147

...
OrgName:        Cloudflare, Inc.
...
```

We can also check the certificate issuer by clicking on the padlock icon in our browser's search bar, then clicking on "connection is secure" or similar to see all the details about the certificate issuer.

![Chrome showing Cloudflare as the certificate-issuing authority, before sidestepping the CDN.](/blog/2022/12/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/cert-issuer-chrome-before.webp)

Before we change anything, our SSL certificate is issued by Cloudflare, as expected.

### Make the host file point directly to our server

We want to change our host file so that www\.endpointdev.com points directly to our site's origin server. We'll go over how to do this on Linux, Windows, and macOS.

* Linux/macOS: Open /etc/hosts in your favorite editor (I use Vim).
* Windows: Open C:\Windows\System32\drivers\etc\hosts as administrator in a decent text editor — I used notepad++.

Once you have your host file open, add a line to point your domain name directly to your origin server. For www\.endpointdev.com:

```plain
23.239.26.161 www.endpointdev.com
```

### Disable DNS-over-TLS/DNS-over-HTTPS

You may also need to disable any DNS-over-TLS or DNS-over-HTTPS.

#### Chrome

In Chrome, this is called Secure DNS, and you can disable it by going to Settings > Privacy and Security > Security > Use secure DNS and disabling it.

![Chrome settings, navigated to Settings > Privacy and Security > Security > Use secure DNS with a radio button disabling Secure DNS](/blog/2022/12/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/secure-dns-chrome.webp)

#### Firefox

In Firefox, go to Network Settings, then disable DNS over HTTPS.

![Firefox preferences, navigated to Network Settings > Enable DNS over HTTPS, with a check box unchecked.](/blog/2022/12/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/dns-over-https-firefox.webp)

Then close any open tabs in your browser and quit it completely. Then start it again.

### Browse the website directly

Now go to www\.endpointdev.com.

![IPvFoo showing the origin's IP address](/blog/2022/12/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/origin.webp)

IPvFoo is now showing the origin IP we gave it, so we know that we're being served directly from that server.

We can also run `whois` on our origin server, for good measure:

```plain
$ whois 23.239.26.161

...
OrgName:        Linode
...
```

Now we're getting the Linode IP, not Cloudflare. This is expected, since our site is hosted by Linode.

### Check certificate issuer

You can also check the certificate issuer for a change. Keep in mind that sometimes your certificate issuer might be the same when serving directly as when serving through a CDN, since most CDNs are also certificate authorities. But if there *is* a change in CA, that shows that our changes worked.

![Chrome showing Sectigo as the certificate-issuing authority, after sidestepping the CDN.](/blog/2022/12/bypassing-a-cdn-to-browse-a-website-directly-on-your-origin-host/cert-issuer-chrome-after.webp)

After sidestepping Cloudflare our certificate is issued by Sectigo, so this is more proof our changes are working.

### Clean up

When you're all done, open /etc/hosts again and either delete the line you added or comment it out by putting a # at the beginning of the line.

```plain
# 23.239.26.161 www.endpointdev.com
```

Save.

Then close all browser windows, quit, and restart, and when you go to www\.endpointdev.com, Cloudflare should be in the middle again.

Note that this won't work on iPhone (as far as I can tell), and for Android, you either need a rooted phone, or a fancy VPN that lets you change hosts. I tried [Hosts Go](https://play.google.com/store/apps/details?id=dns.hosts.server.change&hl=en_US&gl=US) and it worked, despite some annoying ads which you don't have to deal with in a /etc/hosts file 😁.

If you need to test on mobile, or on multiple devices, you could also use a DNS server on your local network, and configure any device to point to your local DNS. [Pi-hole](https://pi-hole.net/) is a great option for this; see our [blog post](https://www.endpointdev.com/blog/2020/12/pihole-great-holiday-gift/) from a couple years ago for some of its other features.
