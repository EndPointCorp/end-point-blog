---
title: "SSH and Old Servers"
author: Josh Ausborne
github_issue_number: 1996
date: 2023-07-21
tags:
- linux
- ssh
- sysadmin
---

![A photo of a whole bivalve seashell lying open and flat on the sandy ground.](/blog/2023/07/ssh-and-old-servers/seashell-beach.webp)

<!-- Photo by Josh Ausborne -->

We recently updated one of our backup servers from [Oracle Linux](https://www.oracle.com/linux/) 8 to Oracle Linux 9, a free rebuild of [Red Hat Enterprise Linux](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) 9, also known as RHEL 9. As with any newer OS, there are bound to be unexpected little differences which crop up and which need to be handled.

In the case of our backup server, we found that it could no longer SSH to older servers, which includes a couple running CentOS 5 (yes, there really are a few of those out in the wild), some CentOS 6, and one Debian 8. We saw similar connection problems when we first went from CentOS 7 to Oracle Linux 8, and we addressed the issues by creating a Host entry for the servers in our `~/.ssh/config` file.

Here is an example of of the entry that we used previously:

```console
Host old-server-1 old-server-2 old-server-3
  User root
  Hostname %h.example.com
  KexAlgorithms +diffie-hellman-group-exchange-sha1
```

This worked fine for a couple of years until we upgraded from Oracle Linux 8 to 9. At this point we started to see a different problem when trying to connect.

```console
Unable to negotiate with <nnn.nnn.nnn.nnn> port 22: no matching host key type found. Their
offer: ssh-rsa,ssh-dss
```

### Troubleshooting

One of the good troubleshooting methods for diagnosing SSH connectivity problems is to enable some verbosity when connecting. This can be done via the use of the `-v` option, which can be stacked up to three times for increasing levels of detail. In this case, I used `ssh -vvv $hostname`, which is the highest level, and I was able to see another error message in the copious output:

```console
ssh_dispatch_run_fatal: Connection to <nnn.nnn.nnn.nnn> port 22: error in libcrypto
```

It was at this time that I had to consult with The Fountain of Knowledge (the Internet) to come up with a solution. There were some suggestions to add `HostKeyAlgorithms` or `PubkeyAcceptedKeyTypes` entries for those hosts in the local SSH config, but that didn’t work in this case.

What I did find, though, is that RHEL 9-based OSes now forbid via crypto policy the ability to connect using SHA-1, but SHA-1 is the default crypto policy in use by CentOS 5 and CentOS 6! To get around this, I needed to add SHA-1 support to our existing policy. You can compare the crypto policies for [RHEL 8 systems](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/security_hardening/using-the-system-wide-cryptographic-policies_security-hardening) and [RHEL 9 systems](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/security_hardening/using-the-system-wide-cryptographic-policies_security-hardening) to see which is right for your use case.

```console
update-crypto-policies --set DEFAULT:SHA1
```

Here I also found a bit of info on [re-enabling SHA-1](https://access.redhat.com/documentation/fr-fr/red_hat_enterprise_linux/9/html/security_hardening/proc_re-enabling-sha-1_using-the-system-wide-cryptographic-policies).

### A problem for every solution

One more problem that we ran into with one of the CentOS 5 servers is that we were getting a different SSH failure even after having updated the crypto policy. This new problem was about the length of the host key on the old remote server.

```console
Bad server host key: Invalid key length
```

That is because RHEL 9 by default doesn’t like short RSA host keys. Thankfully, there is an option that can be enabled at the SSH client level to help us overcome the limitation. It is solved in the usual manner of adding an option to the `~/.ssh/config` file. The option is known as `RequiredRSASize`, and it specifies the minimum length of RSA key that is required to be considered valid.

```console
Host old-server-1 old-server-2 old-server-3
  User root
  Hostname %h.example.com
  KexAlgorithms +diffie-hellman-group-exchange-sha1
  RequiredRSASize 1024
```

### Perfect … enough

Obviously we don't want to let old systems just sit out there and keep doing their thing. They increase the attack surface that hackers can target, and it’s important to stay on top of updating and upgrading. In an ideal world, we’d prefer that we simply replace and modernize the old, thus securing everything, and deal with the pain of upgrading all at one time. We like to just get the headache over with.

In the real world, though, some old systems just have to stay in place for a little longer (or “much longer” in this case) than we’d prefer. It’s helpful to figure out acceptable ways to work around the limitations when these issues arise, while wherever possible making the exceptions only for the specific old hosts we want to tolerate.
