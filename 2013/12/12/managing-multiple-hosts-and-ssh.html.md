---
author: Patrick Lewis
gh_issue_number: 896
tags: devops, hosting, ssh
title: Managing Multiple Hosts and SSH Identities with OpenSSH
---

When I started working at End Point I was faced with the prospect of having multiple SSH identities for the first time. I had historically used an RSA SSH key with the default length of 2048 bits, but for my work at End Point I needed to generate a new key that was 4096 bits long. 

Although I could have used [ssh-copy-id](https://linux.die.net/man/1/ssh-copy-id) to copy my new SSH public key to all of my old servers, I liked the idea of maintaining separate “personal” and “work” identities and decided to look for a way to automatically use the right key based on the server I was trying to connect to.

For the first few days I was specifying my new identity on the command line using:

```
ssh -i .ssh/endpoint_rsa patrick@server.example.com
```

That worked, but I often forgot to specify my new SSH identity when connecting to a server, only realizing my mistake when I was prompted for a password instead of being authenticated automatically.

### Host Definitions

I had previously learned the value of creating an [ssh_config](https://linux.die.net/man/5/ssh_config) file when I replaced a series of command-line aliases with equivalent entries in the SSH config file. 

Instead of creating aliases in my shell:

```
alias server1='ssh -p 2222 -L 3389:192.168.1.99:3389 patrick@server1.example.com'
```

I learned that I could add an equivalent entry to my ~/.ssh/config file:

```
Host server1
  HostName server1.example.com
  Port 2222
  User patrick
  LocalForward 3389 192.168.1.99:3389
```

Then, to connect to that server, all I needed to do was run **ssh server1** and all of the configuration details would be pulled in from the SSH config file. Replacing my series of shell aliases with Host definitions had the added benefit of automatically carrying over to other tools like [git](https://git-scm.com/) and [mosh](https://mosh.mit.edu/) which read the same configuration.

### Switching Identities Automatically

There’s an easy solution to managing multiple SSH identities if you only use one identity per server; use [ssh-add](https://linux.die.net/man/1/ssh-add) to store all of your keys in the SSH authentication agent. For example, I used **ssh-add ~/.ssh/endpoint_rsa** to add my new key, and **ssh-add -l** to verify that it was showing up in the list of known keys. After adding all of your keys to the agent, it will automatically try them in order for SSH connections until it finds one that authenticates successfully. 

### Manually Defining Identities

If you need more control over which identity an SSH session is using, the **IdentityFile** option in [ssh_config](https://linux.die.net/man/5/ssh_config) lets you specify which key will be used to authenticate. Here’s an example:

```
Host server2
  HostName server2.example.com
  User patrick
  IdentityFile ~/.ssh/endpoint_rsa
```

This usage is particularly helpful when you have a server that accepts more than one of your identities and you need to control which one should be used.
