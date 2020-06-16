---
author: Elizabeth Garrett Christensen
gh_issue_number: 1284
tags: case-study, clients, company, hosting, rails, epitrax, pentaho
title: TriSano Case Study
---

### Overview

End Point has been working with state and local health agencies since 2008. We host disease outbreak surveillance and management systems and have expertise providing clients with the sophisticated case management tools they need to deliver in-house analysis, visualization, and reporting—​combined with the flexibility to comply with changing state and federal requirements. End Point provides the hosting infrastructure, database, reporting systems, and customizations that agencies need in order to service to their populations.

Our work with health agencies is a great example of End Point’s ability to use our experience in open source technology, Ruby on Rails, manage and back up large secure datasets, and integrate reporting systems to build and support a full-stack application. We will discuss one such client in this case study.

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2017/01/24/trisano-case-study/image-0.jpeg" imageanchor="1"><img border="0" height="376" src="/blog/2017/01/24/trisano-case-study/image-0.jpeg"/></a></div>

### Why End Point?

End Point is a good fit for this project because of our expertise in several areas including reporting and our hosting capabilities. End Point has had a long history of consultant experts in PostgreSQL and Ruby on Rails, which are the core software behind this application.

Also, End Point specializes in customizing open-source software, which can save not-for-profit and state agencies valuable budget dollars they can invest in other social programs.

Due to the secure nature of the medical data in these database, we and our clients must adhere to all HIPAA and CDC policies regarding hosting of data handling, server hosting, and staff authorization and access auditing.

### Team

<div class="separator" style="clear: both; float: left; text-align: center; padding:10px;"><a href="/blog/2017/01/24/trisano-case-study/image-1-big.jpeg" imageanchor="1"><img border="0" height="100" src="/blog/2017/01/24/trisano-case-study/image-1.jpeg" width="100"/></a></div>

#### Steve Yoman

Steve serves as the project manager for both communication and internal development for End Point’s relationship with the client. Steve brings many years in project management to the table for this job and does a great job keeping track of every last detail, quote, and contract item.

<div class="separator" style="clear: both; float: left; text-align: center; padding:10px;"><a href="/blog/2017/01/24/trisano-case-study/image-2-big.jpeg" imageanchor="1"><img border="0" height="100" src="/blog/2017/01/24/trisano-case-study/image-2.jpeg" width="100"/></a></div>

#### Selvakumar Arumugam

Selva is one of those rare engineers who is gifted with both development and DevOps expertise. He is the main developer on daily tasks related to the disease tracking system. He also does a great job navigating a complex hosting environment and has helped the client make strides towards their future goals.

<div class="separator" style="clear: both; float: left; text-align: center; padding:10px;"><a href="/blog/2017/01/24/trisano-case-study/image-3-big.jpeg" imageanchor="1"><img border="0" height="100" src="/blog/2017/01/24/trisano-case-study/image-3.jpeg" width="100"/></a></div>

#### Josh Tolley

Josh is one of End Point’s most knowledgeable database and reporting experts. Josh’s knowledge of PostgreSQL is extremely helpful to make sure that the data is secure and stable. He built and maintains a standalone reporting application based on Pentaho.

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2017/01/24/trisano-case-study/image-4-big.jpeg" imageanchor="1"><img border="0" src="/blog/2017/01/24/trisano-case-study/image-4.jpeg" width="500"/></a></div>

### Application

The disease tracking system consists of several applications including a web application, reporting application, two messaging areas, and SOAP services that relay data between internal and external systems.

**TriSano**: The disease tracking web app is an open source Ruby on Rails application based on the TriSano product, originally built at the Collaborative Software Initiative. This is a role-based web application where large amounts of epidemiological data can be entered manually or by data transfer.

**Pentaho**: Pentaho is a PostgreSQL reporting application that allows you to run a separate reporting service or embed reports into your website. Pentaho has a community version and an enterprise version, which is what is used on this particular project. This reporting application provides OLAP services, dashboarding, and generates ad hoc and static reports. Josh Tolley customized Pentaho so that the client can download or create custom reports depending on their needs.

**Two Messaging Area applications**: The TriSano system also serves as the central repository for messaging feeds used to collect data from local health care providers, laboratories throughout the state, and the CDC.

SOAP services run between the TriSano web app, the Pentaho reporting application, and the client’s data systems translate messages into the correct formats and relay the information to each application.

### Into the Future

Based on the success over 9+ years working on this project, the client continues to work with their End Point team to manage their few non open-source software licenses, create long term security strategies, and plan and implement all of their needs related to the continuous improvement and changes in epidemiology tracking. We partner with the client so they can focus their efforts on reading results and planning for the future health of their citizens. This ongoing partnership is something End Point is very proud to be a part of and we hope to continue our work in this field well into the future.
