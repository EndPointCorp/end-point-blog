---
author: "Kürşat Kutlu Aydemir"
title: "Migration from Struts 1 to Struts 2"
featured:
  image_url: /blog/2024/10/migration-from-struts1-to-struts2/pexels-alfredinix-29415588-6894704.webp
description: Tips for migrating from Apache Struts 1 to Struts 2.
date: 2024-10-04
github_issue_number: 2077
tags:
- java
- frameworks
- migration
- apache-struts
---

![A flock of flamingos fly against a pink and blue sunset](/blog/2024/10/migration-from-struts1-to-struts2/pexels-alfredinix-29415588-6894704.webp)

<!-- Photo by Alfredinix: https://www.pexels.com/photo/flock-of-birds-flying-under-blue-sky-6894704/ -->

[Apache Struts](https://struts.apache.org/) is an open source web framework. Struts 1 was first released in 2000 and its latest version (1.3.10) was released in December 2008, marking the [EOL of Struts 1](https://struts.apache.org/struts1eol-announcement.html). So Struts 1 is an ancient, dead version. Organizations still using it need to move away from Struts 1.

Apache adapted the WebWork framework as Struts 2. Its architecture significantly differs from that of Struts 1. There are key points and obvious differences [provided by Apache](https://struts.staged.apache.org/migration/) to cover a migration plan from Struts 1 to Struts 2.

The market share of Apache Struts is around [0.01%](https://enlyft.com/tech/products/apache-struts), which gives relatively lower relevance to Apache Struts. However, there are companies still using Apache Struts 1 in their legacy applications, which may not be counted in market share statistics.

### A Comparison of Struts 1 and Struts 2

Struts 1 and Struts 2 [differ significantly](https://struts.staged.apache.org/migration/#PAGE_14048) in their approach to handling web requests. Struts 1 follows a more rigid structure where `Action` classes must extend an abstract base class, limiting flexibility. In contrast, Struts 2 is more dynamic, allowing Action classes to implement interfaces or even function as simple POJOs, enhancing adaptability. Struts 2 also includes the `ActionSupport` class, which implements commonly used interfaces, making development easier and more versatile.

The threading model in Struts 1 is based on a singleton pattern, meaning only one instance of an Action class exists to handle all requests, which requires careful management of thread safety. Struts 2, on the other hand, creates a new Action object for every request, which eliminates concerns about thread safety.

When it comes to servlet dependency, Struts 1 is tightly coupled with the servlet API, requiring Actions to work directly with `HttpServletRequest` and `HttpServletResponse`. Struts 2 decouples the Action from the servlet container, using simple maps to represent the context. This allows for easier testing and more modular code. Struts 2 still offers the flexibility to access the request and response objects when necessary, but often through other architectural patterns that minimize the need for direct servlet interaction.

Testing Struts 1 applications is challenging due to its tight coupling with the servlet API. External libraries like Struts `TestCase` are often required to mock servlet objects for testing purposes. Struts 2 makes testing far more straightforward by supporting dependency injection and allowing Action classes to be tested in isolation, without needing complex mocks.

Input handling in Struts 1 revolves around `ActionForm` objects, which must extend a base class which often leads to redundancy. Struts 2 simplifies this by using Action properties directly, eliminating the need for separate `ActionForm` objects. Additionally, Struts 2 supports complex object types for input and output, allowing domain specific objects to be used.

In terms of expression languages, Struts 1 integrates with `JSTL`, which provides basic object graph traversal but lacks robust support for collections. Struts 2 uses `OGNL` (Object Graph Notation Language), offering more advanced and flexible expression capabilities, giving developers more control over data handling in views.

Binding values into views is handled differently as well. Struts 1 uses standard JSP mechanisms, while Struts 2 introduces the `ValueStack`, a system that decouples the view from the object being rendered. This allows for a greater degree of reuse and flexibility, especially when dealing with varying property types across different objects.

Type conversion in Struts 1 is handled by Commons-Beanutils, which operates on a per-class basis. This can be limiting as it doesn’t allow for instance-level customization. Struts 2 improves on this by utilizing OGNL for type conversion, offering built-in converters for common types while also providing a flexible system for adding custom converters.

Lastly, the control over action execution is much more granular in Struts 2. While Struts 1 uses a single request processor per module, Struts 2 introduces Interceptor Stacks, allowing developers to define different lifecycles for individual Actions. This customization helps tailor the flow of execution to fit specific application requirements.

Actions are central components in both Struts 1 and 2 and play a major role in the architectures of both Struts versions. Struts 2 offers a more modern, flexible, and test-friendly framework, improving upon Struts 1’s limitations by embracing POJO actions, better type conversion, enhanced validation, and a decoupled threading model. These changes make Struts 2 more adaptable and easier to maintain, particularly for complex web applications.

> You can see more about request processing flow in Struts 2 in [this InfoQ article](https://www.infoq.com/articles/converting-struts-2-part1/).

### Migration

#### Dependencies

Add the Struts 2.0 Jars to the existing Struts 1.3 application.  The latest Jar files can be downloaded from the [Apache Struts download page](https://struts.apache.org/download.cgi). Alternatively, you can download the Jar files for any of the previous versions from the [archive](https://archive.apache.org/dist/struts/).

#### Request handling

Configure Struts 2 to handle requests with the `*.action` extension, differently from Struts 1, which uses the `*.do` extension.

#### Configure web application

The web application is enabled in the `web.xml` configuration file. There are a few changes to this file needed for Struts 2. Dispatcher configuration is done by simply renaming the configuration tags from `<servlet>` and `<servlet-mapping>` to `<filter>` and `<filter-mapping>`.

A very basic `web.xml` configuration for Struts 1 would look like:

```xml
<servlet>
    <servlet-name>action</servlet-name>
    <servlet-class>org.apache.struts.action.ActionServlet</servlet-class>
    <init-param>
        <param-name>config</param-name>
        <param-value>/WEB-INF/struts-config.xml</param-value>
    </init-param>
    <load-on-startup>2</load-on-startup>
</servlet>

<servlet-mapping>
    <servlet-name>action</servlet-name>
    <url-pattern>*.do</url-pattern>
</servlet-mapping>
```

The corresponding conversion to Struts 2 would look like:

```xml
<filter>
    <filter-name>webwork</filter-name>
    <filter-class>org.apache.struts.action2.dispatcher.FilterDispatcher</filter-class>
</filter>

<filter-mapping>
    <filter-name>webwork</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

#### Migrating actions

A general structure of a Struts 1 action class is below.

```java
public class CustomAction extends Action {
    public ActionForward execute(
        ActionMapping mapping,
        ActionForm form,
        HttpServletRequest request,
        HttpServletResponse response) throws Exception {
        // add logic
        return (mapping.findForward("success"));
    }
}
```

Struts 1 actions are singletons and extend the base `Action` class. Alternatively, `DispatchAction` can be used instead of the base class. In either case, the `execute` method is the entry point to an Action class. Actions have to be thread-safe and hence all the necessary variables should be handled in method scope. Finally, the `execute` method returns an `ActionForward` response.

On the other hand, in Struts 2 a basic action class structure would look like this:

```java
public class MyAction extends ActionSupport {
   public String execute() throws Exception {
        // add logic
        return "success";
   }
}
```

A Struts 2 action class will usually (but not necessarily) extend `ActionSupport`. The usual entry point is again the `execute` method—however, this method has no parameters. In Struts 2 action classes are not singletons. Instead an instance of the action class is created for each request, so class scope variables can be used safely, alleviating many thread-safety concerns in Struts 1 actions. Struts 2 will inject a `HttpServletRequest` for the current request into actions implementing the `ServletRequestAware` interface, allowing you access to the underlying request object.

#### Action Configuration

In Struts 1 applications, action configurations are made in `struts-config.xml` located in the `WEB-INF` directory. Struts 1 applications need to configure actions and action form beans in this configuration file.

```xml
<struts-config>

     <form-beans>
         <form-bean name="myForm" type="com.endpoint.blog.struts.MyForm"/>
         ...
     </form-beans>

    <global-forwards>
       <forward name="home" path="/home.do" redirect="true" />
       <forward name="projects" path="/myactionProcess.do?dispatch=myDispatch" redirect="true"/>
       ...
   </global-forwards>

   <action-mappings>
       <action path="/myPackage/add" type="org.apache.struts.actions.ForwardAction" />
       ...
   </action-mappings>

 </struts-config> 
```

Struts 2 configuration involves a package wrapper around the action definitions.

```xml
<struts>
  <package name="myPackage" extends="struts-default">
      <action name="add" >
          <result>/myPackage/add.jsp</result>
        </action>
        ...
    </package>
 </struts> 
```

However, in Struts 2, actions can be defined in a more general way using Struts conventions:

```xml
<struts>
  <constant name="struts.action.extension" value="ep"/>
    <constant name="struts.convention.action.packages" value="com.endpoint.blog.actions.*"/>
    ...
</struts>
```

In this article we covered migrating the most basic components from Struts 1 to Struts 2 and compared several features between each version. Complete configuration and code migration from Struts 1 to Struts 2 can be done gradually, involving actions, interceptors, tags, and many other details. Not completely straightforward, but the patterns and convention changes adopted in Struts 2 become clearer as you dive in.
