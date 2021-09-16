---
author: Muhammad Najmi bin Ahmad Zabidi
title: Fetching Outputs From Java Process Monitoring Tool with Icinga/​Nagios
github_issue_number: 1753
tags:
- linux
- monitoring
- nagios
date: 2021-06-07
---

![](/blog/2021/06/getting-inputs-from-jps-in-nagios-icinga/banner.jpg)
Photo by [Mihai Lupascu](https://unsplash.com/@mlupascu) on [Unsplash](https://unsplash.com/photos/epLSTrZ9aOE)

Recently, I encountered an issue when executing [NRPE](https://exchange.nagios.org/directory/Addons/Monitoring-Agents/NRPE--2D-Nagios-Remote-Plugin-Executor/details), a Nagios agent which runs on servers that are being monitored from Icinga’s head server. Usually NRPE-related calls should run without issues on the target server, since it is declared in the sudoers file (commonly `/etc/sudoers`). In this post, I will cover an issue I encountered getting the output from [jps](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jps.html) (Java Virtual Machine Process Status Tool), which needed to be executed with root privileges.

### Method

I wanted to use [Icinga](https://icinga.com/) to get a Java process’s state (in this case, the process is named “Lucene”) from Icinga’s head server, remotely. `jps` works for this, functioning similarly to the `ps` command on Unix-like systems.

Usually, NRPE should be able to execute the remote process (on the target server) from Icinga’s head. In this case we are going to create a workaround through the following steps:

1. Dump the Java process ID into a text file.
2. Dump the running threads into another text file.
3. Put **item 1** and **item 2** above into a single bash script.
4. Create a cronjob to automatically run the bash script.
5. Create an NRPE plugin to evaluate the output of **item 1** and **item 2**.

### Test

To illustrate this, I ran the intended command locally on the target server as the nagios user. Theoretically, this should emulate the NRPE call as if it was executed from Icinga’s server remotely. The file `check_lucene_indexing_deprecated` was meant to demonstrate the NRPE execution failure, whereas `check_lucene_indexing` is the file which is expected to run the NRPE plugin successfully. The paths to both `check_lucene_indexing_deprecated` and `check_lucene_indexing` were already declared in `/etc/sudoers` file on the target machine.

To show the differences, I ran two different scripts from the Icinga’s head server.

Here is the output from both local script executions: first as the nagios user, then as the root user:

```bash
# sudo -s -u nagios ./check_lucene_indexing_deprecated
CRITICAL -- Lucene indexing down

# sudo -s -u root  ./check_lucene_indexing_deprecated
OK -- 2 Lucene threads running
```

As you can see, the script worked fine running as root, but not as the nagios user.

Let’s run the scripts from Icinga’s head server:

```bash
# /usr/lib64/nagios/plugins/check_nrpe -t 5 -H <the target server’s FQDN> -c  check_lucene_indexing_dep
CRITICAL -- Lucene indexing down (0 found)

# /usr/lib64/nagios/plugins/check_nrpe -t 5 -H  <the target server’s FQDN> -c  check_lucene_indexing
OK -- 2 Lucene threads running
```

In the background, we can see different output from running `jps` on the target server using the root user compared to the nagios user. Let’s say I want to check the `jps` process ID (PID):

```bash
# sudo -s -u nagios jps -l
29112 sun.tools.jps.Jps
```

And as root:

```bash
# jps -l
7541 /usr/share/jetty9/start.jar
29131 sun.tools.jps.Jps
```

The point of running the `jps -l` command is to get the process ID of `/usr/share/jetty9/start.jar`, which is 7541. However, as indicated above, the nagios user’s execution did not display the intended result, but the root user’s did.

### The workaround

We can check the existence of the process ID by dumping it into a text file and letting the NRPE plugin read it instead.

In order to get NRPE to fetch the current state of the process, we will create a cronjob; in our case it will be executed every 10 minutes. This script will dump the PID of the Java process into a text file and later NRPE will run another script which will analyze the contents of the text file.

#### Cronjob, creating dump files

```bash
*/10 * * * * /root/bin/fetch_lucene_pid.sh
```

The cron script contains the following details:

```bash
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

So instead of running the `jps` command directly as nagios, we let the system run `jps` (as root) and dump the result into a file. Our NRPE-based script will read the output later and feed the result to the dashboard.

#### NRPE plugin file, reading values generated from the cronjob

So we will take a look at what was written in the successfully executed Bash script (that is, `check_lucene_indexing`).

The NRPE plugin file, `check_lucene_indexing`, contains the following script:

```bash
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

From the NRPE plugin script you can see the following text files being used:

```bash
PID_TARGET=/var/run/nrpe-lucene.pid
THREADS_TARGET=/var/run/nrpe-lucene-thread.txt
```

`PID_TARGET` contains the process’s PID, which I used to determine whether the intended process is running or not.

`THREADS_TARGET` contains the number of the Java threads which are currently running.

The following is the content of the `check_lucene_indexing_deprecated` script:

```bash
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

As you can see, `check_lucene_deprecated` was able to get the result *if* it is being executed locally on the target machine - but not from the remote (Icinga’s head server). This is because `jps` will provide limited results when executed as the nagios compared to the local root user. Note that I have defined the path of the script in the sudoers file prior to the script execution.

```nohighlight
Defaults: nagios !requiretty
nagios  ALL = NOPASSWD: /usr/local/lib/nagios/plugins/check_lucene_indexing
nagios  ALL = NOPASSWD: /usr/local/lib/nagios/plugins/check_lucene_indexing_deprecated
```

### Conclusion

The method which I shared above is just one of the ways to use jps reports with Icinga/​Nagios plugins. As of now this solution works as expected. If you want to reuse the scripts, please customize them according to your environment to get the results you want. Also, as written in the [documentation](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jps.html), getting the output by parsing the output from jps means we need to update the script any time jps changes its output format.

Please comment below if you have experience with jps and Icinga/​Nagios, and tell us how you handle the reporting.

Related reading:

* [Java JPS commands under Linux are parsed in detail](https://developpaper.com/java-jps-commands-under-linux-are-parsed-in-detail/)
* [jps - Java Virtual Machine Process Status Tool](https://docs.oracle.com/javase/7/docs/technotes/tools/share/jps.html)
