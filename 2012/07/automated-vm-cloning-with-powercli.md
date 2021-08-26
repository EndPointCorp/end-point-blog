---
author: Brian Buchalter
title: Automated VM cloning with PowerCLI
github_issue_number: 672
tags:
- hosting
- sysadmin
- virtualization
date: 2012-07-23
---



Most small businesses cannot afford the high performance storage area networks (SANs) that make traditional redundancy options such high availability and fault tolerance possible. Despite this, the APIs available to administrators of virtualized infrastructure using direct attached storage (DAS) make it possible to recreate many of the benefits of high availability.

### High Availability on SAN vs DAS

A single server failure in a virtualized environment can mean many applications and services can become unavailable simultaneously; for small organizations, this can be particularly damaging. High availability with SANs minimize the downtime of applications and services when a host fails by keeping virtual machine (VM) storage off the host and on the SAN. VMs on a failed host can then be automatically restarted on hosts with excess capacity. This of course requires SAN infrastructure to be highly redundant, adding to the already expensive and complex nature of SANs.

Alternatively, direct attached storage (DAS) is very cost effective, performant, and well understood. By using software to automate the snapshot and cloning of VMs via traditional gigabit Ethernet from host to host, we can create a “poor man’s” high availability system.

It’s important for administrators to understand that there is a very real window of data loss that can range from hours to days depending on the number of systems backed up and hardware in use. However, for many small businesses who may not have trustworthy backups, automated cloning is an excellent step forward.

### Automated cloning with VMWare’s PowerCLI

Although End Point is primarily an open source shop, my introduction virtualization was with VMWare. For automation and scripting, PowerCLI, the PowerShell based command line interface for vSphere, is the platform on which we will build. The process is as follows:

- A scheduled task executes the backup script.
- Delete all old backups to free space.
- Read CSV of VMs to be backed up and the target host and datastore.
- For each VM, snapshot and clone to destination.
- Collect data on cloning failures and email report.

I have created a public GitHub repository for the code and called it [powercli_cloner](https://github.com/bbuchalter/powercli_cloner).

Currently, it’s fairly customized around the needs of the particular client it was implemented for, so there is much room for generalization and improvement. One area of improvement is immediately obvious: only delete a backup after successfully replacing it. Also, the script must be run as a Windows user with administrator vSphere privileges, as the scripts assumes pass-through authentication is in place. This is probably best for keeping credentials out of plain text. The script should be run during non-peak hours, especially if you have I/O intensive workloads.

Hopefully this tool can provide opportunities to develop backup and disaster recovery procedures that are flexible, cost-effective, and simple. I’d welcome pull requests and other suggestions for improvement.


