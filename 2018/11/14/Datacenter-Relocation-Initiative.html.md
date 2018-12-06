---
author: Charles Chang
title: 'Data Center Relocation Initiatives'
tags: integration, disaster-recovery, datacenter, infrastructure 
gh_issue_number: 1462
---

### Data Center Relocation Initiatives: Daunting But Achievable ###

#### Introduction ####

A customer asked for our help with logistical nightmares encountered during a hardware update and data center relocation project. The customer had two active data centers, and wanted to relocate one of them to a modern Tier 4 data center to improve its performance and offer redundancy for critical systems. The plan would also help them consolidate or decommission equipment to reduce their carbon footprint, eliminate recurring expenses, and establish green IT systems. The client decided on a Tier 4 data center because they provide across-the-board redundancy within the data center. Below, the specifications for each tier of data center are explained in detail.

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image05.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="Decommissioning Cabinets and Wires" width=250 height=333 />

##### Tier IV Data Center Requirements (Best) #####
Tier IV data centers have redundancies for every process and data protection stream. No single outage or error can shut down the system. To keep Tier IV ranking, data centers must have 99.995% minimum uptime per year.  They come equipped with 2N+1 infrastructure (two times the amount required for operation plus a backup), which is considered “fully redundant.”

##### Tier III Data Center Requirements (Average) #####
N+1 (the amount required for operation plus a backup) fault tolerance — which means a Tier III facility can undergo routine maintenance without a hiccup in operations. 99.982% minimum uptime per annum. This downtime is allowed for maintenance and overwhelming emergency issues.

##### Tier II Data Center Requirements (Minimal) #####
99.749% minimum uptime. Tier II facilities have considerably more downtime than Tier III facilities, primarily because Tier II facilities have less redundancies.  They do however have partial cooling redundancies and multiple power redundancies.

##### Tier I Data Center Requirements - no redundancy (Basic, Cheapest) #####
99.671% minimum uptime, with 28.8 hours of downtime each year.

---

##### Key Issues #####

**Some of the key issues the customer mentioned were:**<br>

1\. To safely move the virtual environment to the new data center.<br> <br>
2\. To protect assets during the relocation.<br> <br>
3\. To completely shut down the current data center and migrate seamlessly to the new data center.<br> <br>
4\. To update external DNS records without causing any downtime for their web applications used by their customers. <br> <br>

Key to a successful migration project is to understand how, when, and where to migrate critical and non-critical systems. Testing and verification of backup and restore procedures prior to any migration is also critical.

---

#### Moving forward with Tier IV ####

The main reason an enterprise would seek a Tier 4 data center is because it offers the highest uptime guarantee, and has zero single points of failure. These facilities are fully redundant in terms of electrical circuits, cooling and networking. This architecture is best able to withstand even the most serious technical incidents without server availability  being affected. Tier IV facilities have contracts with disaster management companies who will provide them, for example, with fuel in the event that a natural disaster damages the power grid.  In a situation like Hurricane Sandy, these data centers activate their disaster recovery procedures to support and sustain their services to their customers.

---

#### Getting Started ####

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image04.jpg" style="float: left; margin: 10px 25px 15px 15px" alt="Data Center Hardware Removal and Clean Up" width=250 height=333 />
Data center migrations must make critical systems available again after migration, which requires solid and extensive preparation. For this particular client, we had the luxury the client already having in place a second data center, which could accommodate a majority of the critical systems. 

We originally planned to change the external DNS records to point to the correct data center, but worried that the external DNS record would not replicate worldwide quickly enough to meet the needs of their global operation. 

---

#### Solutions ####

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image03.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="New Data Center Cabinets" width=250 height=333 />
We discussed various approaches and ended up using a load balancer to resolve two issues with one technology. A load balancer is a network device that routes incoming traffic destined for a single destination (web site, application, or service) and 'shares' the incoming connections across multiple destination devices or services. In this case, the data center being migrated originally housed the critical systems like web servers, sql, etc. The secondary data center housed a replica (offline copy) of the critical systems using a replication technology such as Actifio, Rubrik, SAN mirroring, VMware SRM, or Zerto but we used Actifio in this scenario.

The customer had multiple systems with external DNS records and public IP addresses. The public DNS name for each critical system were  not changed. The public IP associated with the public DNS name were changed, to point to the load balancer, which then pointed to the data center with the critical systems. This setup enabled a gradual, flexible, and fully controlled transition to the new data center.

---

#### Project Planning ####

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image02.jpg" style="float: left; margin: 10px 25px 15px 15px" alt="Pure Flex Hyper-Converged Hardware Stack" width=250 height=333 />
A data center migration and relocation project can be overwhelming, but proper planning can make the process smooth and worry free. Good planning requires hard work and preparation, but is necessary for a successful relocation. 
 
Our approach is to analyze each part of the data center relocation, break it down, and strategize about the best approach for each task. Typically, planning starts 6 months ahead of the scheduled relocation date. Additional time to plan can help especially when a large group of stakeholders is involved.

Here is an example of what needs to be completed ahead of the data center migration:

**For example what needs to be completed ahead of the data center migration?**<br>

1\. Process the paperwork for new hardware, approve all applications, hire movers, schedule and coordinate with internal management and key stakeholders like IT staff, system admins, contractors, circuit providers, etc.<br><br>
2\. Collect and analyze resource usage associated with the critical and non-critical systems and compare to resource availability at the new facility.<br><br>
3\. Design and schedule the migration of critical systems to the secondary data center. Discuss the plan with key stakeholders.<br>
4\. Set up a new environment with new hardware in the new data center and establish network connections.<br><br>
5\. Make sure replicas of critical systems are up to date. <br><br>
6\. Prepare hardware and virtualization technology in new data center.  <br><br>
7\. Test, retest, and burn in the new hardware. (2-4 weeks of testing).<br><br>
8\. Create a non-essential server within the virtualization environment and test it.<br>

Managing all aspects of a data center relocation is challenging because there are many moving parts and variables to deal with. Carefully reviewing an inventory of all system and consulting in depth with all the teams involved  helps us understand the role of each system and allows us to plan how to execute a seamless and successful relocation.

--- 

#### Summary ####

<img src="../blog/2018/11/14/Datacenter-Relocation-Initiative/image01.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="Pure Flex Cabinet" width=250 height=333 />
In this case study, our client wanted to reduce their servers’ power usage 40% by consolidating into a hyper-converged system. Other goals were to reduce floor space by 50%, and monthly recurring data center charges by 50% (or about $240,000 annually). The client ended up leveraging their  savings by purchasing  a new hyper-converged solution along with a new SSD IBM Storwize SAN environment. Some of the highlights of our work for this client were transitioning them to a new hardware stack (compute, storage, network, backup environment) in a Tier 4 data center, and saving them 50% percent on data center operation costs (which was leveraged to cover the new hardware). Additionally, during the process we corrected issues associated with disaster recovery and business continuity, leaving the client’s operations more resilient, cheaper, and more secure. 
