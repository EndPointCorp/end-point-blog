---
author: David Christensen
title: DBD::Pg moves to Git!
github_issue_number: 468
tags:
- dbdpg
- git
- postgres
- perl
date: 2011-06-14
---

Just a note to everyone that development the official DBD::Pg DBI driver for PostgreSQL source code repository has moved from its old home in Subversion to a Git repository. All development has now moved to this repo.

We have imported the SVN revision history, so it’s just a matter of pointing your Git clients to:

```bash
$ git clone git://bucardo.org/dbdpg.git
```

For those who prefer, there is a GitHub mirror:

```bash
$ git clone git://github.com/bucardo/dbdpg.git
```

Git is available via many package managers or by following the download links at [https://git-scm.com/download](https://git-scm.com/download) for your platform.

Enjoy!
