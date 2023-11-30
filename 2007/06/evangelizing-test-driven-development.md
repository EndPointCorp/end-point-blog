---
author: Ethan Rowe
title: Evangelizing Test-Driven Development
github_issue_number: 20
tags:
- testing
- perl
date: 2007-06-02
---

I read [Practices of an Agile Developer](/page/news/technews/practices_of_agile_developer_review/) shortly after it was published,
and I got pretty fired up about many ideas in it, with particular interest in test-driven development. From that point I did progressively more with testing in my day-to-day work, but everything changed for me once I went all-out and literally employed "test-driven development" for a minor project where I once wouldn't have worried about testing at all.

If you're not familiar with the principle, it basically boils down to this: When you are developing something, write the tests first.

I originally greeted this idea with skepticism, or viewed it as unrealistic. It also struck me as overkill for small projects. However, as I've been writing more tests, and finally came around to writing tests first, it's really demonstrated its value to me. I'll list an abstract set of benefits, and then provide a hopefully-not-too-tedious example.

### Benefits

#### 1. Cleaner interfaces

In order to test something, you test its interfaces. Which means you think through how the interface would really need to work from the
user's perspective. Of course, one should always plan a clean interface, but writing a test helps you think more concretely about what the exact
inputs and output should be. Furthermore, it serves to effectively document those interfaces by demonstrating, in code, the expected
behaviors. It isn't exactly a substitute for documentation, but it's worlds better than code with no tests and no docs. In fact, I would
argue that code with working tests and no docs is better than code with docs but no tests.

#### 2. Separation of concerns

When trying to write test cases for some new widget interface, it can become clear early on when you're trying to put too much into your magical widget,
and really need to be building separate, less magical, widgets.

#### 3. Coverage

Manual testing of something in the web-app space tends to mean banging on the website front-end. This does not guarantee coverage of all the
functional possibilities in your component. On the other hand, if you commit yourself to writing the tests for a method before you implement a method, you've got coverage on all your methods.

Of course, as your interface/component increases in complexity, you need to test for corner cases, complex interactions, etc. Just having one
test per component method would only suffice in very simple cases, and probably not even then.

You can use Devel::Cover (in Perl) to check the percentage of code covered by your tests, meaning you can empirically measure how rigorous your testing is.

#### 4. Reliability

Manual testing depends on the whims, time, patience, and attention to detail of a human test user. Users are people, and not to be trusted, no matter how good their intentions. Users do not do the same thing the same way every time. Users forget. They get impatient. They make bad assumptions. Etc. Users are people, people are animals, and animals are shifty. Would you trust a dog to test your app? A racoon? I would not. Mammals are silly things. Birds, reptiles, fish, etc. are also silly.

#### 5. Reusability

Manual tests take time, and that time cannot be recovered. Furthermore, the manual test does not produce anything lasting; your testing procedures and
results are excreted away into the ether, never to benefit anyone or anything ever again. They might as well have never happened, at least once you change anything at all in your code, data, or the environment it all runs in, when everything needs to be tested again.

Tests written alongside the test target component are concrete scripts that can be used and used again. They can be run any time you change the target
component as a basic sanity check. They can be used any time you feel like it, even if it isn't strictly necessary. They can be incorporated into a
larger framework to run periodic tests of a full staging environment. Thus, the time spent developing a test is an investment in the future. The time spent manually testing a component that could be tested in automated fashion simply cannot add any kind of long-term value.

#### 6. Precision

Manual testing works in big chunks; you're testing the overall observable behavior of a system. This is valuable and has its place. But when
something goes wrong, you then need to peel back the layers of your system onion to spot the piece(s) that cause your problem.

With tests written for each method/interface/etc. as you go, you exercise each portion of the interface in isolation (or as close to isolation as can
be realistically achieved). You will find your little problem spots long before you ever get to manual testing. You can enter the manual testing
portion with much greater confidence knowing that all the little pieces in your system have been empirically demonstrated to "work". Your manual
testing can focus only on higher-level concerns, and will usually take much less time.

### Objections refuted

#### "But writing tests takes time, and I don't want to pay extra for it!"

Nobody really *wants* to pay for anything. However, you expect the software you pay for to work, which means you expect the developers to
test it. Therefore, given that the developers (and you) both *are* going to test the software, it follows that you *do* have time to write the tests.

