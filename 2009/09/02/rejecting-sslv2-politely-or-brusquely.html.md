---
author: Jon Jensen
gh_issue_number: 194
tags: browsers, ecommerce, hosting, security, tls
title: Rejecting SSLv2 politely or brusquely
---

Once upon a time there were still people using browsers that only supported SSLv2. It's been a long time since those browsers were current, but when running an ecommerce site you typically want to support as many users as you possibly can, so you support old stuff much longer than most people still need it.

At least 4 years ago, people began to discuss disabling SSLv2 entirely due to fundamental security flaws. See the [Debian](http://lists.alioth.debian.org/pipermail/pkg-mozilla-maintainers/2005-April/000022.html) and [GnuTLS](http://www.gnu.org/software/gnutls/manual/html_node/On-SSL-2-and-older-protocols.html) discussions, and this blog post about [PCI's stance on SSLv2](http://clearskies.net/blog/2009/03/01/insecure-ssl-and-how-pci-nearly-gets-it-right/), for example.

To politely alert people using those older browsers, yet still refusing to transport confidential information over the insecure SSLv2 and with ciphers weaker than 128 bits, we used an [Apache](http://httpd.apache.org/) configuration such as this:

```nohighlight
# Require SSLv3 or TLSv1 with at least 128-bit cipher
<Directory "/">
    SSLRequireSSL
    # Make an exception for the error document itself
    SSLRequire (%{SSL_PROTOCOL} != "SSLv2" and %{SSL_CIPHER_USEKEYSIZE} >= 128) or %{REQUEST_URI} =~ m:^/errors/:
    ErrorDocument 403 /errors/403-weak-ssl.html
</Directory>
```

That accepts their SSLv2 connection, but displays an error page explaining the problem and suggesting some links to free modern browsers they can upgrade to in order to use the secure part of the website in question.

Recently we've decided to drop that extra fuss and block SSLv2 entirely with Apache configuration such as this:

```nohighlight
SSLProtocol all -SSLv2
SSLCipherSuite ALL:!ADH:!EXPORT56:RC4+RSA:+HIGH:+MEDIUM:-LOW:-SSLv2:-EXP
```

The downside of that is that the SSL connection won't be allowed at all, and the browser doesn't give any indication of why or what the user should do. They would simply stare at a blank screen and presumably go away frustrated. Because of that we long considered the more polite handling shown above to be superior.

But recently, after having completely disabled SSLv2 on several sites we manage, we have gotten zero complaints from customers. Doing this also makes PCI and other security audits much simpler because SSLv2 and weak ciphers are simply not allowed at all and don't raise audit warnings.

So at long last I think we can consider SSLv2 dead, at least in our corner of the Internet!
