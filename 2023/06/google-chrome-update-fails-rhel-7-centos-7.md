---
title: Google Chrome Yum/​RPM package update fails on RHEL/​CentOS 7
author: Jon Jensen
github_issue_number: 1979
date: 2023-06-08
tags:
- redhat
- sysadmin
- security
- linux
---

![Fantasy painting of a shipwreck in a jungle backlit by sunlight](/blog/2023/06/google-chrome-update-fails-rhel-7-centos-7/willgard-krause-painted-ship-wreck-jungle.webp)
[Painting by Willgard Krause](https://pixabay.com/photos/fantasy-painted-ship-wreck-jungle-7422641/), Pixabay license

One of our clients uses the Chrome web browser running on their continuous integration server with Jenkins for automated e2e (end-to-end) testing of their website. That server runs Red Hat Enterprise Linux (RHEL) 7—actually the rebuild CentOS 7.

Last month, in May 2023, Google started signing Chrome RPMs with a GnuPG subkey, where they before had signed with the main key. Now `yum upgrade` fails when trying to update Chrome, giving this error:

```plain
warning: /var/cache/yum/x86_64/7/google-chrome/packages/google-chrome-stable-114.0.5735.106-1.x86_64.rpm: Header V4 RSA/SHA512 Signature, key ID a3b88b8b: NOKEY
Retrieving key from https://dl.google.com/linux/linux_signing_key.pub


The GPG keys listed for the "google-chrome" repository are already installed but they are not correct for this package.
Check that the correct key URLs are configured for this repository.


 Failing package is: google-chrome-stable-114.0.5735.106-1.x86_64
 GPG Keys are configured as: https://dl.google.com/linux/linux_signing_key.pub
```

To double-check, we tried to manually verify the signature on the downloaded RPM package with:

```plain
# rpm -K /var/cache/yum/x86_64/7/google-chrome/packages/google-chrome-stable-114.0.5735.106-1.x86_64.rpm
/var/cache/yum/x86_64/7/google-chrome/packages/google-chrome-stable-114.0.5735.106-1.x86_64.rpm: RSA sha1 ((MD5) PGP) md5 NOT OK (MISSING KEYS: (MD5) PGP#a3b88b8b)
```

That showed it is not just a Yum problem, but affects RPM too.

### Sweatin' to the oldies

Long ago (see reference below), people reported that RPM wasn't working with GnuPG subkeys for signatures, and Red Hat confirmed this is the case for RHEL 7 and earlier. They added support, but that first appeared in RHEL 8.

RHEL 7 has another year of support left, until end of June 2024. But it was released in 2014 and is so old that apparently Google isn't testing the RPM packages it produces on RHEL 7 anymore.

Our client is planning to move this system that runs tests with Chrome to Rocky Linux 9, but for the next few months they need it to keep working on CentOS 7.

So to cope, we used `scp` to copy that RPM file to a RHEL 8 or 9 server, imported the Google signing public key, and used the newer version of `rpm` there to verify the signature:

```plain
# rpm -K google-chrome-stable-114.0.5735.106-1.x86_64.rpm 
google-chrome-stable-114.0.5735.106-1.x86_64.rpm: digests signatures OK
```

Then back on the RHEL 7 server we had no qualms skipping the signature check during upgrade because we had just manually checked it elsewhere:

```plain
# rpm -Uvh --nosignature /var/cache/yum/x86_64/7/google-chrome/packages/google-chrome-stable-114.0.5735.106-1.x86_64.rpm 
Preparing...                          ################################# [100%]
Updating / installing...
   1:google-chrome-stable-114.0.5735.1################################# [ 50%]
Cleaning up / removing...
   2:google-chrome-stable-113.0.5672.6################################# [100%]
```

The we ran `yum upgrade` again to get the rest of that server's pending package updates. Yum didn't care about Chrome anymore since we had updated it already.

### References

* [Reddit discussion on this situation](https://www.reddit.com/r/chrome/comments/13s799o/googlechromebeta_1140573545_rpm_invalid_signature/)—thanks especially to user Jskud
* [Red Hat Bugzilla #227632](https://bugzilla.redhat.com/show_bug.cgi?id=227632) where the problem is confirmed and the future fix announced
