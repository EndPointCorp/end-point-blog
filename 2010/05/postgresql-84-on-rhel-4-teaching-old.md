---
author: David Christensen
title: 'PostgreSQL 8.4 on RHEL 4: Teaching an old dog new tricks'
github_issue_number: 307
tags:
- database
- postgres
- redhat
date: 2010-05-19
---

So a client has been running a *really* old version of PostgreSQL
in production for a while. We finally got the approval to upgrade
them from 7.3 to the latest 8.4. Considering the age of the
installation, it should come as little surprise that they had been
running a similarly ancient OS: RHEL 4.

Like the installed PostgreSQL version, RHEL 4 is ancient—​5 years
old. I anticipated that in order to get us to a current version of
PostgreSQL, we’d need to resort to a source build or rolling our own
PostgreSQL RPMs. Neither approach was particularly appealing.

While the age/decrepitude of the current machine’s OS came as
little surprise, what did come as a surprise was that there were
supported RPMs available for RHEL 4 in the [community Yum RPM
repository](https://yum.postgresql.org/8.4/redhat/rhel-4-i386/repoview/) (modulo your architecture of choice).

In order to get things installed, I followed the instructions for
installing the specific yum repo. There were a few seconds where I
was confused because the installation command was giving a “permission
denied” error when attempting to install the 8.4 PGDG rpm as root. A
little brainstorming and a lsattr later revealed that a
previous administrator, apparently in the quest for über-security, had
performed a chattr +i on the /etc/yum.repo.d
directory.

Evil having been thwarted, in the interest of über-usability I did
a quick chattr -i /etc/yum.repo.d and installed the PGDG rpm.
Away we went. From that point, the install was completely
straightforward; I had a PostgreSQL 8.4.4 system running in no time,
and could *finally* get off that 7.3 behemoth. Now to talk my way
into an OS upgrade...
