---
author: Mark Johnson
title: Localize $@ in DESTROY
github_issue_number: 329
tags:
- perl
- tips
date: 2010-07-26
---



I have been conditioned now for many years in Perl to trust the relationship of $@ to its preceding eval. The relationship goes something like this: if you have string or block eval, immediately after its execution, $@ will either be false or it will contain the die message of that eval (or the generic “Died at ...” message if none is provided). Implicit here is that evals contained within an eval have their effects on $@ concealed, unless the containing eval “passes on” the inner eval’s die.

To quickly demonstrate:

```perl
use strict;
use warnings;

eval {
    print "Some stuff\n";
    eval {
        die 'Oops. Bad inner eval';
    };

    printf '$@ in outer eval: %s', $@;
};

printf '$@ after outer eval: %s', $@;
print $/;
```

produces the following output:

```plain
[mark@sokt ~]$ perl demo.pl 
Some stuff
$@ in outer eval: Oops. Bad inner eval at demo.pl line 7.
$@ after outer eval: 
[mark@sokt ~]$ 
```

Only if the containing eval itself dies do we find any data in $@:

```perl
use strict;
use warnings;

eval {
    print "Some stuff\n";
    eval {
        die 'Oops. Bad inner eval';
    };

    printf '$@ in outer eval: %s', $@;
    die 'Uh oh. Bad outer eval, too';
};

printf '$@ after outer eval: %s', $@;
print $/;
```

which produces:

```plain
[mark@sokt ~]$ perl demo.pl 
Some stuff
$@ in outer eval: Oops. Bad inner eval at demo.pl line 7.
$@ after outer eval: Uh oh. Bad outer eval, too at demo.pl line 11.

[mark@sokt ~]$ 
```

Why am I covering this, well known to any serious Perl programmer? Because I was caught off guard troubleshooting for a client last week when the result of an inner eval “leaked” through, affecting $@ of the containing eval. Because I was so conditioned to the stated relationship between eval and $@, it took me quite some time before I even opened up to the possibility.

It turned out the hitch had to do with garbage collection. The key was that the inner eval in question was initially called from a routine within an object’s DESTROY method. As I discovered, at least in Perl 5.10, if a containing eval dies, causing an object to go out of scope, and that object’s DESTROY itself executes an eval, $@ reflects the exit condition of the eval from within DESTROY, and not that of the containing eval. Even more strange, this is only true *if* the containing eval dies. If instead the containing eval completes, then that same dying eval within DESTROY *does not affect* the condition of $@ after the containing eval. It will still be false, as (IMO) it should be.

So, some code demonstrating each situation. We have 3 conditions:

- Containing eval dies, eval within DESTROY dies
- Containing eval dies, eval within DESTROY does not die
- Containing eval does not die, and eval is called within DESTROY, die or not.

Sample code demonstrating 1st condition:

```perl
use strict;
use warnings;

package Obj;

sub DESTROY {
    eval { die 'in DESTROY' };
}

package main;

eval {
    my $obj = {};

    bless $obj, 'Obj';
    die 'in main eval';

    print "Super important stuff that must finish or we really need to know about it!\n";

    return 1;
};

if ($@) {
    printf '$@ comes from code %s', $@;
}
else {
    print "Happy days! Our eval code ran to completion. Woot!\n";
}
```

Output as follows:

```plain
[mark@sokt ~]$ perl test1.pl 
$@ comes from code in DESTROY at test1.pl line 7.
[mark@sokt ~]$ 
```

Demo of 2nd condition:

```perl
use strict;
use warnings;

package Obj;

sub DESTROY {
    eval { 1 };
}

package main;

eval {
    my $obj = {};

    bless $obj, 'Obj';
    die 'in main eval';

    print "Super important stuff that must finish or we really need to know about it!\n";

    return 1;
};

if ($@) {
    printf '$@ comes from code %s', $@;
}
else {
    print "Happy days! Our eval code ran to completion. Woot!\n";
}
```

Output as follows:

```plain
[mark@sokt ~]$ perl test2.pl 
Happy days! Our eval code ran to completion. Woot!
[mark@sokt ~]$ 
```

Notice how particularly insidious the above is. We not only don’t know what the error was from the eval block that immediately precedes the evaluation of $@, but we actually think it succeeds!

Finally, the 3rd condition:

```perl
use strict;
use warnings;

package Obj;

sub DESTROY {
    eval { die 'in DESTROY' };
}

package main;

eval {
    my $obj = {};

    bless $obj, 'Obj';

    print "Super important stuff that must finish or we really need to know about it!\n";

    return 1;
};

if ($@) {
    printf '$@ comes from code %s', $@;
}
else {
    print "Happy days! Our eval code ran to completion. Woot!\n";
}
```

Output as follows:

```plain
[mark@sokt ~]$ perl test3.pl 
Super important stuff that must finish or we really need to know about it!
Happy days! Our eval code ran to completion. Woot!
[mark@sokt ~]$ 
```

So, fortunately, case 3 contains the leak when the outer eval completes successfully. We don’t introduce the worst possible situation: a successful eval that is subsequently treated as a failure. However, cases 1, and especially 2, are bad enough.

Now that I know all this, the solution is thankfully simple. When constructing objects, if they include a supplied DESTROY, always localize $@. It doesn’t matter whether I execute any evals or not; if the code calls any other routines that do, anywhere in the stack, the problem is introduced. A local $@ provides full protection.

A rerun of test1 but with localization provides a much more expected result:

```perl
use strict;
use warnings;

package Obj;

sub DESTROY {
    local $@;
    eval { die 'in DESTROY' };
}

package main;

eval {
    my $obj = {};

    bless $obj, 'Obj';
    die 'in main eval';

    print "Super important stuff that must finish or we really need to know about it!\n";

    return 1;
};

if ($@) {
    printf '$@ comes from code %s', $@;
}
else {
    print "Happy days! Our eval code ran to completion. Woot!\n";
}
```

Output as follows:

```plain
[mark@sokt ~]$ perl test1.pl 
$@ comes from code in main eval at test1.pl line 17.
[mark@sokt ~]$ 
```

and test2, which now doesn’t lie to us about the success of the eval of interest:

```perl
use strict;
use warnings;

package Obj;

sub DESTROY {
    local $@;
    eval { 1 };
}

package main;

eval {
    my $obj = {};

    bless $obj, 'Obj';
    die 'in main eval';

    print "Super important stuff that must finish or we really need to know about it!\n";

    return 1;
};

if ($@) {
    printf '$@ comes from code %s', $@;
}
else {
    print "Happy days! Our eval code ran to completion. Woot!\n";
}
```

Output as follows:

```plain
[mark@sokt ~]$ perl test2.pl 
$@ comes from code in main eval at test2.pl line 17.
[mark@sokt ~]$ 
```

