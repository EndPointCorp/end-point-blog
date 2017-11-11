---
author: Ethan Rowe
gh_issue_number: 32
tags: perl
title: Perl incompatibility moving to 5.10
---

We're preparing to upgrade from Perl 5.8.7 to 5.10.0 for a particular project, and ran into an interesting difference between the two versions.

Consider the following statement for some hashref $attrib:

```
  use strict;
  ...
  my ($a, $b, $c) = @{%{$attrib}}{qw(a b c)};
```

In 5.8.7, the @{...} construct will return a slice of the hash referenced by $attrib, meaning that $a gets $attrib->{a}, $b gets $attrib->{b}, and so on.

In 5.10.0, the same construct will result in an error complaining about using a string for a hashref.

I suspect it's due to the hash dereference (%{$attrib}) being fully executed prior to applying the hash-slice operation (@{...}{qw(a b c)}), meaning that you're not operating against a hashref anymore.

Fortunately, the fix is wonderfully simple and significantly more readable:

```
  my ($a, $b, $c) = @$attrib{qw( a b c )};
```

The "fix" -- which is arguably how it should have been constructed in the first place, but this is software we're talking about -- works in both versions of Perl.
