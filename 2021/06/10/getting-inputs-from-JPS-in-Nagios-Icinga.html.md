---
author: Muhammad Najmi Ahmad Zabidi 
title: 'Monitoring Java's Process Monitoring tool (jps) with Icinga/Nagios'
tags: linux, monitoring, nrpe, nagios, icinga 
gh_issue_number: 1655
---

### Java VM Process Status Tool, jps
`jps` is Java's Virtual Machine Process Status Tool and it could be used much like how the `ps` command works on the *Nix environment. We encountered an issue when executing NRPE, the Nagios agent that runs on servers being monitored, from Icinga's head server. Usually the NRPE-related call should not be an issue to be executed on the target server as it will be declared in the sudoers (commonly /etc/sudoers) file. In this writing, I will explain the situation when I encountered an issue to get the output from jps (Java Virtual Machine Process Status Tool), which only could be executed as the “root” user on the terminal. 

In this writings, I want to get Icinga (Nagios' fork) to get the Java process’ state (in this case, the process is the “Lucene” process) from Icinga’s head server, remotely. 

### Method
Usually, NRPE should be able to execute the remote process (on the target server) from Icinga’s head. In this case we are going to create a workaround by :
Dump the Java process ID into a text file
Dump the running threads into another text file
Put A) and B) into a single bash script
Create a cronjob to automatically update to run the shell script
Create a NRPE plugin so that it will be evaluate the results which were obtained from A) and B)

### Test

To illustrate this, I ran the intended command locally on the target server as the “nagios” user. Theoretically, this will emulate the NRPE call as if it was executed from Icinga’s server remotely. The file `check_lucene_indexing_deprecated` is a file which was meant to demonstrate the NRPE execution failure. Whereas `check_lucene_indexing` is the file which is expected to be able to run the NRPE plugin successfully. Both `check_lucene_indexing_deprecated` and `check_lucene_indexing` paths were already declared in /etc/sudoers file on the target machine 

To show the differences, I ran two different scripts from Icinga’s head server which were named check_lucene_indexing_dep and check_lucene_indexing

Script execution from the target machine locally  (first execution as the "nagios" user, the latter as the "root" user):

```.bash
#sudo -s -u nagios ./check_lucene_indexing_deprecated
CRITICAL -- Lucene indexing down

# sudo -s -u root  ./check_lucene_indexing_deprecated
OK -- 2 Lucene threads running
```

As you can see, the script works fine if I run it as root, but that is not the case as the "nagios" user.



Let's run the scripts from Icinga’s head server:

```.bash
# /usr/lib64/nagios/plugins/check_nrpe -t 5 -H <the target server’s FQDN> -c  check_lucene_indexing_dep
CRITICAL -- Lucene indexing down (0 found)

# /usr/lib64/nagios/plugins/check_nrpe -t 5 -H  <the target server’s FQDN> -c  check_lucene_indexing
OK -- 2 Lucene threads running
```

In the background, see the differences output when we run the `jps` command on the target server by using the “root” user and the “nagios” user:

Let say I want to check the `jps` process ID (PID):

```.bash
# sudo -s -u nagios jps -l
29112 sun.tools.jps.Jps

# jps -l
7541 /usr/share/jetty9/start.jar
29131 sun.tools.jps.Jps
```

As you can see, the output that is being shown by “jps” under the nagios user is different from the “root” user. 

The intention of running the `jps -l` command is to get the process ID of `/usr/share/jetty9/start.jar`, which is 7541. However as indicated above, the “nagios” user’s result did not display the result, unlike if the command being executed as the “root” user. 

### The possible workaround

We could get the process’ ID existence, by dumping the process ID inside a text file and let NRPE plugin to read it instead. 

In order to get NRPE to fetch the current state of the process, we will create a cronjob. In this case it will be executed for every 10 minutes. This script will dump the process ID of the Java process onto a text file and later NRPE will another script which will analyze the content of the text file.

#### Cronjob, creating dump files
```.bash
*/10 * * * * /root/bin/fetch_lucene_pid.sh
```

The cron script contains the following details:
 
