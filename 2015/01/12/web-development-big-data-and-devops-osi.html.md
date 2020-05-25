---
author: Selvakumar Arumugam
gh_issue_number: 1069
tags: angular, conference, containers, mongodb, nodejs, php, cms
title: Web Development, Big Data and DevOps—​OSI Days 2014, India
---

This is the second part of an article about the conference [Open Source India](https://opensourceindia.in/osidays/), 2014 was held at Bengaluru, India. The first part is available [here](/blog/2014/11/19/mongodb-and-openstack-osi-days-2014). The second day of the conference started with the same excitement level. I plan to attend talks covering Web, Big Data, Logs monitoring and Docker.

### Web Personalisation

Jacob Singh started the first talk session with a wonderful presentation along with real-world cases which explained the importance of personalisation in the web. It extended to content personalisation for users and A/B testing (comparing two versions of a webpage to see which one performs better). The demo used the [Acquia Lift](https://www.drupal.org/project/acquia_lift) personalisation module for the [Drupal](https://www.drupal.org/) CMS which is developed by his team.

### MEAN Stack

Sateesh Kavuri of Yodlee spoke about the [MEAN](http://mean.io/) stack which is a web development stack equivalent to popular LAMP stack. MEAN provides a flexible compatibility to web and mobile applications. He explained the architecture of MEAN stack.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="480" src="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-0.png" width="640"/></a></div>

He also provided an overview of each component involved in MEAN Stack.

[MongoDB](https://www.mongodb.org/) — NoSQL database with dynamic schema, in-built aggregation, mapreduce, JSON style document, auto-sharding, extensive query mechanism and high availability.

[ExpressJS](http://expressjs.com/) — A node.js framework to provide features to web and mobile applications.

[AngularJS](https://angularjs.org/) — seamless bi-directional model with extensive features like services and directives.

[Node.js](https://nodejs.org/) — A server side javascript framework with event based programming and single threaded (non blocking I/O with help of request queue).

[Sails.js](https://sailsjs.org/) — MEAN Stack provisioner to develop applications quickly.

Finally he demonstrated a MEAN Stack demo application provisioned with help of Sails.js.

### Moving fast with high performance Hack and PHP

Dushyant Min spoke about the way Facebook optimised the PHP code base to deliver better performance when they supposed to handle a massive growth of users. Earlier there were compilers HipHop for PHP (HPHPc) or HPHPi (developer mode) to convert the php code to C++ binary and executed to provide the response. After sometime, Facebook developed a new compilation engine called [HipHop Virtual Machine](https://hhvm.com/) which uses Just-In-Time (JIT) compilation approach and converts the code to HipHop ByteCode (HHBC). Both Facebook’s production and development environment code runs over HHVM.

Facebook also created a new language called [Hack](http://hacklang.org/) which is very similar to PHP which added static typing and many other new features. The main reason for Hack is to get the fastest development cycle to add new features and release frequent versions. Hack also uses the HHVM engine.

HHVM engine supports both PHP and Hack, also it provides better performance compare to Zend engine. So Zend Engine can be replaced with HHVM without any issues in the existing PHP applications to get much better performance. It is simple as below:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="480" src="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-1.png" width="640"/></a></div>

Also PHP code can be migrated to Hack by changing the `<?php` tag to `<?hh` and there are some converters (hackficator) available for code migration. Both PHP and Hack provide almost the same performance on the HHVM engine, but Hack has some additional developer-focussed features.

### Application Monitoring and Log Management

Abhishek Dwivedi spoke about a stack to process the logs with various formats, myriad timestamp and no context. He explains a stack of tools to process the logs, store and visualize in a elegant way.

ELK Stack = Elasticsearch, LogStash, Kibana. The architecture and the data flow of ELK stack is stated below:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-2.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="438" src="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-2.png" width="640"/></a></div>

[Elasticsearch](https://www.elastic.co/) — Open source full text search and analytics engine

[Log Stash](https://www.elastic.co/products/logstash) — Open source tool for managing events and logs which has following steps to process the logs

[Kibana](https://www.elastic.co/products/kibana) — seamlessly works with Elasticsearch and provides elegant user interface with various types of graphs

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-3.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="138" src="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-3.png" width="640"/></a></div>

### Apache Spark

Prajod and Namitha presented the overview of Apache Spark which is a real time data processing system. It can work on top of Hadoop Distributed FileSystem (HDFS). [Apache Spark](https://spark.apache.org/) performs 100x faster in memory and 10x faster in disk compare to Hadoop. It fits with Streaming and Interactive scale of Big Data processing.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-4.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="480" src="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-4.png" width="640"/></a></div>

Apache Spark has certain features in processing the data to deliver the promising performance:

- Multistep Directed Acyclic Graph
- Cached Intermediate Data
- Resilient Distributed Data
- Spark Streaming — Adjust batch time to get the near real time data process
- Implementation of Lambda architecture
- Graphx and Mlib libraries play an important role

### Online Data Processing in Twitter

Lohit Vijayarenu from Twitter spoke about the technologies used at Twitter and their contributions to Open Source. Also he explained the higher level architecture and technologies used in the Twitter microblogging social media platform.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-5.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" height="338" src="/blog/2015/01/12/web-development-big-data-and-devops-osi/image-5.png" width="640"/></a></div>

The Twitter front end is the main data input for the system. The Facebook-developed Scribe log servers gather the data from the Twitter front end application and transfers the data to both batch and real time Big Data processing systems. Storm is a real time data processing system which takes care of the happening events at the site. Hadoop is a batch processing system which runs over historical data and generates result data to perform analysis. Several high level abstraction tools like PIG are used write the MR jobs. Along with these frameworks and tools at the high level architecture, there are plenty of Open Source tools used in Twitter. Lohit also strongly mentioned that in addition to using Open Source tools, Twitter contributes back to Open Source.

### Docker

Neependra Khare from Red Hat given a talk and demo on [Docker](https://www.docker.com/) which was very interactive session. The gist of Docker is to build, ship and run any application anywhere. It provides good performance and resource utilization compared to the traditional VM model. It uses the Linux core feature called containerization. The container storage is ephemeral, so the important data can be stored in persistent external storage volumes. Slides can be found [here](https://github.com/nkhare/presetations/blob/master/osidays/osi_docker.md).
