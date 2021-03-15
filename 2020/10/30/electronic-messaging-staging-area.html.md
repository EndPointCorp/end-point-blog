---
author: "Elizabeth Garrett Christensen"
title: "EMSA: Electronic Messaging Staging Area"
tags: epitrax, open-source
gh_issue_number: 1680
---

![Sunset](/blog/posts/2020/10/30/electronic-messaging-staging-area/emsa-banner.jpg)
[Photo](https://flic.kr/p/pnRYaf) by [Lee Roberts](https://flic.kr/ps/2bXFPr), [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/)

End Point has been involved with developing disease surveillance software for over a decade. One component of that work is EMSA, short for “Electronic Messaging Staging Area”.

The EMSA system we’re currently using was developed by a consortium of states led by Utah, Kansas, and Nevada. It is a PHP web application and can be hosted in the cloud or on-premises as you would any other PHP application. 

### EMSA:

- Is an ingest system for HL7 or CSV-formatted lab reports from doctor offices, labs, and other official reporting groups.
- Allows exporting XML output to your disease surveillance system.
- Is a web console for managing messages.
- Allows you to see messages that are malformed.
- Has configurable rules for disease types and message routing; some messages may go directly into a surveillance system while others may be stored for later.
- Has configurable “automated workflows” to validate message information and perform tasks.
- Can be connected to a BI (Business Intelligence) tool for reporting, or the database can be queried directly.
- Works with integration packages like Rhapsody to bring in data from other systems.

End Point has also made custom modifications to EMSA allowing address validation for incoming messages.

EMSA can be deployed along with EpiTrax, the open source tracking system, or as a standalone application connected to a different disease surveillance system.

### Benefits of EMSA

Aside from all the features mentioned above, EMSA as an open-source solution brings other benefits:

- Reduced cost: Other than development and consulting to help set it up, there are no ongoing licensing costs.
- Designed to work as part of the open-source [EpiTrax disease surveillance system](/expertise/epitrax).
- Participating in the open source community that is growing in the healthcare industry.

### Help is available!

Interested in talking to us more about EMSA for your disease tracking? [Reach out today.](/contact)

### References

Emily Roberts, Rachelle Boulton, Josh Ridderhoff, Theron Jeppson. “Automated Processing of Electronic Data for Disease Surveillance.” *Online Journal of Public Health Informatics, 10(1):e2, May 22, 2018.* [https://doi.org/10.5210/ojphi.v10i1.8903](https://doi.org/10.5210/ojphi.v10i1.8903)
