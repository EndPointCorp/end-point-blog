---
author: Jon Jensen
gh_issue_number: 190
tags: perl
title: Perl's Scalar::Util::dualvar
---



I just came across this fun Perl function that I can't think of a (good) use for, but have to share.

In the [Scalar::Util](http://search.cpan.org/perldoc?Scalar::Util) module is the function dualvar:

dualvar NUM, STRING

Returns a scalar that has the value NUM in a numeric context and the value STRING in a string context.

```perl
    $foo = dualvar 10, "Hello";
    $num = $foo + 2;                    # 12
    $str = $foo . " world";             # Hello world
```

Using that in the right place could lead a future programmer down some fun debugging paths!


