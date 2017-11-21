---
author: "Piotr Hankiewicz"
tags: java
title: "Hot-deploy Java classes and assets in Wildfly 8/9/10"
gh_issue_number: 1333
---

<img border="0" src="/blog/2017/10/27/hot-deploy-java-classes-and-assets-in/image-0.jpg" style="width: 100%; max-width: 100%;" />

## Introduction

Java development can be really frustrating when you need to re-build your project and restart a server every time you change something. I know about JRebel, but while it’s a good tool, it’s also pretty expensive. You can use the open-source version, but then you need to send project statistics to the JRebel server, which is not a viable option for your more serious projects.

Fortunately, there is an open-source project called HotSwapAgent and it does the same thing as JRebel, for free (thank you, guys!).

I will explain how to combine it with Widlfly in order to hot-deploy Java classes as well as how to hot-deploy other resources (Javascript, CSS, images).

## Wildfly configuration

Let’s assume that we use the `standalone-full.xml` configuration file.

We need to use exploded deployment instead of deploying WAR or EAR. You can do this in production as well to allow for application changes with zero downtime.

Start by configuring the metaspace size; we had to increase defaults for our application, but it’s possible that it will be just fine in your case. It’s encouraged that you play with these values after completing all steps.

In:

`WILDFLY_DIR/bin/standalone.conf`

set:

`-XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=512m`

so it looks like this:

`JAVA_OPTS="-Xms512m -Xmx1024m -XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=512m"`.

Now, look for the `deployment-scanner` node in:

`WILDFLY_DIR/standalone/configuration/standalone-full.xml`

Replace it so it looks like this:

`<deployment-scanner path="PATH_TO_DEPLOYMENT_DIR" relative-to="RELATIVE_TO_PATH" scan-enabled="true" scan-interval="2000" auto-deploy-exploded="false" runtime-failure-causes-rollback="${jboss.deployment.scanner.rollback.on.failure:false}"/>`

Note:

`PATH_TO_DEPLOYMENT_DIR` is `WILDFLY_DIR/standalone/deployments`

`RELATIVE_TO_PATH` is, as the name suggests the dir that the `PATH_TO_DEPLOYMENT_DIR` is relative to.

## HotSwapAgent installation and configuration

We need to download and install the latest release of DCEVM Java patch from here: [https://github.com/dcevm/dcevm/releases](https://github.com/dcevm/dcevm/releases). Why it’s needed? It will allow us unlimited redefinition of loaded classes at runtime. This is not possible with the original Java HotSpot VM. Make sure you update to the same Java version that you’re going to use to run the Wildfly server.

Now, download the latest release of the Hotswap agent from here:

[https://github.com/HotswapProjects/HotswapAgent/releases](https://github.com/HotswapProjects/HotswapAgent/releases)

The only thing that you need to do is get the JAR and put it anywhere on your hard drive (I recommend to add it to your Java project).

Ok, great, now just some configuration.

Open:

`WILDFLY_DIR/bin/standalone.conf`

and add new Java opts:

`-XXaltjvm=dcevm -javaagent:PATH_TO_HOTSWAPAGENT_JAR`.

What does this do?

- The `altjvm` option sets an alternative Java Virtual Machine.
- The `javagent` is just an interceptor on the top of your classes that allows the HotSwapAgent library to manipulate your code on the fly.

That’s all you need. It’s a good idea to create a configuration file for the HotSwapAgent. This is well explained here:

[http://hotswapagent.org/mydoc_configuration.html](http://hotswapagent.org/mydoc_configuration.html)

Basically create a new file, name it hotswap-agent.properties, set all needed configuration inside and add it to the classpath of the application.

If you use Netbeans, Eclipse or Intellij you should check the HotSwapAgent page for some helpful plugins here: [http://hotswapagent.org/mydoc_setup_intellij_idea.html](http://hotswapagent.org/mydoc_setup_intellij_idea.html), [http://hotswapagent.org/mydoc_setup_eclipse.html](http://hotswapagent.org/mydoc_setup_eclipse.html), and [http://hotswapagent.org/mydoc_setup_netbeans.html](http://hotswapagent.org/mydoc_setup_netbeans.html).

## Application configuration

Now that we have everything in place, I will explain how to put it all together.
I doesn’t really matter which build-tool you use (Ant, Gradle or Maven). The process should look like this (you can do it in many ways, in our case, it’s pretty specific as our build process is really complicated):

1. Build your application and deploy it to the `PATH_TO_DEPLOYMENT_DIR` in the exploded version,
2. Create a script that will look for changes in the application directory (this one is interesting: [https://gist.github.com/peter-hank/3ecf7fc285ba4b9c50cf8cace1badaf4]()),
3. On change, trigger a job that will:
    1. Copy all resources like JSP, JavaScript, CSS and copy to the `PATH_TO_DEPLOYMENT_DIR`,
    2. Compile classes and copy them to the `PATH_TO_DEPLOYMENT_DIR`.

That’s it, after you replace files in the `PATH_TO_DEPLOYMENT_DIR` HotSwapAgent and Wildfly will do the rest really fast. We have a ton of assets and classes and the whole process takes only a few seconds!

## Summary

I feel this process is really worth doing. It doesn’t take a lot of time to configure everything and saves a lot of manual work. Just multiply the number of manual deployments and the number of developers in your team and you understand how much time you lose everyday without hot-deployment.

From now on, focus on development, forget about deployment!

Lastly, good luck!
