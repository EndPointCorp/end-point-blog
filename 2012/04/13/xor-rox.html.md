---
author: Jeff Boes
gh_issue_number: 589
tags: perl
title: XOR ROX
---



Recently a co-worker posed an interesting issue:

> Given a non-zero integer $delta,
> 
> 
> 
> an array of structures with two key/value pairs,
> 
> { flag => boolean, quantity => non-zero value }
> 
> 
> 
> Sort the array so that the first structures are those where either
> 
> 
> 
> flag is true and (sign of $delta and sign of $quantity are different)
> 
> or
> 
> flag is false and (sign of $delta and sign of $quantity are the same)
> 
> 
> 
> Secondarily, sort on the absolute value of $quantity.
> 
> 

A solution fairly leaped out at me, but I’m not claiming incredible programming skill: in fact, the solution suggested an XOR operation, which was the *second* time in about as many weeks that I’d gotten to use XOR in Perl code. (It’s one of those things that you can literally write tens of thousands of lines of code without ever needing, so a second opportunity within the same decade was pretty pleasing in a code-geek kind of way.)

The key to recognizing XOR in your problem solution is a pattern like:

A AND (B != C) or ~A AND (B == C)

or more simply:

(A AND ~B) or (~A AND B)

which is nothing more complex than the expanded equivalent of (A XOR B), from your college symbolic-logic class. The daunting sort problem becomes:

```perl
@sorted = sort {(
        ($a->{flag} xor ($a->{quantity} > 0 xor $delta > 0))
        <=>
        ($b->{flag} xor ($b->{quantity} > 0 xor $delta > 0))
) || abs($a->{quantity} <=> abs($b->{quantity})} @items;
```

That’s more “xor” operations in one statement than I’ve used in the last year.