In my experience, writing the test first -- or at least alongside -- the new component does not negatively impact the overall delivery time
of a new component. It can actually positively impact delivery time compared with the tedium of manual testing; it is very inexpensive to
run the same test script over and over again while debugging, while it is more time-consuming to click "reload" or resubmit a form in your
web browser and then manually monitor the behaviors. Humans get tired of scanning lots of output looking for trouble and can miss problems;
automated tests always work the same way, so the effort put into them is an investment that pays off as long as the code exists.

It may vary for each individual, I suppose. For me, writing the test first made a lot of sense.

#### "You don't really mean 'write the test first', do you? That doesn't make sense."

It seems overly structured at first, until you get into the swing of it.

For my latest little project, I needed to create a newsletter recipient list. That meant adding a table to the database and creating a few
actions that would manipulate the table's contents. I used Moose to build a helper object module; this object should handle all the details
of manipulating the table, all done through a simple interface with methods that approximately matched the language of the problem domain.
In this case: "add_recipients", "remove_recipients", and "recipients", all working on top of a "newsletter_recipients" table; can you guess
what each method does?

So, I fired up vim, with my new Perl module in place. Then, I used vsplit to vertically split my editor screen with an empty test script in
the other window. I have my test script use Test::More's require_ok() function to make sure my new module can be loaded:

```
use lib '/path/to/my/custom/lib';
use Test::More tests => 1;

require_ok('My::Newsletter::RecipientList');
```

I save the script and run it. Lo and behold, my test script failed! Oh no! So I go back to vim, go to the window with my new module, and create the package skeleton:

```
package My::Newsletter::RecipientList;

use strict;
use warnings;
use Moose;

1;
```

Save the file. Get out of vim, run the script. It passes.

Then I decide that my new object needs a database handle to be passed in, and also needs the newsletter name to be specified. Both would be
object instance attributes. And given that it's a Moose-derived object, it'll use "new" as the constructor.

Back to vim, adding to the test:

```
use Test::More tests => 4;
use DBI;

my $module = 'My::Newsletter::RecipientList';
my $newsletter = 'some_newsletter';

my $dbh = DBI->connect(...);
my $lister = $module->new(
    dbh => $dbh,
    newsletter_name => $newsletter_name,
);

# Test object blessing
isa_ok(
    $lister,
    $module,
);

# Test the dbh attribute
cmp_ok(
    $lister->dbh,
    '==',
    $dbh,
    'Database handle attribute',
);

# Test the newsletter name
cmp_ok(
    $lister->newsletter_name,
    'eq',
    $newsletter,
    'Newsletter name attribute',
);
```

Save the script, run it, and I now have three failing tests. Go back to vim, go to my module, and add the code that provides the dbh and
newsletter_name attributes (which is trivial in Moose). Save the module, run the script, and now those three tests pass.

Repeat. Until you're done.

My example above is fairly tedious; I'm effectively testing that my test script is using the correct Perl search path, and that Moose is setting up
attributes correctly; I haven't tested anything specific to the problem domain. However, I found that as I sat down to write the next test for my
module's interface, the tests started flowing, and writing the tests became a way of sorting out mentally how the interface should behave. At one
point, I wrote something like 6 or 7 tests all in a row before returning to the module to implement the stuff that would actually get tested.

### Final thoughts

Object-oriented programming books and classes talk about documenting your preconditions and postconditions, and documenting the "object contract". It
doesn't always work that well to figure these things out on paper or in your head ahead of time, though, and documenting the stuff doesn't always help
much either. However, writing the tests effectively codifies the object contract, the expectations, everything. And it gives you something tangible
you'll be able to use for the rest of the project's life.

These methods obviously don't lend themselves easily to every kind of development project. It would be entirely different trying to
write tests for behaviors that are implemented in an ITL/PHP/JSP/ASP code-heavy page, for instance. However, any time you're getting into
significant business logic, you really shouldn't have that stuff in your page anyway. It's much better off living separately in a module that
you can run and test completely outside the context of your application server.

Furthermore, you don't need to have some big test suite framework in place to deal with this. Just put your tests in a reasonable place (I
like using a t/ subdirectory alongside the module being tested) and have them use Test::More. If they use Test::More, then it's really easy
to have them integrate into something larger under Test::Harness later on. A bunch of tests sitting in one directory is vastly preferable to
no tests at all. But using something like Test::More is much better than writing one-off Perl scripts that use your own custom routines
and whatnot, for the Test::Harness integration and because it doesn't require you to parse the output at all to determine success or failure.
Test::More is really, really easy to use, yet does most of what you'd ever need, at least what's possible to generalize.

Try it, and I think you'll like it.

(This was originally an internal email Ethan sent on November 3, 2006, and has been lightly edited by Jon Jensen.)
