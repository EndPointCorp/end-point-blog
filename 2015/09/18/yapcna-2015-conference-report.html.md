---
author: Josh Lavin
gh_issue_number: 1159
tags: conference, perl
title: YAPC::NA 2015 Conference Report
---

In June, I attended the [Yet Another Perl Conference (North America)](http://www.yapcna.org/yn2015/), held in Salt Lake City, Utah. I was able to take in a training day on [Moose](https://metacpan.org/pod/Moose), as well as the full 3-day conference.

The [Moose Master Class](http://www.yapcna.org/yn2015/masters.html#Moose) ([slides and exercises here](https://github.com/moose/intro-to-moose)) was taught by Dave Rolsky (a Moose core developer), and was a full day of hands-on training and exercises in the Moose object-oriented system for Perl 5. I’ve been experimenting a bit this year with the related project [Moo](https://metacpan.org/pod/Moo) (essentially the best two-thirds of Moose, with quicker startup), and most of the concepts carry over, with just slight differences.

Moose and Moo allow the modern Perl developer to quickly write [OO Perl code](http://www.modernperlbooks.com/books/modern_perl_2014/07-object-oriented-perl.html), saving quite a bit of work from the [older](http://perltricks.com/article/25/2013/5/20/Old-School-Object-Oriented-Perl) “[classic](https://perlmaven.com/getting-started-with-classic-perl-oop)” methods of writing OO Perl. Some of the highlights of the Moose class include: 

- Sub-classing is discouraged; this is better done using Roles
- Moose eliminates more typing; more typing can often equal more bugs
- Using [namespace::autoclean](https://metacpan.org/pod/namespace::autoclean) at the top is a best practice, as it cleans up after Moose
- Roles are what a class *does*, not what it *is*. Roles add functionality.
- Use [types](https://en.wikipedia.org/wiki/Type_system) with [MooseX::Types](https://metacpan.org/pod/MooseX::Types) or [Type::Tiny](https://metacpan.org/pod/Type::Tiny) (for Moo)
- Attributes can be objects (see slide 231)

Additional helpful resources for [OO Perl](http://perldoc.perl.org/perlootut.html) and [Moo](http://kablamo.org/slides-intro-to-moo/#/).

At the YAPC::NA conference days, I attended all joint sessions, and breakout sessions that piqued my interest. Here are some of the things I noted:

- The author of [Form::Diva](https://metacpan.org/pod/Form::Diva) gave a lightning talk (approx. 5 minutes) about this module, which allows easier HTML form creation. I was able to chat with the author during a conference mixer, and the next time I need a long HTML form, I will be giving this a try.
- One lightning talk presenter suggested making *comments stand out*, by altering your editor’s code highlight colors. Comments are often muted, but making them more noticeable helps developers, as comments are often important guides to the code.
- [plenv](https://github.com/tokuhirom/plenv) (which allows one to install multiple versions of Perl) can remember which Perl version you want for a certain directory (plenv local)
- [pinto](https://metacpan.org/pod/pinto) is useful for managing modules for a project
- Sawyer did a [talk on web scraping](http://www.yapcna.org/yn2015/talk/6077) in which he demonstrated the use of [Web::Query](https://metacpan.org/pod/Web::Query), which provides jQuery-like syntax for finding elements in the page you wish to scrape. There are many tools for web scraping, but this one seems easy to use, if you know jQuery.
- [DBIC’s](https://metacpan.org/pod/DBIx::Class) “deploy” will create new tables in a database, based on your schema. [DBIx::Class::Fixtures](https://metacpan.org/pod/DBIx::Class::Fixtures) can grab certain data into files for tests to use, so you can keep data around to ensure a bug is still fixed.

The presenter of *[What is this “testing” people keep talking about?](http://www.yapcna.org/yn2015/talk/6046)* did a great job researching a topic which he knew nothing about until after his talk was accepted. If there is ever a good way to learn something, it’s teaching it! [Slides are here.](http://deanza.edu/faculty/metcalfkevin/whatistesting.pdf) 

The [talk on Docker](http://www.yapcna.org/yn2015/talk/5915) ([slides](https://www.slideshare.net/lembark/perl-inside-a-box-building-perl-for-docker)) was interesting. Highlights I noted: use [busybox](https://en.wikipedia.org/wiki/BusyBox), then install Perl on top of busybox (you can run [Plack](http://plackperl.org/) *from* this Perl); Gentoo is easy to dockerize, as about half the size of Ubuntu; [Perl Dockerfiles](https://github.com/perl/docker-perl); build Perl on a local system, then copy to Docker image, in Docker file.

I attended some talks on the long-awaited Perl 6, which is apparently to be released by the end of this year. While I’m not sure how practical Perl 6 will be for a while, one of the most interesting topics was that Perl 6 knows [how to do math](https://www.slideshare.net/Ovid/perl-6-for-mere-mortals), such as: `solve for "x": x = 7 / 2`. Perl 6 gets this “right”, as far as humans are concerned. It was interesting that many in attendance did not feel the answer should be “3.5”, due to what I suspect is prolonged exposure to how computers do math.

One talk not related to Perl was [Scrum for One](http://www.yapcna.org/yn2015/talk/6031) ([video](https://youtu.be/Zh7dXvQY-hg)), which discussed how to use the principles of [Scrum](https://en.wikipedia.org/wiki/Scrum_%28software_development%29) in one’s daily life. Helpful hints included thinking of your tasks in the [User Story](https://en.wikipedia.org/wiki/User_story) format: “as a $Person, I would like $Thing, so that $Accomplishment”; leave murky stories on the backlog, as you must know what “done” looks like; the current tasks should include things doable in the next week—​this prevents you from worrying about *all* tasks in your list. Personally, I’ve started using [Trello](https://trello.com/) boards to implement this, such as: Done, Doing, ToDo, Later.

Finally, while a great technical conference, YAPC’s biggest strength is bringing together the Perl community. I found this evident myself, as I had the opportunity to meet another attendee from my city. We were introduced at the conference, not knowing each other previously. When you have two Perl developers in the same city, it is time to resurrect your local [Perl Mongers](https://www.pm.org/) group, which is [what we did](http://bend.pm.org/)!
