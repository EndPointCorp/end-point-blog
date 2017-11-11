---
author: Mike Farmer
gh_issue_number: 781
tags: conference, ruby
title: 'Code Smells: Your Refactoring Cheat Codes'
---

Code smells are heuristics for refactoring. Resistance from our code are hints for refactoring. [John Pignata](https://twitter.com/jpignata) shares some great tips on how to actually go about refactoring a long method. Here are some of the highlights and steps that were covered.

First:

- Wrap entire method in a class
- Promote locals to instance variables

Second:

- Move the work into private methods

Third:

- Look for multiple responsibilities in the class
- Create new classes and adjust interfaces so everything still works

Fourth:

- Wrap your lower levels of abstraction (IO, Sockets).

Fifth:

- Your class may know too much about your lower level abstractions. Find ways to remove that knowledge using design patterns such as Observer/Listener.

Sixth:

- Look for case statements or other big conditionals
- Replace conditionals with polymorphism
- Move the conditional to a factory if applicable

Seventh:

- Remove data clumps such as knowledge of indexes in arrays or arrays of arrays (data[1][2]).

Eighth:

- Remove uncommunicative names such as “data” and “new”

Ninth:

- Look for variables that have same name but different meaning such as local variables that match instance variables.

Tenth:

- Look for nil checks. Look for indicators that nil actually means something and replace it with a NullObject.

These are all great suggestions for refactoring. If you want more information on this topic, I highly recommend Martin Fowler’s book “[Refactoring](http://amzn.com/0201485672)”.
