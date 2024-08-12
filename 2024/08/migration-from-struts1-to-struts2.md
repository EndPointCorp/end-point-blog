---
author: "Kürşat Aydemir"
title: "Migration from Struts 1 to Struts 2"
featured:
  image_url: **/blog/2024/08/migration-from-struts1-to-struts2/pexels-alfredinix-29415588-6894704.jpg
description: Migration tips from Apache Struts 1 to Struts 2.
date: 2024-08-13
tags:
- java
- apache-struts
- web-framework
---

![Lines of wispy clouds move upward and to the left against a backdrop of light blue sky](/blog/2024/07/migration-from-struts1-to-struts2/pexels-alfredinix-29415588-6894704.jpg)

<!-- Photo by Alfredinix: https://www.pexels.com/photo/flock-of-birds-flying-under-blue-sky-6894704/ -->

[Apache Struts](https://struts.apache.org/) is an open source web framework. Struts 1 started in 2000 and had its latest version 1.3.10. Apache [announced EOL of Struts 1](https://struts.apache.org/struts1eol-announcement.html) as December 2008. So Struts 1 is a dead ancient version which needs to be got rid of already by organizations still using it. Apache adapted WebWork framework as Struts 2 and its architectures significantly differs from Struts 1. So a migration from Struts 1 to Struts 2 would be straight forward. But there are key points and obvious differences [provided Apache](https://struts.staged.apache.org/migration/) to cover a migration plan from Struts 1 to Struts 2.
The marketshare of Apache Struts is around [0.01%](https://enlyft.com/tech/products/apache-struts) which gives relatively lower relevance to Apache Struts. The topic sounds outdated, however there are companies still using Apache Struts 1 in their legacy applications and possibly not involved in marketshare statistics of Apache Struts.

### A Comparison of Struts 1 and Struts 2

|Feature|Struts 1|Struts 2|
|--- |--- |--- |
|Action classes|Struts 1 requires Action classes to extend an abstract base class. A common problem in Struts 1 is programming to abstract classes instead of interfaces.|An Struts 2 Action may  implement an Action interface, along with other interfaces to enable optional and custom services. Struts 2 provides a base ActionSupport class to implement commonly used interfaces. Albeit, the Action interface is not required. Any POJO object with a execute signature can be used as an Struts 2 Action object.|
|Threading Model|Struts 1 Actions are singletons and must be thread-safe since there will only be one instance of a class to handle all requests for that Action. The singleton strategy places restrictions on what can be done with Struts 1 Actions and requires extra care to develop. Action resources must be thread-safe or synchronized.|Struts 2 Action objects are instantiated for each request, so there are no thread-safety issues. (In practice, servlet containers generate many throw-away objects per request, and one more object does not impose a performance penalty or impact garbage collection.)|
|Servlet Dependency|Struts 1 Actions have dependencies on the servlet API since the HttpServletRequest and HttpServletResponse is passed to the execute method when an Action is invoked.|Struts 2 Actions are not coupled to a container. Most often the servlet contexts are represented as simple Maps, allowing Actions to be tested in isolation. Struts 2 Actions can still access the original request and response, if required. However, other architectural elements reduce or eliminate the need to access the HttpServetRequest or HttpServletResponse directly.|
|Testability|A major hurdle to testing Struts 1 Actions is that the execute method exposes the Servlet API. A third-party extension, Struts TestCase, offers a set of mock object for Struts 1.|Struts 2 Actions can be tested by instantiating the Action, setting properties, and invoking methods. Dependency Injection support also makes testing simpler.|
|Harvesting Input|Struts 1 uses an ActionForm object to capture input. Like Actions, all ActionForms must extend a base class. Since  other JavaBeans cannot be used as ActionForms, developers often create redundant classes to capture input. DynaBeans can used as an alternative to creating conventional ActionForm classes, but, here too, developers may be redescribing existing JavaBeans. \||
|Struts 2 uses Action properties as input properties, eliminating the need for a second input object. Input properties may be rich object types which may have their own properties. The Action properties can be accessed from the web page via the taglibs. Struts 2 also supports the ActionForm pattern, as well as POJO form objects and POJO Actions. Rich object types, including business or domain objects, can be used as input/output objects. The ModelDriven feature simplifies taglb references to POJO input objects. \|||
||||
|Expression Language|Struts 1 integrates with JSTL, so it uses the JSTL EL. The EL has basic object graph traversal, but relatively weak collection and indexed property support.|Struts 2 can use JSTL, but the framework also supports a more powerful and flexible expression language called “Object Graph Notation Language” (OGNL).|
|Binding values into views|Struts 1 uses the standard JSP mechanism for binding objects into the page context for access.|Struts 2 uses a “ValueStack” technology so that the taglibs can access values without coupling your view to the object type it is rendering. The ValueStack strategy allows reuse of views across a range of types which may have the same property name but different property types. \|
||||
|Type Conversion|Struts 1 ActionForm properties are usually all Strings. Struts 1 uses Commons-Beanutils for type conversion. Converters are per-class, and not configurable per instance.|Struts 2 uses OGNL for type conversion. The framework includes converters for basic and common object types and primitives.|
|Validation|Struts 1 supports manual validation via a validate method on the ActionForm, or through an extension to the Commons Validator. Classes can have different validation contexts for the same class, but cannot chain to validations on sub-objects.|Struts 2 supports manual validation via the validate method and the XWork Validation framework. The Xwork Validation Framework supports chaining validation into sub-properties using the validations defined for the properties class type and the validation context.|
|Control Of Action Execution|Struts 1 supports separate Request Processors (lifecycles) for each module, but all the Actions in the module must share the same lifecycle.|Struts 2 supports creating different lifecycles on a per Action basis via Interceptor Stacks. Custom stacks can be created and used with different Actions, as needed.|

Table 1: [Comparing Struts 1 and 2](https://struts.staged.apache.org/migration/#PAGE_14048)

As seen in the comparison in Table 1, `Actions` are central components of both Struts 1 and 2 and play a major role in both Struts 1 and Struts 2 architectures. The primary distinction lies under action classes. In the comparison table most of the differences arise around these actions. Implementation of actions, threading model, action interceptors differ from Struts 1 to Struts 2 significantly although similar terms remained.

![Request processing flow in Struts 2](/blog/2024/07/migration-from-struts1-to-struts2/struts2-request-processing.webp)
Image 1: [Request processing in Struts 2](https://www.infoq.com/articles/converting-struts-2-part1/)

### Migration

#### Dependencies

Add Struts 2.0 Jars to the existing Struts 1.3 application. Jars can be downloaded from [Apache Struts download page](https://struts.apache.org/download.cgi) or from the [archives](https://archive.apache.org/dist/struts/) for the prior versions.

#### Request handling

Configure Struts 2 to handle requests at `*.action` extension where Struts 1 handles at `*.do` extension.

#### Configure web application

Web application is enabled in `web.xml` configuration file. There are a few changes needed for Struts 2 in this file. Dispatcher configuration is just done by renaming the configuration tags from `<servlet>` and `<servlet-mapping>` to `<filter>` and `<filter-mapping>`.

A very basic `web.xml` configuration for Struts 1 would be like below to show the settings.

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

The corresponding conversion to Struts 2 be like:

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

A general structure of a Struts 1 action class is like below.

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

Struts 1 actions are singleton and extends base `Action` class. Alternatively `DispatchAction` can be used but the entrry point to an Action class is `execute` method for both implementation. Actions has to be thread-safe and hence all the needed variables are handled in method scope. Finally an action methods return `ActionForward` response.

On the other hand, a Struts 2 a basic action class structure would be:

```java
public class MyAction extends ActionSupport {
   public String execute() throws Exception {
        // add logic
        return "success";
   }
}
```

A Struts 2 action class not necessarily but usually extends `ActionSupport` and usual entry point is again `execute()` method without any parameters. In Struts 2 action classes are not singleton and creates instance for each request, so Class scope variables can be used. Struts 2 finally injects HttpServletRequest into ServletRequestAware actions to complete the request flow.

#### Action Configuration

In Struts 1 applications action configurations are made in `struts-config.xml` located in `WEB-INF` directory. Struts 1 applications need to configure actions and action form beans in this configuration file.

```XML
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

In this article, we covered migrating the most skeletal components from Struts 1 to Struts 2 and comparison of several features between them. Complete configuration and code migration can be done gradually from Struts 1 to Struts 2 which would involve actions, interceptors, tags and many other details. Not that straight-forward but a convention change can be seen easily.