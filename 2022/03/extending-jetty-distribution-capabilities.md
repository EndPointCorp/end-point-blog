---
author: "Kürşat Kutlu Aydemir"
title: "Extending Your Jetty Distribution’s Capabilities"
date: "2022-03-31"
tags:
- java
- jetty
- development
github_issue_number: 1849
---

![Jetty Logo](/blog/2022/03/extending-jetty-distribution-capabilities/jetty-logo.svg)

### What is Jetty?

"Jetty is a lightweight highly scalable Java-based web server and servlet engine." ([Jetty Project](https://github.com/eclipse/jetty.project))

Jetty can run standalone or embedded in a Java application and the details about running a Jetty webserver can be found in the Jetty Project Git repository and [documentation](https://www.eclipse.org/jetty/documentation) as well. The Jetty project has been hosted at the Eclipse Foundation since 2009 ([Jetty, Eclipse](https://www.eclipse.org/jetty/)).

### Know Your Jetty

In many legacy environments using the Jetty web server there may be an older version of Jetty. If you know the version of the Jetty distribution in your environment then you can find its source code in the Jetty project GitHub repo. Some of the distributions are in project releases but most of the distributions can be found in the tags as well.

For instance `jetty-9.4.15.v20190215` distribution can be found in the Jetty project tags at this URL: `https://github.com/eclipse/jetty.project/releases/tag/jetty-9.4.15.v20190215` 

When you clone the `jetty.project` Git repo, you can then easily switch to any specific release tag:

```sh
$ git clone git@github.com:eclipse/jetty.project.git
$ git checkout jetty-9.4.15.v20190215
```

Then you can build or add your custom code in that version.

### Extending Your Jetty Capabilities

The reason you might want to build Jetty yourself is that you have a specific Jetty version in your environment and want to add some custom handlers or wrappers so that you can add additional capabilities in your environment.

Jetty is written in Java and you can add new features or patch your own fork like other open-source Java projects. 

### Build

Once you have your target version code base you can just work on that individually. This is one way to add new features to your Jetty distribution.

After you add your custom code you'll need to build. You can find the building instructions on Jetty Project GitHub home, which is simply:

```sh
$ mvn clean install
```

If you want to skip the tests the option below is your friend:

```sh
$ mvn clean install -DskipTests
```

### Compile Classes Individually

This is a tricky way to inject your newly created custom classes into your Jetty distribution. In this way, instead of building the whole Jetty project, you can just create individual custom Java classes consuming Jetty libraries and compile them manually. You don't need the whole project this way.

If we come back to the question: what new features would I want to add to my new or ancient local Jetty distribution? Well, that really depends on the issues you face or improvements you need to add.

For one of our customers, once we needed to log request and response headers in Jetty. We couldn't find an existing way to do that. So I decided to create a custom RequestLog handler class and inject this into the Jetty deployment we already have rather than building the whole project.

Even if you don't build the whole project it is still useful and handy to get the whole project code to refer the existing code and prepare your code by learning the existing way things are done in the project.

I found `RequestLog` interface in `jetty-server` sub-project and it is created under `org.eclipse.jetty.server` package. There is also a class `RequestLogCollection` in the same level implementing `RequestLog` which may give you some idea about the implementations.

So I followed the structure and created my custom handler in the same level and implemented `RequestLog`. Below is a part of my `CustomRequestLog` class:

```java
package org.eclipse.jetty.server;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.eclipse.jetty.http.pathmap.PathMappings;
import org.eclipse.jetty.util.component.ContainerLifeCycle;
import org.eclipse.jetty.util.log.Log;
import org.eclipse.jetty.util.log.Logger;

import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.*;

public class CustomRequestLog extends ContainerLifeCycle implements RequestLog
{
    protected static final Logger LOG = Log.getLogger(CustomRequestLog.class);

    private static ThreadLocal<StringBuilder> _buffers = ThreadLocal.withInitial(() -> new StringBuilder(256));

    protected final Writer _requestLogWriter;

    private String[] _ignorePaths;
    private transient PathMappings<String> _ignorePathMap;

    public CustomRequestLog(Writer requestLogWriter)
    {
        this._requestLogWriter = requestLogWriter;
        addBean(_requestLogWriter);
    }

    /**
     * Is logging enabled
     *
     * @return true if logging is enabled
     */
    protected boolean isEnabled()
    {
        return true;
    }

    /**
     * Write requestEntry out. (to disk or slf4j log)
     *
     * @param requestEntry the request entry
     * @throws IOException if unable to write the entry
     */
    public void write(String requestEntry) throws IOException
    {
        _requestLogWriter.write(requestEntry);
    }

    private void append(StringBuilder buf, String s)
    {
        if (s == null || s.length() == 0)
            buf.append('-');
        else
            buf.append(s);
    }

    /**
     * Writes the request and response information to the output stream.
     *
     * @see RequestLog#log(Request, Response)
     */
    @Override
    public void log(Request request, Response response)
    {
        try
        {
            if (_ignorePathMap != null && _ignorePathMap.getMatch(request.getRequestURI()) != null)
                return;

            if (!isEnabled())
                return;

            StringBuilder buf = _buffers.get();
            buf.setLength(0);

            Gson gsonObj = new GsonBuilder().disableHtmlEscaping().create();
            Map<String, Object> reqLogMap = new HashMap<String, Object>();
            Map<String, String> reqHeaderMap = new HashMap<String, String>();
            // epoch timestamp
            reqLogMap.put("timestamp_epoch", System.currentTimeMillis());

            // timestamp
            DateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSXXX");
            String nowAsString = df.format(new Date());
            reqLogMap.put("timestamp", nowAsString);

            // request headers
            List<String> reqHeaderList = Collections.list(request.getHeaderNames());
            for(String headerName : reqHeaderList) {
                reqHeaderMap.put(headerName.toLowerCase(), request.getHeader(headerName));
            }
            reqLogMap.put("request_headers", reqHeaderMap);

            // response headers
            Map<String, String> resHeaderMap = new HashMap<String, String>();
            for(String headerName : response.getHeaderNames()) {
                resHeaderMap.put(headerName.toLowerCase(), response.getHeader(headerName));
            }
            reqLogMap.put("response_headers", resHeaderMap);

            // http method
            reqLogMap.put("http_method", request.getMethod());

            // original URI
            reqLogMap.put("original_uri", request.getOriginalURI());

            // protocol
            reqLogMap.put("protocol", request.getProtocol());

            // http status
            reqLogMap.put("http_status", response.getStatus());

            // query string
            reqLogMap.put("query_string", request.getQueryString());

            String reqJSONStr = gsonObj.toJson(reqLogMap);
            buf.append(reqJSONStr);

            String log = buf.toString();
            write(log);
        }
        catch (IOException e)
        {
            LOG.warn(e);
        }
    }
}
```

In this custom RequestLog class the most interesting part is `public void log(Request request, Response response)` method where the logging operation is actually done. You can simply override the existing logging behaviour and put anything you want. Here I added the raw request and response headers coming and going through Jetty server.

Now it is time to compile this class. You can find many tutorials about compiling a single Java class using classpath. Here's how I did it:

```sh
$ javac -cp ".:$JETTY_HOME/lib/jetty-server-9.4.15.v20190215.jar:$JETTY_HOME/lib/jetty-http-9.4.15.v20190215.jar:$JETTY_HOME/lib/jetty-util-9.4.15.v20190215.jar:$JETTY_HOME/lib/servlet-api-3.1.jar:$JETTY_HOME/lib/gson-2.8.2.jar" CustomRequestLog.java
```

If you look at my classpath I even added a third party library `gson-2.8.2.jar` since I also used this in my custom code. Remember to put this in your `$JETTY_HOME` directory as well.

The command above generates the `CustomRequestLog.class` file which is now available to be injected. So where do you need to inject this?

Since I followed where the `RequestLog` interface is located and packaged we better inject this into the same project JAR file, which is `jetty-server.jar`. In my environment it is `jetty-server-9.4.15.v20190215.jar`. I also added other required dependencies in the classpath to compile this code. 

Now, I want to inject `CustomRequestLog.class` into `jetty-server-9.4.15.v20190215.jar`. I copied this jar into a temporary directory and I extracted the content of `jetty-server-9.4.15.v20190215.jar` into the temp directory using this command:

```sh
$ jar xf jetty-server-9.4.15.v20190215.jar
```

This command extracts all the content of the jar file including resource files and the classes in their corresponding directory structure `org/eclipse/jetty/server`. You would see `RequestLog.class` also extracted in this directory.

So what we need to do is now simply copy our `CustomRequestLog.class` into this extracted `org/eclipse/jetty/server` directory and pack up the JAR file again by running this command:

```sh
$ jar cvf jetty-server-9.4.15.v20190215.jar org/ META-INF/
```

This command re-bundles compiled code along with the other extracted resources (in this case the `META-INF/` directory only) and creates our injected JAR file. You'd better create this injected Jetty JAR file in the temp directory so that you can control the backup of existing original JAR files.

For this specific case I added this custom `RequestLog` handler in my Jetty config file `jetty.xml`. It may not be the case for all the custom changes or extensions you'd add to your Jetty instance.

Here is an example `RequestLog` config entry for this custom handler:

```xml
<Set name="RequestLog">
  <New id="RequestLog" class="org.eclipse.jetty.server.CustomRequestLog">
    <!-- Writer -->
    <Arg>
      <New class="org.eclipse.jetty.server.AsyncRequestLogWriter">
        <Arg>
          <Property name="jetty.base" default="." />/
          <Property>
            <Name>jetty.requestlog.filePath</Name>
            <Default>
              <Property name="jetty.requestlog.dir" default="logs"/>/yyyy_mm_dd.request.log
            </Default>
          </Property>
        </Arg>
        <Arg/>
        <Set name="filenameDateFormat">
          <Property name="jetty.requestlog.filenameDateFormat" default="yyyy_MM_dd"/>
        </Set>
        <Set name="retainDays">
          <Property name="jetty.requestlog.retainDays" default="90"/>
        </Set>
        <Set name="append">
          <Property name="jetty.requestlog.append" default="false"/>
        </Set>
        <Set name="timeZone">
          <Property name="jetty.requestlog.timezone" default="GMT"/>
        </Set>
      </New>
    </Arg>
  </New>
</Set>
```

That's all.
