---
author: Richard Templet
gh_issue_number: 542
tags: database, interchange, perl
title: Interchange loops using DBI Slice
---

One day I was reading through the documentation on [search.cpan.org](http://search.cpan.org) for the [DBI](https://metacpan.org/pod/DBI) module and ran across an attribute that you can use with selectall_arrayref() that creates the proper data structure to be used with Interchange’s object.mv_results loop attribute. The attribute is called Slice which causes selectall_arrayref() to return an array of hashrefs instead of an array of arrays. To use this you have to be working in global Perl modules as Safe.pm will not let you use the selectall_arrayref() method.

An example of what you could use this for is an easy way to generate a list of items in the same category. Inside the module, you would do like this:

```perl
my $results = $dbh->selectall_arrayref(
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
  { Slice => {} }, 
  $category
);
$::Tag->tmpn("product_list", $results);
```

In the actual HTML page, you would do this:

```nohighlight
<table cellpadding=0 cellspacing=2 border=1>
<tr>
  <th>Image</th>
  <th>Description</th>
  <th>Product Group</th>
  <th>Category</th>
  <th>Price</th>
</tr>
[loop object.mv_results=`$Scratch->{product_list}` prefix=plist]
[list]
<tr>
  <td><a href="/cgi-bin/vlink/[plist-param sku].html"><img src="[plist-param thumb]"></a></td>
  <td>[plist-param description]</td>
  <td>[plist-param prod_group]</td>
  <td>[plist-param category]</td>
  <td>[plist-param price]</td>
</tr>
[/list]
[/loop]
</table>
```

We normally use this when writing ActionMaps and using some template as our setting for mv_nextpage.


