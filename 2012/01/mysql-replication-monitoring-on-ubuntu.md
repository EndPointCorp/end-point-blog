---
author: Brian Buchalter
title: MySQL replication monitoring on Ubuntu 10.04 with Nagios and NRPE
github_issue_number: 545
tags:
- hosting
- monitoring
- mysql
- ubuntu
date: 2012-01-21
---



If you're using MySQL replication, then you're probably counting on it for some fairly important need.  Monitoring via something like Nagios is generally considered a best practice.  This article assumes you've already got your Nagios server setup and your intention is to add a Ubuntu 10.04 NRPE client.  This article also assumes the Ubuntu 10.04 NRPE client is your MySQL replication master, not the slave.  The OS of the slave does not matter.

### Getting the Nagios NRPE client setup on Ubuntu 10.04

At first it wasn't clear what packages would be appropriate packages to install.  I was initially misled by the naming of the nrpe package, but I found the correct packages to be:

```nohighlight
sudo apt-get install nagios-nrpe-server nagios-plugins
```

The NRPE configuration is stored in /etc/nagios/nrpe.cfg, while the plugins are installed in /usr/lib/nagios/plugins/ (or lib64).  The installation of this package will also create a user nagios which does not have login permissions.  After the packages are installed the first step is to make sure that /etc/nagios/nrpe.cfg has some basic configuration.

Make sure you note the server port (defaults to 5666) and open it on any firewalls you have running.  (I got hung up because I forgot I have both a software and hardware firewall running!)  Also make sure the server_address directive is commented out; you wouldn't want to only listen locally in this situation.  I recommend limiting incoming hosts by using your firewall of choice.

### Choosing what NRPE commands you want to support

Further down in the configuration, you'll see lines like command[check_users]=/usr/lib/nagios/plugins/check_users -w 5 -c 10.  These are the commands you plan to offer the Nagios server to monitor.  Review the contents of /usr/lib/nagios/plugins/ to see what's available and feel free to add what you feel is appropriate.  Well designed plugins should give you a usage if you execute them from the command line.  Otherwise, you may need to open your favorite editor and dig in!

After verifying you've got your NRPE configuration completed and made sure to open the appropriate ports on your firewall(s), let's restart the NRPE service:

```nohighlight
service nagios-nrpe-server restart
```

This would also be an appropriate time to confirm that the nagios-nrpe-server service is configured to start on boot.  I prefer the chkconfig package to help with this task, so if you don't already have it installed:

```nohighlight
sudo apt-get install chkconfig
chkconfig | grep nrpe

# You should see...
nagios-nrpe-server     on

# If you don't...
chkconfig nagios-nrpe-server on
```

### Pre flight check - running check_nrpe

Before going any further, log into your Nagios server and run check_nrpe and make sure you can execute at least one of the commands you chose to support in nrpe.cfg.  This way, if there are any issues, it is obvious now, while we've not started modifying your Nagios server configuration.  The location of your check_nrpe binary may vary, but the syntax is the same:

```nohighlight
check_nrpe -H host_of_new_nrpe_client -c command_name
```

If your command output something useful and expected, your on the right track.  A common error you might see: Connection refused by host.  Here's a quick checklist:

- Did you start the nagios-nrpe-server service?
- Run netstat -lunt on the NRPE client to make sure the service is listening on the right address and ports.
- Did you open the appropriate ports on all your firewall(s)?
- Is there NAT translation which needs configuration?

### Adding the check_mysql_replication plugin

There is a lot of noise out there on Google for Nagios plugins which offer MySQL replication monitoring.  I wrote the following one using ideas pulled from several existing plugins.  It is designed to run on the MySQL master server, check the master's log position and then compare it to the slave's log position.  If there is a difference in position, the alert is considered Critical.  Additionally, it checks the slave's reported status, and if it is not "Waiting for master to send event", the alert is also considered critical.  You can find the source for the plugin at my Github account under the project [check_mysql_replication](https://github.com/bbuchalter/check_mysql_replication/blob/master/check_mysql_replication.sh).  Pull that source down into your plugins directory (/usr/lib/nagios/plugins/ (or lib64)) and make sure the permissions match the other plugins.

With the plugin now in place, add a command to your nrpe.cfg.

```nohighlight
command[check_mysql_replication]=sudo /usr/lib/nagios/plugins/check_mysql_replication.sh -H <slave_host_address></slave_host_address>
```

At this point you may be saying, WAIT!  How will the user running this command (nagios) have login credentials to the MySQL server?  Thankfully we can create a home directory for that nagios user, and add a .my.cnf configuration with the appropriate credentials.

```nohighlight
usermod -d /home/nagios nagios #set home directory
mkdir /home/nagios
chmod 755 /home/nagios
chown nagios:nagios /home/nagios

# create /home/nagios/.my.cnf with your preferred editor with the following:
[client]
user=example_replication_username
password=replication_password

chmod 600 /home/nagios/.my.cnf
chown nagios:nagios /home/nagios/.my.cnf
```

This would again be an appropriate place to run a pre flight check and run the check_nrpe from your Nagios server to make sure this configuration works as expected.  But first we need to add this command to the sudoer's file.

```nohighlight
nagios ALL= NOPASSWD: /usr/lib/nagios/plugins/check_mysql_replication.sh
```

### Wrapping Up

At this point, you should run another check_nrpe command from your server and see the replication monitoring report.  If not, go back and check these steps carefully.  There are lots of gotchas and permissions and file ownership are easily overlooked.  With this in place, just add the NRPE client using the existing templates you have for your Nagios servers and make sure the monitoring is reporting as expected.


