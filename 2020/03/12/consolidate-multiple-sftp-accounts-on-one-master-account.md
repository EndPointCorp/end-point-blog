---
author: "Selvakumar Arumugam"
title: "Consolidate Multiple SFTP Accounts on One Master Account"
tags: ssh, sftp, shell
---


Recently, a data intensive client implemented a workflow process to generate various reports and insights from a list of facilities. Because a significant portion of these files contain sensitive data, they would need to strictly adhere to HIPAA compliance. Optimally, facilities should be able to transfer files securely and exclusively to our server. Arguably, the best method of achieving this is to create individual SSH File Transfer Protocol (SFTP) accounts for each source.


### SFTP Account

Private SFTP accounts were established for each facility and the data was received at a designated path. At these individual points of contact, a third party application picks up the data and processes further into the pipeline. The following demonstrates how SFTP accounts are developed and configured:


* Create a user group for SFTP accounts

```bash
$ addgroup sftpusers
```

* Configure the following settings in sshd_config (this enables an SFTP account and defaults the location as the home path)

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

* Restart SSH Server to apply changes

```bash
$ systemctl restart ssh
```

* Create an SFTP user account for a facility and place in a folder on the home path to receive data

```bash
# set new user name
sftpuser=the-new-username
useradd $sftpuser
usermod -g sftpusers -s /usr/sbin/nologin $sftpuser
mkdir -p /home/$sftpuser/INPUT_PATH/
chown -R root:root /home/$sftpuser
```

### Multiple Accounts Mounts to One Account

The goal here is to point the data from many facilities to one location. Yet, using a single account and path for multiple sites’ data will result in a breach in security and privacy. However, mounting the receiving path of a facility’s data onto a single master account to then “mount point” with a unique facility name takes care of this issue. The process continues on to consolidate files from individual paths on a master account in one place where the application picks up messages for further processing.


Both the SFTP accounts as well as master account should be attached to one group. This will permit individual accounts to write on the master account-mounted path. In turn, the master account can read files from the same location. This location now has administrative rights of both the SFTP user as well as shared group permission. Group permission of the mounted folder is set to sftpgroup and user permission is set to facility account.


A script is written to automate the list of actions in order to create an SFTP account, mount it at the master account path, and add fstab entries to save the mount in the case of a reboot. The script not only saved much time, but also avoided human error when creating accounts for all facilities in addition to future usage.

* Create master account, sftpgroup and mount paths

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

* Automated script to create sftp account and mount folders

```bash
#!/bin/bash

# sh create_sftp_account.sh sftpfacilityone FACILITY_ONE

sftpuser=$1
facility_name=$2

# Create SFTP account and add to sftpgroup 
useradd $sftpuser
usermod -g sftpusers -s /usr/sbin/nologin $sftpuser
usermod -a -G sftpgroup $sftpuser
mkdir -p /home/$sftpuser
chown root:root /home/$sftpuser
mkdir -p /home/$sftpuser/INPUT_PATH

# Create path specific to facility in master account Input folder
mkdir -p /home/master/MOUNT_PATH/Input/$facility_name
chown -R $sftpuser:sftpgroup /home/master/MOUNT_PATH/Input/$facility_name


# Mount sftp account into master account and set permissions
mount --bind /home/master/MOUNT_PATH/Input/$facility_name /home/$sftpuser/INPUT_PATH
chown -R $sftpuser:sftpgroup /home/$sftpuser/INPUT_PATH
chmod g=rwxs /home/$sftpuser/INPUT_PATH

# Add fstab entry to persist and mount on reboot
echo "/home/master/MOUNT_PATH/Input/$facility_name        /home/$sftpuser/INPUT_PATH        none        bind        0        0" >> /etc/fstab
echo "Created user $sftpuser at $facility_name mount point successfully"
```

### Files to One Location

Now, data files from facilities are available at individual folders under MOUNT_PATH/Input on the master account. It helps third party application to pick up files in a straight forward way to proceed with further processing. Also our client access the data files for review from master account in a effortless way without navigating into each facility account.


### Summary
Mounting multiple SFTP accounts on one master account that collects files at a single path turns out to be a very efficient and rewarding method of consolidating data. Both safe and secure, running individual SFTP accounts establishes an exclusively private link between facilities and servers. Only the master account has the unique ability to access files belonging to each facility in order to process the data further. 

**Tip**: In order to avoid broken mounts, check the status by using the mount -fav command. Broken mounts can cause issues when rebooting the server
