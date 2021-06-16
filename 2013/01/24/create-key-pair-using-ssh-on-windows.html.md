---
author: Bianca Rodrigues
gh_issue_number: 751
tags: security
title: Create an SSH key pair on Windows
---

I recently joined End Point as a full-time employee after interning with the company since August 2012. I am part of the marketing and sales team, working out of the New York City office.

One of the frequent queries we receive from our non-technical clients is how to create an SSH key pair. This post is an introduction to using SSH on Windows for anyone who needs some clarification on this network protocol.

SSH stands for Secure Shell, which is used to provide secure access to remote systems. PuTTY is an open source SSH client that is available for Windows.

Using the concept of “key-based” SSH logins, you can avoid the usual username/​password login procedure, meaning only those with a valid private/​public key pair can log in. This allows for a more secure system.

To begin, install PuTTYgen, PuTTY and Pageant on your Windows system:

- [PuTTYgen](https://the.earth.li/~sgtatham/putty/latest/x86/puttygen.exe)
- [PuTTY](https://the.earth.li/~sgtatham/putty/latest/x86/putty.exe)
- [Pageant](https://the.earth.li/~sgtatham/putty/latest/x86/pageant.exe)

Let’s focus on PuTTYgen – used to create a private/​public key pair.

* After downloading PuTTYgen, run puttygen.exe
* In the “Parameters” – “Type of key” section, make sure “SSH-2 RSA” is selected:

<a href="/blog/2013/01/24/create-key-pair-using-ssh-on-windows/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/01/24/create-key-pair-using-ssh-on-windows/image-0.png"/></a>

SSH-2 RSA is what End Point recommends at this time. The other types provide poorer security.

The default key size of 1024 is a minimum, but 2048 or 4096 bits makes more sense given the power of modern computers to crack keys.

* Click Generate in the “Actions” section above.

* Once the key starts to generate follow the instructions written, by moving the mouse pointer over the blank area to generate some randomness. The faster you move the mouse, the faster it will generate:

<a href="/blog/2013/01/24/create-key-pair-using-ssh-on-windows/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/01/24/create-key-pair-using-ssh-on-windows/image-1.png"/></a>

* Congratulations! Your private/​public key pair has been generated. Next to “Key comment”, enter text (usually your email address). Next, enter and confirm your “Key passphrase”. Note: You will need this passphrase to log in using your new key, so make sure to record this information in a secure place. The passphrase should be unique, not used for anything else, especially not any online services, to limit exposure if some other accounts are “hacked”.

* Next, click on “Save private key” and save it on your computer (in a location **only you** can access). Do the same for “Save public key”.

* After you’re done saving, copy the public key in the section titled “Public key for pasting into OpenSSH authorized_keys file” and send it to your server administrator.

<a href="/blog/2013/01/24/create-key-pair-using-ssh-on-windows/image-2.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/01/24/create-key-pair-using-ssh-on-windows/image-2.png"/></a>

The above description demonstrates only one of the uses of SSH: a reasonably secure method of remotely connecting to another computer. Once a secure SSH connection has been established, it can also be used to transfer files securely using SCP (Secure Copy) or SFTP (Secure File Transfer Program). SFTP is the secure alternative to “classic FTP” and the best common secure option for transferring files to or from a server.
