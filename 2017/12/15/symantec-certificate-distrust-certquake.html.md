---
author: "Josh Lavin"
title: "Symantec Certificate Distrust (CertQuake)"
tags: tls, security, browsers, chrome
---

If you are accustomed to running your browser with the “developer tools” panel open (which probably indicates you are a web developer), you may have seen it show the following message:

> The certificate used to load https://www.example.com/ uses an SSL
> certificate that will be distrusted in an upcoming release of Chrome.
> Once distrusted, users will be prevented from loading this resource.
> See https://g.co/chrome/symantecpkicerts for more information.

What’s this all about? Glad you asked.

### The Root of All Certificates (well, most)

**Symantec** is a company that operated a “PKI” ([Public Key Infrastructure](https://en.wikipedia.org/wiki/Public_key_infrastructure)) business. As a [Certificate Authority](https://en.wikipedia.org/wiki/Certificate_authority), they would dole out digital certificates to requestors. 

#### Certified

These certificates are used to secure the communication we have with websites. When a site uses a certificate correctly, you will see the leading part of the URL begin with `https://` (known as the protocol), and the “green-lock” icon in your browser.

Certificates can also be issued with more stringent requirements on the company obtaining them, where they must verify their company by providing articles of incorporation, etc. These are known as “EV” (Extended Validation) certs, and browsers will show the company name in the URL bar next to the green-lock icon.

#### Essential Trust

Since users have become accustomed to trusting a website if the green-lock icon is present, especially if the name of the company behind the website appears in the URL bar alongside it, there is a lot of inherent trust in the system. **All parties must honor that trust by operating with adherence to well-established security requirements.**

The system to provide this trust includes:

- *browsers*, who trust a built-in set of “root” certificates
- *root certificate issuers*, who can send trust down the line to certificates ordered from their infrastructure (like Symantec)
- *websites*, who install their certificates and configure their applications and web servers to use them properly

### Poor Decisions

At several points over time, Symantec made decisions that Google and others felt **jeopardized the system’s inherent trust**. You can [read more on those](https://wiki.mozilla.org/CA:Symantec_Issues), but the result is that Google decided that enough is enough: they would **remove trust in Symantec’s roots from the Chrome browser**. Mozilla followed soon after for their Firefox browser.

The first distrust will occur in **March 2018**, when Chrome 66 is released to beta.

Symantec also resold their security offerings to multiple partners. Thus, several certificate vendors with completely different names turned out to use Symantec root certificates behind the scenes, and are also affected. This includes *all* certificates with Symantec as the root issuer, such as **Equifax, GeoTrust, Thawte, and VeriSign**, among others.

You can read more on [Google’s plan](https://security.googleblog.com/2017/09/chromes-plan-to-distrust-symantec.html), and also see [Qualys’s overview on the situation](https://blog.qualys.com/ssllabs/2017/09/26/google-and-mozilla-deprecating-existing-symantec-certificates).

### Quaking In Our Boots

This root-level distrust is a big deal, so in the spirit of [catchy names for security vulnerabilities](https://medium.com/threat-intel/bug-branding-heartbleed-14ef1a64047f), End Point is referring to this as **CertQuake**. Maybe it will catch on. Alas, probably not, because we have more important things to do than design fancy artwork for it.

### How To Tell

The easiest way to tell if your site is affected is to use Qualys’s [SSL Server Test](https://www.ssllabs.com/ssltest/index.html). Just enter your hostname in the box, and let Qualys scan your site. 

If you are affected by the Symantec distrust, there will be a large yellow warning box, near the top of the page.

### Where To Go From Here

If you operate a site that is affected, you need to **act quickly to re-issue** your certificate from your certificate vendor. While the deadline can vary based on when your certificate was issued, we are using the March 2018 date for all certificates we manage.

Some issuers are offering [free replacement](https://www.namecheap.com/symantec-replace/) of affected certs with their own certificates, to try to capture market share from Symantec and its survivor, DigiCert.

### What We Did

Since End Point manages hundreds of secure websites for our clients, it would be time-consuming to manually check each website to see if it is affected.

Instead, we downloaded a copy of all affected root certificates, which we [found here](https://chromium.googlesource.com/chromium/src/+/master/net/data/ssl/symantec/roots/).

Then, armed with a list of all our secure client websites, we devised a set of Bash scripts that would extract the issuers from the root certs and compare them to our clients’ certificate issuers.

We then were able to take a list of affected certs, and unless they were going to expire before March 2018, re-issue them.

If you are interested in our Bash scripts, we have placed a [copy on GitHub](https://github.com/jdigory/symantec-distrust).

### Summary

Our process allowed us to quickly discover all affected certificates, and re-issue them for our clients. Most of the time, this was done behind the scenes, where our clients didn’t even need to get involved — we were on the job, protecting them and their businesses.

In this Internet Age, we all have to do our part to ensure trust in the system. It’s unfortunate when one thing can affect so many websites, but it’s how the system works.
