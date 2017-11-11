---
author: Brian Buchalter
gh_issue_number: 609
tags: testing
title: Inherit an application by rewriting the test suite
---



One of my first tasks at End Point was to inherit a production application from the lead developer who was no longer going to be involved.  It was a fairly complex domain model and had passed through many developers' hands on a tight client budget.  Adding to the challenge was the absence of any active development; it's difficult to "own" an application which you're not able to make changes to or work with users directly.  Moreover, we had a short amount of time; the current developer was leaving in just 30 days.  I needed to choose an effective strategy to understand and document the system on a budget.

### Taking Responsibility

At the time I was reading  [Robert C. Martin's The Clean Coder](http://www.amazon.com/dp/0137081073), which makes a case for the importance of taking responsibility as a "Professional Software Developer".  He defines responsibility for code in the broadest of terms.

> 
> 
> Drawing from the Hippocratic oath may seem arrogant, but what better source is there?  And, indeed, doesn't it make sense that the first responsibility, and first goal, of an aspiring professional is to use his or her powers for good?
> 
> 

From there he continues to expound in his declarative style about how to do no harm to the function and structure of the code.  What struck me most about this was his conclusions about the necessity of testing.  The only way to do no harm to function is *know* your code works as expected.  The only way to *know* your code works is with automated tests. The only way to do no harm to structure is by "flexing it" regularly.

> 
> 
> The fundamental assumption underlying all software projects is that software is easy to change.  If you violate this assumption by creating inflexible structures, then you undercut the economic model that the entire industry is based on.
> 
> 
> 
> In short: *You must be able to make changes without exorbitant costs*.
> 
> 
> 
> The only way to prove that your software is easy to change is to make easy changes to it.  Always check in a module cleaner than when you checked it out.  Always make some random act of kindness to the code whenever you see it.
> 
> 
> 
> Why do most developers fear to make continuous changes to their code?  They are afraid they'll break it!  Why are they afraid to break it?  Because they don't have tests.
> 
> 
> 
> **It all comes back to the tests.  If you have an automated suite of tests that covers virtually 100% of the code, and if that suite of tests can be executed quickly on a whim, then *you simply will not be afraid to change the code*.**
> 
> 

### Test Suite for the Triple Win

Fortunately, there was a fairly large test suite in place for the application, but as common with budget-constrained projects, the tests didn't track the code.  There were hundreds of unit tests, but they weren't even executable at first.  After just a few hours of cleaning out tests for classes which no longer existed, I found about half of the 500 unit tests passed.  As I worked through repairing the tests, I was learning the business rules, classes, and domain of the application, all without touching "production" code (win). These tests were the documentation that future developers could use to understand the expected behavior of the system (double win).  While rebuilding the tests, I got to document bugs, deprecation warnings, performance issues and general code quality issues (triple win).

By the end of my 30 day transition, I had 500+ passing unit tests that were more complete and flexible than before.  Additionally, I added 100+ integration tests which allowed me to exercise the application at a higher level. Not only was I taking responsibility for the code, I was documenting important issues for the client and myself.  This helps the client feel I had done my job transitioning responsibilities.  This trust leaves the door open to further development, which means a better system over the long haul.