```.bash
PID_TARGET=/var/run/nrpe-lucene.pid
THREADS_TARGET=/var/run/nrpe-lucene-thread.txt

/usr/bin/jps -l | grep "start.jar" | cut -d' ' -f1 1>$PID_TARGET 2>/dev/null

PID=$(cat $PID_TARGET)

re='^[0-9]+$'

if  [[ -z $PID ]]  || ! [[ $PID =~ $re ]]  ; then
exit 0
fi

THREADS=$(/usr/bin/jstack $PID | grep -A 2 "ProjectIndexer\|ConsultantIndexer" | grep -c "java.lang.Thread.State: WAITING (parking)")

echo $THREADS > $THREADS_TARGET
```

So instead of running the `jps` command directly as nagios, we let the system run (as root) to run jps and dump the result onto a file. NRPE-based script later will read the output and feed the result to the dashboard. 

#### NRPE plugin file, reading values generated from the cronjob

So we will take a look at what was written in the successfully executed Bash script, that is `check_lucene_indexing`.

The NRPE plugin file, `check_lucene_indexing` contains the following script:

```.bash
#!/bin/bash 

PID_TARGET=/var/run/nrpe-lucene.pid
THREADS_TARGET=/var/run/nrpe-lucene-thread.txt

PID=$(cat $PID_TARGET)
THREADS=$(cat $THREADS_TARGET)

re='^[0-9]+$'

if  [[ -z $PID ]]  || ! [[ $PID =~ $re ]]  ; then
  echo "CRITICAL -- Lucene indexing down (a)"
  exit 2
fi


if [ $THREADS -eq 2 ]
then
  echo "OK -- $THREADS Lucene threads running"
  exit 0
else
  echo "CRITICAL -- Lucene indexing down (b)"
  exit 2
fi
```

From the NRPE plugin script you can see that the following text files being used:

```.bash
PID_TARGET=/var/run/nrpe-lucene.pid
THREADS_TARGET=/var/run/nrpe-lucene-thread.txt
```

`PID_TARGET` variable contains the process’ PID in which I used to determine whether the process ID of the intended program is running or not.

`THREADS_TARGET` variable contains the number of the Java threads which are currently running.


The following is the content of `check_lucene_indexing_deprecated` script :

```.bash
#!/bin/bash 

PID=$(/usr/bin/jps -l | grep "start.jar" | cut -d' ' -f1)

if [[ -z $PID ]]; then
  echo "CRITICAL -- Lucene indexing down"
  exit 2
fi

THREADS=$(/usr/bin/jstack $PID | grep -A 2 "ProjectIndexer\|ConsultantIndexer" | grep -c "java.lang.Thread.State: WAITING (parking)")

if [ $THREADS -eq 2 ]
then
  echo "OK -- $THREADS Lucene threads running"
  exit 0
else
  echo "CRITICAL -- Lucene indexing down"
  exit 2
fi
```

As you can see previously, `check_lucene_deprecated` was able to get the result *if* it is being executed locally on the target machine - but not from remote (Icinga's head server).
This is due to `jps` will provide limited result if it was being executed as the "nagios" user as compared to the local root user. Note that I have define the path of the script in the sudoers file prior to the script execution.

```
Defaults: nagios !requiretty
nagios  ALL = NOPASSWD: /usr/local/lib/nagios/plugins/check_lucene_indexing
nagios  ALL = NOPASSWD: /usr/local/lib/nagios/plugins/check_lucene_indexing_deprecated
```

## Conclusion

There could be another way to solve this issue (which I might not be aware of). As of now this script works as expected - and if you want to reuse the script - please customize the script according to your environment so that you will be able to get the expected result that you want. Also, as being written in jps’ documentation - getting the output by parsing from jps’ output means we need to maintain the script given the new version of jps changed its output. The method which I shared above is just one of the ways to get jps’ report works with Icinga/Nagios plugin. Please let me know if you have experience with jps and Icinga/Nagios - and how do you handle the reporting. 



Related readings:

* [Java JPS commands under Linux are parsed in detail](https://developpaper.com/java-jps-commands-under-linux-are-parsed-in-detail/)

* [jps - Java Virtual Machine Process Status Tool](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jps.html)







