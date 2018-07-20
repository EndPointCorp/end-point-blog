---
author: David Christensen
gh_issue_number: 328
tags: database, postgres, scalability
title: 'PostgreSQL: Migration Support Checklist'
---



A database migration (be it from some other database to PostgreSQL, or even from an older version of PostgreSQL to a nice shiny new one) can be a complicated procedure with many details and many moving parts. I’ve found it helpful to construct a list of questions in order to make sure that you’re considering all aspects of the migrations and gauge the scope of what will be involved.  This list includes questions we ask our clients; feel free to contribute your own additional considerations or suggestions.

Technical questions:

1. **Database servers:** How many database servers do you have? For each, what are the basic system specifications (OS, CPU architecture, 32- vs 64-bit, RAM, disk, etc)? What kind of storage are you using for the existing database, and what do you plan to use for the new database? Direct-attached storage (SAS, SATA, etc.), SAN (what vendor?), or other? Do you use any configuration management system such as Puppet, Chef, etc.?

1. **Application servers and other remote access:** How many application servers do you have? For each, what are the basic system specifications (OS, CPU architecture, 32- vs 64-bit, RAM, disk, etc)?  Do you use any configuration management system such as Puppet, Chef, etc.? What other network considerations are there? Is ODBC used, or SSL transport, any VPNs? Are multiple datacenters involved? How about egress/ingress firewalls?

1. **Middleware:** Do you currently use any sort of connection pooling, load balancing, or other middleware between your application and database servers?

1. **Data needs:** Can you describe your data access patterns? i.e., is the majority of your data historical and rarely accessed? Are there any existing reporting needs that will need to be duplicated on the PostgreSQL system? Do you already have reports of database usage, including traffic levels, frequent or intensive queries, etc?

1. **Size:** What kind of transaction volume do you see? How large are your databases? How many tables do you have and what is the size of the larger ones? How many users or database connections will you need to support?

1. **Backups:** What are your current backup policies/procedures? How will these need to change with the move to PostgreSQL?

1. **Replication/load balancing:** What kind of system redundancy do you currently have/need? Do you have any kind of database load-balancing or master-slave replication?

1. **Monitoring:** What is the current monitoring/in-house support infrastructure? What needs to be duplicated, and can any portion of this facility be reused?

1. **Interfaces:** What language are your applications written in, and what drivers exist to connect to your current database? Will there be a compatible driver available in your language of choice in order?

1. **Extensions:** Are you currently using any in-database procedures or functionality (i.e., in PL/SQL or another embedded language of choice)? If so, how many? What will the difficulty be in porting these functions to PostgreSQL?

And a couple of business-related questions:

1. **Scheduling:** What is the timeframe for transition? When can appropriate downtime be scheduled? How much database downtime can you afford?

1. **Staffing:** Do you currently have in-house DBAs to manage the servers, etc on a day-to-day basis? Is there anyone with PostgreSQL experience or familiarity on staff?

Being able to answer all of these questions is critical to formulating a migration plan and carrying out a migration successfully.

Particularly with the impending (July 2010) end of life for previous PostgreSQL releases 7.4, 8.0 and (in November 2010) 8.1, a database migration may be on your radar. End Point is one of many professional PostgreSQL support companies who would be happy to assist you in your transition.


