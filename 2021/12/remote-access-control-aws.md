---
title: "Remote Access Control with AWS Security Groups"
author: Ardyn Majere
tags:
- cloud
- security
- networking
github_issue_number: 1808
date: 2021-12-23
---

![Utah salt flats with no trespassing sign](/blog/2021/12/remote-access-control-aws/salt-flats.jpg)

<!-- Photo by Seth Jensen -->

With the onset of COVID-19, a lot of companies started working remotely and had to allow their employees to access systems remotely while keeping unwanted traffic out.

As a company of almost all remote workers, even pre-pandemic, we have long had a solution for this. We have a web application that allows people to register their current IP address with one or more servers to gain access to SSH, SFTP, databases, and other services that aren’t open to the public.

The application relies on `iptables` (Linux) or `pf` (OpenBSD) to give people access to the system. For customers that are using cloud providers like AWS, we added support for this application to work with AWS Security Groups.

### The Basics

The system uses a single web application and relies on the [Apache `mod_authn_file` format](https://httpd.apache.org/docs/2.4/mod/mod_authn_file.html#authuserfile) and `htpasswd` command to create users and hashed passwords for the system. `htpasswd` allows you to create bcrypt, MD5, SHA-1, and Unix crypt passwords. We suggest using bcrypt wherever possible, since it is the only one that is not fairly easily reversible nowadays.

The system also allows for grouping of users to allow them access to different sets of systems. These are handled by the simple [Apache `mod_authz_groupfile` format](https://httpd.apache.org/docs/2.4/mod/mod_authz_groupfile.html) that looks like this:

```plain
web: richard, joe, jon
dbs: richard, jon
```

The data format is the group followed by a colon (:), then a comma-separated list of users who should be allowed to access that service. In this example, the users `richard`, `joe`, and `jon` would be allowed to access the `web` group but only `richard` and `jon` would be allowed to access the `dbs` group.

The groups in this file then dictate what servers and services you are allowed to access. For example, the `dbs` group might allow you ssh and database connectivity to the specific production and replication database systems in AWS. It does this by adding rules to the proper security groups in AWS via their API.

We typically set up two different security groups that a set of servers can use: a static whitelist and a dynamic whitelist. The static whitelist is populated with IP addresses that should always be allowed in. This could be anything from a set of IP addresses for people still working at the office to employees’ dedicated IP addresses from their ISPs. This could also be certain other systems (remote data sources or such) that would need access to these systems. The dynamic whitelist is what the web application will add rules to after someone enters their proper username and password. 

### The API layer

Now that we’ve reviewed the way to setup users and the way users can be organized into groups, we can talk about how the web application interfaces with AWS itself.

After the user passes the username and password validation, the system will use the AWS API key to add the user to the appropriate security groups. We need certain information about each security group we are going to add people to: the Security Group ID, description, profile, and region. We also need to know what ports we are going to open for someone for this group.

So using our previous example, if we are going to be granting access to the user `jon` and giving him access to the web servers then we’d want to open up ports 443 (https) and probably port 80 (http). The same goes with granting access to the database servers: give `jon` access to whatever port the database allows you to connect on. 

### The Security Group Layer

The secret sauce in this is interfacing with AWS’s security group.

Create a new security group in the account—one per server or logical group (e.g. port 22 on all servers).

Then create a new IAM account. Go to the IAM menu and click on Groups in the side tab. 

- Click “create a group”
  - Name the group `whitelist-user-group_id`
- Click “Create Policy”
  - Choose Service “Ec2”
  - Set the following permissions:  
    ```plain
    List (4 of 123 actions)
    DescribeSecurityGroupReferences
    DescribeSecurityGroups
    DescribeStaleSecurityGroups
    DescribeVpcs

    Write (4 of 285 actions)
    AuthorizeSecurityGroupEgress
    AuthorizeSecurityGroupIngress
    RevokeSecurityGroupEgress
    RevokeSecurityGroupIngress
    ```

> Hint: You can find all but one of these by searching 'SecurityGroup', and the last one by searching for DescribeVpcs

The write functions you'll need to attach to a specific security group or groups, which you created earlier. 

When you're done, you should have:

**User** (`whitelist_groupid`) → in **group** (`whitelist_group_groupid`) → with attached **policy** (`pol-whitelist`) → with the above eight permissions, the four latter ones pointed at your new security group.

Attach the security group to your VM.

You’ll need to make calls to the security groups over the API. You can find more info about the API call for changing firewall rules in [AWS’s docs](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_UpdateSecurityGroupRuleDescriptionsIngress.html).

### When the layers combine

With these pieces in place, you can start thinking about what groups would give people access to what. How widespread or granular you want to be is up to you! If you want to have a group that gives access to every system and all the ports (maybe for your operations team), go for it! If you want to have a group that just needs access to https on certain systems (like a sales and marketing team) then you can easily control that as well.

