---
author: Charles Chang
title: 'Data Center Relocation Initiatives'
tags: integration, disaster-recovery, datacenter, infrastructure 
gh_issue_number: 1462
---

### Data Center Relocation Initiatives: Daunting But Achievable ###

#### Introduction ####

A customer was running into a logistical nightmares during a hardware refresh and data center relocation project, and needed some expert advice to complete the task. The customer had two active data centers, and needed to relocate one of the active data centers to a modern Tier 4 data center to improve its  performance and offer redundancy for critical systems. The customer decided to move to a more modern data center in order to consolidate or decommission equipment to reduce their carbon footprint, eliminate recurring expenses, and establish green IT systems. The client decided on a Tier 4 datacenter due to the prospect of redundancy across the board within the data center. Below each Tier is explained in detail.

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image05.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="Decommissioning Cabinets and Wires" width=250 height=333 />

##### Tier IV Data Center Requirements (Best) #####
Tier IV providers have redundancies for every process and data protection stream. No single outage or error can shut down the system. 99.995 % uptime per annum. This is the level with the highest guaranteed uptime and must be maintained well for a data center to keep up Tier IV ranking. 2N+1 infrastructure (two times the amount required for operation plus a backup). 2N+1 is another way of saying “fully redundant.”

##### Tier III Data Center Requirements (Average) #####
N+1 (the amount required for operation plus a backup) fault tolerance. A Tier III provider can undergo routine maintenance without a hiccup in operations. No more than 1.6 hours of downtime per annum. This downtime is allowed for purposes of maintenance and overwhelming emergency issues.

##### Tier II Data Center Requirements (Minimal) #####
No more than 22 hours of downtime per annum. There is a considerable jump between levels II and III regarding downtime. Redundancy is one of the primary reasons for this. 99.741 % uptime per annum is the minimum uptime for this type of provider. Partial cooling and multiple power redundancies.

##### Tier I Data Center Requirements - no redundancy (Basic, Cheapest) #####
No more than 28.8 hours of downtime per annum. These facilities are allowed the highest amount of downtime of any level.

---

##### Key Issues #####

**Some of the key issues the customer mentioned were:**<br>

1\. How to move the virtual environment to the new data center.<br> <br>
2\. How to protect assets during the relocation.<br> <br>
3\. How to completely shut down the current data center and migrate seamlessly into the new data center.<br> <br>
4\. How to update external DNS records without creating downtime to the web application used by customers. <br> <br>
5\. How to seamlessly allow our customers access to the secondary data center which will temporary house the critical systems during the migration. <br> 

Key to a successful migration project is to understand how, when and where to migrate critical and non-critical systems. Basically, before the day of the relocation, the goal is to relocate or shutdown the systems residing in the data center being relocated.

---

#### Moving forward with Tier IV ####

The main reason an enterprise company would seek a Tier 4 data center is because it offers the highest level of guarantee that a data center can provide, with 99.99% availability with zero single points of failure. This tier is fully redundant in terms of electrical circuits, cooling and networking. This architecture can withstand even the most serious of technical incidents without server availability ever being affected. In a situation like the recent Hurricane Sandy that hit New York a few years ago, the data center is contracted with a company to deliver diesel fuel to the complex to sustain their generators during a power outage. Typically in a situation like hurricane Sandy, the data center will mobilize their disaster recovery procedure to support and sustain their services to their customer.

---

#### Getting Started ####

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image04.jpg" style="float: left; margin: 10px 25px 15px 15px" alt="Data Center Hardware Removal and Clean Up" width=250 height=333 />
It seems like a daunting task, but the most important part of a data center migration project is  to make the critical systems available again after migration. For this particular client, we had the luxury of a second data center with adequate resources to accommodate a majority of the critical systems coming over from the data center being relocated. If the client did not have a 2nd data center to work with, then a different proposal and strategy would be needed. In this case, the client had a secondary data center to work with ample resources to work with. We originally planned to change the external DNS records to point to the correct data center, but we  were worried that the external DNS record would not replicate worldwide quickly enough to meet the needs of their global operation. 

---
#### Solutions ####

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image03.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="New Data Center Cabinets" width=250 height=333 />
We threw around some ideas and ended up using a load balancer to resolve two issues with one technology. A load balancer is a network device that routes incoming traffic destined for a single destination (web site, application, or service) and 'shares' the incoming connections across multiple destination devices or services. In this case, the data center being migrated originally housed the critical systems like web servers, sql, etc. The secondary data center housed a replica (offline copy) of the web servers, SQL, etc using a replication technology. (Actifio, Rubrik, SAN mirroring, VMware SRM, Zerto, etc) These are all potential tools/systems to use in a migration project. 
 
The customer had multiple systems with external DNS records and public IP addresses. The public DNS name for each critical system will not change. The public IP associated with the public DNS name will change, and point to the load balancer which then points to the correct data center servicing the critical systems. This setup enables a gradual, flexible, and fully controlled transition to the new data center.

---

#### Project Planning ####

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image02.jpg" style="float: left; margin: 10px 25px 15px 15px" alt="Pure Flex Hyper-Converged Hardware Stack" width=250 height=333 />
A data center migration and relocation project could be overwhelming, but proper planning can make the process smooth and worry free. The planning stage requires hard work and preparation, but is necessary for a successful relocation. 
 
Our approach is to break down each part of the data center relocation, analyze it, and strategize about the best approach to each task. Typically, planning would start 6 months +/- ahead of the scheduled relocation date. Some customers might need additional time to plan if there is a large group of stakeholders involved.
Here is an example of what needs to be completed ahead of the data center migration:


**For example what needs to be completed ahead of the data center migration?**<br>

1\. Process the paperwork for new hardware, approve all applications, hire movers, schedule and coördinate with internal management team and key stakeholders like IT staffs, system admins, contractors, circuit providers, etc.<br><br>
2\. Collect and analyze resource usage associated with the critical and non-critical systems and compare to resource availability at the new facility.<br><br>
3\. Design and schedule critical systems migration to secondary data center. Discuss plan with key stakeholders.<br>

**Samples of Pre-Relocation Task**

1\. Set up a new environment with new hardware in the new data center and establish network connections.<br><br>
2\. Make sure replicas of critical systems are up to date. <br><br>
3\. Prepare hardware and virtualization technology in new data center. <br><br>
4\. Test, retest, and burn in the new hardware. (2-4 weeks of testing)<br><br>
5\. Create a non-essential server within the virtualization environment and test it.<br>

Covering all aspects of the data center relocation is daunting since there are many moving parts and variables to deal with. Brainstorming between teams and dissecting an inventory of all system helps us understand the role of each system  and allows us to decide the how to to execute a seamless and successful relocation.
 

--- 

#### Summary ####

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image01.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="Pure Flex Cabinet" width=250 height=333 />
Data center migration projects are complex and have many moving parts. In this case study, our client wanted to reduce power usage by large servers by 40%, by consolidating into an hyper-converged system. Other goals were to reduce floor space by 50% and monthly recurring data center charges by 50% (or about $240,000 annually). The client ended up leveraging their data center savings by purchasing new hyper-converged compute hardware with a new SSD IBM Storwize SAN environment. <br>

Some of the major highlights of our work for this client were transitioning them to a new hardware stack (compute, storage, network, backup environment) in a Tier 4 data center, and saving them 50% percent on data center operation costs (which was leveraged to cover the new hardware). Additionally, during the process we corrected issues associated with disaster recovery and business continuity, leaving the client’s operations more resilient, cheaper, and more secure. 


