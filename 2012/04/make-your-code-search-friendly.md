---
author: Jeff Boes
title: Make your code search-friendly
github_issue_number: 587
tags:
- perl
- search
date: 2012-04-12
---



Here’s something about coding style that you may not have considered: is your code “search-friendly”? That is, does the format of your code help or hinder someone who might be searching it for context while debugging, extending, or just learning how it works?

Seriously Contrived Example (from Perl):

```perl
my $string = q{Your transaction could not be} .
   q{ processed due to a charge} .
   q{ card error.};
return $string;
```

Now someone’s going to experience this error and wonder where it occurs. So armed with grep, or ack, or git-grep, they set off into the wilderness:

```plain
$ git grep 'could not be processed'
$ git grep 'charge card error'
$ git grep -e 'transaction.*charge.*error'
$ alsdkjgalkghkf
```

(The last simulates pounding the keyboard with both fists.) I would suggest humbly that “strings you emit as a line should appear as a line in your code”, if for no other reason than that it makes it so much easier for you or others to find them. Thus:

```perl
my $string = <<'MSG';
Your transaction could not be processed due to a charge card error.
MSG
return $string;
```

