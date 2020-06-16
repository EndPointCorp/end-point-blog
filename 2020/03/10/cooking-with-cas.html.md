---
author: "Josh Tolley"
title: "Cooking with CAS"
tags: java, architecture, security, programming, php, spring
gh_issue_number: 1600
---

<img src="/blog/2020/03/10/cooking-with-cas/4696900602_77582d1d5d_c.jpg" alt="passwords" />
[Photo](https://www.flickr.com/photos/reidrac/4696900602/in/photolist-8a3QUS-XN6XAe)
by Flickr user [reidrac](https://www.flickr.com/photos/reidrac/), licensed
under [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/)

One of our customers asked us to host a new suite of web-based applications for them and to protect them with a single sign-on (SSO) solution. Ok, easy enough;
these applications were in fact designed with a particular SSO system in mind already, but our situation required a different one, and we eventually chose
Apereo’s open source [Central Authentication Server project](https://www.apereo.org/projects/cas), or CAS. I’d like to describe the conversion process we went
through.

### The ingredients

Our customer’s application suite included:

* The principal Java application using [JAAS authentication](https://docs.oracle.com/javase/7/docs/technotes/guides/security/jaas/JAASRefGuide.html)
* Another Java application based on [Spring Security](https://spring.io/projects/spring-security)
* A pair of PHP applications
* A few automated tasks that needed to authenticate.

The original SSO system sets a header on each request, identifying an authenticated user. This requires a gateway system to sanitize request headers to ensure
malicious users cannot forge a header themselves. It also requires each application inspect request headers and respond appropriately.

CAS is a bit more complex: applications redirect unauthenticated requests to a CAS server, which authenticates the user through any of various configurable
methods. The CAS server then redirects the user back to the original application with a parameter called a “Service Ticket”, a seemingly random number
identifying an individual authentication request. The original application contacts the CAS server directly to validate the service ticket and to collect
information to identify the user. It can then establish a session for that user, and proceed normally.

To CAS-enable an application, we incorporate one of the CAS [client
libraries](https://apereo.github.io/cas/6.1.x/integration/CAS-Clients.html#build-your-own-cas-client), which exist for various languages. In fact we won’t use
the Java client directly, but rather we’ll incorporate components that extend it. When evaluating CAS, I was a bit concerned by what appeared to be a
surprisingly limited selection of actively supported client libraries, and of course your results may vary, but we found software to meet our own needs without
too much difficulty.

### Configuring Wildfly Authentication

The most important application in the suite depends on the JAAS-based security subsystem of the [Wildfly application server](https://www.wildfly.org/) it’s
deployed to. Originally it used a custom [LoginModule](https://docs.oracle.com/javase/7/docs/api/javax/security/auth/spi/LoginModule.html) that inspected
request headers to find the ID of the authenticated user. Our first task was to configure our proxy server to remove this header from every request. We planned
to disable the old authentication system entirely, of course, but this change ensured that even if we mistakenly left it enabled somewhere, malicious users
couldn’t exploit it for access.

This application uses a declarative security policy: the deployment descriptor identifies a set of user roles, and another set of “security constraints”. Each
security constraint describes one or more URL patterns used in the application, and the set of user roles allowed to access URLs matching those patterns. Here
are two examples:

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

We installed the [cas-extension library](https://github.com/soulwing/cas-extension) in our Wildfly server to handle the CAS protocol. When an unauthenticated
user attempts to access a URL matching a pattern in one of the application’s security constraints, the CAS extension automatically intercepts control and
redirects the user to the CAS server. Assuming the user authenticates successfully, our application will receive another request with a service ticket
parameter. The cas-extension intercepts this request as well, validates the service ticket, and creates an “identity assertion”, which it sends to the Wildfly
security system. Wildfly’s role mapper queries a database to find the user’s roles, after which the authentication process is complete.

Configuration of the cas-extension begins with a CAS profile, a combination of the URL of the CAS server and the URL of the service the extension should
protect.

```xml
<subsystem xmlns="urn:soulwing.org:cas:1.0">
    <cas-profile name="default" service-url="https://our.application.server/application" server-url="https://our.cas.server"/>
</subsystem>
```

This tells the extension where to send authentication requests, where to listen for requests returning from the CAS server, and where to validate service
tickets. Next we need to validate that identity assertion, and figure out what roles belong to the user. This happens in a [Wildfly security
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

The last piece of the puzzle is a CAS deployment descriptor for our application, which activates cas-extension for that application. In its simplest form, this
is an empty file in the right place, but ours ended up a little more complex. It identifies both the CAS profile we want to use (unnecessary in this case, as
there’s only one CAS profile on the system, but it helped keep things more clear in our minds), and instructs the extension to load some other libraries into
our application.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<cas xmlns="urn:soulwing.org:cas:1.0">
  <profile>default</profile>
  <add-api-dependencies/>
</cas>
```

This configuration proved sufficient to let users log in and use the application, but as is sometimes the case with single sign-on, we needed a little more work
to let them log out properly. Each application in the suite sets a cookie in the user’s browser to identify its session. The CAS server likewise sets a cookie.
When a user logs out of the application, that application’s session cookie is destroyed, but we also need to destroy the CAS server’s session cookie as well as
the other applications’ cookies. Single log-out can be complicated, and I won’t go into the full setup here. One reason the CAS deployment descriptor loads
cas-extension libraries was so we could use cas-extension to generate the proper logout URL, and redirect our users to that URL once the application has
destroyed its own session.

### Configuring Spring Authentication

Another Java-based application in our suite uses Spring Security. [This document](https://docs.spring.io/spring-security/site/docs/3.0.x/reference/cas.html)
describes the bulk of the configuration, which seemed less straightforward than for cas-extension, but follows essentially the same mechanism. Here we
configured a Spring
[UserDetailsService](https://docs.spring.io/spring-security/site/docs/3.2.3.RELEASE/apidocs/org/springframework/security/core/userdetails/UserDetailsService.html)
to execute the same database query we used above to find the user’s roles. I’m not fully conversant in the large stack of beans Spring uses to manage the
process, and it took some time to get this configuration sorted out.

### Enter PHP

Two of these applications use PHP, which meant yet another configuration. Apereo maintains a [PHP client](https://github.com/apereo/phpCAS), which includes
several helpful examples. I tracked down the part of the application that authenticates users, and replaced the existing code with calls to phpCAS:

```php
phpCAS::client(CAS_VERSION_2_0, $phpCASHost, $phpCASPort, $phpCASContext);
phpCAS::forceAuthentication();
$_SESSION[EXPORT_SERVERNAME]['umdid'] = phpCAS::getUser();
```

The `forceAuthentication` call determines the current phase of the authentication process this request is in, whether it’s unauthenticated, fully authenticated, or
requires service ticket validation, and responds appropriately. We then set a session variable to the ID of the authenticated user, which replicates what
the original authentication code would have done.

One of these two applications requires authenticated access to a REST API exposed by the Wildfly application. CAS calls this “proxy” authentication, when one
application requests access to another. Here, CAS issues not only its usual service ticket, but also a “proxy granting ticket”. When the application wants to
use the API, it asks the CAS server for a service ticket, using the proxy granting ticket. The CAS server itself requires some new configuration in this case,
but for the PHP code, the only difference in the login phase from the simpler, non-proxy case is that we call `phpCAS::proxy` instead of `phpCAS::client` to
configure CAS. Later, when calling the service itself, we used more phpCAS services in place of the cURL library the original used.

```php
$service = \phpCAS::getProxiedService(PHPCAS_PROXIED_SERVICE_HTTP_GET);
$service->setUrl($serviceURL);
$service->send();
```

### The return of header authentication

Finally, we have a few automated tasks which use various APIs, and need to authenticate. We can’t redirect requests to a CAS server and expect a user to provide
credentials, so we’ve taken our cue from the applications’ original form, and configured CAS to recognize a “trusted header”. We add this header to any requests
issued by these automated jobs. Of course, we’ve also configured the proxy to disallow this header from any systems outside our internal network.

### A few loose ends

Of course, there were other considerations in this project that I’ve not covered here. Configuring CAS itself wasn’t necessarily straightforward, and included a
custom authentication module I hope to describe in a later article. Selecting among CAS server’s available
[deployment](https://apereo.github.io/cas/6.1.x/installation/Configuring-Servlet-Container.html)
[options](https://apereo.github.io/cas/6.1.x/installation/Docker-Installation.html) and fitting the winner into our existing infrastructure in a way that makes
it easy to manage and monitor was another task entirely. We needed to customize the server’s default user interface to prevent it from offering users an
imaginary method to recover forgotten passwords. The series of redirected browser requests involved in the CAS protocol presents a notable performance impact
under some circumstances. And it has taken me no small effort to learn to appreciate the CAS server’s sometimes distressingly circular
[documentation](https://apereo.github.io/cas/6.1.x/index.html). But several months into the project, CAS seems to be working well enough for our purposes that
other users of the same application suite have begun to express interest.
