---
author: Ron Phipps
title: DevCamps on different systems, including Plesk, CPanel and ISPConfig
github_issue_number: 249
tags:
- camps
- hosting
- interchange
- testing
date: 2010-01-08
---



In the last few months I’ve been active setting up [DevCamps](http://www.devcamps.org) for several of our newer clients. DevCamps is an open source development environment system, that once setup, allows for easily starting up and tearing down a development environment for a specific site/code base.

I’ve done many camps setups, and you tend to run into surprises from system to system, but what was most interesting and challenging about these latest installs was that they were to be done on systems running Plesk, CPanel, and ISPConfig. Some things that are different between a normal deployment and one on the above mentioned platforms are:

- On the Plesk system there was a secured Linux called ‘Atomic Secured Linux’ which includes the grsecurity module. One restriction of this module is (TPE) Trusted Path Execution which required the camp bin scripts to be owned by root and the bin directory could not be writable by other groups, otherwise they would fail to run.

- Permissions are a mixed bag, where typically we set all of the files to be owned by the site owner, in Plesk there are special groups such as psacln that the files need to be owned by.

- On the CPanel system we needed to move the admin images for Interchange to a different directory since CPanel includes Interchange and has aliases for /interchange/ and /interchange-5/ to point at a central location which we would not be using.

- On ISPConfig and Plesk the home directories of the sites are in different places, which required deploying the code in such places as /var/www/clients/client/user/domain.com or /var/www/vhosts/domain.com.

In the end we were able to get DevCamps to run properly on these various platforms both in development and production. If you are starting a new project or working on an existing project and could use a strong development environment, consider [DevCamps](http://www.devcamps.org).


