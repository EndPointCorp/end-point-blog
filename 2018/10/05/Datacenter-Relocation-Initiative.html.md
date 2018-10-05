---

author: Charles Chang

title: 'Data Center Relocation Initiatives'

tags: windows, servers, virtualization, data center

gh_issue_number: 1460

---

### Data Center Relocation Initiatives: Daunting But Achievable ###

#### Introduction ####

A customer was running into some logistical nightmare about a hardware refresh and data center relocation project but needed some expert advice as to which was the best approach and ways to complete the task. Currently, the customer has two active data centers, and looking to relocate one of the active data center to a modernize Tier 4 data center to better the performance and offer redundancy for critical systems. The reason the customer decided to move forward with the data center relocation initiatives was to move to a more modern data center, consolidate or decommission equipments to reduce carbon footprint, eliminate recurring expenses, and establish green IT Initiative. The reason the client decided on a Tier 4 datacenter was due to the prospect of redundancy across the board within the data center.  Below will better explain each Tier in detail.

<img src="/blog/2018/10/05/Datacenter-Relocation-Initiative/image05.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="Decommissioning Cabinets and Wires" width=250 height=333 />

##### Tier IV Data Center Requirements (Best) #####
Zero single points of failure. Tier IV providers has redundancies for every process and data protection stream. No single outage or error can shut down the system. 99.995 % uptime per annum. This is the level with the highest guaranteed uptime and must be maintained well for a data center to keep up Tier IV ranking. 2N+1 infrastructure (two times the amount required for operation plus a backup). 2N+1 is another way of saying “fully redundant.”

##### Tier III Data Center Requirements (Average) #####
N+1 (the amount required for operation plus a backup) fault tolerance. A Tier III provider can undergo routine maintenance without a hiccup in operations. No more than 1.6 hours of downtime per annum. This downtime is allowed for purposes of maintenance and overwhelming emergency issues.

##### Tier II Data Center Requirements (Minimal) #####
No more than 22 hours of downtime per annum. There is a considerable jump between levels II and III regarding downtime. Redundancy is one of the primary reasons for this. 99.741 % uptime per annum. This is a minimum amount of uptime that this provider can produce in a year. Partial cooling and multiple power redundancies.

##### Tier I Data Center Requirements - no redundancy (Basic, Cheapest) #####
No more than 28.8 hours of downtime per annum. These facilities are allowed the highest amount of downtime of any level.

---

##### Key Issues #####

**Some of the key issues the customer mentioned were:**<br>

1\. How do we move the virtual environment to the new data center.<br> <br>
2\. How do we protect our assets during the relocation.<br> <br>
3\. How do we completely shut down the current data center and migrate seamlessly into the new data center.<br> <br>
4\. How to update external DNS records without creating downtime to the web application available to the customers. <br> <br>
5\. How do we seamlessly allow our customers access to the secondary data center which will temporary house the critical systems during the migration. <br> <br>

Key elements to have a successful migration project is to understand how, when and where to migrate critical and non-critical systems, and then give access to the systems once it completes the migration. Basically, before the day of the relocation, the goal is to relocate, or shutdown the systems residing in the data center being relocated.

---

#### Moving forward with Tier IV ####

Main reason an enterprise company would seek a Tier 4 data center is because it offer the highest level of guarantee that a data center can provide, with 99.99% availability with zero single points of failure.. This data center is fully redundant in terms of electrical circuits, cooling and network. This architecture can withstand even the most serious of technical incidents without server availability ever being affected. In a situation like the recent Hurricane Sandy that hit New York a few years ago, the data center is contracted with a company to deliver diesel fuel to the complex to sustain their generators during a power outage. Typically in a situation like hurricane Sandy, the data center will mobilize their disaster recovery procedure to support and sustain their services to their customer.  

---

#### Getting Started ####
<img src="/blog/2018/10/05/Datacenter-Relocation-Initiative/image04.jpg" style="float: left; margin: 10px 25px 15px 15px" alt="Data Center Hardware Removal and Clean Up" width=250 height=333 />
It seems like a daunting task, but most important part of a data center migration project is how to migrate and make the critical systems available. For this particular client, we had the luxury of having a second data center with adequate resources to accommodate majority of the critical systems coming over from the data center being relocated. If client did not have a 2nd data center to work with, then a new proposal and strategy would be proposed. In this case, the client had a secondary data center to work with, ample resources to work with, except for adding additional storage to the SAN environment and planning for some minor maintenance to free up storage. 

---

#### Alternatives ####

