---
author: Elizabeth Garrett Christensen
gh_issue_number: 1216
tags: ecommerce, hosting, payments, security
title: "A Beginner\u2019s Guide to PCI DSS Compliance and TLS Versions"
---



I recently did some research for one of End Point’s ecommerce clients on their PCI compliance and wanted to share some basic information for those of you who are new to this topic.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/03/29/a-beginners-guide-to-pci-dss-compliance/image-0-big.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/03/29/a-beginners-guide-to-pci-dss-compliance/image-0.jpeg"/></a></div>

### TLS

TLS (Transport Layer Security) is a standard for secure communications between applications. TLS is the current version of what used to be called SSL, the secure sockets layer. In the case of a financial transaction, this is the communication between the website selling a product and the end user. TLS works by encrypting data between two endpoints to ensure any sensitive data (such as financial details and private customer information) is exchanged securely. As security measures increase, new versions of TLS are released. To date, TLS 1.2 is the most up-to-date, with TLS 1.1 being considered safe, and TLS 1.0 being phased out. For details about OS versions supporting the latest TLS standards, please see [Jon Jensen’s write-up here](http://blog.endpoint.com/2015/07/e-commerce-website-encryption-changes.html).

### Compliance with PCI DSS

As all online retailers know, becoming and staying compliant with PCI DSS (Payment Card Industry Data Security Standard) is a big job. PCI is *THE* ecommerce security standard and in order to accept payment with Visa, MasterCard, American Express, and Discover, you must comply with their security standards.

As the Internet security landscape changes, PCI DSS standards are updated and reflect new risks and adjustments in security protections. As of today, PCI is requiring vendors to upgrade TLS 1.1 or above by June of 2016, with an optional extension until June 2018.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/03/29/a-beginners-guide-to-pci-dss-compliance/image-1-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/03/29/a-beginners-guide-to-pci-dss-compliance/image-1.jpeg"/></a></div>

### Compliance Assessors

Here’s where things get tricky. PCI does not actually do their own compliance, instead each merchant must have a neutral third party help them fulfill their PCI requirements. These are called ‘assessors’ and there are a large number of companies that offer this service along with help for other security-related tasks.

In preparation for the new requirements, many of the assessor companies are including the new TLS standards in their current compliance protocols.

What does that mean? Well, it means that even though PCI might not be requiring you to have TLS 1.1 until June of 2018, your compliance assessor might be require you to do it right **now**.

### Bite the Bullet

So, now, given that you know you this change is coming AND you need it to get your compliance done, you might as well get your site updated. So where’s the catch?

### Unsupported browsers

The big catch is that some browsers do not support TLS 1.1 or 1.2. In those cases, some of your users will not be able to complete a payment transaction and will instead hit an error screen and cannot continue. They are:

- Internet Explorer on Windows XP
- Internet Explorer older than version 11 on any version of Windows
- the stock Android browser on versions of Android before 5.0
- Safari 6 or older on Mac OS X 10.8 (Mountain Lion) or older
- Safari on iOS 4 or older
- very, very old versions of Firefox or Chrome that have been set not to auto-update

Okay, so how many people still use those old browsers? We’ll take a look at some of the breakdowns here:

[http://www.w3schools.com/browsers/browsers_explorer.asp](http://www.w3schools.com/browsers/browsers_explorer.asp)

You might be thinking, ‘That doesn’t seem like very many people’. And that’s true. However, every site has a different customer base and browsers use varies widely by demographics. So where can you go to find out what kinds of browser’s your customers use?

### Google Analytics, your old friend

If you have Google Analytics setup, you can go through the Audience/Technology/Browser&OS screens to find out what kind of impact this might have.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2016/03/29/a-beginners-guide-to-pci-dss-compliance/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2016/03/29/a-beginners-guide-to-pci-dss-compliance/image-2.png"/></a></div>

### Plan for the Worst

Now armed with your information, you will probably want to go ahead and get your website on the newest TLS version. The change is coming anyways but help your staff and web team plan for the worst by making sure everyone knows about the browser limitations and can help your customers through the process.

### Server Compatibility Notes

For many ecommerce sites, enabling TLS 1.1 and 1.2 is easy, just changing a configuration setting and restarting the web server. But on older operating systems, such as the still supported and very popular Red Hat Enterprise Linux 5 and CentOS Linux 5, TLS 1.0 is the newest supported version. Various workarounds might be possible, but the only real solution is to migrate to a newer version of the operating system. There can be cost and time factors to consider, so it’s best to plan ahead. Ask us or your in-house developers whether a migration will be necessary!

### Need Help?

As End Point’s client liaison, I’m happy to chat with anyone who needs answers or advice about PCI DSS and your ecommerce site.


