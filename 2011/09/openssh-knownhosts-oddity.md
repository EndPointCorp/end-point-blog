---
author: Jon Jensen
title: OpenSSH known_hosts oddity
github_issue_number: 496
tags:
- hosting
- security
date: 2011-09-12
---



A new version of the excellent [OpenSSH](https://www.openssh.com/) was recently released, [version 5.9](https://www.openssh.com/txt/release-5.9). As you’d expect from such widely-used mature software, there are lots of minor improvements to enjoy rather than anything too major.

But what I want to write about today is a little surprise in how ssh handles multiple cached host keys in its known_hosts files.

I had wrongly thought that ssh stopped scanning known_hosts when it hit the first hostname or IP address match, such as happens with lookups in /etc/hosts. But that isn’t how it works. The [sshd manual](https://man.openbsd.org/sshd#SSH_KNOWN_HOSTS_FILE_FORMAT) reads:

> It is permissible (but not recommended) to have several lines or different host keys for the same names. This will inevitably happen when short forms of host names from different domains are put in the file. It is possible that the files contain conflicting information; authentication is accepted if valid information can be found from either file.

The “files” it refers to are the global /etc/ssh/known_hosts and the per-user ~/.ssh/known_hosts.

The surprise was that if there are multiple host key entries in ~/.ssh/known_hosts, say, for 10.0.0.1. If the first one has a non-matching host key, the ssh client tries the second one, and so on until it runs out of matching IP address entries to check. If none have a matching host key, the ssh client error reports the offending line number for the last matching IP address, but gives no indication there are earlier mismatches as well.

This is actually kind of convenient if you have scripts that simply append new host keys to the end of the known_hosts file, and it also makes sense since hostname wildcards and multiple hostnames per line are allowed. It’s fine, but it isn’t what I expected and is nice to know.


