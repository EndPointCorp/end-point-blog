---
author: Spencer Christensen
gh_issue_number: 904
tags: automation, devops, puppet, salt
title: Setting a server role in Salt (comparing Puppet and Salt)
---

There are many ways to solve a given problem, and this is no truer than with configuration management.  Salt ([http://www.saltstack.com](http://www.saltstack.com)) is a fairly new tool in the configuration management arena joining the ranks of Puppet, Chef, and others.  It has quickly gained and continues to grow in popularity, boasting its scalable architecture and speed.  And so with multiple tools and multiple ways to use each tool, it can get a little tricky to know how best to solve your problem.

Recently I've been working with a client to convert their configuration management from Puppet to Salt.  This involved reviewing their Puppet configs and designs and more-or-less mapping them to the equivalent for Salt.  Most features do convert pretty easily.  However, we did run into something that didn't at first- assigning a role to a server.

We wanted to preserve the "feeling" of the configs where possible.  In Puppet they had developed and used a convention for using some custom variables in their configs to assign an "environment" and a "role" for each server.  These variables were assigned in the node and role manifests.  But in Salt we struggled to find a similar way to do that, but here is what we learned.

In Puppet, once a server's "role" and "environment" variables were set, then they could be used in other manifest files to select the proper source for a given config file like so:

```
    file    {
        "/etc/rsyslog.conf":
            source  =>
            [
                "puppet:///rsyslog/rsyslog.conf.$hostname",
                "puppet:///rsyslog/rsyslog.conf.$system_environment-$system_role",
                "puppet:///rsyslog/rsyslog.conf.$system_role",
                "puppet:///rsyslog/rsyslog.conf.$system_environment",
                "puppet:///rsyslog/rsyslog.conf"
            ],
            ensure  => present,
            owner   => "root",
            group   => "root",
            mode    => "644"
    }
```

Puppet will search the list of source files in order and use the first one that exists.  For example, if $hostname = 'myniftyhostname' and $system_environment = 'qa' and $system_role = 'sessiondb', then it will use rsyslog.conf.myniftyhostname if it exists on the Puppet master, or if not then use rsyslog.conf.qa-sessiondb if it exists, or if not then rsyslog.conf.sessiondb if it exists, or if not then rsyslog.conf.qa if it exists, or if not then rsyslog.conf.

In Salt, environment is built into the top.sls file, where you match your servers to their respective state file(s), and can be used within state files as {{ env }}.  Salt also allows for multiple sources for a managed file to be listed in order and it will use the first one that exists in the same way as Puppet.  We were nearly there; however, setting the server role variable was not as straight forward in Salt.

We first looked at using Jinja variables (which is the default templating system for Salt), but soon found that setting a Jinja variable in one state file does not carry over to another state file.  Jinja variables remain only in the scope of the file they were created in, at least in Salt.

The next thing we looked at was using Pillar, which is a way to set custom variables from the Salt master to given hosts (or minions).  Pillar uses a structure very similar to Salt's top.sls structure- matching a host with its state files.  But since the hostnames for this client vary considerably and don't lend themselves to pattern matching easily, this would be cumbersome to manage both the state top.sls file and the Pillar top.sls file and keep them in sync.  It would require basically duplicating the list of hosts in two files, which could get out of sync over time.

We asked the salt community on #salt on Freenode.net how they might solve this problem, and the recommended answer was to set a custom grain.  Grains are a set of properties for a given host, collected from the host itself- such as, hostname, cpu architecture, cpu model, kernel version, total ram, etc.  There are multiple ways to set custom grains, but after some digging we found how to set them from within a state file.  This meant that we could do something like this in a "role" state file:

```
# sessiondb role
# {{ salt['grains.setval']('server_role','sessiondb') }}

include:
  - common
  - postgres
```

And then within the common/init.sls and postgres/init.sls state files we could use that server_role custom grain in selecting the right source file, like this:

```
/etc/rsyslog.conf:
  file.managed:
    - source:
      - salt://rsyslog/files/rsyslog.conf.{{ grains['host'] }}
      - salt://rsyslog/files/rsyslog.conf.{{ env }}-{{ grains['server_role'] }}
      - salt://rsyslog/files/rsyslog.conf.{{ grains['server_role'] }}
      - salt://rsyslog/files/rsyslog.conf.{{ env }}
      - salt://rsyslog/files/rsyslog.conf
    - mode: 644
    - user: root
    - group: root
```

This got us to our desired config structure.  But like I said earlier, there are probably many ways to handle this type of problem.  This may not even be the best way to handle server roles and environments in Salt, if we were more willing to change the "feeling" of the configs.  But given the requirements and feedback form our client, this worked fine.
