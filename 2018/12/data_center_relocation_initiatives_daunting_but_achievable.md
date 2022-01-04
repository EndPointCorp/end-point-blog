---
author: Charles Chang
title: 'Data Center Relocation Initiatives: Daunting But Achievable'
github_issue_number: 1475
tags:
- windows
- virtualization
- storage
- networking
- integration
- environment
- disaster-recovery
- hardware
date: 2018-12-20
---

![Datacenter room](/blog/2018/12/data_center_relocation_initiatives_daunting_but_achievable/banner.jpg)
[Photo by Seeweb · CC BY-SA 2.0, cropped](https://www.flickr.com/photos/seeweb/9771315606/)

### Introduction

A customer asked for our help dealing with logistical nightmares they encountered during a hardware update and data center relocation project. The customer had two active data centers, and wanted to relocate one of them to a modern Tier 4 facility to improve its performance and provide redundancy for critical systems. They also wanted to consolidate or decommission equipment to reduce recurring expenses and reduce their carbon footprint. The client decided to move to a Tier 4 data center because they provide across-​the-​board redundancy within the data center.


### Moving forward with Tier IV

<p>
<img align="right" src="/blog/2018/12/data_center_relocation_initiatives_daunting_but_achievable/data-center-1.jpg" style="margin: 1em" width="200">
Enterprises typically transition to Tier 4 data centers because they offer the highest uptime guarantees, and have no single points of failure. These facilities are fully redundant in terms of electrical circuits, cooling, and networking. This architecture is best able to withstand even the most serious technical incidents without server availability being affected. Tier IV facilities have contracts with disaster management companies who will provide them, for example, with fuel in the event that a natural disaster damages the power grid.
</p>

(More information about the four data center levels is at the end of this post.)

### Key Issues

Some of the customer’s key concerns were:

1\. To safely move their virtual environment to the new data center.

2\. To protect assets during the relocation.

3\. To completely shut down the current data center and migrate seamlessly to the new data center.

4\. To update external DNS records without causing any downtime for the web applications used by their customers.

### Project Planning

To manage data center relocations is challenging because there are many moving parts and variables. Typically, planning starts 6 months ahead of the scheduled relocation date. We seek to understand the role of each system by consulting in-depth with all the teams involved. We analyze each part of the client’s tech infrastructure, break it down, and strategize about the best approach for handling the migration of each component. Additional time to plan can help especially when a large group of stakeholders is involved. Successful planning requires hard and sometimes extensive work, but makes an otherwise overwhelming data center migration smooth and worry free.

Here are some of our procedures for pre-​migration preparation:

1\. Process the paperwork for new hardware. Identify, review, and approve all applications. Hire movers. Schedule and coordinate with internal management and key stakeholders like IT staff, system admins, contractors, circuit providers, etc.<img align="right" src="/blog/2018/12/data_center_relocation_initiatives_daunting_but_achievable/data-center-2.jpg" style="margin: 1em" width="200"/>

2\. Collect and analyze resource usage associated with the critical and non-critical systems and compare resource needs to resource availability at the new facility.

3\. Design and schedule the migration of critical systems to the new data center. Discuss the plan with key stakeholders.

4\. Make sure replicas of critical systems are up to date.

5\. Set up a new environment with new hardware in the new data center and establish network connections.

6\. Prepare hardware and virtualization technology in the new data center.

7\. Test, retest, and burn in the new hardware (2–4 weeks of testing).

8\. Create a non-​essential server within the virtualization environment and test it.

### A Challenge: Eliminating Downtime
<img align="right" src="/blog/2018/12/data_center_relocation_initiatives_daunting_but_achievable/data-center-3.jpg" style="margin: 1em" width="200"/>

To minimize or eliminate downtime requires very careful preparation. With this particular client, we had the luxury of their already having a secondary data center, which could accommodate a majority of the critical systems during the migration.

We originally planned to leverage this by simply changing the external DNS records to point to this data center during the migration, but during planning determined that the external DNS record would not replicate worldwide quickly enough to meet the uptime needs of their global operation.

### Solutions

After discussing various approaches, we ended up using a load balancer. A load balancer is a network device that routes incoming traffic destined for a single destination (web site, application, or service) and ‘shares’ the incoming connections across multiple destination devices or services. In this case, the data center we were to migrate to housed the client’s critical systems like web servers, database, etc. The secondary data center housed a replica of the critical systems using a replication technology, e.g. Actifio, Rubrik, SAN mirroring, VMWare SRM, or Zerto — we used Actifio in this scenario.
<img align="right" src="/blog/2018/12/data_center_relocation_initiatives_daunting_but_achievable/data-center-4.jpg" style="margin: 1em" width="200"/>

The customer had multiple systems with external DNS records and public IP addresses. We did not change the public DNS names for the critical systems. We did change the public IP addresses associated with the public DNS names, to point to the load balancer, which then pointed to the appropriate data center throughout the process. This setup enabled a gradual, flexible, and fully controlled transition to the new data center.

### Summary
<img align="right" src="/blog/2018/12/data_center_relocation_initiatives_daunting_but_achievable/data-center-5.jpg" style="margin: 1em" width="200"/>

Our client wanted to reduce their servers’ power usage 40% by consolidating into a hyper-​converged system. Other goals were to reduce floor space by 50%, and monthly recurring data center charges by 50%. We transitioned them to a new hardware stack (compute, storage, network, backup environment) in a Tier 4 data center, and saved them 50% percent on data center operation costs. Additionally, during the process we corrected issues associated with disaster recovery and business continuity, leaving the client’s operations more resilient, affordable, and more secure.

<hr>

### Appendix: Data Center Classifications

#### Tier IV (Best)

Tier IV data centers have redundancies for every process and data protection stream. No single outage or error can shut down the system. To keep Tier IV ranking, data centers must have 99.995% minimum uptime per year. They come equipped with 2N+1 infrastructure (two times the amount required for operation plus a backup), which is considered “fully redundant.”

#### Tier III (Average)

N+1 (the amount required for operation plus a backup) fault tolerance, which means a Tier III facility can undergo routine maintenance without a hiccup in operations. 99.982% minimum uptime per annum, used for maintenance and overwhelming emergencies.

#### Tier II (Minimal)

99.749% minimum uptime. Tier II facilities have considerably more downtime than Tier III facilities, primarily because Tier II facilities have less redundancy. They do however have partial cooling redundancy and multiple power redundancies.

#### Tier I (Basic, Cheapest)

99.671% minimum uptime, with 28.8 hours of downtime each year.
