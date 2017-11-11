---
author: Jeff Boes
gh_issue_number: 694
tags: interchange, perl
title: Insidious List Context
---



Recently, I fell into a deep pit. Not [literally](http://www.theatlanticwire.com/entertainment/2012/09/actually-literally-what-your-crutch-word-says-about-you/56614/), but a deep pit of Perl debugging. As a result, I'm here to warn you and yours about "Insidious List Context(TM)".

(Note: this is a fairly elementary discussion, for people early in their Perl wizardry training.)

Perl has two contexts for evaluating expressions: list and scalar. (All who know this stuff cold can [skip down a ways](#skip_here).) "Scalar" context is what non-Perl languages just call "normal reality", but Perl likes to do things ... differently ... so we have more than one context.

In scalar context, a scalar is a scalar is a scalar, but a list becomes a scalar that represents the number of items in the list. Thus,

```nohighlight
@x = (1, 1, 1);  # @x is a list of three 1s
# vs.
$x = (1, 1, 1);  # $x is "3", the list size
```

In list context, a list of things is still a list of things. That's pretty simple, but when you are expecting a scalar and you get a list, your world can get pretty confused.

[]()
Okay, now the know-it-alls have rejoined us. I had a Perl hashref being initialized with code something like this:

```nohighlight
my $hr = {
  KEY1 => $value1,
  KEY2 => $value2,
  KEY_TROUBLE => (defined($foo) ? mysub($foo) : 1),
  KEY3 => $value3,
};
```

So here is the issue: if mysub() returns a list, then the hashref will get extra data. Remember, Perl n00bs, "=>" is not a magical operator, it's just a "fat comma". So a construction like this:

```nohighlight
1 => (2, 3, 4)
```

is really the same as:
```nohighlight
1, 2, 3, 4
```

Here's a complete example to illustrate just what size and shape hole I fell into:

```nohighlight
use strict;
use Data::Dumper;

my($value1,$value2,$value3,$foo) = qw(value1 value2 value3 foo);

my $hr = {
  KEY1 => $value1,
  KEY2 => $value2,
  KEY_TROUBLE => (defined($foo) ? mysub($foo) : 1),
  KEY3 => $value3,
};

print Data::Dumper->Dumper($hr);

sub mysub {
  return qw(junk extrajunk);
}
```

This outputs:

```nohighlight
$VAR1 = 'Data::Dumper';
$VAR2 = {
          'extrajunk' => 'KEY3',
          'KEY2' => 'value2',
          'KEY1' => 'value1',
          'value3' => undef,
          'KEY_TROUBLE' => 'junk'
        };
```

Now, the actual subroutine involved in my little adventure was even more insidious: it returned a list context because it was evaluating a regular expression, in a list context. Its actual source:

```nohighlight
sub is_yes {
   return( defined($_[0]) && ($_[0] =~ /^[yYtT1]/));
}
```

So watch those expression-evaluation contexts; they can turn fairly harmless expressions into code-busters.


