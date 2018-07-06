---
author: Selena Deckelmann
gh_issue_number: 166
tags: postgres, windows
title: 'PostgreSQL Windows installer tip: passwords'
---

*Updated below!*

When specifying a password for the Windows PostgreSQL one-click installer, you get this message:

> Please provide a password for the database superuser and service
> account (postgres). If the service account already exists in Windows,
> you must enter the current password for the account. If the account
> does not exist, it will be created when you click ‘Next’.

If you have already installed Postgres as a service, you will need to enter the **current user postgres service user** password to get past the password dialog box. Meaning, if you’re logged in to Windows as ‘selena’, you need to enter selena’s password. As a non-Windows user, this baffled me, and [a few other people on this thread](https://www.postgresql.org/message-id/937d27e10907021018o65776517heaee04605b088ad7@mail.gmail.com).

Otherwise, you can just enter a password that will be used for the ‘postgres’ database user. Hope this helps someone!

**Update:**

Further explanation from **Dave Page**, the maintainer of the Windows package:

Selena: It’s not the password for the user that you are logged in as that you need to enter, it’s the password for the service account (ie. postgres).

Unlike *nix & Mac, service accounts on Windows need to have passwords so unfortunately we need to ensure we have the correct password to install the service. Hence, if there’s an existing postgres account, we need the existing password, otherwise the account will be created with whatever password you specify.

In all OSes, we use the password entered on that page as the database superuser password.
