---
author: Brian Gadoury
title: 'SFTP virtual users with ProFTPD and Rails: Part 1'
github_issue_number: 832
tags:
- database
- mysql
- postgres
- ruby
- rails
- sysadmin
date: 2012-12-20
---



I recently worked on a Rails 3.2 project that used the sweet [PLupload](http://www.plupload.com/) JavaScript/Flash upload tool to upload files to the web app. To make it easier for users to upload large and/or remote files to the app, we also wanted to let them upload via SFTP. The catch was, our users didn't have SFTP accounts on our server and we didn't want to get into the business of creating and managing SFTP accounts. Enter: [ProFTPD](http://www.proftpd.org/) and virtual users.

[ProFTPD's virtual users](http://www.proftpd.org/docs/directives/linked/config_ref_SQLAuthenticate.html) concept allows you to point ProFTPD at a SQL database for your user and group authentication. This means SFTP logins don't need actual system logins (although you can mix and match if you want). Naturally, this is perfect for dynamically creating and destroying SFTP accounts. Give your web app the ability to create disposable SFTP credentials and automatically clean up after the user is done with them, and you have a self-maintaining system.

Starting from the inside-out, you need to configure ProFTPD to enable virtual users. Here are the relevant parts from our proftpd.conf:

```nohighlight
##
# Begin proftpd.conf excerpt. For explanation of individual config directives, see the 
# great ProFTPD docs at http://www.proftpd.org/docs/directives/configuration_full.html
##
DefaultServer off
Umask 002
AllowOverwrite on

# Don't reference /etc/ftpusers
UseFtpUsers off

<ifmodule mod_sftp.c="">

# Enable SFTP
SFTPEngine on

# Enable SQL based authentication
SQLAuthenticate on

# From http://www.proftpd.org/docs/howto/CreateHome.html
# Note that the CreateHome params are kind of touchy and easy to break.
CreateHome on 770 dirmode 770 uid ~ gid ~

# chroot them to their home directory
DefaultRoot ~

# Defines the expected format of the passwd database field contents. Hint: An
# encrypted password will look something like: {sha1}IRYEEXBUxvtZSx3j8n7hJmYR7vg=
SQLAuthTypes OpenSSL

# That '*' makes that module authoritative and prevents proftpd from
# falling through to system logins, etc
AuthOrder mod_sql.c*

# sftp_users and sftp_groups are the database tables that must be defined with
# the proceeding column names. You can have other columns in these tables and
# ProFTPD will leave them alone. The sftp_groups table can be empty, but it must exist.
SQLUserInfo sftp_users username passwd uid sftp_group_id homedir shell
SQLGroupInfo sftp_groups name id members

SFTPHostKey /etc/ssh/ssh_host_rsa_key
SFTPHostKey /etc/ssh/ssh_host_dsa_key

SFTPCompression delayed
SFTPAuthMethods password
RequireValidShell no

# SQLLogFile is very verbose, but helpful for debugging while you're getting this working
SQLLogFile /var/log/proftpd_sql.sql

## Customize these for production
SQLConnectInfo database@localhost:5432 dbuser dbpassword

# The UID and GID values here are set to match the user that runs our web app because our
# web app needs to read and delete files uploaded via SFTP. Naturally, that is outside
# the requirements of a basic virtual user setup. But in our case, our web app user needs
# to be able to cd into a virtual user's homedir, and run a `ls` in there. Also, note that
# setting these two IDs here (instead of in our sftp_users table) *only* makes sense if
# you are using the DefaultRoot directive to chroot virtual users.
SQLDefaultUID  510
SQLDefaultGID  500

</ifmodule>
```

The CreateHome piece was the trickiest to get working just right for our use-case. But there are two reasons for that; we needed our web app to be able to read/delete the uploaded files, and we wanted to make ProFTPD create those home directories itself. (And it only creates that home directory once a user successfully logs in via SFTP. That means you can be more liberal in your UI with generating credentials that may never get used without having to worry about a ton of empty home directories lying about.)

That's it for the introductory "Part 1" of this article. In Part 2, I'll show how we generate credentials, the workflow behind displaying those credentials, and our SftpUser ActiveRecord model that handles it all. In Part 3, I'll finish up by running through exactly how our web app accesses these files, and how it cleans up after it's done.


