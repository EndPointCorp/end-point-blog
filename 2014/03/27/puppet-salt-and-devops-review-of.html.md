---
author: Spencer Christensen
gh_issue_number: 955
tags: automation, cloud, conference, devops, puppet, salt
title: Puppet, Salt, and DevOps (a review of the MountainWest DevOps conference)
---

Last week I attended the MountainWest DevOps conference held in Salt Lake City, Utah. This was a one day conference with a good set of presenters and lightning talks. There were several interesting topics presented, but I’ll only review a few I wanted to highlight.

## I Serve No Master!

Aaron Gibson of [Adaptive Computing](http://www.adaptivecomputing.com/) discussed a very common problem with Puppet (and other configuration management systems): they work well in the scenario they were designed for but what about when the situation isn’t typical? Aaron had a situation where developers and QA engineers could instantiate systems themselves via OpenStack, however the process for installing their company’s software stack on those VMs was inconsistent, mostly manual, and took many hours. One of the pain points he shared, which I related to, was dealing with registering a puppet node with a puppet master- the sometimes painful back and forth of certificate issuing and signing.

His solution was to remove the puppet master completely from the process. Instead he created a bash wrapper script to execute a workflow around what was needed, still using puppet manifests on each system but run locally. This wrapper tool, called “Builder”, relies on property files to customize the config and allow the script to manage different needs. This new script allowed them to keep using puppet to manage these self-serve OpenStack servers gaining the benefits of consistency and removing manual setup steps, providing the ability to automate installs with Jenkins or other tools. But it freed them from having to use a puppet master for nodes that were disposable. It also helped to reduce software install time from 12 hours down to a 11 minutes.

His Builder tool is still an internal only tool for his company, but he discussed some next steps he would like to add, including better reporting and auditing of executions. I pinged him after the conference on twitter and mentioned that [Rundeck](http://rundeck.org/) might be a good fit to fill that gap. I used Rundeck for 2 years at my last job, integrating nicely with other automation tools and providing reporting and auditing as well as access control of arbitrary jobs.

## Automating cloud factories and the internet assembly line with SaltStack

Tom Hatch of [Salt Stack](http://www.saltstack.com/) spoke about Salt as an automation and remote execution platform. I’ve done quite a bit of work with Salt recently with a client and so I was pretty familiar with Salt. But one thing that he mentioned I didn’t know was that Salt was originally designed as a Cloud management tool, not necessarily a configuration management tool. However in the course of time configuration management became a higher priority for the Salt dev team to focus on. Tom mentioned that recently they have been working on Cloud management tools again- providing integration with Rackspace, AWS, xen, and more. I’ll have to dig more into these tools and give them a try.

## How I Learned to Stop Worrying and Love DevOps

Bridget Kromhout of [8thBridge](http://www.8thbridge.com/) spoke on the culture of DevOps and her journey from a corporate, strictly siloed environment to a small start-up that embraced DevOps. One of the first things she brought up that was different was the focus and approach to goals of each organization. In an organization where Ops teams are strictly separate from Developers, they often butt heads and have a limited vision of priorities. Each focuses on the goals of their own team or department, and have little understanding of the goals of the other departments. This leads to an adversarial relationship and culture of not caring much about different teams or departments.

In contrast, the organization that embraces DevOps as a culture will see to it that Ops and Devs work together on whatever solution best reaches the goals of the whole organization. In doing so, barriers will have to be questioned. Any “special snowflake” servers/applications/etc. that only one person knows and can touch can’t exist in this culture. Instead, any unique customizations need to be minimized through automation, documentation (sharing knowledge), and reporting/monitoring. This doesn’t mean root access for all- but it means reducing barriers as much as possible. Good habits from the Ops world to keep include: monitoring, robustness, security, scaling, and alerting.

The main pillars of DevOps are: culture, automation, measurement, and sharing. Culture is important and can be supportive or rejecting of the other pillars. Without a culture in the organization that supports DevOps, it will fizzle back into siloed "us vs. them" enmity.

Thanks to all the presenters and those that put on the conference. It was a great experience and I am glad I attended.

## Links

- [Slide deck for Aaron Gibson: “Serve No Master!”](https://github.com/biggiemac/mtnwest_prez/blob/master/I%20Serve%20No%20Master!%20-%20Aaron%20Gibson%20-%20MTN%20West%20DevOps%202014.pdf)
- [Slide deck for Bridget Kromhout: DevOps culture](http://www.slideshare.net/bridgetkromhout/how-i-learnedtostopworryingandlovedevops201403)
