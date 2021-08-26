---
author: Jon Jensen
title: Postfix, ~/.forward, and SELinux on RHEL 5
github_issue_number: 65
tags:
- redhat
date: 2008-09-18
---



For the record, and maybe to save confusion for someone else who runs into this:

On Red Hat Enterprise Linux 5 with SELinux in enforcing mode, Postfix cannot read ~/.forward files by default. It's probably not hard to fix -- perhaps the .forward files just need to have the right SELinux context set -- but we decided to just use /etc/aliases in this case.


