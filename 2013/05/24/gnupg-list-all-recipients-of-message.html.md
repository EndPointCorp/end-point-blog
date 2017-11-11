---
author: Jon Jensen
gh_issue_number: 807
tags: security
title: 'GnuPG: list all recipients of a message'
---



<img align="right" src="/blog/2013/05/24/gnupg-list-all-recipients-of-message/image-0.png" style="padding: 5px"/> http://www.gettyicons.com/free-icon/112/finance-icon-set/free-safe-icon-png/ At End Point we frequently use [GnuPG](http://www.gnupg.org/) for PGP-compatible secure data storage and delivery, both internally and with some of our clients.

For many years, GnuPG 1 has been the standard for Unix-like operating systems such as Linux and Mac OS X, as well as Windows. Relatively new is GnuPG 2, which is a modularized version but not (yet) a replacement. It's often built and installed as "gpg2" so it can coexist with trusty old "gpg" version 1. I mention this to raise awareness, since it seems to be little known.

When you have an encrypted file, how can you see who the recipients are who will be able to decrypt it? It's easy enough to test if *you* can decrypt it, by just trying and seeing if it lets you. But what if you want to confirm others can see it before you send it to them? The manpage shows this option:

--list-only

> 
> Changes the behaviour of some commands. This is like --dry-run but different in some cases. The semantic of this command may be extended in the future. Currently it only skips the actual decryption pass and therefore enables a fast listing of the encryption keys.
> 

That sounds like the answer. And it almost is. However, for no reason I can discern, it doesn't show any recipients who have a secret key in the keyring of the running GnuPG instance! They just aren't included. We can't simply assume we are recipients, either, because there's no visible difference between not being a recipient and being one with it being omitted.

I've looked for an answer to this before, and found people saying --list-only *does* include everyone, but for both gpg 1 and 2 that just isn't true for me.

Taking desperate measures, I moved my ~/.gnupg/secring.gpg away and then it worked fine, because it can no longer see my secret keys, so I'm like any other recipient.

Now, to achieve that same effect without actually moving the secret keyring around. Here's how:

```
gpg --list-only --no-default-keyring --secret-keyring /dev/null $infile
```

I'd love to hear of any easier way to achieve this, but in the meantime, that works.

(Cute safe icon by [VisualPharm](http://www.visualpharm.com/).)


