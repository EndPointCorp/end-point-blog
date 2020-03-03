---
author: "Joshua Tolley"
title: "Cooking with CAS"
tags: java, architecture. security, programming, php
---

One of our customers asked us to host a new suite of web-based applications for them and to protect them with a single sign-on (SSO) solution. Ok, easy enough;
the applications in question were in fact designed with a particular SSO system in mind already. But for various good reasons, our customer needed a different
system, and we eventually settled on [Apereo's "Central Authentication Server"
project](https://www.apereo.org/projects/cas), or CAS. I'd like to describe the
conversion process we went through.

## The ingredients

Our customer's application suite included one principle Java application using [JAAS
authentication](https://docs.oracle.com/javase/7/docs/technotes/guides/security/jaas/JAASRefGuide.html), another Java application based on [Spring
Security](https://spring.io/projects/spring-security), one PHP application (later joined by another), and a few automated tasks that also needed to
authenticate. In their original form, these applications supported single sign-on by expecting each request to include a header identifying an authenticated
user. This works fine, of course, provided some gateway system reliably sanitizes request headers to ensure malicious users cannot forge a header themselves.
CAS is a bit more complex: in browser-based applications, for which CAS is best suited, applications redirect unauthenticated requests to a CAS server, which
identifies the application requesting service, and authenticates the user through any of various configurable methods. The CAS server then redirects the user back
to the original application with a parameter called a "Service Ticket", a seemingly random number identifying this particular authentication request. The
original application contacts the CAS server directly to validate the service ticket and to collect information to identify the user, and then proceeds with its
own internal processes to establish a session for that user and to go about its normal work.

To CAS-enable an application, we incorporate a CAS client library.
[Clients](https://apereo.github.io/cas/6.1.x/integration/CAS-Clients.html#build-your-own-cas-client) exist in one form or another for various languages. In fact
we won't use the Java client directly, but rather we'll incorporate compponents that extend it. Truthfully, I was a bit concerned by what appeared to be limited
selection of actively supported client libraries, and of course your results may vary, but we found software to meet our own needs without too much difficulty.

## Configuring Wildfly Authentication

I mentioned above that our applications use a variety of languages, and a variety of authentication systems. We had to teach each one to cooperate with the CAS
server, each in a different way. The most important application in the suite depends on the JAAS-based security subsystem of the [Wildfy application
server](https://www.wildfly.org/) it's
deployed to, and originally it used a custom [LoginModule](https://docs.oracle.com/javase/7/docs/api/javax/security/auth/spi/LoginModule.html) that checked for
the magic header I mentioned to find the ID of the right user. Our first modification was to configure our proxy server to remove that magic header from every
request. That way, although we planned to disable the old authentication system entirely, we ensured that users couldn't forge a header to log in, even if we
made a mistake and left some support for the old authentication system active somewhere in our deployment. 

This application uses a declarative security policy: the deployment descriptor identifies a set of user roles, and another set of "security constraints". Each
security constraint describes one or more URL patterns used in the application, and the set of user roles allowed to access URLs matching those patterns. Here's
an example snippet.

```xml
    <!-- clients -->
    <security-constraint>
        <web-resource-collection>
            <web-resource-name>Secure Area</web-resource-name>
            <url-pattern>/views/clients/*</url-pattern>
            <url-pattern>/client/edit/*</url-pattern>
            <url-pattern>/client/edit_tree/*</url-pattern>
            <url-pattern>/client/view/*</url-pattern>
            <url-pattern>/client/view/id/*</url-pattern>
        </web-resource-collection>
        <auth-constraint>
            <role-name>client_role</role-name>
        </auth-constraint>
    </security-constraint>

    <!-- places -->
    <security-constraint>
        <web-resource-collection>
            <web-resource-name>Secure Area</web-resource-name>
            <url-pattern>/views/places/*</url-pattern>
        </web-resource-collection>
        <auth-constraint>
            <role-name>manage_places</role-name>
        </auth-constraint>
    </security-constraint>
```

We installed the [cas-extension library](https://github.com/soulwing/cas-extension) in our Wildfly server to handle the CAS protocol. Authentication
works in a series of steps: First, an unauthenticated user attempts to access a URL matching a pattern in one of the security constraints described above. This
triggers the CAS extension to redirect the user to the CAS server, and to accept and validate the service ticket when the CAS server sends the user back again.
Assuming the user authenticates successfully, we determine the user's roles with a database query, using a role mapper built into Wildfly. With an authenticated
user and that user's roles, the authentication process is complete.

Configuration of the cas-extension begins with a CAS profile, a combination of the URL of the CAS server and the URL of the service the extension should
protect.

```xml
    <subsystem xmlns="urn:soulwing.org:cas:1.0">
        <cas-profile name="default" service-url="https://our.application.server/application" server-url="https://our.cas.server"/>
    </subsystem>
```

This tells the extension where to send authentication requests, where to listen for requests returning from the CAS server, and where to validate service
tickets, whereupon the CAS extension can create an "identity assertion", and send that back to the Wildfly security subsystem. Next we need to validate that
identity assertion, and figure out what roles belong to the user. This happens in a [Wildfly security
domain](https://docs.wildfly.org/14/Admin_Guide.html#security-domains).

```xml
    <security-domain name="MySecurityDomain">
        <authentication>
            <login-module name="IdentityAssertion" code="org.soulwing.cas.jaas.IdentityAssertionLoginModule" flag="required" module="org.soulwing.cas"/>
        </authentication>
        <mapping>
            <mapping-module code="DatabaseRoles" type="role">
                <module-option name="dsJndiName" value="java:/comp/env/jdbc/databaseConnection"/>
                <module-option name="rolesQuery" value="select role from user_roles where user_id = ?"/>
            </mapping-module>
        </mapping>
    </security-domain>
```

The `authentication` portion of the security domain refers to a JAAS LoginModule shipped with the CAS extension, which simply verifies that the identity
assertion comes from the CAS extension and not somewhere else. Then the `mapping` portion ([documented here](https://docs.wildfly.org/14/Admin_Guide.html#mapping))
looks up the given user in a database to find what roles it should be assigned.

The last piece of the puzzle is a CAS deployment descriptor for our application, which activates cas-extension for that application. It could be as simple as an
empty file called `cas.xml` in the right place, but ours ended up a little more complex, identifying both the CAS profile we wanted to use (unnecessary in this
case, as there's only one CAS profile on the system, but it helped keep things more clear in our minds), and instructing the extension to load other API bits
into our application for later use.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<cas xmlns="urn:soulwing.org:cas:1.0">
  <profile>default</profile>
  <add-api-dependencies/>
</cas>
```

This configuration proved sufficient to let users log in and use the application, but as is sometimes the case with single sign-on, we needed to do a little
more work to let them log out properly. By default, each application in the suite sets a cookie in the user's browser to identify its session. The CAS server
likewise sets a cookie. So a user can log out of the application, destroying the application's session cookie, but we need to destroy the CAS server's session
cookie as well as the other applications' cookies. Single log-out can be complicated, and I won't go into the full setup here. Suffice it to say we did need to
fetch the proper logout URL from the CAS extension API and redirect to it once users log out of the application itself, using API calls provided by
cas-extension.

## Configuring Spring Authentication

Another Java-based application in our suite uses Spring Security, for which CAS configuration proceeded differently. [This
document](https://docs.spring.io/spring-security/site/docs/3.0.x/reference/cas.html) describes the bulk of the configuration, which in my opinion was more
complex than for the first case I described, and for brevity I'll include only the broad strokes. This system functions by intercepting AuthenticationException
objects and inserting itself to handle the CAS process. We also configured a Spring
[UserDetailsService](https://docs.spring.io/spring-security/site/docs/3.2.3.RELEASE/apidocs/org/springframework/security/core/userdetails/UserDetailsService.html)
to execute the same database query we used above to find the user's roles. It works just fine for our purposes, but I'm not fully conversant in the large stack
of beans Spring uses to manage the process, and I admit it took some time to get this configuration sorted out.

## Enter PHP

Some of these applications use PHP, which meant yet another configuration. Apereo maintains a [PHP client](https://github.com/apereo/phpCAS), which includes
several helpful examples. Once I refreshed my memory about how to use PHP, I tracked down the part of the application that authenticates users, and replaced the
existing code with calls to phpCAS:

```php
    phpCAS::proxy(CAS_VERSION_2_0, $phpCASHost, $phpCASPort, $phpCASContext);
    phpCAS::forceAuthentication();
    $_SESSION[EXPORT_SERVERNAME]['umdid'] = phpCAS::getUser();
```

The `forceAuthentication` call determines the current phase of the authentication process this request is in, whether unauthenticated, fully authenticated, or
requring validation of a service ticket, and responds appropriately. We then set a session variable to the ID of the authenticated user, which replicates what
the original authentication code would have done.

This application requires access to a REST API exposed by the first application, a situation which CAS calls "proxy" authentication. Here, CAS issues not only
its usual service ticket, but also a "proxy granting ticket". When the application wants to use the API, it uses the proxy granting ticket to request a service
ticket for the API from the CAS server. The CAS server itself requires some new configuration in this case, but for the PHP code, the only difference from the
simpler, non-proxy case is that we call `phpCAS::proxy` instead of `phpCAS::client` to configure CAS.

## The return of header authentication

Finally, we have a few automated tasks which use various APIs, and need to authenticate. Since there's no user sitting at a browser in these cases, we need some
other authentication system. In these cases, we've taken our cue from the applications' original form, and configured CAS to recognize a "trusted header", which
we add to any requests issued by these automated jobs. Of course, we've also configured the proxy to disallow this header from any systems outside our internal
network.

## A few loose ends

Of course, there were other considerations in this project I've not covered. Configuring CAS itself wasn't necessarily straightforward, and included a custom
authentication module I hope to describe in a later article. Selecting among CAS server's available
[deployment](https://apereo.github.io/cas/6.1.x/installation/Configuring-Servlet-Container.html)
[options](https://apereo.github.io/cas/6.1.x/installation/Docker-Installation.html) and fitting the winner into our
existing infrastructure in a way that makes it easy to manage and monitor was another task entirely. We needed to customize the server's default user interface
to prevent it from offering users an imaginary method to recover forgotten passwords. The series of redirected browser requests involved in the CAS protocol
presents a notable performance impact under some circumstances. And it has taken me no small effort to learn to appreciate the CAS server's sometimes
distressingly circular [documentation](https://apereo.github.io/cas/6.1.x/index.html). But several months into the project, CAS seems to be working well enough
for our purposes that other users of the same application suite have begun to express interest.
