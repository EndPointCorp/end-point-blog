---
author: Muhammad Najmi bin Ahmad Zabidi
title: 'HGCI Summit Conference 2017, Malaysia: A conference on cloud, security and
  big data'
github_issue_number: 1349
tags:
- conference
- cloud
- security
date: 2017-12-12
---

I was asked by a friend to give a talk in the HGCI Summit conference on November 28th, 2017. This conference is meant to bridge the academic world and industry via knowledge and experience sharing, focusing on big data and cloud topics. It took place in the Center of Advanced Professional Education (CAPE), a center under the Universiti Teknologi Petronas (UTP) which has its main campus in Tronoh, Perak, Malaysia.

I will highlight several tracks which I attended.

### Forum

On the first day, several faculty members sat together within a forum in which they discussed the main issues academics face when they need access to high performance computing. An audience member shared her experience completing her research group’s work which took very long to be rendered, while she could do it in a day when she submitted the work in a university in the US. One of the forum’s members then replied she could always work collaboratively with the other universities, and he (the forum member) offered his university’s facilities to be used for her research. Inter-varsity network bandwidth was also discussed in the forum.

### Dr. Izzatdin

<img src="/blog/2017/12/hgci-summit-2017/utp.jpg"/>

An interesting talk which I attended was delivered by Dr. Izzatdin from UTP. He shared his work on cloud-based crude oil refinery monitoring. The monitoring system web page is hosted on Microsoft’s Azure, where it will display the oil refinery data which were gathered batch by batch from the sensors. Metal corrosion is among the things monitored by the systems.

### Mr. Aizat

<img src="/blog/2017/12/hgci-summit-2017/aizat.jpg"/>

I also attended a talk delivered by a friend of mine, Mr. Aizat from Informology. He shared the use of OpenStack for the provision of highly parallel computing instances. I saw that Aizat also used ready-made Ansible scripts in order to get the computing instances ready. By using Horizon (OpenStack’s user interface) it seems we could speed up the process of the instance provisioning. Aizat also shared a link for anyone interested to try out the “vanilla” version of OpenStack at [TryStack](http://trystack.org/). Another tool which he shared is [ElastiCluster](https://github.com/gc3-uzh-ch/elasticluster), a set of Python scripts which allow the user to create, manage, and set up cloud infrastructures using Ansible. Aizat also showed the use of [Jujucharms](https://jujucharms.com), a portal which handles Juju, an open source application modelling tool developed by Canonical (the maker of Ubuntu Linux).

### My talk

My talk was shortly after Aizat’s slot. I covered the use of algorithms to detect the similarity subsequence of patterns between malware and non-malware (benign software) and between the malware family variants. I obtained the malware samples from a Windows malware researcher when he did his PhD study and another dataset from a research unit in Asia. (Please contact me if you want these samples.)

These datasets contain either the Application Programming Interface (API) calls only, or the API calls with their arguments. These API calls were obtained by running the malware within a safe, virtualized environment and the calls were dumped into text files.

Since procedural language code commonly runs from top bottom, the API calls which were generated inherit the same idea, making them have the same structures if they share a common root. I used **n-gram** and **Longest Common Subsequence (LCS)** to perform the experiment. These two algorithms are categorized under the dynamic programming algorithms group, in which they created a subsequence from the sequence of problem for a pattern matching.

I also mentioned the use of Python (for example with **scikit-learn**) and [Weka](https://www.cs.waikato.ac.nz/ml/weka) if we want to work on the problem using machine learning methods.

If you are interested, check out my PDF slides, [Machine Learning Applications for the Cyber Security Threats](/blog/2017/12/hgci-summit-2017/najmi_hgci_slides_2017.pdf).

<img src="/blog/2017/12/hgci-summit-2017/aizat2.jpg"/>
