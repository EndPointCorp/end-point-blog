---
author: Muhammad Najmi bin Ahmad Zabidi
title: 'Getting Output from jps with NRPE'
date: 2025-03-22
github_issue_number: 2102
description: How to get process information from jps using NRPE on a server
featured:
  image_url: /blog/2025/03/monitoring-java-based-process-with-jps-and-nrpe/green-river.webp
tags:
- linux
- monitoring
- nagios
- java
---

![A mellow river winds across the image, with verdant trees reaching over the water.](/blog/2025/03/monitoring-java-based-process-with-jps-and-nrpe/green-river.webp)

<!-- Photo by Seth Jensen, 2024. -->

One of the tools our hosting team uses for server and site monitoring is Icinga (which is based on Nagios). When monitoring host resources, one of the tools we use is Nagios Remote Plugin Executor or NRPE.

We encountered an issue when executing NRPE: though NRPE runs on the server being monitored, it wasn't giving the same output as a script which was executed on the server itself. The NRPE-related call should have no issues be executed on the target server, as it is declared in the sudoers file (commonly /etc/sudoers). In this post, I will explain how to get the output from jps (Java Virtual Machine Process Status Tool), which can only be executed as root.

### Getting process information with jps

Let’s say we have a "hello world" program named Hello.java. How do we get the process's state from Icinga's head server?

