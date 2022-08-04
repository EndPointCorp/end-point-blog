---
author: "Jeffry Johar"
title: "Ansible tutorial with AWS EC2"
date: 2022-08-04
tags:
- ansible
- aws
- ec2
- amazon linux
- postgresql

---
![A ferris wheel](/blog/2022/08/ansible-tutorial-with-aws-ec/wheel.webp)
Photo by David Buchi


### Introduction
Ansible is a tool to manage multiple remote systems from a single command center. In Ansible environments, the single command center is known as Control Node and the remote systems to be managed is known as Managed Node. The following tables describe about the 2 types of Ansible nodes:

| # | Ansible Node | Remarks |
|---|--------------|------------|
| 1 | Control Node | - The command center were Ansible is installed<br> - Supported OS are Unix and Unix Like ( Linux, BSD , MacOS )<br> - Required python and sshd |
| 2 | Managed Node | - The remote systes to be managed<br> - Most modern OS ( Unix, Unix Like, Windows, Appliances ( eg: Cisco, Netapp ) |

In this  tutorial we will use Ansible to manage multiple EC2 instances. For simplicity we are going to provision EC2 instances by AWS web console. Then we will configure one EC2 as the Control Node that will be managing multiple EC2 instances as Managed Nodes.

 


