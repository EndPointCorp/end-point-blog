---
author: Dylan Wooters
title: "Separate and Not Equal: Development Environments to Support People, Process, and Automation"
tags: development, environment, devops
gh_issue_number: 1367
---
<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2017/01/18/separate-not-equal-dev-environments/bauhausstage.jpg"/></div>

I believe in the separation of software environments for the long term peace and prosperity of developers, product owners, and users. Ideally, there’s a dedicated environment purpose-built to support each community: the developers, the testers, the acceptors, and the users.

I learned this process from taking part in software development projects over the course of many years and working with a variety of different teams, including my own dev team, our clients’ in-house IT teams, and often other consulting firms. While each group had its own approach, one consistent factor for success was the separation of environments to support key roles.

###Dev

Development environments will vary by project and technology stack. A common decision is developing locally or creating a remote VM, and both approaches have trade-offs. Developing remotely allows you to setup an environment that mirrors QA and Production, and it also allows you to use remote desktop to connect to your dev environment from any machine: PC, Mac, or Linux. However, developing remotely comes with latency, and often it doesn’t feel as smooth as working locally. More importantly, if I find myself traveling or otherwise without a stable internet connection, developing remotely can be challenging if not impossible.

The setup of the dev environment should be quick and painless, and the project should have clear documentation on how to get started developing. We often keep this in a Wiki in the project’s Git repository. Pairing this documentation with a pre-built dev environment is the ultimate way to get new developers up-and-running. This can be done by packaging up a VM, which can then be run locally or remotely using virtualization software like [VirtualBox](www.virtualbox.org) or a cloud platform like [AWS](https://aws.amazon.com). [Vagrant](https://www.vagrantup.com) is another option worth checking out, as it touts a one-command setup of a complete dev environment.

###QA
The QA environment serves two purposes: as a place where various team members’ code can be built and run together, and a place where the specific task of QA can be performed. When you move to QA testing, it’s a good idea to create a separate branch in source control.This allows developers to push to a common QA branch, which can then be deployed to the QA environment, ideally using a CI tool like TeamCity.

Once the QA testers have signed off, you can move into the UAT/Staging environment. It’s crucial that this environment match production as closely as possible, to rule out any “environmental bugs” that may creep in after deployment to Production. This means ensuring that all the framework versions match (.NET, Node, etc.), system resources are similar, and that the same security is in place (firewalls, VPNs). The data should also replicate what will be found in production, if not outright synced from production using a tool like [SQL Delta](https://www.sqldelta.com/).

###Stage
In staging, the software is put before a specially designated group of users for a dress rehearsal.

If I’m developing a desktop or mobile application (not a web app), I ensure that testing on a variety of different OS versions is incorporated into the UAT process. For example, I use Apple’s [TestFlight](<https://developer.apple.com/testflight/) to test across a variety of devices using different iOS versions.

###Prod
Production is the main stage, and code should obviously only be pushed there after proper testing. Even if I have customers, clients, and/or bosses yelling at me, I try and resist the urge to push a fix directly to Production! Although the fix may have worked perfectly in my dev environment, it might not work in production, and then I can easily find myself in even deeper trouble than before. If there is not time to coordinate UAT, then at the very least I push to QA, where the build can be verified in a separate environment, and another set of eyes can perform some testing. It goes without saying that all of this can be made less frightful with unit testing, a topic that we will explore later.

It’s also important to ensure that production has adequate resources before going live. If I’m building a new version or replacement of existing software, I review the existing reporting/​analytics to know things like concurrent user count and storage requirements per user. This may seem obvious, but in the rush to get software out to market, basic things can be overlooked. Also, I ensure that I have some baseline security in place on production. This means encrypting sensitive data in config files, not storing passwords (just salted hashes!), and if I’m using a cloud provider like AWS or Azure, I add two-factor authentication to the admin account.
