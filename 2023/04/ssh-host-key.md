---
author: "Selvakumar Arumugam"
title: "Unable to negotiate with xxxx port xx: no matching host key type found. Their offer: ssh-rsa [preauth]"
github_issue_number: 1953
date: 2023-04-04
tags:
- ssh
- authentication
---

![A close shot of a large golden key sitting on top of a wooden fence. There is green grass visible behind the fence, on the left and right upper sides of the image.](/blog/2023/04/ssh-host-key/key.webp)

The SSH connections between a client and a remote server begin with a host key verification as an initial handshake. If the default key algorithm is not supported between the client and server, the SSH connection attempt is closed with no matching host key type response. In this article, we will explore the host key verification process and discuss ways to handle the non-matching host key issue to establish the connection.

```plain
$ sftp username@domain
Unable to negotiate with xx.xx.xx.xx port 22: no matching host key type found. Their offer: ssh-rsa
Connection closed.
Connection closed
```

### Host Keys

By default, OpenSSH automatically generates a public-private key pair on the server and stores it in `/etc/ssh`. These keys, known as host keys, are created using several encryption algorithms including RSA, DSA, ECDSA, and ED25519.

The pair of private and public keys is available on the host server at the path `/etc/ssh`.

```plain
$ ls /etc/ssh | grep key
ssh_host_dsa_key
ssh_host_dsa_key.pub
ssh_host_ecdsa_key
ssh_host_ecdsa_key.pub
ssh_host_ed25519_key
ssh_host_ed25519_key.pub
ssh_host_rsa_key
ssh_host_rsa_key.pub
```

### How does OpenSSH decide which host key to use?

During SSH connection establishment, the OpenSSH server presents a default host key signature algorithm to the SSH client. To check the list of key signature algorithms and their order, you can perform a query with `ssh -Q sig`.

```plain
$ ssh -Q sig
ssh-ed25519
sk-ssh-ed25519@openssh.com
ssh-rsa
rsa-sha2-256
rsa-sha2-512
ssh-dss
ecdsa-sha2-nistp256
ecdsa-sha2-nistp384
ecdsa-sha2-nistp521
sk-ecdsa-sha2-nistp256@openssh.com
webauthn-sk-ecdsa-sha2-nistp256@openssh.com
```

### HostKeyAlgorithms

You can also get a list of key types and signature algorithms with `ssh -Q HostKeyAlgorithms`:

```plain
$ ssh -Q HostKeyAlgorithms
ssh-ed25519
ssh-ed25519-cert-v01@openssh.com
sk-ssh-ed25519@openssh.com
sk-ssh-ed25519-cert-v01@openssh.com
ssh-rsa
rsa-sha2-256
rsa-sha2-512
ssh-dss
ecdsa-sha2-nistp256
ecdsa-sha2-nistp384
ecdsa-sha2-nistp521
sk-ecdsa-sha2-nistp256@openssh.com
webauthn-sk-ecdsa-sha2-nistp256@openssh.com
ssh-rsa-cert-v01@openssh.com
rsa-sha2-256-cert-v01@openssh.com
rsa-sha2-512-cert-v01@openssh.com
ssh-dss-cert-v01@openssh.com
ecdsa-sha2-nistp256-cert-v01@openssh.com
ecdsa-sha2-nistp384-cert-v01@openssh.com
ecdsa-sha2-nistp521-cert-v01@openssh.com
sk-ecdsa-sha2-nistp256-cert-v01@openssh.com
```

The default list of host keys can be modified on the OpenSSH server by configuring the `/etc/ssh/sshd_config` file, as described below.

| Symbol  | Description | Example |
| ------------- | ------------- | ------------- |
| +<algorithm_name>  | Algorithm will be appended to default set of list  |  +rsa-sha  |
| -<algorithm_name>  | Algorithm will be removed  |  -rsa-sha  |
| ^<algorithm_name>  | Algorithm will be default value on top of list  |  ^rsa-sha  |

> You can see more in-depth info about SSH configuration with `man 5 ssh_config`.

### Identify host key type

SSH client and server logs provide valuable information about the host key algorithm types that are offered during SSH connections. In case of a mismatch between the client and server, the logs will record the offered key information from the other end. This information will be useful for troubleshooting and identifying the root cause of the issue.

SSH client output:

```plain
$ sftp -o HostKeyAlgorithms=ssh-rsa  username@domain
Unable to negotiate with <server_id> port 22: no matching host key type found.
Their offer: rsa-sha2-512,rsa-sha2-256
```

SSH Server log (`/var/log/auth.log`):

```plain
2022-06-28T22:26:46.692753-07:00 localhost sshd[445086]:
Unable to negotiate with <client_id> port 55872: no matching host key type found.
Their offer: ssh-rsa [preauth]
```

#### Third-party application logs

Some third-party applications return the MD5 hash code in the event of a failed SSH connection attempt. This code can be useful in identifying the exact matching key algorithm that needs to be included in the server.

```plain
Limiting the SSH algorithms for the SFTP connection to
the following: none, zlib, zlib@openssh.com, aes256-chc, aes192-che,
aes128-cbe, diffie-hellman-group14-sha256, ecdh-sha2-nistp256,
ecdh-sha2-nistp384, ecdh-sha2-nistp521, ssh-dss, ssh-rsa, hmac-sha2-
256, hmac-sha2-512, hmac-shal.

Configuring server validation for the SSH connection using
public keys: 3072: 8b 7e de 33 d8 f4 f5 82 d6 86 68 41 17 ba 72 4c.
```

The MD5 value of a key found in a third-party application log can be used to identify the matching key on the server with the help of the ssh-keygen utility.

