---
author: Jeff Boes
title: SQL errors in Interchange
github_issue_number: 493
tags:
- interchange
- sql
date: 2011-09-07
---



Interchange has a little feature whereby errors in a [query] tag are reported back to the session just like form validation errors. That is, given the intentional syntax error here:

```nohighlight
[query ... sql="select 1 from foo where 1="]
```

Interchange will paste the error from your database in

```perl
  $Session->{errors}{'table foo'}
```

That’s great, but it comes with a price: now you have a potential for a page with SQL in it, which site security services like McAfee will flag as "SQL injection failures". Sometimes you just don’t want your SQL failures plastered all over for the world to see.

Simple solution:

```nohighlight
  DatabaseDefault LOG_SESSION_ERROR 0
```

in your Interchange configuration file, possibly constrained so it only affects production (because you’d love to see your SQL errors when you are testing, right?).


