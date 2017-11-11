---
author: Jon Jensen
gh_issue_number: 46
tags: networking
title: Some handy cryptography/networking tools
---

Here's a list of some nifty cryptography/networking tools Kiel's pointed out lately:

- [socat](http://www.dest-unreach.org/socat/) - multipurpose relay; think netcat gone wild -- we used this recently to tunnel UDP DNS queries over ssh
- [cryptcat](http://sourceforge.net/projects/cryptcat/) - netcat with twofish encryption (the Debian package adds a man page)
- [rsyncrypto](http://rsyncrypto.lingnu.com/) - partial transfer-friendly encryption (modified CBC for smaller change windows similar to gzip; less secure than regular CBC)

And a pretty unrelated but useful [Red Hat Magazine article](http://www.redhatmagazine.com/2008/01/16/tips-and-tricks-yum-security/) on the new yum-security plugin.
