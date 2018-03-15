---
author: Selvakumar Arumugam
gh_issue_number: 1161
tags: automation, conference, devops, containers
title: DevOpsDays India — 2015
---

DevOpsIndia 2015 was held at The Royal Orchid in Bengaluru on Sep 12-13, 2015. After saying hello to a few familiar faces who I often see at the conferences, I collected some goodies and entered into the hall. Everything was set up for the talks. Niranjan Paranjape, one of the organizers, was giving the introduction and overview of the conference.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/09/30/devopsdays-india-2015/image-0-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/09/30/devopsdays-india-2015/image-0.jpeg"/></a></div>

Justin Arbuckle from Chef gave a wonderful keynote talk about the “Hedgehog Concept” and spoke more about the importance of consistency, scale and velocity in software development.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/09/30/devopsdays-india-2015/image-1-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/09/30/devopsdays-india-2015/image-1.jpeg"/></a></div>

In addition, he quoted “A small team with generalists who have a specialization, deliver far more than a large team of single skilled people.”

A talk on “DevOps of Big Data infrastructure at scale” was given by Rajat Venkatesh from Qubole. He explained the architecture of Qubole Data Service (QDS), which helps to autoscale the Hadoop cluster. In short, scale up happens based on the data from Hadoop Job Tracker about the number of jobs running and time to complete the jobs. Scale down will be done by decommissioning the node, and the server will be chosen by which is reaching the boundary of an hour. This is because most of the cloud service providers charge for an hour regardless of whether the usage is 1 minute or 59 minutes.

Vishal Uderani, a DevOps guy from WebEngage, presented “Automating AWS infrastructure and code deployment using Ansible.” He shared the issues facing the environments like task failure due to ssh timeout on executing a giant task using Ansible and solved by monitoring the task after triggering the task to get out of the system immediately. Integrating Rundeck with Ansible is an alternative for enterprise Ansible Tower. He also stated the following reasons for using Ansible:

- Good learning curve
- No agents will be running on the client side, which avoids having to monitor the agents at client nodes
- Great deployment tool

<br/>

Vipul Sharma from CodeIgnition stated the importance of Resilience Testing. The application should be tested periodically to be tough and strong enough to handle any kind of load. He said Simian Army can be used to create the problems in environments and then resolving them to make them flawless. Simian Army can used to improve application using security monkey, chaos monkey, janitor monkey, etc… Also “Friday Failure” is a good method to identify the problem and improve the application.

Avi Cavale from Shippable gave an awesome talk on “Modern DevOps with Docker”. He talk started with “What is the first question that arises during an outage ? ... What changed ?”After fixing these issues, the next question will be “Who made the change?” Both questions are bad for the business. Change is the root cause of all outage but business requires changes. In his own words, DevOps is a culture of embracing change. Along with that he explained the zero downtime ways to deploy the changes using a container.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/09/30/devopsdays-india-2015/image-2-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/09/30/devopsdays-india-2015/image-2.jpeg"/></a></div>

He said DevOps is a culture, make it FACT(F-Frictionless, A-Agile, C-Continuous and T-Transparency).

Rahul Mahale from SecureDB gave a demo on [Terraform](https://terraform.io/), a tool for build and orchestration in Cloud. It features “Infrastructure as Code” and also provides an option to generate the diagrams and graphs of the present infrastructure.

Shobhit and Sankalp from CodeIgnition shared their experience on solving network based issues. Instead of whitelisting the user’s location every time manually to provide the access to systems, they created a VPN to enable access only to users, not locations. They have resolved two more additional kind of issues by adding Router to bind two networks using FIP.  Another issue is that they need to whitelist to access third party services from containers, but it was hard to whitelist all the containers. Therefore, they created and whitelisted VMs and containers accessed the third party services through VMs.

Ankur Trivedi from Xebia Labs spoke about the “[Open Containers Initiative](https://www.opencontainers.org/)” project. He explained the evolution of the containers (Docker — 2013 & Rocket — 2014). The various distributions of containers are compared based on the Packing, Identity, Distribution and Runtime capabilities. Open Containers is supported by the community and various companies who are doing extensive work on containers in order to standardize them.

Vamsee Kanala, a DevOps consultant, presented a talk on “Docker Networking — A Primer”. He spoke about Bridge networking, Host Networking, Mapped container networking and None (Self Managed) with dockers. The communications between the containers can happen through:

- Port mapping
- Link
- Docker composing (programmatically)

<br/>

In addition, he explained the tools which feature the clustering of containers, and listed the tools that have their own way of clustering and advantages:

- Kubernetes
- Mesos
- Docker Swarm

<br/>

Aditya Patawari from BrowserStack gave a demo on “Using Kubernetes to Build Fault Tolerant Container Clusters”. Kubernetes has a feature called “Replication Controllers,” which helps to maintain number of pods running at any time. “Kubernetes Services” defines a policy to enable access among the pods which provisions the pods as micro services.

Arjun Shenoy from LinkedIn introduced a tool called “[SIMOORG](https://github.com/linkedin/simoorg).” The tool was developed at LinkedIn and does the failure induction in a cluster for testing the stability of the code. It is a components-based Open Source framework and few components are replaceable with external ones.

Dharmesh Kakadia, a researcher from Microsoft, gave a wonderful talk on “Mesos is the Linux”. He started with a wonderful explanation on Micro services (relating with linux commands, each command is a micro service) which is simplest, independently updatable, runnable and deployable. Mesos is a “Data Center Kernel” which takes care of scalability, fault tolerance, load balance, etc… in Data Center.

At the end, I got a chance to do some hands-on things on Docker and played with some of its features. It was a wonderful conference to learn more about configuration management and the containers world.
