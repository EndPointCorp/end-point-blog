---
author: "Dylan Wooters"
title: "8 Simple Steps to Saner Software Development"
tags: development, environment, devops
gh_issue_number: 1365
---

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2016/11/10/8-simple-steps-to-saner-software-development/layercake.jpg"/></div>

While these might seem obvious for seasoned developers, many projects, especially legacy software, still fail to follow most of the steps below.

In future posts, I’ll expand on these steps and give more details. For now, here’s an overview of some basic guidelines for making the process of software development smoother (& saner) for both the client and the dev team.

### Separate environments:

Ideally there should be Dev, QA, UAT/Staging, and Production environments. And, UAT/Staging should be as close to Production as possible. It’s amazing how many software projects are still done on someone’s local machine and pushed directly to Production.

### Use a bug tracking tool:

This is pretty obvious. Bugs need to be logged and labeled so that they can be tracked through stages of development (i.e., To-Do, In Progress, Completed). Using a bug tracking tool like Jira or GitHub also helps the non-technical stakeholders comment on and clarify requirements/issues.

### Have a source control strategy:

It doesn’t have to be fancy. For example, if you’re using Git, it should be more than having multiple developers working out of the master branch. Ideally link branches to features or bugs defined in a bug tracking tool, and keep in mind the separation of environments, especially if the application is already in Production.

### Do pull/merge requests:

Even a short five minute review will improve the overall quality of code, reduce bugs, and communicate changes between developers responsible for different parts of the application. Web-based source control systems like GitLab, GitHub, and Bitbucket make this simple.

### Write unit tests:

A lot of developers either feel pressure to move quickly or get lazy and don’t write tests. Regression testing becomes a nightmare without unit tests. Plus it makes you feel better to see all those tests passing.

### Use a continuous integration tool:

[TeamCity](https://www.jetbrains.com/teamcity/), [Jenkins](https://jenkins-ci.org), or even basic [GitHooks](http://githooks.com) are some options. Automated deployments save time and, if integrated with unit tests, reduce the bugs that make it to Production.

### Setup notifications:

If the CI tool alerts team members of deployment status, hundreds of “is the deployment done yet?” emails and chat messages can be saved. Slack integration is a good option here.

### Consolidate project credentials:

Have a secure and centralized location for managing passwords. We like keeping a KeePass checked into the relevant project’s repo.
