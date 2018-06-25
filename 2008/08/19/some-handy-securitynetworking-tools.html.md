---
author: Jon Jensen
gh_issue_number: 46
tags: networking
title: Some handy cryptography/networking tools
---

Here’s a list of some nifty cryptography/networking tools Kiel’s pointed out lately:

- [socat](http://www.dest-unreach.org/socat/) — multipurpose relay; think netcat gone wild—​we used this recently to tunnel UDP DNS queries over ssh
- [cryptcat](https://sourceforge.net/projects/cryptcat/) — netcat with twofish encryption (the Debian package adds a man page)
- [rsyncrypto](https://rsyncrypto.lingnu.com/index.php/Home_Page) — partial transfer-friendly encryption (modified CBC for smaller change windows similar to gzip; less secure than regular CBC)

And a pretty unrelated but useful [Red Hat Magazine article](https://web.archive.org/web/20090207200409/http://magazine.redhat.com/2008/01/16/tips-and-tricks-yum-security/) on the new yum-security plugin.
