---
author: Muhammad Najmi bin Ahmad Zabidi 
title: 'Getting output from JPS with NRPE'
tags: 
- linux
- monitoring
- nrpe
- nagios
- icinga
- java 
gh_issue_number: 1655
---

### Nagios and NRPE
The hosting team’s routine typically involves the server’s and site monitoring task. One of the tools that is being used for monitoring is Icinga (which is based on Nagios). When monitoring the host resources, one of the tools that we could use is Nagios Remote Plugin Executor or NRPE. 

We encountered an issue when executing NRPE, the Nagios agent that runs on servers being monitored didn’t give the expected output which is similar compared to when the script was executed on the server itself. Usually the NRPE-related call should not be an issue to be executed on the target server as it will be declared in the sudoers (commonly /etc/sudoers) file. In this writing, I will explain the situation when I encountered an issue to get the output from jps (Java Virtual Machine Process Status Tool), which only could be executed as the “root” user on the terminal. 

### Examples
To get the process’ state (in this case, the process is the “Hello World” process) from Icinga’s head server. 

Let’s say we have a small program with the name of Hello.java

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


Run the program after we compile it
```plain
java Hello.java 
Hello, World!
``` 
(the program will stick around on the terminal until the time out)

Checking the process with `ps`
```plain
# ps aux|grep Hello.java|grep -v grep
najmi      61609 16.7  0.3 11541184 109360 pts/5 Sl+  01:19   0:00 java Hello.java
```
Checking with jps will show the process ID
From "najmi" user view:
```plain
# sudo -s -u najmi jps -l
61609 jdk.compiler/com.sun.tools.javac.launcher.SourceLauncher
61695 jdk.jcmd/sun.tools.jps.Jps

```
From "root" user view:
```plain
# whoami
root
# jps -l
61609 jdk.compiler/com.sun.tools.javac.launcher.SourceLauncher
61852 jdk.jcmd/sun.tools.jps.Jps
# ps aux|grep Hello.java|grep -v grep
najmi      61609  1.2  0.3 11541184 109360 pts/5 Sl+  01:19   0:01 java Hello.java
```

However, the nrpe user does not see it:
```plain
# sudo -s -u nrpe jps -l
61790 jdk.jcmd/sun.tools.jps.Jps
```

So instead of running the `jps` command directly as Nagios, we let the system run (as root) to run jps and dump the result onto a file. NRPE-based script later will read the output and feed the result to the dashboard.

Ok, now let us consider this case. We are going to check whether "jetty" service is running or not.

I started `jetty` with sudo

```plain
sudo /usr/share/jetty/bin/jetty.sh start
```

Check the status as the normal user. It sees the process as "not running".

```plain
  {  home }  /usr/share/jetty/bin/jetty.sh status
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

Let us check the jetty service status with `sudo`
```
  user on Tuesday at 10:53 AM                                                                                            0.372s  CPU: 17.01%  RAM: 32/33GB 
  {  home }  sudo /usr/share/jetty/bin/jetty.sh status
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

Then, we are going validate it:

```plain
$ sudo /usr/share/jetty/bin/jetty.sh status 2>/dev/null|grep "running pid"
Jetty running pid=89969

$ sudo jps -l
89969 org.eclipse.jetty.xml.XmlConfiguration
91635 jdk.jcmd/sun.tools.jps.Jps

$ sudo -s -u nrpe jps -l
91711 jdk.jcmd/sun.tools.jps.Jps
```
For now, we can opt whether to use "jetty" service script as the process check tool or we could use jps. For this writing's purpose, let us focus on `jps`.

Consider the following example of a bash script, which will dump the Java process ID inside a temporary file. We can use this script to be invoked as an NRPE script.
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
The given example could be adapted with your use case.

### Conclusion

This write up is just an example when we need to get the output from `jps`. Most of time,`ps` or `pgrep` command might be adequate. As for the `jetty` service status above, the usage of `/usr/share/jetty/bin/jetty.sh status` might be fine as well, but still the subsequent process of filtering/parsing and feed the info to the NRPE plugin seems pretty much the same.

There could be another way to solve this issue (which I might not be aware of). The method which I shared above is just one of the ways to get jps’ report works with Icinga/Nagios plugin. Please let me know if you have experience with jps and Icinga/Nagios - and how do you handle the reporting. 



Related readings:

https://opensource.com/article/21/10/check-java-jps

https://docs.oracle.com/javase/7/docs/technotes/tools/share/jps.html