```plain
$ ssh-keygen -lf ssh_host_rsa_key.pub
3072 SHA256:kkcdlhNcj8DndHvyLBXGfhI/oZkrTRIAbwuqqd58uY0

$ ssh-keygen -E md5 -lf ssh_host_rsa_key.pub
3072 MD5:8b:7e:de:33:d8:f4:f5:82:d6:86:68:41:17:ba:72:4c root@ndpbh-test-epitrax-app01 (RSA)
```

### ssh-rsa disabled by default

Since the release of OpenSSH version 8.8, the ssh-rsa key algorithm has been disabled. As a result, accessing the latest version of the OpenSSH server from an older client version may lead to non-matching host key failures.

```plain
$ ssh -V
OpenSSH_8.9p1 Ubuntu-3, OpenSSL 3.0.2 15 Mar 2022
```

Notice: http://www.openssh.com/txt/release-8.7

```plain
Imminent deprecation notice
===========================
OpenSSH will disable the ssh-rsa signature scheme by default in the
next release.
```

Legacy Support: https://www.openssh.com/txt/release-8.8

```plain
Potentially-incompatible changes
================================

This release disables RSA signatures using the SHA-1 hash algorithm
by default. This change has been made as the SHA-1 hash algorithm is
cryptographically broken, and it is possible to create chosen-prefix
hash collisions for <USD$50K [1]

For most users, this change should be invisible and there is
no need to replace ssh-rsa keys. OpenSSH has supported RFC8332
RSA/SHA-256/512 signatures since release 7.2 and existing ssh-rsa keys
will automatically use the stronger algorithm where possible.

Incompatibility is more likely when connecting to older SSH
implementations that have not been upgraded or have not closely tracked
improvements in the SSH protocol. For these cases, it may be necessary
to selectively re-enable RSA/SHA1 to allow connection and/or user
authentication via the HostkeyAlgorithms and PubkeyAcceptedAlgorithms
options. For example, the following stanza in ~/.ssh/config will enable
RSA/SHA1 for host and user authentication for a single destination host:

    Host old-host
        HostkeyAlgorithms +ssh-rsa
	PubkeyAcceptedAlgorithms +ssh-rsa

We recommend enabling RSA/SHA1 only as a stopgap measure until legacy
implementations can be upgraded or reconfigured with another key type
(such as ECDSA or Ed25519).

[1] "SHA-1 is a Shambles: First Chosen-Prefix Collision on SHA-1 and
    Application to the PGP Web of Trust" Leurent, G and Peyrin, T
    (2020) https://eprint.iacr.org/2020/014.pdf
```

### Solution

The SSH client and server offer options to specify the host key algorithm to use during SSH connections. Therefore, you can modify the client or server configuration to establish a connection based on the restrictions of one of the systems involved.

Establishing an SSH connection using the most secure host key algorithm is highly recommended for optimal security. However, in situations where there are limitations on upgrading or changing the algorithm, users must make decisions based on the security policies of their application environment.

In such cases, a suggested solution is to carefully evaluate the security requirements of the application environment and choose the host key algorithm that best aligns with those requirements. This may involve a trade-off between security and compatibility, so it is important to weigh the potential risks and benefits of each option.

#### SSH Client

When the privilege to configure the SSH server is restricted, the SSH client can be configured to use a specific algorithm. To do this, you can use the `-o HostKeyAlgorithms=<host_key>` option with the SSH client to specify a particular host key algorithm type.

```plain
$ sftp username@server
Unable to negotiate with <server> port 22: no matching host key type found. Their offer: ssh-rsa
Connection closed.
Connection closed
```

In the above case, the SSH server uses ssh-rsa as the host key algorithm to establish connections. To use ssh-rsa as the key algorithm for the SSH client, you can configure it as follows.

```plain
$ sftp -o HostKeyAlgorithms=ssh-rsa username@server
username@server~:$
```

#### SSH Server

In some cases, it may not be possible to configure the SSH client to use a specific key when a third-party proprietary application is used to establish the connection. In such scenarios, the SSH server can be configured to include the required key.

In our scenario, the third-party application expects the ssh-rsa key type, but the latest version of OpenSSH server does not provide ssh-rsa as it has been deprecated.

To support old client attempts with ssh-rsa, the key should be added to the bottom of the list with a "+" symbol. This will allow the server to present the deprecated ssh-rsa key to old clients, while still offering more secure key algorithms to newer clients. The new lines in `/etc/ssh/sshd_config` should look like the following:

```plain
HostKeyAlgorithms +ssh-rsa
PubkeyAcceptedAlgorithms +ssh-rsa
```

Before restarting the SSH service, it is advisable to test the configuration for syntax errors to prevent potential issues, like the following which occurs if you add an extra space to `Host KeyAlgorithms +ssh-rsa`:

```plain
# sshd -t
/etc/ssh/sshd_config: line 32: Bad configuration option: Host
/etc/ssh/sshd_config: terminating, 1 bad configuration options
```

Once you've verified the configuration and `sshd -t` gives no output, go ahead and restart the service to apply the changes.

```plain
# sshd -t

# systemctl reload sshd.service
```

With this configuration, SSH clients can connect to the server using ssh-rsa. To verify the host key type used in an SSH connection, you can use the verbose (`-v`) option with the `ssh` command. This will display additional information about the SSH connection, including the host key algorithm being used. Here we increase the verbosity by adding the maximum of 3 `-v` options.

```plain
$ ssh -vvv -oHostKeyAlgorithms=ssh-rsa username@domain
…
debug2: host key algorithms: ssh-rsa
debug1: Will attempt key: .ssh/id_rsa RSA
SHA256:CmARXi+/8UwrvzwS7RkJNqD/rhroYTnfB285OnovVFs agent
…
```
