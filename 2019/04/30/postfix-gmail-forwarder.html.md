---
author: Jon Jensen
title: 'Linux desktop Postfix queue for Gmail SMTP'
tags: sysadmin, email, linux
gh_issue_number: 1518
---

<img src="/blog/2019/04/30/postfix-gmail-forwarder/20190216-123757-crop.jpg" alt="Winter view of snow, river, trees, mountains, clouds at Flagg Ranch, Rockefeller Parkway, Wyoming" />

[//]: # (Photo by Jon Jensen)

On a Linux desktop, I want to start sending email through Gmail in a G Suite account using SMTP, rather than a self-hosted SMTP server. Since Gmail supports SMTP, that should be easy enough.

Google’s article [Send email from a printer, scanner, or app](https://support.google.com/a/answer/176600?hl=en) gives an overview of several options. I’ll choose the “Gmail SMTP server” track, which seems designed for individual user cases like this.

However, since I am using two-factor authentication (2FA) on this Google account — as we should all be doing now for all accounts wherever possible! — my Gmail login won’t work for SMTP because the clients I am using don’t have a way to supply the 2FA time-based token.

Google’s solution to this is to have me generate a separate “App Password” that can sidestep 2FA for this limited purpose: [Set up an App Password](https://support.google.com/mail/answer/185833).

That works fine, but the app password is a randomly-generated 16-letter password that is not amenable to being memorized. For security reasons, my mail client doesn’t cache passwords between sessions, so I have to look it up and enter it each time I start the mail client. That’s generally only once per day for me, so it’s not a big problem, but it would be nice to avoid.

I also want other local programs — such as cron jobs, development projects underway, etc. — to be able to send mail out through my Gmail account. How can I do that, ideally without teaching each one separately how to do it?

As a server operating system at heart, Linux of course has many SMTP servers that can intermediate by acting as a local SMTP server, queue, and sending client. Such a server could have my Gmail password configured and stored under a separate user account, giving a bit more isolation from my main desktop user.

### What local SMTP program to use?

#### esmtp

I first tried using the lightweight and ephemeral `esmtp` since I had already used it on my desktop computer to forward email through an SSH tunnel. I wasn’t able to get it working with Gmail, which could easily have been operator error on my part.

Before trying much to solve the problem, I realized that I really would like a local queue for outgoing email so I don’t have to wait for my mail client to connect and send each message before I can get on with more email. Given how much email I handle each day, even fairly brief delays add unwanted drag.

#### ssmtp

I used another similar program called `ssmtp` a long time ago, and considered trying that again.

Then I read that ssmtp is unmaintained and does not validate TLS certificates, negating some of the security value of using TLS in the first place. So, no to that.

#### E-MailRelay

I next saw a few people mention that `E-MailRelay` is a nice option to locally queue and forward email. But looking at a new and more comprehensive email daemon like that, I realized I would likely find it easier to just use an SMTP server I already know, such as Exim, Sendmail, or …

#### Postfix

Postfix is one of the most widely-deployed mail servers. I already know it well and have used it for many years. It has most every option I would ever want. So I’ll use that.

This seems like a slight bit of overkill for just sending outgoing email, but Postfix is battle-hardened and comparatively lightweight, using around 30 MiB resident RAM between its 4 daemon processes on my computer. Yes, that is laughably bloated by the standards of yore, but svelte compared to even a single tab in a modern graphical browser.

### Configuring Postfix

(You’ll need to be root to do the following setup.)

First, install Postfix as appropriate for your Linux distribution:

```plain
# dnf install postfix    # Fedora
# yum install postfix    # CentOS/​RHEL
# apt install postfix    # Debian/​Ubuntu
```

Now, time to edit the default Postfix configuration. The options are all [well-documented on the Postfix website](http://www.postfix.org/postconf.5.html) but there are a *lot* of them and it can take a while to figure out what you need and want.

Here is what I added to `/etc/postfix/main.cf`:

```plain
relayhost = [smtp.gmail.com]:465

smtp_tls_wrappermode = yes
smtp_tls_security_level = verify
smtp_tls_mandatory_protocols = !SSLv2, !TLSv1, !TLSv1.1
tls_high_cipherlist = ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256
smtp_tls_mandatory_ciphers = high
smtp_tls_loglevel = 2

smtp_sasl_auth_enable = yes
smtp_sasl_mechanism_filter = plain
smtp_sasl_password_maps = hash:/etc/postfix/smtp_auth
smtp_sasl_security_options = noanonymous

header_checks = regexp:/etc/postfix/header_checks

smtp_address_preference = ipv6
```

Let’s go through each of those settings:

With `relayhost` we define the remote server we want to route all our outgoing mail through. The `[...]` around the hostname disables MX lookups, since there is no MX record for smtp.gmail.com. Port 465 is used for TLS-wrapped (called “implicit”) mail submission, so we also need to set `smtp_tls_wrappermode`.

I used the port number 465 rather than the name `smtps` because the port has been reassigned for another purpose, so it may be mentioned in the `/etc/services` file under either the old or new names or both, and isn’t worth risking breakage for.

Enabling `smtp_tls_wrappermode` means we initiate a TLS connection immediately, rather than first connecting with classic plain-text SMTP protocol, and then requesting a switch to TLS mode with the `STARTTLS` SMTP verb. This option is why we specified port 465 above for our `relayhost`.

Like me, you may recall the option for SSL-wrapped SMTP to port 465 as little more than an odd Microsoft Exchange and Outlook convention from years ago. Once upon a time it was. Why not use the more standard submission port 587? Up until fairly recently that would have been best.

In a funny turn of events, nowadays TLS-wrapped SMTP on port 465 is recommended as the best way for end-users to submit mail! See [RFC 8314](https://tools.ietf.org/html/rfc8314#section-3) for details. I found the helpful [FastMail explanation of all the historical twists](https://www.fastmail.com/help/technical/ssltlsstarttls.html) well worth reading. As they say, the best thing about standards is that there are so many to choose from. 😆

Setting `smtp_tls_security_level` to `verify` means that we want TLS to be mandatory for every connection, and we want Postfix to validate that the certificate name matches the hostname we are using to connect to prevent man-in-​the-​middle (MITM) attacks.

With `smtp_tls_mandatory_protocols` we are disabling all older TLS protocols, allowing only the most current (as of this writing) versions 1.2 and 1.3. That would be overly restrictive and unsafe to do on a public mail server, but since we are only talking to a single mail server here, and we know that Google supports modern TLS, we can restrict ourselves to that.

The `tls_high_cipherlist` list is our restricted set of TLS ciphers in our preferred order. Again, this would be unwise to do on a public mail server, but in our role as a client forwarding to only one destination here, it is a good thing. My list comes from [Mozilla’s modern TLS recommendation](https://wiki.mozilla.org/Security/Server_Side_TLS#Modern_compatibility).

With `smtp_tls_mandatory_ciphers` set to `high`, we ensure the list we just specified gets used.

I set `smtp_tls_loglevel` to 2 so that the Postfix logs will show helpful details about TLS connection negotiations and results.

The next several `smtp_sasl_` options configure our use of a username and password. (SASL means “Simple Authentication and Security Layer”.) Note the `smtp_sasl_password_maps` file we specified. The file name is arbitrary. Let’s create that now in `/etc/postfix/smtp_auth`:

```plain
[smtp.gmail.com]:465    user@gsuite.domain:apppassword
```

Of course substitute your own email address and Gmail app password there.

We need to create a fast binary map equivalent of that file for Postfix to read, and since it contains a password that should be kept private, let’s make it unreadable by other users on the system:

```plain
# postmap hash:smtp_auth
# chmod go= smtp_auth*
```

Next I set option `header_checks` to look for regular expressions in another file we need to create, `/etc/postfix/header_checks`:

```plain
/^Received:\ (from|by)\ .*(yourhostname|localhost|localdomain)/      IGNORE
```

That removes a pair of headers that Postfix normally adds to each message we send, tracking the receipt and forwarding on of the email:

```plain
Received: by yourhostname.localdomain (Postfix, from userid 1000)
    id F2F7111C64A1; Tue, 30 Apr 2019 17:36:12 -0600 (MDT)
Received: from localhost (localhost [127.0.0.1])
    by yourhostname.localdomain (Postfix) with ESMTP id EE7DB11C161C;
    Tue, 30 Apr 2019 17:36:12 -0600 (MDT)
```

In our case those are a waste of space because it is not interesting to track the flow of email around localhost. So we just remove them before sending the mail on.

Finally, a minor nicety I like to enable is to set `smtp_address_preference` to `ipv6` so that when we have an IPv6 connection to the outside world, that is used to send the mail. An IPv4 connection will still be used if IPv6 isn’t available. I figure we’d might as well use the newer routing tubes of the Internet when we can.

### Trying it out

Now we’re ready to start Postfix, and set it to start automatically at boot time:

```plain
# systemctl start postfix
# systemctl enable postfix
```

Now you need to configure your mail client. My enthusiasm for [Pine (now Alpine)](https://en.wikipedia.org/wiki/Alpine_%28email_client%29) hasn’t waned after over 20 years, so that is what I use. Perhaps you prefer [Mutt](https://en.wikipedia.org/wiki/Mutt_(email_client)) or [Thunderbird](https://www.thunderbird.net/) or something else.

Whatever it is, set your mail client to send mail through local Postfix executable `/usr/sbin/sendmail` (the default for many), or through SMTP to `localhost:25`. For me, that meant editing `~/.pinerc`. When I was sending mail directly from Pine to Gmail, it contained:

```plain
smtp-server=smtp.gmail.com/submit/tls/user=you@your.domain
```

But now I want there to be no setting so it falls back to `/usr/sbin/sendmail`:

```plain
smtp-server=
```

Now watch your Postfix logs, usually in `/var/log/mail.log` on Debian and Ubuntu systems, and `/var/log/maillog` on Fedora and CentOS.

And send a message!

Let’s look at what Postfix logged when I sent a test message.

When using rsyslog my complete log lines look like this:

```plain
2019-04-30T17:59:11.887004-06:00 localhost postfix/smtpd[10962]: connect from localhost[127.0.0.1]
```

That timestamp and hostname prefix waste a lot of room on each line here, so I will trim them from the rest of the xample:

```plain
postfix/smtpd[10962]: connect from localhost[127.0.0.1]
postfix/smtpd[10962]: DA75311C649C: client=localhost[127.0.0.1]
postfix/smtpd[10962]: disconnect from localhost[127.0.0.1] ehlo=1 mail=1 rcpt=1 data=1 quit=1 commands=5
postfix/pickup[10947]: DE8FE11C64A1: uid=1000 from=<you@your.domain>
postfix/cleanup[10964]: DE8FE11C64A1: message-id=<f15302b5-cd03-488a-a401-e1eb8544895f@ybpnyubfg>
postfix/qmgr[10948]: DE8FE11C64A1: from=<you@your.domain>, size=393, nrcpt=1 (queue active)
postfix/smtp[10967]: initializing the client-side TLS engine
postfix/smtp[10967]: setting up TLS connection to smtp.gmail.com[2607:f8b0:4001:c03::6c]:465
postfix/smtp[10967]: smtp.gmail.com[2607:f8b0:4001:c03::6c]:465: TLS cipher list "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:!aNULL"
postfix/smtp[10967]: SSL_connect:before SSL initialization
postfix/smtp[10967]: SSL_connect:SSLv3/TLS write client hello
postfix/smtp[10967]: SSL_connect:SSLv3/TLS write client hello
postfix/smtp[10967]: SSL_connect:SSLv3/TLS read server hello
postfix/smtp[10967]: smtp.gmail.com[2607:f8b0:4001:c03::6c]:465: depth=2 verify=1 subject=/OU=GlobalSign Root CA - R2/O=GlobalSign/CN=GlobalSign
postfix/smtp[10967]: smtp.gmail.com[2607:f8b0:4001:c03::6c]:465: depth=1 verify=1 subject=/C=US/O=Google Trust Services/CN=Google Internet Authority G3
postfix/smtp[10967]: smtp.gmail.com[2607:f8b0:4001:c03::6c]:465: depth=0 verify=1 subject=/C=US/ST=California/L=Mountain View/O=Google LLC/CN=smtp.gmail.com
postfix/smtp[10967]: SSL_connect:SSLv3/TLS read server certificate
postfix/smtp[10967]: SSL_connect:SSLv3/TLS read server key exchange
postfix/smtp[10967]: SSL_connect:SSLv3/TLS read server done
postfix/smtp[10967]: SSL_connect:SSLv3/TLS write client key exchange
postfix/smtp[10967]: SSL_connect:SSLv3/TLS write change cipher spec
postfix/smtp[10967]: SSL_connect:SSLv3/TLS write finished
postfix/smtp[10967]: SSL_connect:SSLv3/TLS write finished
postfix/smtp[10967]: SSL_connect:SSLv3/TLS read server session ticket
postfix/smtp[10967]: SSL_connect:SSLv3/TLS read change cipher spec
postfix/smtp[10967]: SSL_connect:SSLv3/TLS read finished
postfix/smtp[10967]: smtp.gmail.com[2607:f8b0:4001:c03::6c]:465: Matched subjectAltName: smtp.gmail.com
postfix/smtp[10967]: smtp.gmail.com[2607:f8b0:4001:c03::6c]:465 CommonName smtp.gmail.com
postfix/smtp[10967]: smtp.gmail.com[2607:f8b0:4001:c03::6c]:465: subject_CN=smtp.gmail.com, issuer_CN=Google Internet Authority G3, fingerprint=DF:CB:AA:81:ED:77:D4:BE:E5:47:6F:0E:A3:44:99:BA, pkey_fingerprint=EE:0F:3A:CC:6E:4E:EB:C0:1D:88:B6:73:BD:42:C4:83
postfix/smtp[10967]: Verified TLS connection established to smtp.gmail.com[2607:f8b0:4001:c03::6c]:465: TLSv1.2 with cipher ECDHE-RSA-CHACHA20-POLY1305 (256/256 bits)
postfix/smtp[10967]: DE8FE11C64A1: to=<them@their.domain>, relay=smtp.gmail.com[2607:f8b0:4001:c03::6c]:465, delay=1.3, delays=0.03/0.03/0.52/0.75, dsn=2.0.0, status=sent (250 2.0.0 OK  1556668753 y199sm14693187iof.88 - gsmtp)
postfix/qmgr[10948]: DE8FE11C64A1: removed
```

We can see that the TLS connection was made, negotiated over IPv6 with TLS 1.2 and a nice modern cipher, and the certificate matches the hostname we used. Then the email was sent.

Google has some of their SMTP servers offering the newer, unfinalized TLS 1.3 protocol, since I see that about half the time:

```plain
postfix/smtp[13812]: Verified TLS connection established to smtp.gmail.com[2607:f8b0:4001:c06::6d]:465: TLSv1.3 with cipher TLS_AES_256_GCM_SHA384 (256/256 bits) key-exchange X25519 server-signature RSA-PSS (2048 bits) server-digest SHA256
```

And I received my test mail on the other end.

### Conclusion

Now I can use any local mail client without having to separately configure each one to send outgoing mail to Gmail, and without having to enter the Gmail app password each time I start my mail client.

Sending email is immediate since the client only waits for the fast local queueing to complete, and Postfix forwards the mail in the background.

Remember to check your logs to make sure your mail is getting delivered, since your client will no longer know if it is not. If nobody replies to you for too many hours, check the logs first! Or set up something to monitor your logs for errors and alert you.

This approach is also useful on servers that need to send application email from a Gmail account, such as when you want mail to have a From: header with a @gmail.com or G Suite domain address.

Thanks, open source community, for the good software and documentation and open standards!
