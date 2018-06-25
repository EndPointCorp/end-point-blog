---
author: Jon Jensen
gh_issue_number: 47
tags: security, conference
title: Subversion or CVS metadata exposure
---

At the talk “Rails Security” by Jonathan Weiss at [LinuxTag 2008](http://www.linuxtag.org/2008/), he mentioned (among other things) a possible security problem for sites being run out of a Subversion (or CVS or even RCS) working copy, where the metadata inside the .svn/ or CVS/ directories may be exposed to the world. [This post](https://scottbarnham.com/blog/2008/04/22/serving-websites-from-svn-checkout-considered-harmful/) by someone else explains it nicely.

[Interchange](http://www.icdevgroup.org/i/dev) appears not to be vulnerable to this by default as it will only serve files that end in .html, and all the .svn/ and CVS/ filenames have no suffix, or end with .svn-base, so are not served by Interchange.

But if the docroot is served from a Subversion or CVS checkout, its metadata files are likely served to the world—​relatively harmless, but can reveal internal file paths, hostnames, and OS account names.

For PHP or SSI, on the other hand, this could be a disaster, as the complete source to all files could be revealed, since the .svn-base suffix will cause Apache not to parse the code as PHP but pass through the source.

If you use Subversion, CVS, or RCS on any project, I recommend you look into how your files are being served and see if there’s anything being exposed. Checkouts from Git, Mercurial, or Bazaar are not likely to be a problem, since they only have metadata directories (.git, .hg, .bzr) and associated files at the root of the checkout, which would often be outside the docroot.

(This is based on my earlier [mailing list post](http://www.icdevgroup.org/pipermail/interchange-users/2008-August/049379.html) to the [interchange-users list](http://www.icdevgroup.org/mailman/listinfo/interchange-users).)
