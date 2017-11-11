---
author: Emanuele “Lele” Calò
gh_issue_number: 998
tags: apache, redhat, php, selinux
title: SELinux, PHP and FTP issues
---

Sometimes it feels like working with SELinux is much like playing Wack-A-Mole. You manage to squash a bug/issue and another one appears elsewhere.

A similar situation happened to one of our customers when he tried connecting via FTP from his PHP code (through Apache).

After much debugging and a lot more Google-ing it turned out it was just a matter of enabling the right SELinux boolean setting.

In order to verify that it really was SELinux fault, we usually keep an eye on the "/var/log/audit/audit.log" log file and then temporarily set SELinux to "Permissive" with:

```bash
setenforce 0
```

In our case things started working as expected so we knew that it was SELinux fault, though we had no "AVC (denial)" error in the audit.log file, neither in Enforce nor in Permissive.

When this kind of situations happens it's usually a matter of finding which SELinux booleans needs to be toggled.

To discover which SELinux booleans is blocking the wanted behavior we need to temporarily disable the "dontaudit" setting by using:

```bash
semodule -DB
```

and then continue looking at the audit.log file. In our case we found that the interested setting was "httpd_can_network_connect".

First we verified that it really was set to off:

```bash
getsebool httpd_can_network_connect
```

If it is actually set to "off" then go on with the next steps, otherwise you'll probably need to investigate somewhere else.

Next set the SELinux boolean to "on" and put SELinux back to "Enforce" by running:

```bash
setsebool httpd_can_network_connect=1
setenforce 1
```

Now check again the the code is still running as expected and if so set the SELinux boolean to stick between reboots:

```bash
setsebool -P httpd_can_network_connect=1
```

If you toggled the "dontaudit" setting, remember to re-enable it or you'll end up with a very noisy log file:

```bash
semodule -B
```

If everything went well your PHP code trying to connect via FTP should now be working. If that's not the case, keep searching for errors and let us know in the comments what was your problem.

Feel free to skim through our other articles for some ideas and hints:

* [SELinux fix for sudo PAM audit_log_acct_message() failed](http://blog.endpoint.com/2013/11/selinux-fix-for-sudo-pam.html)

* [SELinux and the need of talking about problems](http://blog.endpoint.com/2013/11/selinux-and-need-of-talking-about.html)

* [SELinux Local Policy Modules](http://blog.endpoint.com/2012/05/selinux-local-policy-modules.html)

* [Passenger and SELinux](http://blog.endpoint.com/2009/03/passenger-and-selinux.html)
