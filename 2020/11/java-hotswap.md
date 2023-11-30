---
author: Josh Tolley
title: Demonstrating the HotSwap JVM
github_issue_number: 1693
tags:
- development
- java
- tools
- programming
date: 2020-11-25
---

![zebras](/blog/2020/11/java-hotswap/zebras-scale-crush.jpg)

[Photo](https://unsplash.com/photos/dgH8NSdEDv0) by [Neil and Zulma Scott](https://unsplash.com/@valenciascott)

For a recent Java development project I spent a while setting up an environment to take advantage of the HotSwap JVM, a Java virtual machine that automatically reloads classes when they change. This feature can potentially eliminate the need to redeploy each time code changes, reducing development cycle time considerably. While setting up the environment, I found I wanted a simple example of hot swapping available for my own experimentation, and I thought I’d share that example here.

First, let’s create a simple Java program. It needs to be slightly more complex than the ubiquitous “Hello, World!” application, because we need it to keep running for a while; if it just prints some message and exits immediately, we won’t have time to compile new code and see the hot swap feature in action.  Here’s an example that uses a simple infinite loop, wherein it sleeps for one second, prints a message, and then repeats.

```java
import java.lang.Thread;

public class HotSwapTest {
  public static void main(String[] args) {
    while (true) {
      try {
        System.out.println("Hi");
        Thread.sleep(1000);
      } catch (InterruptedException e) {
        // Ignore this
      }
    }
  }
}
~
```

If I build this into build/​classes/​java/​main and run it, as expected it prints out “Hi” every second:

```plain
josh@igtre:~/hotswaptest$ java -cp build/classes/java/main/ HotSwapTest
Hi
Hi
Hi
...
```

The usual JVM doesn’t include the HotSwap feature. For my purposes I downloaded [DCEVM](https://dcevm.github.io/), an alternative JVM which includes HotSwap. It’s also possible to patch some existing JVMs to add HotSwap, if you’d prefer. When I run the same code with DCEVM, it runs the code just like it did with the normal JVM, with additional debugging output:

```plain
Starting HotswapAgent '/home/josh/hotswaptest/dcevm/lib/hotswap/hotswap-agent.jar'
HOTSWAP AGENT: 15:01:23.423 INFO (org.hotswap.agent.HotswapAgent) - Loading Hotswap agent {1.4.1} - unlimited runtime class redefinition.
HOTSWAP AGENT: 15:01:24.189 INFO (org.hotswap.agent.config.PluginRegistry) - Discovered plugins: [JdkPlugin, Hotswapper, WatchResources, ClassInitPlugin, AnonymousClassPatch, Hibernate, Hibernate3JPA, Hibernate3, Spring, Jersey1, Jersey2, Jetty, Tomcat, ZK, Logback, Log4j2, MyFaces, Mojarra, Omnifaces, ELResolver, WildFlyELResolver, OsgiEquinox, Owb, Proxy, WebObjects, Weld, JBossModules, ResteasyRegistry, Deltaspike, GlassFish, Vaadin, Wicket, CxfJAXRS, FreeMarker, Undertow, MyBatis]
```

To make hot swapping work automatically, we need to provide the JVM with a properties file in the JVM’s classpath. Mine looks like this, and lives in build/​classes/​java/​main, next to the compiled class files:

```plain
autoHotswap=true
LOGGER=debug
```

These properties are pretty self-explanatory: they tell the JVM to hot swap automatically when it finds new code, and turn up logging to DEBUG level.

So, with that all set up, let’s run the program again, change the code and rebuild it, and see what happens. For this test, I’ll just edit the message printed in each loop from “Hi” to “Hello”.

```plain
josh@igtre:~/hotswaptest$ ./dcevm/bin/java -cp build/classes/java/main/ HotSwapTest
Starting HotswapAgent '/home/josh/hotswaptest/dcevm/lib/hotswap/hotswap-agent.jar'
HOTSWAP AGENT: 15:36:22.132 INFO (org.hotswap.agent.HotswapAgent) - Loading Hotswap agent {1.4.1} - unlimited runtime class redefinition.
HOTSWAP AGENT: 15:36:22.543 DEBUG (org.hotswap.agent.annotation.handler.OnClassLoadedHandler) - Init for method public static void org.hotswap.agent.plugin.jdk.JdkPlugin.flushIntrospectClassInfoCache(java.lang.ClassLoader,org.hotswap.agent.javassist.CtClass)
HOTSWAP AGENT: 15:36:22.546 DEBUG (org.hotswap.agent.util.HotswapTransformer) - Registering transformer for class regexp '.*'.
HOTSWAP AGENT: 15:36:22.549 DEBUG (org.hotswap.agent.annotation.handler.OnClassLoadedHandler) - Init for method public static void org.hotswap.agent.plugin.jdk.JdkPlugin.flushObjectStreamCaches(java.lang.ClassLoader,org.hotswap.agent.javassist.CtClass)
HOTSWAP AGENT: 15:36:22.550 DEBUG (org.hotswap.agent.util.HotswapTransformer) - Registering transformer for class regexp '.*'.
...
```

The flurry of DEBUG messages tells me that it must have read my properties file correctly, and when I change the code and rebuild, I see the JVM respond with still more debug messages, saying it found and reloaded my code:

```plain
HOTSWAP AGENT: 15:38:27.066 DEBUG (org.hotswap.agent.watch.nio.WatcherNIO2) - Watch event 'ENTRY_DELETE' on '/home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class' --> HotSwapTest.class
HOTSWAP AGENT: 15:38:27.118 DEBUG (org.hotswap.agent.watch.nio.WatcherNIO2) - Watch event 'ENTRY_CREATE' on '/home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class' --> HotSwapTest.class
HOTSWAP AGENT: 15:38:27.119 DEBUG (org.hotswap.agent.watch.nio.WatcherNIO2) - Watch event 'ENTRY_MODIFY' on '/home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class' --> HotSwapTest.class
HOTSWAP AGENT: 15:38:27.280 DEBUG (org.hotswap.agent.annotation.handler.WatchEventCommand) - Executing resource changed method watchReload on class org.hotswap.agent.plugin.hotswapper.HotswapperPlugin for event WatchFileEvent on path /home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class for event ENTRY_MODIFY
...
HOTSWAP AGENT: 15:38:27.439 DEBUG (org.hotswap.agent.plugin.jdk.JdkPlugin) - Flushing HotSwapTest from introspector
Hi
HOTSWAP AGENT: 15:38:27.482 DEBUG (org.hotswap.agent.config.PluginManager) - ... reloaded classes [HotSwapTest] (autoHotswap)
Hi
Hi
Hi
```

But although it says it swapped in the new code successfully, it’s still printing “Hi”, not “Hello”. Why?

It turns out this ability to hot swap new code isn’t unlimited, and one important limitation is that methods you’re already running aren’t reloaded. Since the `main()` method was running, it didn’t get swapped out. What if I change the code so that instead of printing a string every second, it calls a method, and that method prints the string? Here’s some code to test that technique.

```java
import java.lang.Thread;

public class HotSwapTest {
  public static void printMsg() {
    System.out.println("Here is printMsg");
  }

  public static void main(String[] args) {
    while (true) {
      try {
        HotSwapTest.printMsg();
        Thread.sleep(1000);
      } catch (InterruptedException e) {
        // Ignore this
      }
    }
  }
}
```

Now, I start the JVM over again, and as expected, it prints “Here is printMsg” once every second. When I change to “Here is printMsg v2.0” and rebuild, this happens:

```plain
Here is printMsg
Here is printMsg
HOTSWAP AGENT: 15:48:34.923 DEBUG (org.hotswap.agent.watch.nio.WatcherNIO2) - Watch event 'ENTRY_DELETE' on '/home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class' --> HotSwapTest.class
HOTSWAP AGENT: 15:48:35.007 DEBUG (org.hotswap.agent.watch.nio.WatcherNIO2) - Watch event 'ENTRY_CREATE' on '/home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class' --> HotSwapTest.class
HOTSWAP AGENT: 15:48:35.008 DEBUG (org.hotswap.agent.watch.nio.WatcherNIO2) - Watch event 'ENTRY_MODIFY' on '/home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class' --> HotSwapTest.class
HOTSWAP AGENT: 15:48:35.174 DEBUG (org.hotswap.agent.annotation.handler.WatchEventCommand) - Executing resource changed method watchReload on class org.hotswap.agent.plugin.hotswapper.HotswapperPlugin for event WatchFileEvent on path /home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class for event ENTRY_CREATE
HOTSWAP AGENT: 15:48:35.188 DEBUG (org.hotswap.agent.plugin.hotswapper.HotswapperPlugin) - Class HotSwapTest will be reloaded from URL file:/home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class
HOTSWAP AGENT: 15:48:35.175 DEBUG (org.hotswap.agent.annotation.handler.WatchEventCommand) - Executing resource changed method watchReload on class org.hotswap.agent.plugin.hotswapper.HotswapperPlugin for event WatchFileEvent on path /home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class for event ENTRY_MODIFY
HOTSWAP AGENT: 15:48:35.191 DEBUG (org.hotswap.agent.plugin.hotswapper.HotswapperPlugin) - Class HotSwapTest will be reloaded from URL file:/home/josh/hotswaptest/build/classes/java/main/HotSwapTest.class
HOTSWAP AGENT: 15:48:35.352 DEBUG (org.hotswap.agent.command.impl.SchedulerImpl) - Executing pluginManager.hotswap([class HotSwapTest])
HOTSWAP AGENT: 15:48:35.355 RELOAD (org.hotswap.agent.config.PluginManager) - Reloading classes [HotSwapTest] (autoHotswap)
HOTSWAP AGENT: 15:48:35.370 DEBUG (org.hotswap.agent.plugin.jdk.JdkPlugin) - Flushing HotSwapTest from com.sun.beans.introspect.ClassInfo cache
HOTSWAP AGENT: 15:48:35.375 DEBUG (org.hotswap.agent.plugin.jdk.JdkPlugin) - Flushing HotSwapTest from ObjectStreamClass caches
HOTSWAP AGENT: 15:48:35.376 DEBUG (org.hotswap.agent.plugin.jdk.JdkPlugin) - Flushing HotSwapTest from introspector
HOTSWAP AGENT: 15:48:35.415 DEBUG (org.hotswap.agent.config.PluginManager) - ... reloaded classes [HotSwapTest] (autoHotswap)
Here is printMsg v2.0
Here is printMsg v2.0
```

As you can see, it swapped in the new code correctly, and now prints the new message. HotSwap was a success!

I imagine there are very few production environments where this feature would be applicable, and even in development, getting this to work properly for something like a JEE app deployed to some application container isn’t necessarily a simple task. But if it can cut down on redeployment cycles, it can certainly be a valuable developer tool.
