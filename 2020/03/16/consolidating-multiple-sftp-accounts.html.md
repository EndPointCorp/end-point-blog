---
author: "Selvakumar Arumugam"
title: "Consolidating Multiple SFTP Accounts Into One Master Account"
tags: ssh, shell, security
gh_issue_number: 1605
---

<img src="/blog/2020/03/16/consolidating-multiple-sftp-accounts/image-0.jpg" alt="merging roads" />

[Photo](https://unsplash.com/photos/kzSNNqqS3Qs) by [Dan Meyers](https://unsplash.com/@dmey503)

Recently, a client implemented a data-intensive workflow to generate various reports and insights from a list of facilities. Because a significant portion of these files contain sensitive data, they needed to strictly comply with HIPAA. Optimally, facilities should be able to transfer files securely and exclusively to our server. One of the best methods of achieving this is to create individual SSH File Transfer Protocol (SFTP) accounts for each source.

### SFTP account

Private SFTP accounts were established for each facility and the data was received at a designated path. At these individual points of contact, a third-party application picks up the data and processes further into the pipeline. The following demonstrates how SFTP accounts are developed and configured:

* Create a user group for SFTP accounts:

```bash
$ addgroup sftpusers
```

* Configure the following settings in sshd_config (this enables an SFTP account and sets the default location as the home path):

```bash
$ vi /etc/ssh/sshd_config
...
# override default of no subsystems
Subsystem       sftp    internal-sftp...

Match Group sftpusers
    ChrootDirectory /home/%u
    AllowTCPForwarding no
    X11Forwarding no
    ForceCommand internal-sftp
```

* Restart SSH server to apply changes:

```bash
$ systemctl restart ssh
```

* Create an SFTP user account for a facility and place in a folder on the home path to receive data:

```bash
# set new user name
sftpuser=the-new-username
useradd $sftpuser
usermod -g sftpusers -s /usr/sbin/nologin $sftpuser
mkdir -p /home/$sftpuser/INPUT_PATH/
chown -R root:root /home/$sftpuser
```

### Mount multiple accounts to one account

The goal here is to point the data from many facilities to one location, but using a single account and path for multiple sites’ data could result in a breach of security and/​or privacy. Mounting the receiving path of a facility’s data onto a single master account and then to a “mount point” with a unique facility name takes care of this issue. The process next consolidates files from individual paths on a master account in one place where the application picks up messages for further processing.

The SFTP accounts and the master account should be attached to the same group. This will permit individual accounts to write on the master account-mounted path. In turn, the master account can read files from the same location. This location now has administrative rights for both the SFTP user the group. Group permission of the mounted folder is set to sftpgroup and user permission is set to the facility account.

```bash
# create master user account
$ adduser master
$ passwd master

# Add master user to sftpgroup group
usermod -a -G sftpgroup master
getent group sftpgroup

# MOUNT_PATH and sub folders
mkdir -p /home/master/MOUNT_PATH/{Input,Pickup,Backup,Archive}
chown -R master:master /home/master/MOUNT_PATH
```

We wrote a script to automate the process of creating an SFTP account, mounting it at the master account path, and adding fstab entries to save the mount in the case of a reboot. The script not only saves time, but also avoids human error when creating accounts for all facilities.

```bash
#!/bin/bash

# ./create_sftp_account.sh sftpfacilityone FACILITY_ONE

sftpuser=$1
facility_name=$2

# Create SFTP account and add to sftpgroup
useradd $sftpuser
usermod -g sftpusers -s /usr/sbin/nologin $sftpuser
usermod -a -G sftpgroup $sftpuser
mkdir -p /home/$sftpuser/INPUT_PATH
chown root:root /home/$sftpuser

# Create path specific to facility in master account Input folder
mkdir -p /home/master/MOUNT_PATH/Input/$facility_name
chown -R $sftpuser:sftpgroup /home/master/MOUNT_PATH/Input/$facility_name

# Mount sftp account into master account and set permissions
mount --bind /home/master/MOUNT_PATH/Input/$facility_name /home/$sftpuser/INPUT_PATH
chown -R $sftpuser:sftpgroup /home/$sftpuser/INPUT_PATH
chmod g=rwxs /home/$sftpuser/INPUT_PATH

# Add fstab entry to persist and mount on reboot
echo "/home/master/MOUNT_PATH/Input/$facility_name /home/$sftpuser/INPUT_PATH none bind 0 0" >> /etc/fstab
echo "Created user $sftpuser at $facility_name mount point successfully"
```

### Files at one location

Now, data files from facilities are available at individual folders under MOUNT_PATH/Input on the master account. This enables third-party applications to pick up files in a straightforward way to proceed with further processing. It also helps our client access the files for review from the master account easily without navigating into each separate account.

### Summary

Mounting multiple SFTP accounts onto one master account turns out to be an efficient and beneficial method of consolidating data. Both safe and secure, running separate SFTP accounts establishes an exclusive private link between facilities and servers. The master account has the unique ability to access files belonging to each facility in order to process the data further.

**Tip**: In order to avoid broken mounts, check the status by using the command `mount -fav`. Problems with mount configurations can cause broken mounts after rebooting the server.
