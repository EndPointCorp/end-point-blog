---
author: "Kannan Ponnusamy"
title: "Introduction to BorgBackup"
tags: linux, sysadmin, backups
---
![black and silver hard disk drive photo](/blog/2020/09/09/introduction-to-borg-backup/image-1.jpg)
[Photo](https://unsplash.com/photos/ShHkXuZdpTw) by [Frank R](https://unsplash.com/@frank041985)

### What is Borg?
BorgBackup (also referred to as: Borg) is a ‘deduplicating’ backup program that eliminates duplicate or redundant information. Optionally, it can also support compression and authenticated encryption. 

The main objective of Borg is to provide an efficient and secure way to backup data. The deduplication technique utilized to produce the backup process is very quick and effective. 

#### Step 1 - How to install the Borg backups
On Ubuntu:

`apt install borgbackup`

On Fedora/RHEL:

`dnf install borgbackup`

#### Step 2 - Initialize Local Borg repository
Firstly, the system that is going to be backed up needs a new designated backup directory. Name the parent directory ‘backup’ and then create a child directory called ‘borgdemo’, which serves as the repository.

`mkdir -p /mnt/backup/`
`borg init --encryption=repokey /mnt/backup/borgdemo`

#### Step 3 - Let’s create the first backup (archive)
In Borg terms, each backup instance will be called as an archive. 
The following demonstrates how to backup the ‘photos’ directory and designate the archive as ‘archive_1’

`borg create —stats —progress /mnt/backup/borgdemo::archive_1 /home/kannan/photos`

**Note: the archive label for each backup run needs to be specified. 

#### Step 4 - Next backup (Incremental)
In order to see if the run was successful, the same command will be executed again. However, this time, with the different unique archive label.

`borg create —stats —progress /mnt/backup/borgdemo::archive_2 /home/kannan/photos`

The following backup is noticeably identical to the previous one. Because of deduplication, the process will not only run faster this time, it will be incremental as well. 

Executing `—stats`  will provide statistics regarding the size of deduplication

#### Step 5 - List all the archives
The ‘Borg list’ command lists all of the archives stored within the Borg repository

`borg list /mnt/backup/borgdemo`

#### Step 6 - Remote Borg Repository
Take the scenario where the backups of many servers need to be maintained in a separate server. In this instance, a directory needs to be created for each of the systems that will be backed up. For this backup repository, create a folder named ‘backup’, and then within ‘Backup,’ a folder called ‘linode_01.’ This folder will be initialized as a Borg repository. 

`/mnt/backup/linode_01` - Server name is ‘linode_01’

`borg init —encryption=repokey user@backup_server:/mnt/backup/linode_01`

Note: the username, backup_server, repo can all be customized at the user’s discretion. 

While initialising the repo, a passphrase for each backup repository can be set for authentication.

#### Step 7 - Create an initial backup to the remote Borg repository
`borg create --stats ssh://user@backup_server/mnt/backup/linode_01::archive_1 /home/kannan/photos`

To enable the remote backups, the following three environment variables can be used to simplify the automation process:
- export BORG_REPO=‘ssh://user@backup_server/mnt/backup/linode_01’
- export BORG_PASSPHRASE=‘set_your_passpharase’
- export BORG_RSH=’ssh -I /home/kannan/.ssh/id_rsa_backups’

With these env variables activated, the ‘borg create’ command will be shortened and will resemble the following:

`borg create --stats ::archive_1 /home/kannan/photos`

#### Step 8 - How are certain directories or files excluded? 
In order to exclude certain directories or files, the create command has an —exclude option or an exclude file/directory pattern can be generated. For example, the following command demonstrates how to exclude `/dev and /opt`:

`borg create --stats ::archive_1 / --exclude /dev /opt`

#### Step 9 - How to restore an archive through extraction.
The ‘Borg extract’ command extracts the contents of an archive. As a preset default, the entire archive will be extracted. However, the extraction can be limited by passing the directory path or file path as arguments to the command. For example, this is how a single photo can be extracted from the Photos archive:

`borg extract ::archive_1 /home/kannan/photos/sunrise.jpg`

#### Step 10 - How to prune older backups?
Every backup solution should have a way to maintain the older backups. For that, borg utilizes ‘borg prune’. This command prunes a repository by deleting all archives not matching any of the specified retention options. 

For example, to retain the following specified backups: the final 10 archives from the day, another 6 end of week archives, and 3 of the end of month archive for every month can be attained using the following syntax: 

`borg prune -v —list —keep-daily=10 —keep-weekly=6 —keep-monthly=3 ::`

Note: The double ellipsis (::) is required in order to automatically utilize the environment variables that were set prior for further processing. 

For more in-depth documentation on the borgbackup process: https://borgbackup.readthedocs.io/en/stable/quickstart.html



