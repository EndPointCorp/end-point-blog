---
author: Jon Jensen
gh_issue_number: 265
tags: hosting, optimization, tips
title: On Linux, noatime includes nodiratime
---

Note to performance-tweaking Linux sysadmins, pointed out to me by Selena Deckelmann: On Linux, the filesystem attribute [noatime includes nodiratime](https://web.archive.org/web/20100523223021/lwn.net/Articles/244941/), so there’s no need to say both “noatime,nodiratime” as I once did. (See [this article on atime](https://www.howtoforge.com/reducing-disk-io-by-mounting-partitions-with-noatime) for details if you’re not familiar with it.)

Apparently the nodiratime attribute was added later as a subset of noatime applying only to directories to still offer a bit of performance boost in situations where noatime on files would cause trouble (as with mutt and a few other applications that care about atimes).

See also the related newer relatime attribute in the mount(8) manpage.
