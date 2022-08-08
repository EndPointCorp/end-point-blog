---
title: "SSH Key Auth using KeeAgent with Git Bash and Windows CLI OpenSSH"
author: Ron Phipps
github_issue_number: 1889
date: 2022-08-08
tags:
- windows
- ssh
---

![A leather couch in surprisingly good condition sits on a patch of grass between the sidewalk and the road. Harsh sunlight casts shadows of trees and buildings on the street and couch.](/blog/2022/08/keeagent-with-git-bash-and-windows-cli-openssh/street-couch.webp)

<!-- Photo by Seth Jensen -->

In a [previous blog post](/blog/2022/07/windows-ssh-key-agent-forwarding-confirmation/) we showed how to configure KeePass and KeeAgent on Windows to provide SSH key agent forwarding with confirmation while using PuTTY and other PuTTY agent compatible programs. In this post we’ll expand on that by showing how to use the same key agent to provide SSH key auth when using Git Bash and the Windows command line OpenSSH.

### Git Bash support

Open KeePass, click on Tools → Options, select the KeeAgent tab.

Create `C:\Temp` if it does not exist.

Check the two boxes in the Cygwin/MSYS Integration section.

Directly after each box, fill in the path: `C:\Temp\cygwin-ssh.socket` for the Cygwin compatible socket file, and `C:\Temp\msys-ssh.socket` for the msysGit compatible socket file.

![KeePass options, open to the KeeAgent tab. Highlighted is the Cygwin/MSYS section, with two boxes checked. One reads "Create Cygwin compatible socket file (works with some versions of MSYS)". The other reads "Create msysGit compatible socket file". After each is the path described above.](/blog/2022/08/keeagent-with-git-bash-and-windows-cli-openssh/1-options-gitbash.webp)

Click OK.

Open Git Bash.

Create the file `~/.bash_profile` with the contents:

```bash
test -f ~/.profile && . ~/.profile
test -f ~/.bashrc && . ~/.bashrc
```

Create the file `~/.bashrc` with the contents:

```bash
export SSH_AUTH_SOCK="C:\Temp\cygwin-ssh.socket"
```

Close and reopen Git Bash.

You should now be able to SSH with Git Bash using your loaded SSH key and a dialog box should appear to approve the use of the key.

![Git Bash running ssh to a redacted server, with a dialog box reading "(ssh) has requested to use the SSH key (redacted) with fingerprint (redacted). Do you want to allow this?" The dialog's "No" button is selected by default.](/blog/2022/08/keeagent-with-git-bash-and-windows-cli-openssh/2-gitbash-ssh.webp)

### Windows command line OpenSSH support

Open KeePass, click on Tools → Options, select the KeeAgent tab.

Scroll down and click on the box next to “Enable agent for Windows OpenSSH (experimental).”

![KeePass options open to the KeeAgent tab. Inside a scrollable list is a checked checkbox reading "Enable agent for Windows OpenSSH (experimental)"](/blog/2022/08/keeagent-with-git-bash-and-windows-cli-openssh/3-options-windowsopenssh.webp)

Click OK.

Open a Windows Command Prompt.

You should now be able to SSH with Windows CLI using your loaded SSH key and a dialog box should appear to approve the use of the key.

![Windows Command Prompt running SSH, with the same KeePass dialog box asking approval for using the loaded SSH key](/blog/2022/08/keeagent-with-git-bash-and-windows-cli-openssh/4-windows-cli-ssh.webp)

