---
author: "Kürşat Kutlu Aydemir"
title: "How to Migrate from Struts 2 to Struts 6"
date: 2025-04-17
github_issue_number: 2105
featured:
  image_url: /blog/2025/04/migration-from-struts2-to-struts6/paint-roller.webp
description: Tips for migrating from Apache Struts 2 to Apache Struts 6.
tags:
- java
- apache-struts
- frameworks
- migration
---

![Upgrade your walls. Close up of a paint roller balanced on top of a blue paint can, at a 45 degree angle from the camera.](/blog/2025/04/migration-from-struts2-to-struts6/paint-roller.webp)

<!-- Photo by cottonbro studio: https://www.pexels.com/photo/a-paint-roller-on-the-paint-can-9222200/ -->

With the introduction of Struts 6, developers are provided enhanced features, security improvements, and modern practices that align with contemporary Java development. If you're currently using Struts 2, migrating to Struts 6 is a worthwhile endeavor that can future-proof your application.

Also, since Struts 2.5.x reached its [end of life](https://struts.apache.org/struts25-eol-announcement), there won't be any security updates for this version. This guide will walk you through the key differences between Struts 2 and Struts 6, including some significant changes in Struts 6 with practical configuration and code examples.

### Getting Ready for Migration from Struts 2 to Struts 6

Starting from Struts 6.0.0 the framework requires Java 8 at minimum. So, if you are running a Struts 2.x environment on an old version of Java, it needs to be upgraded to Java 8 at least. Check out the [Struts 6.0.0 version notes](https://cwiki.apache.org/confluence/display/WW/Version+Notes+6.0.0) for a list of changes.

### Config and Code Changes

#### Servlet API Dependency

Struts 6.0.0 requires Servlet API 3.1 or newer and won't work with the older versions. The Maven dependency that you can use for this is below:

```xml
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>3.1.0</version>
    <scope>provided</scope>
</dependency>
```

#### Deprecated Sitegraph Plugin Removed

Support for the sitegraph plugin, which was already deprecated, has now been removed entirely.

#### Velocity Plugin

Velocity support has been moved into a dedicated plugin. To continue using the Velocity plugin in your Struts application, you can extend the Struts config package definition, adding `velocity-default` in `struts.xml` as in the below example:

```xml
<package name="mystrutsapp" extends="struts-default, velocity-default">
  ...
</package>
```

#### DTD of struts.xml

The proper DTD (Document Type Definition) header of struts.xml should be updated as below:

```xml
<!DOCTYPE struts PUBLIC
    "-//Apache Software Foundation//DTD Struts Configuration 6.0//EN"
    "https://struts.apache.org/dtds/struts-6.0.dtd">
```

#### Class Changes

There are some class changes you might need to consider.

* `com.opensymphony.xwork2.config.providers.XmlConfigurationProvider` was made abstract. You should now use `org.apache.struts2.config.StrutsXmlConfigurationProvider` instead.
* `com.opensymphony.xwork2.conversion.TypeConversionException` was replaced by`org.apache.struts2.conversion.TypeConversionException`.
* `com.opensymphony.xwork2.XWorkException` was replaced by `org.apache.struts2.StrutsException`.

#### Constant Changes

Xwork config constants like `devMode` were already deprecated and replaced with new constants like `struts.devMode`. In Struts 6.0.0, the deprecated constants were completely removed. Also, new constants [`struts.i18n.search.defaultbundles.first`](https://struts.apache.org/core-developers/localization#search-in-default-bundles-first) and [`struts.ui.escapeHtmlBody`](https://struts.apache.org/tag-developers/tag-syntax#escaping-body-of-a-tag) were introduced.

#### OGNL

Starting from Struts 6.0.0 OGNL expression length is limited to 256 characters by default as longer expressions can be [considered harmful](https://struts.apache.org/security/#apply-a-maximum-allowed-length-on-ognl-expressions). However, the limit can be changed by adjusting the `struts.ognl.expressionMaxLength` constant in struts.xml.

Static method access is not possible using OGNL expressions like `@com.mypack.MyClass@MyStaticMethod()`. This usage should be converted to alternative approaches such as Value Stack access through Action methods:

```java
// MyAction.java
public class MyAction extends ActionSupport {

    public String getMyData() {
        return MyStaticClass.getMyStaticData();
    }

    public String execute() {
        return SUCCESS;
    }
}
```

```java
// MyClass.java
public class MyStaticClass {
    public static String getMyStaticData() {
        return "Data from static method";
    }
}
```

In your JSP you can access the data using an OGNL expression:

```xml
<s:property value="myData" />
```

#### HTML Escaping

Struts 6 uses a newer `FreeMarker` version with auto-escaping enabled by default, affecting how output is rendered. You should avoid manual escaping (e.g., `?html`) in FreeMarker templates when migrating to Struts 6.

Struts 2 manual escaping:

```plain
${user.name?html}
```

Struts 6 auto-escaping happens by default, so no `?html` escape is necessary:

```plain
${user.name}
```

### Tiles Support

Until version 6.3.0, Struts 2 and Struts 6 had been supporting Tiles through [Apache Tiles](https://tiles.apache.org/). The Apache Tiles project has been retired and is not updated anymore. The Struts team incorporated the Apache Tiles codebase into Struts and essentially added built-in support for Tiles starting with [Struts version 6.3.0](https://cwiki.apache.org/confluence/display/WW/Version+Notes+6.3.0) through the new [Tiles Plugin](https://struts.apache.org/plugins/tiles/).

If you are using Maven you can use the following dependency to setup the Tiles plugin in Struts 6.x:

```xml
<dependency>
  <groupId>org.apache.struts</groupId>
  <artifactId>struts2-tiles-plugin</artifactId>
  <version>${version.tiles}</version>
</dependency>
```

And then register the Tile listener in your `web.xml`:

```xml
<listener>
  <listener-class>org.apache.struts2.tiles.StrutsTilesListener</listener-class>
</listener>
```

### Conclusion

Migrating from Struts 2 to Struts 6 involves several significant changes due to updates in the framework's architecture, dependencies, and requirements. Struts 6 (starting with version 6.0.0) introduces modernizations to align with newer Java versions, servlet specifications, and security practices.


