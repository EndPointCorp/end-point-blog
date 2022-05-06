---
author: Elizabeth Garrett Christensen
title: 'Client Case Study: Carjojo'
github_issue_number: 1279
tags:
- angular
- case-study
- clients
- django
date: 2016-12-23
---

[Carjojo](https://www.carjojo.com/)’s site makes use of some of the best tools on the market today for accessing and displaying data. Carjojo is a car buying application that takes data about car pricing, dealer incentives, and rebate programs and aggregates that into a location-specific vehicle pricing search tool. The Carjojo work presented a great opportunity for End Point to utilize our technical skills to build a state-of-the-art application everyone is very proud of. End Point worked on the Carjojo development project from October of 2014 through early 2016, and the final Carjojo application launched in the summer of 2016. This case study shows that End Point can be a technology partner for a startup, enabling the client to maintain their own business once our part of the project is over.

### Why End Point?

<div class="separator" style="clear: both; float: right; text-align: center;"><img height="375" id="docs-internal-guid-bf89d7d8-193d-dd5c-ed85-19fbe48e18e4" src="/blog/2016/12/client-case-study-carjojo/image-0.png" style="border: medium none; transform: rotate(0rad);" width="338"/></div>

#### Reputation in full stack development

End Point has deep experience with full stack development so for a startup getting advice from our team can prove really helpful when deciding what technologies to implement and what timelines are realistic. Even though the bulk of the Carjojo work focused on specific development pieces, having developers available to help advise on the entire stack allows a small startup to leverage a much broader set of skills.

#### Startup Budget and Timelines

End Point has worked with a number of startups throughout our time in the business. Startups require particular focused attention on budget and timelines to ensure that the minimum viable product can be ready on time and that the project stays on budget. Our consultants focus on communication with the client and advise them on how to steer the development to meet their needs, even if those shift as the project unfolds.

#### Client Side Development Team

One of the best things about a lot of our clients is their technological knowledge and the team they bring to the table. In the case of Carjojo, End Point developers fit inside of their Carjojo team to build parts that they were unfamiliar with. End Point developers are easy to work with and already work in a remote development environment, so working in a remote team is a natural fit.

#### Client Side Project Management

End Point works on projects where either the project management is done in-house or by the client. In the case of a project like Carjojo where the client has technical project management resources, our engineers work within that team. This allows a startup like Carjojo insight into the project on a daily basis.

<div class="separator" style="clear: both; float: left; text-align: center;"><img height="350" id="docs-internal-guid-adf4efb0-193f-f2b6-279f-301698d2fdc2" src="/blog/2016/12/client-case-study-carjojo/image-1.png" style="-webkit-transform: rotate(0.00rad); border: none; transform: rotate(0.00rad);" width="150"/></div>

### Project Overview

The main goal of the Carjojo project was to aggregate several data sources on car price and use data analytics to provide useful shopper information, and display that for their clients.

Carjojo’s staff had experience in the car industry and leveraged that to build a sizeable database of information. Analytics work on the database provided another layer of information, creating a time- and location-specific market value for a vehicle.

Carjojo kept the bulk of the database collection and admin work in house, as well as provided an in-house designer that closely worked with them on their vision for the project. End Point partnered to do the API architecture work as well as the front end development.

A major component of this project was using a custom API to pull information from the database and display it quickly with high end, helpful infographics. Carjojo opted to use APIs so that the coding work would seamlessly integrate with future plans for a mobile application, which normally require a substantial amount of recoding.

Creating a custom API also allows Carjojo to work with future partners and leverage their data and analytics in new ways as their business grows.

### Team

<div class="separator" style="clear: both; float: left; text-align: center;"><img height="151" id="docs-internal-guid-c5221843-1937-962a-43e0-fc2b316dbed6" src="/blog/2016/12/client-case-study-carjojo/image-2.png" style="border: medium none; transform: rotate(0rad);" width="151"/></div>

**Patrick Lewis**: End Point project manager and front end developer. Patrick led development of the AngularJS front end application which serves as the main customer car shopping experience on the Carjojo site. He also created data stories using combinations of integrated Google Maps, D3/DimpleJS charts, and data tables to aid buyers with car searches and comparisons.

<div class="separator" style="clear: both; float: left; text-align: center;"><img height="153" id="docs-internal-guid-adf4efb0-1938-fb69-fe18-cada954bb90b" src="/blog/2016/12/client-case-study-carjojo/image-3.png" style="border: medium none; transform: rotate(0rad);" width="153"/></div>

**Matt Galvin:** Front end developer. Matt led the efforts for data-visualization with D3 and DimpleJS. He created Angular services that were used to communicate with the backend, used D3 and DimpleJS to illustrate information graphically about cars, car dealers, incentives, etc., sometimes neatly packaging them into directives for easy re-use when the case fit. He also created a wealth of customizations and extensions of DimpleJS which allowed for rapid development without sacrificing visualization quality.

<div class="separator" style="clear: both; float: left; text-align: center;"><b><img height="155" id="docs-internal-guid-adf4efb0-1939-cb73-eb4e-29fafe866ac4" src="/blog/2016/12/client-case-study-carjojo/image-4.png" style="-webkit-transform: rotate(0.00rad); border: none; transform: rotate(0.00rad);" width="155"/></b></div>

**Josh Williams:** Python API development. Josh led the efforts in connecting the database into Django and Python to process and aggregate the data as needed. He also used TastyPie to format the API response and created authentication structures for the API.

<div class="separator" style="clear: both; float: right; text-align: center;"><img height="279" id="docs-internal-guid-adf4efb0-1941-c6b8-7c03-547234b8105c" src="/blog/2016/12/client-case-study-carjojo/image-5.png" style="border: medium none; transform: rotate(0rad);" width="309"/> </div>

### Project Specifics

#### API Tools

Carjojo’s project makes use of some of the best tools on the market today for accessing and displaying data. [Django](https://www.djangoproject.com/) and [Tastypie](http://tastypieapi.org/) were chosen to allow for rapid API development and to keep the response time down on the website. In most cases the Django ORM was sufficient for generating queries from the data, though in some cases custom queries were written to better aggregate and filter the data directly within Postgres.

To use the location information in the database, some GIS location smarts were tied into Tastypie. Location searches tied into [GeoDjango](https://docs.djangoproject.com/en/1.10/ref/contrib/gis/) and generated [PostGIS](http://postgis.net/) queries in the database.

#### Front End Tools

[D3](https://d3js.org/) is standard in data-visualization and is great for doing both simple and complicated graphics. Many of Carjojo’s graphs were bar graphs, pie charts and didn’t really require writing out D3 by hand. We also wanted to make many of them reusable and dynamic (often based on search terms or inputs) with use of Angular directives and services. This could have been done with pure D3, but Dimple makes creating simple D3 graphs easy and fast.

[DimpleJS](http://dimplejs.org/) was used a lot in this project. Since Carjojo is data-driven, they wanted to display their information in an aesthetically pleasing manner and DimpleJS allowed us to quickly spin up information against some of the project’s tightest deadlines.

<div class="separator" style="clear: both; text-align: center;"><span id="docs-internal-guid-adf4efb0-192c-c5d7-47f8-c173ae3b292c" style='background-color: transparent; color: black; font-family: "arial"; font-size: 14.6667px; font-style: normal; font-variant: normal; font-weight: 400; margin-left: 1em; margin-right: 1em; text-decoration: none; vertical-align: baseline;'><img height="120" src="/blog/2016/12/client-case-study-carjojo/image-6.png" style="border: medium none; transform: rotate(0rad);" width="356"/></span></div>

The approach worked well for most cases. However, sometimes Carjojo wanted something slightly different than what DimpleJS does out of the box. One example of DimpleJS customization work can be found [here on our blog](/blog/2015/10/intro-to-dimplejs-graphing-in-6-easy/).

Another thing to note about the data visualizations was that sometimes when the data was plotted and graphed, it brought to light some discrepancies in the back-end calculations and analytics, requiring some back-and-forth between the Carjojo DBA and End Point.

### Results

Carjojo had a successful launch of their service in the summer of 2016. Their system has robust user capabilities, a modern clean design, and a solid platform to grow from. The best news for Carjojo is that now the project has been turned back over to them for development. End Point believes in empowering our clients to move forward with their business and goals without us. Carjojo knows that we’ll be here for support if they need it.

<img height="491" id="docs-internal-guid-adf4efb0-192c-4e5e-97ff-690dabfbb0ec" src="/blog/2016/12/client-case-study-carjojo/image-7.png" style="border: medium none; transform: rotate(0rad);" width="640"/>
