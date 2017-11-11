---
author: Phin Jensen
gh_issue_number: 1324
tags: browsers, hosting, security, ssl, sysadmin
title: Web Security Services Roundup
---



Security is often a very difficult thing to get right, especially when it’s not easy to find reliable or up-to-date information or the process of testing can be confusing and complicated. We have a lot of history and experience working on the security of websites and servers, and we’ve found many tools and websites to be very helpful. Here is a collection of those.

## Server-side security

There are a number of tools available that can scan your website to check for common vulnerabilities and the quality of SSL/TLS configuration, as well as give great tips on how to improve security for your website.

- [Qualys SSL Labs Server Test](https://www.ssllabs.com/ssltest/) takes a simple domain name, performs a series of tests from a variety of clients, and returns a simple letter grade (from A+ down to F) indicating the quality of your SSL/TLS configuration, as well as a detailed summary for a host of configuration options. It covers certificates key and algorithms; TLS and SSL configurations; cipher suites; handshakes on a wide variety of platforms including Android, iOS, Chrome, Firefox, Internet Explorer and Edge, Safari, and others; common protocols and vulnerabilities; and other details.
- [HTTP Security Report](https://httpsecurityreport.com/) does a similar scan, but provides a much more simplified summary of a website, with a numeric score from 0 to 100. It gives a simple, easy to understand list of results, with a green check mark or a red X to indicate whether something is configured for security or not. It also provides short paragraphs explaining settings and recommended configurations.
- [HT-Bridge SSL/TLS Server Test](https://www.htbridge.com/ssl/) is very similar to Qualys SSL Labs Server Test, but provides some valuable extra information, such as PCI-DSS, HIPAA, and NIST guidelines compliance, as well as industry best practices and basic analysis of third-party content.
    - [securityheaders.io](https://securityheaders.io/) is another letter-grade scan, but focuses on server headers only. It provides simple explanations for each recommended server header and links to guides on how to configure them correctly.
- [Observatory by Mozilla](https://observatory.mozilla.org/) scans and gives information on HTTP, TLS, and SSH configuration, as well as simple summaries from other websites, including Qualys, HT-Bridge, and securityheaders.io as covered above.
- [SSL-Tools](https://ssl-tools.net/) is focused on SSL and TLS configuration and certificates, with tools to scan websites and mail servers, check for common vulnerabilities, and decode certificates.
- [Microsoft Site Scan](https://dev.windows.com/en-us/microsoft-edge/tools/staticscan/) performs a series of simple tests, focused more on general website guidelines and best practices, including tests for outdated libraries and plugins which can be a security issue.
- [testssl.sh](https://testssl.sh/), the final website scanning tool I’ll cover, is a more advanced bash script that covers many of the same things these other websites do, but provides lots of options for fine-tuning test methods, returned information, and testing abnormal configurations. It’s also open source and doesn’t rely on any third parties.

These websites provide valuable information on SSL/TLS which can be used to create a secure, fast, and functional server configuration:

- [Security/Server Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS) on the Mozilla wiki is a fantastic page which provides great summaries, recommendations, and reference information on many TLS topics, including handshakes, OCSP Stapling, HSTS, HPKP, certificate ciphers, and common attacks.
- [Mozilla SSL Configuration Generator](https://mozilla.github.io/server-side-tls/ssl-config-generator/) is a simple tool that generates boilerplate server configuration files for common servers, including Apache and Nginx, and specific server and OpenSSL versions. It also allows you to target “modern”, “intermediate”, or “old” clients and servers, which will give the best configuration possible for each level.
- [Is TLS Fast Yet?](https://istlsfastyet.com/) is a great, simple, and to-the-point informational website which explains why TLS is so important and how to improve its performance so it has the smallest impact possible on your website’s speed.

## Client-side security

These websites provide information and diagnostic tools to ensure that you are using a secure browser.

- [badssl.com](https://badssl.com/) gives a list of links to subdomains with various SSL configurations, including badly configured SSL, so you can have a good idea of what a well-configured website looks like versus one with errors in configuration, weak ciphers or key exchange protocols, or insecure HTTP forms.
- [IPv6 Test](http://ipv6-test.com/) checks your network and browser for IPv6 support, showing you your ISP, reverse DNS pointers, both your IPv4 and IPv6 addresses, and giving an idea of when your computer or network may have problems with dual-stack IPv4 + IPv6 remote hosts or DNS.
- [How’s My SSL?](https://www.howsmyssl.com/) and [Qualys Labs SSL Client Test](https://www.ssllabs.com/ssltest/viewMyClient.html) both check your browser for support of SSL/TLS versions, protocols, ciphers, and features, as well as susceptibility to common vulnerabilities.

## General Tools

- [NeverSSL](http://neverssl.com/) is a simple website that promises to never use SSL. Many public wifi networks require you to go through a payment or login page, which can be blocked when trying to access a well-secured website such as Google, Facebook, Twitter, or Amazon, which can cause trouble connecting to that website. NeverSSL provides an easy and simple way to access that login website.
- [crt.sh](https://crt.sh/) is a search engine for public TLS certificate information. It provides a history of certificates for a given domain name, with information including issuer and issue date, as well as an advanced search.
- [Digital Attack Map](http://www.digitalattackmap.com/) is an interactive map showing DDoS attacks across the world.
- [The Internet-Wide Scan Data Repository](https://scans.io/) is a public archive of scans across the internet, intended for research and provided by the University of Michigan Censys Team.
- [take-a-screenshot.org](https://www.take-a-screenshot.org/) is a simple website that shows how to take a screenshot on a variety of operating systems and desktop environments. It’s a fantastic tool to help less technically-minded people share their screens or issues they’re having.


