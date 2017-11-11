---
author: Richard Templet
gh_issue_number: 542
tags: database, interchange, perl
title: Interchange loops using DBI Slice
---



One day I was reading through the documentation on [search.cpan.org](http://search.cpan.org) for the [DBI](http://search.cpan.org/~timb/DBI-1.616/DBI.pm) module and ran across an attribute that you can use with selectall_arrayref() that creates the proper data structure to be used with Interchange's object.mv_results loop attribute. The attribute is called Slice which causes selectall_arrayref() to return an array of hashrefs instead of an array of arrays. To use this you have to be working in global Perl modules as Safe.pm will not let you use the selectall_arrayref() method.

An example of what you could use this for is an easy way to generate a list of items in the same category. Inside the module, you would do like this:

```perl
my $results = $dbh-&gt;selectall_arrayref(
  q{
    SELECT
      sku,
      description,
      price,
      thumb,
      category, 
      prod_group
    FROM
      products
    WHERE
      category = ?},
  { Slice =&gt; {} }, 
  $category
);
$::Tag-&gt;tmpn("product_list", $results);
```

In the actual HTML page, you would do this:

```nohighlight
&lt;table cellpadding=0 cellspacing=2 border=1&gt;
&lt;tr&gt;
  &lt;th&gt;Image&lt;/th&gt;
  &lt;th&gt;Description&lt;/th&gt;
  &lt;th&gt;Product Group&lt;/th&gt;
  &lt;th&gt;Category&lt;/th&gt;
  &lt;th&gt;Price&lt;/th&gt;
&lt;/tr&gt;
[loop object.mv_results=`$Scratch-&gt;{product_list}` prefix=plist]
[list]
&lt;tr&gt;
  &lt;td&gt;&lt;a href="/cgi-bin/vlink/[plist-param sku].html"&gt;&lt;img src="[plist-param thumb]"&gt;&lt;/a&gt;&lt;/td&gt;
  &lt;td&gt;[plist-param description]&lt;/td&gt;
  &lt;td&gt;[plist-param prod_group]&lt;/td&gt;
  &lt;td&gt;[plist-param category]&lt;/td&gt;
  &lt;td&gt;[plist-param price]&lt;/td&gt;
&lt;/tr&gt;
[/list]
[/loop]
&lt;/table&gt;
```

We normally use this when writing ActionMaps and using some template as our setting for mv_nextpage.


