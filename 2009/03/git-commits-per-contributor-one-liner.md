---
author: Jon Jensen
title: Git commits per contributor one-liner
github_issue_number: 118
tags:
- git
- spree
date: 2009-03-18
---

Just for fun, in the [Spree Git repository](https://github.com/spree/spree):

```nohighlight
git log | grep ^Author: | sed 's/ <.*//; s/^Author: //' | sort | uniq -c | sort -nr
    813 Sean Schofield
     97 Brian Quinn
     81 Steph (Powell) Skardal
     42 Jorge Calás Lozano
     37 paulcc
     27 Edmundo Valle Neto
     16 Dale Hofkens
     13 Gregg Pollack
     12 Sonny Cook
     11 Bobby Santiago
      8 Paul Saieg
      7 Robert Kuhr
      6 pierre
      6 mjwall
      6 Eric Budd
      5 Fabio Akita
      5 Ben Marini
      4 Tor Hovland
      4 Jason Seifer
      2 Wynn Netherland
      2 Will Emerson
      2 spariev
      2 ron
      2 Ricardo Shiota Yasuda
      1 Yves Dufour
      1 yitzhakbg
      1 unknown
      1 Tomasz Mazur
      1 tom
      1 Peter Berkenbosch
      1 Nate Murray
      1 mwestover
      1 Manuel Stuefer
      1 Joshua Nussbaum
      1 Jon Jensen
      1 Chris Gaskett
      1 Caius Durling
      1 Bernd Ahlers
```
