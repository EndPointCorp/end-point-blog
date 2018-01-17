---
author: Greg Davidson
gh_issue_number: 911
tags: database, environment, mysql, tools
title: Copy Data Between MySQL Databases with Sequel Pro
---

### Sequel Pro

<img alt="Sequel pro" border="0" height="350" src="/blog/2014/01/10/copy-data-between-mysql-databases-with/image-0.png" style="display:block" title="sequel-pro.png" width="450"/>

I often use [Sequel Pro](https://www.sequelpro.com/) when I’m getting up to speed on the data model for a project or when I just want to debug in a more visual way than with the mysql command-line client. It’s a free OS X application that lets you inspect and manage MySQL databases. I also find it very useful for making small changes to the data while I develop and test web apps.

### Quickly Copy Data Between Databases

I recently needed a way to copy a few dozen records from one [camp](http://www.devcamps.org/) to another. I tried using the ["SELECT...INTO OUTFILE"](https://dev.mysql.com/doc/refman/5.7/en/select-into.html) method but ran into a permissions issue with that approach. Using [mysqldump](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html) was another option but that seemed like overkill in this case — I only needed to copy a few records from a single table. At this point I found a really neat and helpful feature in Sequel Pro: Copy as SQL INSERT

<img alt="Copy as sql insert" border="0" height="407" src="/blog/2014/01/10/copy-data-between-mysql-databases-with/image-1.png" title="copy-as-sql-insert.png" width="562"/>

I simply selected the records I wanted to copy and used the “Copy as SQL INSERT” feature. The SQL insert statement I needed was now copied to the system clipboard and easily copied over to the other camp and imported via the mysql command-line client.

### Bundles

The Sequel Pro website describes [Bundles](https://www.sequelpro.com/bundles) which extend the functionality in various ways—including copying data as JSON. Very handy stuff. Many thanks to the [developers](https://web.archive.org/web/20140208071143/http://northofthree.com/) of this fine software. If you’re on OS X, be sure to give it a try.

