---
author: Jon Jensen
gh_issue_number: 196
tags: hosting, open-source
title: Increasing maildrop's hardcoded 5-minute timeout
---



One of the ways I like to retrieve email is to use [fetchmail](http://fetchmail.berlios.de/) as a POP and IMAP client with [maildrop](http://www.courier-mta.org/maildrop/) as the local delivery agent. I prefer maildrop to Postfix, Exim, or sendmail for this because it doesn't add any headers to the messages.

The only annoyance I have had is that maildrop has a hardcoded hard timeout of 5 minutes for delivering a mail message. When downloading a very long message such as a Git commit notification of a few hundred megabytes, or a short message with an attached file of dozens of megabytes, especially over a slow network connections, this timeout prevents the complete message from being delivered.

Confusingly, a partial message will be delivered locally without warning -- with the attachment or other long message data truncated. When fetchmail receives the error status return from maildrop, it then tries again, and given similar circumstances it suffers a similar fate. In the worst case this leads to hours of clogged tubes and many partial copies of the same email message, and no other new mail.

This maildrop hard timeout is compiled in and there is no runtime option to override it. Thus it is helpful to compile a custom build from source, specifying a different timeout at configure time. In my case, I set the timeout to be 1 day:

```bash
./configure --enable-global-timeout=86400 --without-db --enable-syslog=1 \
    --enable-tempdir=tmp --enable-smallmsg=65536 
make
```

If you choose to configure with --without-db as I do, you need to manually remove two occurrences of makedatprog from Makefile, as makedatprog is a utility only needed by DBM and won't have been compiled. Then make install as root and edit your ~/.fetchmailrc lines, adding mda "/usr/local/bin/maildrop", and restart the fetchmail daemon.

Long messages will still take a long time to deliver over a slow link, but they will at least be allowed to eventually finish this way.


