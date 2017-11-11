---
author: Joshua Tolley
gh_issue_number: 558
tags: java, pentaho
title: Spring authentication plugin
---

One of our clients regularly deploys [Pentaho](http://www.pentaho.com/) with their application, and wanted their users to be able to log in to both applications with the same credentials. We could, of course, have copied the user information from one application to another, but Pentaho, and the Spring system it uses for authentication, allows us to be much more elegant.

[Spring](http://www.springsource.org/) is often described as an "application development framework", or sometimes an ["Inversion of Control container"](http://en.wikipedia.org/wiki/Spring_Framework), which essentially means that you can redefine, at run time, exactly which objects perform various services within your application. That you have to navigate a bewildering and tangled web of configuration files in order to achieve this lofty goal, and that those files suffer from all the verbosity you'd expect from the combined forces of XML and Java, normally isn't as loudly proclaimed. Those inconveniences notwithstanding, Spring can let you do some pretty powerful stuff, like in our case, redefining exactly how a user gets authenticated by implementing a few classes and reciting the proper incantation in the configuration files.

Spring handles most of the plumbing in the Pentaho authentication process, and it all starts with this particular definition from one of the Spring configuration files:

<script src="https://gist.github.com/1902255.js"> </script>

The authenticationManager bean contains a list of authentication processors, and here's where our custom code begins. These beans must implement the [Spring AuthenticationProvider interface](http://static.springsource.org/spring-security/site/docs/3.1.x/apidocs/org/springframework/security/authentication/AuthenticationProvider.html), and to customize the authentication we can just put a new bean in this list. The list is ordered; refer to the [ProviderManager](http://static.springsource.org/spring-security/site/docs/3.1.x/apidocs/org/springframework/security/authentication/ProviderManager.html) documentation for details, but essentially any of the beans in the list can accept a set of credentials. Here, we've simply added a reference to our new bean, to the beginning of the list. The new bean is indicated by name only; it needs to be defined elsewhere, like this:

<script src="https://gist.github.com/1902423.js"> </script>

Here we've mapped the bean name to a specific class name. We can also add whatever configuration properties we need. So long as there are corresponding setter methods in the actual code (e.g. "public void setProperty_1(String value)") these will Just Work. Along with these setter methods, we must implement the two methods in Spring's AuthenticationProvider interface. The most important is the aptly-named [authenticate()](http://static.springsource.org/spring-security/site/docs/3.1.x/apidocs/org/springframework/security/authentication/AuthenticationProvider.html#authenticate(org.springframework.security.core.Authentication)), which Spring will call when a user tries to log in.

authenticate() gets one argument, an Authentication object, and when a user presents valid credentials, that's also what it returns. The first thing our new implementation needs to do is get the username and password from the authentication object:

<script src="https://gist.github.com/1902398.js"> </script>

At this point we've got two jobs to do: first, validate the credentials, and second (assuming the credentials are valid), determine what roles the user should be given. In this particular case we used the authentication database from the client's application to validate the credentials; that code will be completely different from one bean to the next, so I won't share it here, but the second part, finding the user's roles, is pretty consistent. Spring lets you set up as many roles as you'd like, giving each a different text name, and simply assumes all the different roles will mean something to the application (Pentaho, in this case) later on. For our setup, we look up the user's roles from a database, and then tell Spring about them like this:

<script src="https://gist.github.com/1902541.js"> </script>

At this point, the user has successfully logged in. If we didn't want to allow the user in, we could instead throw an AuthenticationException, and Spring would go on to next AuthenticationProvider in the list. The beauty of it all is now that I have a working plugin, I can modify my application's authentication system simply by modifying a configuration file or two (or three) and restarting the application.
