---
author: Selvakumar Arumugam
gh_issue_number: 1058
tags: big-data, cloud, conference, mongodb, open-source
title: MongoDB and OpenStack — OSI Days 2014, India
---

The 11th edition of Open Source India, 2014 was held at Bengaluru, India. The two day conference was filled with three parallel tech talks and workshops which was spread across various Open Source technologies.

<img alt="IMG_20141110_223543.jpg" height="440px;" src="/blog/2014/11/19/mongodb-and-openstack-osi-days-2014/image-0.jpeg" style="-webkit-transform: rotate(0.00rad); border: none; transform: rotate(0.00rad);" width="624px;"/>

### In-depth look at Architecting and Building solutions using MongoDB

Aveekshith Bushan & Ranga Sarvabhouman from MongoDB started off the session with a comparison of the hardware cost involved with storage systems in earlier and recent days. In earlier days, the cost of storage hardware was very expensive, so the approach was to filter the data to reduce the size before storing into the database. So we were able to generate results from filtered data and we didn’t have option to process the source data. After the storage became cheap, we can now store the raw data and then we do all our filter/processing and then distribute it.

Earlier,

        Filter -> Store -> Distribute

Present,

        Store -> Filter -> Distribute

Here we are storing huge amount of data, so we need a processing system to handle and analyse the data in efficient manner. In current world, the data is growing like anything and 3Vs are phenomenal of growing (Big)Data. We need to handle the huge Volume of Variety of data in a Velocity. MongoDB follows certain things to satisfy the current requirement.

<div class="separator" style="clear: both; text-align: center;">
  <a href="/blog/2014/11/19/mongodb-and-openstack-osi-days-2014/image-1.png" style="margin-left: 1em; margin-right: 1em;">
    <img border="0" height="152" src="/blog/2014/11/19/mongodb-and-openstack-osi-days-2014/image-1.png" width="400" />
  </a>
</div>

MongoDB simply stores the data as a document without any data type constraints which helps to store huge amount of data quickly. It leaves the constraints checks to the application level to increase the storage speed in database end. But it does recognises the data type after the data is stored as document. In simple words, the philosophy is: Why do we need to check the same things (datatype or other constraints) in two places (application and database)?

MongoDB stores all relations as single document and fetches the data in single disk seek. By avoiding multiple disk seeks, this results in the fastest retrieval of data. Whereas in relational database the relations stored in different tables which leads to multiple disk seek to retrieve the complete data of an entity. And MongoDB doesn’t support joins but it have Reference option to refer another collection(Table) without imposing foreign key constraints.

As per [db-engines](https://db-engines.com/en/ranking) rankings, MongoDB stays in the top of NoSQL database world. Also it provides certain key features which I have remembered from the session:

- Sub-documents duplicates the data but it helps to gain the performance(since the storage is cheap, the duplication doesn’t affect much)
- Auto-sharding (Scalability)
- Sharding helps parallel access to the system
- Range Based Sharding 
- Replica Sets (High availability)
- Secondary indexes available
- Indexes are single tunable part of the MongoDB system 
- Partition across systems 
- Rolling upgrades
- Schema free
- Rich document based queries
- Read from secondary

When do you need MongoDB?

- The data grows beyond the system capacity in relational database
- In a need of performance in online requests

Finally, speakers emphasized to understand use case clearly and choose right features of MongoDB to get effective performance.

### OpenStack Mini Conf

A special half day OpenStack mini conference was organised at second half of first day. The talks were spread across basics to in depth of OpenStack project. I have summarised all the talks here to give an idea of OpenStack software platform.

OpenStack is a Open Source cloud computing platform to provision the Infrastructure as a Service(IaaS). There is a wonderful project [DevStack](https://docs.openstack.org/developer/devstack/) out there to set up the OpenStack on development environment in easiest and fastest way. A well written [documentation](https://docs.openstack.org/) of the OpenStack project clearly explains everything. In addition, anyone can contribute to OpenStack with help of [How to contribute](https://wiki.openstack.org/wiki/How_To_Contribute) guide, also project uses Gerrit review system and Launchpad bug tracking system.

OpenStack have multiple components to provide various features in Infrastructure as a Service. Here is the list of OpenStack components and the purpose of each one.

- Nova (Compute) — manages the pool of computer resources
- Cinder (Block Storage) — provides the storage volume to machines
- Neutron (Network) — manages the networks and IP addresses
- Swift (Object Storage) — provides distributed high availability(replication) on storage system.
- Glance (Image) — provides a repository to store disk and server images
- KeyStone (Identity) — enables the common authentication system across all components
- Horizon (Dashboard) — provides GUI for users to interact with OpenStack components
- Ceilometer (Telemetry) — provides the services usage and billing reports
- Ironic (Bare Metal) — provisions bare metal instead of virtual machines
- Sahara (Map Reduce) — provisions hadoop cluster for big data processing

OpenStack services are usually mapped to AWS services to better understand the purpose of the components. The following table depicts the mapping of similar services in OpenStack and AWS:

<table style="border-collapse: collapse; border: none; width: 624px;"><colgroup><col width="*"/><col width="*"/></colgroup><tbody>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 25px 7px 25px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt; text-align: center;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; font-weight: bold; vertical-align: baseline; white-space: pre-wrap;">OpenStack</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt; text-align: center;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; font-weight: bold; vertical-align: baseline; white-space: pre-wrap;">AWS</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Nova</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">EC2</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Cinder</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">EBS</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Neutron</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">VPC</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Swift</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">S3</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Glance</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">AMI</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">KeyStone</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">IAM</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Horizon</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">AWS Console</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Ceilometer</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Cloudwatch</span></div>
</div>
</td></tr>
<tr style="height: 0px;"><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Sahara</span></div>
</div>
</td><td style="border-bottom: solid #ffffff 1px; border-left: solid #ffffff 1px; border-right: solid #ffffff 1px; border-top: solid #ffffff 1px; padding: 7px 7px 7px 7px; vertical-align: top;"><div dir="ltr" style="line-height: 1; margin-bottom: 0pt; margin-top: 0pt;">
<div style="text-align: center;">
<span style="font-family: Arial; font-size: 15px; vertical-align: baseline; white-space: pre-wrap;">Elastic Mapreduce</span></div>
</div>
</td></tr>
</tbody></table>


Along with the overview of OpenStack architecture, there were couple of in-depth talks which are listed below with slides.

- Neependra Khare from RedHat gave a presentation on using [Docker in OpenStack Nova](https://github.com/nkhare/presetations/blob/master/osidays/osi_openstack_nova_docker.md). 
- Pushpesh Sharma presented a [comparison between storage component OpenStack Swift and Ceph](http://pushpeshsharma.blogspot.in/2014/11/openstack-swift-vs-ceph-rgw-read.html)
- Sridhar Rao presented about OpenStack and its role in Network Function Virtualisation (NFV) — [Slides](https://dl.dropboxusercontent.com/u/1527696/OpenStack-NfV.pptx)

That was a wonderful Day One of OSI 2014 which helped me to get better understanding of MongoDB and OpenStack.
