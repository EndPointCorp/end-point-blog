---
author: Josh Tolley
gh_issue_number: 795
tags: database, pentaho, reporting
title: Dimensional Modeling
---

People occasionally bring up the question, “What exactly is a data warehouse?” Though answers to this question vary, in short a data warehouse exists to analyze data and its behavior over large swaths of time or many different data sources. There’s more to it, though, than simply cramming historical data into the same old database. There are a number of defining characteristics, including the following:

- Query patterns and behavior
- Data retention policy
- Database structure

### Query Behavior

Data warehouses are sometimes called “OLAP” databases, which stands for “on-line analytical processing”, in contrast to the more common “OLTP”, or “on-line transaction processing” databases that manage data for an online storefront, a bug tracker, or a blog. A typical OLTP database supports applications that issue short, simple queries, and expect quick answers and support for many simultaneous transactions. The average OLAP query, by contrast, is generally read-only, but can be quite complex, and might take minutes or hours to complete. Such queries will often include heavy-duty statistical processing and data mining, involving terabytes of data.

### Data Retention

In a typical e-commerce database, eventually it becomes helpful to archive away older data that the front-end applications won’t need anymore. This helps performance, simplifies backups, and has the nice side-effect of leaving less data available for nefarious black hats that come snooping around. But it doesn’t make sense simply to discard much of this data, because it contains valuable information: customer behavior, supplier response time, etc. Often this deleted data remains alive, in a different form perhaps, in a data warehouse, which can contain data spanning many years.

### Database structure

Because query patterns in data warehouses differ so much from OLTP databases, it makes sense to structure the OLAP database to support its queries better. OLTP databases typically follow an “entity” model, hence the ubiquitous (if often not particularly useful) entity-relationship diagram. In such a design, tables represent objects stored in the database, such as an order, a user, or a product. OLAP databases, on the other hand, are commonly “dimensionally” modeled, which results in something called a “star schema”. In a star schema, the database contains large “fact” tables, full of foreign keys pointing to a set of “dimension” tables; when diagrammed, this looks like star with the fact table in the center, or for the more mechanically oriented, a wheel with the fact table at the hub and dimension tables at the end of each spoke. Rather than modeling a particular entity, the fact table generally describes business processes, such as customer conversion or shipping efficiency.

Dimensional modeling is an interesting topic full of its own rules of thumb, which often differ quite dramatically from typical entity modeling. For instance, whereas many database modelers complain about the use of [surrogate keys](https://en.wikipedia.org/wiki/Surrogate_key) in OLTP databases, it’s recommended in dimensional modeling. Dimensional databases generally don’t need OUTER joins, and rarely contain NULL values. As a result, business intelligence applications designed for data warehousing can make certain assumptions about how they’ll be asked to query the database. These assumptions obviously place some limits on the types of queries the database can process effectively. However it is through these assumptions that the system gains most of its efficiency.

Biggest among the limitations of an OLAP database is what’s called the “grain”. The grain describes exactly what information the fact table contains, and at what level of detail; it should be made clear during the first stages of warehouse design and widely understood by all involved. Queries that require information that isn’t part of the grain, or at finer levels of detail, must find a different fact table to use. But for queries which depend only on the available data, the fact table can be very efficient, as the database can partition it easily, and scan it unencumbered by simultaneous writes from other transactions, and filtered by simple conditions and INNER joins to the various dimension tables.

Data warehouses differ from the traditional database in several other ways, but this covers some of the basics. Dimensional modeling alone is a well-developed field of study with numerous intricacies, where experience and careful training are important for developing a useful final model. But the analytical power of such databases has been proven.
