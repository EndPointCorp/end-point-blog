---
author: Piotr Hankiewicz
title: JBoss 4/5/6 to Wildfly migration tips
github_issue_number: 1319
tags:
- java
date: 2017-07-31
---

<img border="0" data-original-height="246" data-original-width="1089" src="/blog/2017/07/jboss-456-to-wildfly-migration-tips/image-0.jpeg" style="max-width: 100%;"/>

### Introduction

Recently, we have taken over a big Java project that ran on the old **JBoss 4** stack. As we know how dangerous for a business is outdated software, we and our client agreed that the most important task is to upgrade the server stack to the latest **WildFly** version.

It’s definitely not an easy job, but it’s worth to invest to sleep well and don’t worry about software problems.

This time it was even more work because of a complicated and not documented application, that’s why I wanted to share some tips and problem resolutions for issues I encountered.

### Server configuration

You can set it up using multiple configuration files in the standalone/configuration directory.

I can recommend to use the standalone-full.xml file for most of setup, it contains a default full stack as opposed to **standalone.xml**.

You can also set up an application specific configuration using various configuration XML files ([https://docs.jboss.org/author/display/WFLY10/Deployment+Descriptors+used+In+WildFly](https://docs.jboss.org/author/display/WFLY10/Deployment+Descriptors+used+In+WildFly)). Remember to keep the application specific configuration in the Classpath.

### Quartz as a message queue

The **Quartz library** was used as a native message queue in previous JBoss versions. If you struggle and try to use its resource adapter with WildFly just skip it. It’s definitely too much work, even if it’s possible.

In the latest WildFly version (as of today 10.1) the default message queue library is **ActiveMQ**. It has almost the same API as the old Quartz has, so it’s easy to use it.

### Quartz as a job scheduler

We had multiple cron-like jobs to migrate as well. All the jobs used Quartz to schedule runs.

The best solution here is to update Quartz to the latest version (yes!) and use a new API ([http://www.quartz-scheduler.org/documentation/quartz-2.2.x/tutorials/tutorial-lesson-06.html](http://www.quartz-scheduler.org/documentation/quartz-2.2.x/tutorials/tutorial-lesson-06.html)) to create CronTriggers for the jobs.

```java
trigger = newTrigger()
    .withIdentity("trigger3", "group1")
    .withSchedule(cronSchedule("0 42 10 * * ?"))
    .forJob(myJobKey)
    .build();
```

You can use the same cron syntax (e.g 0 42 10 * * ?) as in the 12 years old Quartz version. Yes!

### JAR dependencies

In WildFly you can set up an internal module for each JAR dependency. It can be pretty time consuming to create declarations for more than 100 libraries (exactly 104 in our case). We decided to use **Maven** to handle dependencies of our application and skip declaring modules in WildFly. Why? In our opinion it’s better to encapsulate everything in an EAR file and keep WildFly configuration minimal as we won’t use our server for any other application in the future.

Just keep your dependencies in the Classpath and you will be fine.

### JBoss CLI

I really prefer the bin/jboss-cli.sh interface to the web interface to handle deployments. It’s a powerful tool and much faster to work with than clicking through the UI.

### JNDI path

If you can’t access your JNDI definition try to use the global namespace. Up to JAVA EE6 developers defined their own JNDI names. These names had a global scope. This doesn’t work anymore. To access a previously globally scoped name use this pattern: java:global/OLD_JNDI_NAME.

The java:global namespace was introduced in **JAVA EE 6**.

### Reverse proxy

To configure a WildFly application with a reverse proxy you need to, of course, set up a virtual host with a reverse proxy declaration.

In addition, you must add an attribute to the server’s http-listener in the **standalone-full.xml** file. The attribute is proxy-address-forwarding and must be set to true.

Here is an example declaration:

```xml
<subsystem xmlns="urn:jboss:domain:undertow:3.1">
    <buffer-cache name="default">
        <server name="default-server">
            <http-listener enable-http2="true" name="default" proxy-address-forwarding="true" redirect-socket="https" socket-binding="http">
 </http-listener></server>
    </buffer-cache>
</subsystem>
```

### Summary

If you consider to upgrade to WildFly I can recommend it, it’s much faster than JBoss 4/5/6, scalable and fully prepared for modern applications.
