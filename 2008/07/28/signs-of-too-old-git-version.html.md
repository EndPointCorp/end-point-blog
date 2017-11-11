---
author: Jon Jensen
gh_issue_number: 31
tags: git
title: Signs of a too-old Git version
---

When running git clone, if you get an error like this:

```
Couldn't get http://some.domain/somerepo.git/refs/remotes/git-svn for remotes/git-svn
The requested URL returned error: 404 error: Could not interpret remotes/git-svn as something to pull
```

You're probably using a really old version of Git that can't handle some things in the newer repository. The above example was from Git 1.4.4.4, the very old version included with Debian Etch. The best way to handle that is to use [Debian Backports](http://www.backports.org/) to upgrade to Git 1.5.5.

On Red Hat Enterprise Linux, Fedora, or CentOS, the [Git maintainers' RPMs](http://kernel.org/pub/software/scm/git/RPMS/) usually work (though you may need to get a dependency, the perl-Error package from [RPMforge](https://rpmrepo.org/RPMforge)).

If all else fails, grab the [Git source](http://git.or.cz/) and build it. I've never had a problem building the code anywhere, though building the docs requires a newer version of asciidoc than is easy to get on RHEL 3.