First, let's compile and run the program.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");

        try {
            Thread.sleep(3000);  // Sleep for 3 seconds
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

```plain
java Hello.java
Hello, World!
```

The program will run until it times out.

First, let's check the process by running `ps` on the server:

```plain
# ps aux | grep Hello.java | grep -v grep
najmi      61609 16.7  0.3 11541184 109360 pts/5 Sl+  01:19   0:00 java Hello.java
```

We can also get the process ID with jps. Here's the output from the "najmi" user view:

```plain
# sudo -s -u najmi jps -l
61609 jdk.compiler/com.sun.tools.javac.launcher.SourceLauncher
61695 jdk.jcmd/sun.tools.jps.Jps

```

And from the "root" user view:

```plain
# whoami
root
# jps -l
61609 jdk.compiler/com.sun.tools.javac.launcher.SourceLauncher
61852 jdk.jcmd/sun.tools.jps.Jps
# ps aux | grep Hello.java | grep -v grep
najmi      61609  1.2  0.3 11541184 109360 pts/5 Sl+  01:19   0:01 java Hello.java
```

However, the "nrpe" user does not see it:

```plain
# sudo -s -u nrpe jps -l
61790 jdk.jcmd/sun.tools.jps.Jps
```

Instead of running the `jps` command directly as Nagios, we will let the system run jps as root and dump the results into a file. An NRPE-based script will later read the output and feed the result to the dashboard.

### Running jps as root, with output to a file

For this example, I started the `jetty` process with sudo.

```plain
sudo /usr/share/jetty/bin/jetty.sh start
```

Now let's check whether the "jetty" service is running or not.

First we'll check the status as a non-root user. It sees the process as "not running".

```plain
$ /usr/share/jetty/bin/jetty.sh status
** WARNING: JETTY_LOGS is Deprecated. Please configure logging within the jetty base.
Jetty NOT running

JAVA                  =  /usr/bin/java
JAVA_OPTIONS          =
JETTY_HOME            =  /usr/share/jetty
JETTY_BASE            =  /usr/share/jetty
START_D               =  /usr/share/jetty/start.d
START_INI             =  /usr/share/jetty/start.ini
JETTY_START           =  /usr/share/jetty/start.jar
JETTY_CONF            =  /usr/share/jetty/etc/jetty.conf
JETTY_ARGS            =  jetty.state=/run/jetty/jetty.state jetty.pid=/run/jetty/jetty.pid --module=pid,state
JETTY_RUN             =  /run/jetty
JETTY_PID             =  /run/jetty/jetty.pid
JETTY_START_LOG       =  /run/jetty/jetty-start.log
JETTY_STATE           =  /run/jetty/jetty.state
JETTY_START_TIMEOUT   =  60
JETTY_SYS_PROPS       =
RUN_ARGS              =  -Djava.io.tmpdir=/tmp -Djetty.home=/usr/share/jetty -Djetty.base=/usr/share/jetty --class-path /etc/jetty/resources:/usr/share/jetty/lib/logging/slf4j-api-2.0.16.jar:/usr/share/jetty/lib/logging/jetty-slf4j-impl-12.0.16.jar:/usr/share/jetty/lib/jetty-http-12.0.16.jar:/usr/share/jetty/lib/jetty-server-12.0.16.jar:/usr/share/jetty/lib/jetty-xml-12.0.16.jar:/usr/share/jetty/lib/jetty-util-12.0.16.jar:/usr/share/jetty/lib/jetty-io-12.0.16.jar org.eclipse.jetty.xml.XmlConfiguration java.version=23.0.1 jetty.base=/usr/share/jetty jetty.base.uri=file:///usr/share/jetty jetty.home=/usr/share/jetty jetty.home.uri=file:///usr/share/jetty jetty.pid=/run/jetty/jetty.pid jetty.state=/run/jetty/jetty.state jetty.webapp.addHiddenClasses=org.eclipse.jetty.logging.,file:///usr/share/jetty/lib/logging/,org.slf4j. runtime.feature.alpn=true slf4j.version=2.0.16 /etc/jetty/jetty-bytebufferpool.xml /etc/jetty/jetty-pid.xml /etc/jetty/jetty-threadpool.xml /etc/jetty/jetty.xml /etc/jetty/jetty-state.xml
ID                    =  uid=1000(user) gid=1000(user) groups=1000(user),90(network),98(power),984(users),987(storage),991(lp),994(input),996(audio),998(wheel)
JETTY_USER            =  jetty
USE_START_STOP_DAEMON =  0
START_STOP_DAEMON     =  0
```

Now, let's check the status of the jetty service with `sudo`:

```plain
$ sudo /usr/share/jetty/bin/jetty.sh status
** WARNING: JETTY_LOGS is Deprecated. Please configure logging within the jetty base.
Jetty running pid=89969

JAVA                  =  /usr/bin/java
JAVA_OPTIONS          =
JETTY_HOME            =  /usr/share/jetty
JETTY_BASE            =  /usr/share/jetty
START_D               =  /usr/share/jetty/start.d
START_INI             =  /usr/share/jetty/start.ini
JETTY_START           =  /usr/share/jetty/start.jar
JETTY_CONF            =  /usr/share/jetty/etc/jetty.conf
JETTY_ARGS            =  jetty.state=/run/jetty/jetty.state jetty.pid=/run/jetty/jetty.pid --module=pid,state
JETTY_RUN             =  /run/jetty
JETTY_PID             =  /run/jetty/jetty.pid
JETTY_START_LOG       =  /run/jetty/jetty-start.log
JETTY_STATE           =  /run/jetty/jetty.state
JETTY_START_TIMEOUT   =  60
JETTY_SYS_PROPS       =
RUN_ARGS              =  -Djava.io.tmpdir=/tmp -Djetty.home=/usr/share/jetty -Djetty.base=/usr/share/jetty --class-path /etc/jetty/resources:/usr/share/jetty/lib/logging/slf4j-api-2.0.16.jar:/usr/share/jetty/lib/logging/jetty-slf4j-impl-12.0.16.jar:/usr/share/jetty/lib/jetty-http-12.0.16.jar:/usr/share/jetty/lib/jetty-server-12.0.16.jar:/usr/share/jetty/lib/jetty-xml-12.0.16.jar:/usr/share/jetty/lib/jetty-util-12.0.16.jar:/usr/share/jetty/lib/jetty-io-12.0.16.jar org.eclipse.jetty.xml.XmlConfiguration java.version=23.0.1 jetty.base=/usr/share/jetty jetty.base.uri=file:///usr/share/jetty jetty.home=/usr/share/jetty jetty.home.uri=file:///usr/share/jetty jetty.pid=/run/jetty/jetty.pid jetty.state=/run/jetty/jetty.state jetty.webapp.addHiddenClasses=org.eclipse.jetty.logging.,file:///usr/share/jetty/lib/logging/,org.slf4j. runtime.feature.alpn=true slf4j.version=2.0.16 /etc/jetty/jetty-bytebufferpool.xml /etc/jetty/jetty-pid.xml /etc/jetty/jetty-threadpool.xml /etc/jetty/jetty.xml /etc/jetty/jetty-state.xml
ID                    =  uid=0(root) gid=0(root) groups=0(root)
JETTY_USER            =  jetty
USE_START_STOP_DAEMON =  0
START_STOP_DAEMON     =  0
```

Then, check that it's running with jps as root, and note that the nrpe user still can't see the process using jps:

```plain
$ sudo /usr/share/jetty/bin/jetty.sh status 2>/dev/null | grep "running pid"
Jetty running pid=89969

$ sudo jps -l
89969 org.eclipse.jetty.xml.XmlConfiguration
91635 jdk.jcmd/sun.tools.jps.Jps

$ sudo -s -u nrpe jps -l
91711 jdk.jcmd/sun.tools.jps.Jps
```

We can decide whether to use the "jetty" service script as the process check tool, or whether to use jps. For this post, we'll focus on `jps`.

We can run jps as root in a Bash script to dump the Java process ID into a temporary file. We can then use this script as an NRPE script.

```bash
#!/bin/bash

# Check if program name was provided
if [ -z "$1" ]; then
    echo "UNKNOWN: Please specify a program name to check"
    exit 3
fi

TEMP_FILE="/tmp/java_pid.txt"

# Clear the temp file first
> $TEMP_FILE

# Run jps and save output to temp file
jps -l > $TEMP_FILE

# Check if program is in the temp file
if grep -q "$1" $TEMP_FILE; then
    PID=$(grep "$1" $TEMP_FILE | awk '{print $1}')
    echo "OK - $1 is running with PID $PID"
    exit 0
else
    echo "CRITICAL - $1 is down"
    exit 2
fi
```

### Conclusion

Most of time, using `ps` or `pgrep` will be adequate to check for running processes. This post just shows how to get the output from jps, when you need to use jps. As for checking the status of the `jetty` service, `/usr/share/jetty/bin/jetty.sh status` might be fine as well, but the process of filtering, parsing, and feeding the output to the NRPE plugin should be pretty much the same.

There could be another way to solve this issue, which I am not be aware of. The method I shared above is just one way to get jps’s report working with NRPE. Please let me know if you have experience with jps and Icinga/​Nagios, and how you handle their reporting.

### Related reading

- https://opensource.com/article/21/10/check-java-jps
- https://docs.oracle.com/javase/7/docs/technotes/tools/share/jps.html
