---
author: Jeff Boes
gh_issue_number: 942
tags: interchange
title: Interchange table hacking
---



[Interchange](http://www.interchange.rtfm.info/docs/index.html) has a powerful but terribly obscure table administration tool called the Table Editor. You can create, update, and delete rows, and even upload whole spreadsheets of data, but the Table Editor isn't the most flexible thing in the world, so sometimes it just flat-out refuses to do what you want.

So you trick it.

A client wanted to upload data to a table that had a single-column primary key (serial), but also had a unique three-column key that was only used in the upload process (because the uploaded data was intended to replace rows with identical three-column combinations). Example:

In the table:

```nohighlight
code: 243
field1: AAA
field2: BBB
field3: CCC
data-fields: ...
```

In the spreadsheet:

```nohighlight
field1  field2  field3  data-fields...
 AAA     BBB     CCC     ...
```

In the database definition for this table, I had to add a secondary key definition for Interchange's use:

```nohighlight
Database  my_table  COMPOSITE_KEY  field1 field2 field3
```

in addition to the original key:

```nohighlight
Database  my_table  KEY  code
```

Here's
the problem this presents: when you add a COMPOSITE_KEY to a table, the table editor refuses to show per-row checkboxes that allow you to delete rows. I thought I might have to write a custom admin page to carry this off, but then I had an inspiration -- the REAL_NAME attribute of the Database directive:

```nohighlight
Database  my_table_edit my_table_edit.txt __SQLDSN__
Database  my_table_edit REAL_NAME my_table
Database  my_table_edit KEY code
Database  my_table_edit  PREFER_NULL code
Database  my_table_edit  AUTO_SEQUENCE 
```

This chunk of config-code tells Interchange that a second table can be accessed in the database, which is in fact the same table as the first (not a view, not a copy, but the actual table), but it doesn't have the COMPOSITE_KEY. When Interchange is restarted with this new definition in place, the Table Editor will show this second table with the familiar per-row checkboxes, even as it refuses to show them for the original table.

Phew. I dodged a bullet with that, as I didn't want to have to write a special page just to mimic the Table Editor.