Originally, the practice was to change the external DNS records to point to the correct data center but management team was worried the external DNS record would not replicate worldwide quick enough since they operate globally and have customers and other global systems interconnected. 

---

#### Solutions ####
<img src="/blog/2018/10/05/Datacenter-Relocation-Initiative/image03.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="New Data Center Cabinets" width=250 height=333 />
We threw around some ideas and ended up using a load balancer to basically resolve two issues with one technology. A load balancer is a network device that routes incoming traffic destined for a single destination (web site, application, or service) and 'shares' the incoming connections across multiple destination devices or services. In this case, the primary data center being migrate originally house the critical systems like web servers, sql, etc. The secondary data center house a replica (offline copy) of the web servers, SQL, etc using a replication technology. (Actifio, Rubrik, SAN mirroring, VMware SRM, Zerto, etc) These are all potential tools/systems to use in a migration project. <br><br> 

In this case, the customer had multiple systems with external DNS records and Public IP. The public DNS name for each critical system will not change. The public IP associated with the public DNS name of the critical system will change and point to the load balancer which then points to the correct data center servicing the critical systems. This setup would allow the load balancer to store the two public IP of the critical system pointing to either the primary or secondary data center. When we were ready to power up the replica web server, we could adjust the load balancer to point to the secondary data center where the replica web servers is located and provide access to the critical system. 

By providing this solution, the critical systems will start providing service from the secondary data center and will be accessible once the web server configuration are confirmed and powered up to provide service.

---

#### Project Planning ####
<img src="/blog/2018/10/05/Datacenter-Relocation-Initiative/image02.jpg" style="float: left; margin: 10px 25px 15px 15px" alt="Pure Flex Hyper-Converged Hardware Stack" width=250 height=333 />
A data center migration and relocation project could be overwhelming but typically resolving known issues ahead of the migration and proper planning in stages will better the outcome once the relocation occurs. The planning stages could take weeks if not months but necessary to have a successful relocation. <br><br>

Key is to break apart each part of the data center relocation, analyze, and then strategy what would be the best approach to complete each task. Typically, planning would start 6 months +/- ahead of the scheduled relocation date. Some customers might need additional time to plan due to a large group of stakeholders involved. 

**For example what needs to be completed ahead of the data center migration?**<br>

1\. Process the paperwork from new hardware, approve all applications, hire movers, schedule and coördinate with internal management team and key stakeholders like IT staffs, system admins, contractors, circuit providers, etc.<br><br>
2\. Collect, and analyze resource usage associated with the critical and non-critical systems and prepare and compare resource availability between the two data center.<br><br>
3\. Determine and schedule critical systems migration to secondary data center. Discuss approach with key stakeholder in regards to task associate with the critical servers.<br><br>

**Samples of Pre-Relocation Task**

1\. Stand up new environment with new hardware in new data center and prepare and establish network connectivity to secondary data center. <br> <br>
2\. Make sure replica of critical systems are up to date. <br> <br>
3\. Prepare hardware and virtualization technology in newly built data center. <br> <br>
4\. Test, retest, burn in the new hardware. (2-4 weeks of testing)<br> <br>
5\. Create a non-essential server within the virtualization environment and test.<br>

Covering all aspect of the data center relocation is daunting since there will be a bit of moving parts and variables to deal with. There will probably be a few things to discuss but with proper planning and setting reasonable goals for each phase of the project will definitely ease the transition. Brainstorming between teams and dissecting an inventory of all system and understanding the criticality of each system would allow each team to decide best approach to make their service available. Thus allow a seamless and successful relocation. 

--- 

#### Summary ####
<img src="/blog/2018/10/05/Datacenter-Relocation-Initiative/image01.jpg" style="float: right; margin: 10px 25px 15px 15px" alt="Pure Flex Cabinet" width=250 height=333 />
This article was to understand the complexity of a data center migration project and the number of moving parts needed to successfully migrate a data center. The goal was to reduce large servers power usage by 40% by consolidating into an hyper-converged system. Other goals were to reduce floor space by 50% and reducing the monthly recurring data center charges by 50% which is about $20,000 saved per month and $240,000 annually. The client ended up leveraging their data center saving by purchasing new hyper-converged compute hardware with a new SSD IBM Storwize SAN environment. <br><br>

Some of the major highlight achieved by this client were a new hardware stack (compute, storage, network, backup environment) in a Tier 4  data center, saved 50% percent on data center operation cost which was leveraged to pay for the new hardware, and during the process corrected two issues associated with system migration between the two data center. Once the two key issues that hampered the disaster recovery and business continuity effort were resolved, changing systems roles in multiple data center was much easier to provide service during critical moment when time comes. 

