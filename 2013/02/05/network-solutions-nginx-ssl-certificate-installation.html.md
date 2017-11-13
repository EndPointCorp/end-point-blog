---
author: Brian Buchalter
gh_issue_number: 756
tags: hosting, tls
title: Install SSL Certificate from Network Solutions on nginx
---

Despite nginx serving pages for [12.22% of the web's million busiest sites](http://news.netcraft.com/archives/2012/11/01/november-2012-web-server-survey.html), Network Solutions **does not** provide [instructions for installing SSL certificates](http://www.networksolutions.com/support/nsprotect-secure-ssl-topics/) for nginx. This artcle provides the exact steps for chaining the intermediary certificates for use with nginx.

### Chaining the Certificates

Unlike Apache, nginx does not allow specification of intermediate certificates in a directive, so we must combine the server certificate, the intermediates, and the root in a single file. The zip file provided from Network Solutions contains a number of certificates, but no instructions on the **order** in which to chain them together. Network Solutions' [instructions for installing on Apache](http://www.networksolutions.com/support/installation-of-an-ev-ssl-certificate-on-apache-mod-ssl-openssl/) provide a hint, but let's make it clear.

```bash
cat your.site.com.crt UTNAddTrustServer_CA.crt NetworkSolutions_CA.crt > chained_your.site.com.crt
```

This follows the general convention of "building up" to a trusted "root" authority by appending each intermediary. In this case UTNADDTrustServer_CA.crt is the intermediary while NetworkSolutions_CA.crt is the parent authority. With your certificates now chained together properly, use the usual nginx directives to configure SSL.

```bash
listen                 443;
ssl                    on;
ssl_certificate        /etc/ssl/chained_your.site.com.crt;
ssl_certificate_key    /etc/ssl/your.site.com.key;
```

As always, make sure your key file is secure by giving it minimal permissions.

```bash
chmod 600 your.site.com.key
```

I hope this little note helps to ease nginx users looking to use a Network Solutions SSL certificate.
