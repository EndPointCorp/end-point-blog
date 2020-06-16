---
author: Josh Tolley
gh_issue_number: 216
tags: open-source, postgres, pentaho, reporting, epitrax
title: Automatically building Pentaho metadata
---

Every so often I’ll hear of someone asking for a way to allow their users to write queries against their database without having to teach everyone SQL. There are various applications to do this: [BusinessObjects](https://web.archive.org/web/20091124142134/http://www.sap.com/solutions/sapbusinessobjects/index.epx) and [Cognos](https://www.ibm.com/products/cognos-analytics), are two common commercial examples, among many others. [Pentaho](http://www.pentaho.com) and [JasperReports](https://www.jaspersoft.com/) provide similar capabilities in the open-source world. These tools allow users to write reports by selecting fields from a user-friendly list, adding suitable constraints, and making other formatting and filtering choices, all without needing to understand SQL.

Those familiar with these packages know that in order to provide those nice, readable field names and simple, meaningful field groupings, the software generally needs some sort of metadata file. This file maps actual database fields to readable descriptions, specifies relationships between tables, and translates database field types to data types the reporting software understands. Typically to create such a file, an administrator spends a few hours in front of a vendor-supplied GUI application dragging graphical representations of their tables and columns around, defining joins and entering friendly descriptions.

For the [TriSano](https://web.archive.org/web/20091103150826/http://www.trisano.org/)™ project’s data warehouse, we needed a way to make regular modifications to the metadata file we gave to our Pentaho instance, in order to allow users to write reports that included data from the custom-built forms TriSano allowed them to create. To this end, we dove into the Pentaho APIs and developed a system to modify the metadata file automatically, adding tables and relationships whenever users create a new custom form.

TriSano is a Ruby-on-Rails application, running on JRuby, and the ability to use Java objects natively within JRuby was critical to interfacing correctly with Pentaho, a Java application. Within JRuby, our script can create Pentaho objects at will. Interested parties are encouraged to browse the [source code](https://github.com/csinitiative/trisano/blob/master/avr/bi/scripts/build_metadata/build_metadata.rb) of the TriSano script for the many details required to make this work.

In short, the script makes a new Pentaho metadata file entirely from scratch, using only information from a small number of purpose-built database tables, and database structure information taken directly from the PostgreSQL catalogs. It creates a schema file, populates it with descriptions of each of the actual database tables our users are interested in, assigns friendly names to each of the database objects with which users will interact, and divides up the results into user-defined groupings meaningful to their business.

I’m not familiar with a commercial reporting package that allows for modification of the underlying metadata without user intervention; doing something like this without the benefit of open-source software would have been daunting indeed.
