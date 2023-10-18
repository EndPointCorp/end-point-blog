---
author: Jon Jensen
title: SELinux fix for sudo PAM audit_log_acct_message() failed
github_issue_number: 886
tags:
- redhat
- security
- selinux
- sysadmin
date: 2013-11-20
---

I was just reading my co-worker Lele’s blog post about [making SELinux dontaudit AVC denial messages visible](/blog/2013/11/selinux-and-need-of-talking-about/) and realized it was likely the solution to a mystery I ran into a few days ago.

As Lele explains, the SELinux dontaudit flag suppresses certain very common SELinux AVC denials to keep the audit logs from bloating beyond belief and being too hard to use. But sometimes a commonly harmless denial can be the cause of further errors. You can tell this is the case if temporarily disabling SELinux enforcing (setenforce 0) makes the problem go away, but /var/log/audit/audit.log still doesn’t show any AVC denial actions being allowed through.

In my somewhat unusual case there is an Apache CGI shell script that calls sudo to invoke another program as a different user without using setuid or suEXEC. Everything works fine with SELinux enforcing, but there are some strange errors in the logs. In /var/log/secure:

```plain
sudo: PAM audit_log_acct_message() failed: Permission denied
```

And in the Apache error_log is the apparently strangely unbuffered output:

```plain
[error] sudo
[error] :
[error] unable to send audit message
[error] :
[error] Permission denied
[error]
```

To show the dontaudit AVC denials, I ran semodule -DB as Lele explained, and then I saw in /var/log/audit/audit.log:

```plain
type=AVC msg=audit(1384959223.974:4192): avc:  denied  { write } for  pid=14836 comm="sudo" scontext=system_u:system_r:httpd_sys_script_t:s0 tcontext=system_u:system_r:httpd_sys_script_t:s0 tclass=netlink_audit_socket
type=AVC msg=audit(1384959223.975:4194): avc:  denied  { read } for  pid=14836 comm="sudo" scontext=system_u:system_r:httpd_sys_script_t:s0 tcontext=system_u:system_r:httpd_sys_script_t:s0 tclass=netlink_audit_socket
type=AVC msg=audit(1384959223.999:4196): avc:  denied  { write } for  pid=14836 comm="sudo" scontext=system_u:system_r:httpd_sys_script_t:s0 tcontext=system_u:system_r:httpd_sys_script_t:s0 tclass=key
```

Somewhat as expected from the error messages we saw before, sudo is being denied permission to send a message into the kernel. Now that we have the AVC errors from the audit log it’s easy to [make a local SELinux policy module](/blog/2012/05/selinux-local-policy-modules/) to allow this.

The spurious error messages go away, and we can run semodule -B to re-suppress the dontaudit messages.

Thanks, Lele. :)
