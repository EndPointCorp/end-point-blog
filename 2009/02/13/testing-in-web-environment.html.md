---
author: Jeff Boes
gh_issue_number: 101
tags: browsers
title: Testing in the Web Environment
---

## Introduction

[Testing](http://en.wikipedia.org/wiki/Software_testing) is an important part of good software engineering practices. In fact, it can be said that it is at once the most important, and yet most neglected part of software engineering. Testing methodology for software engineering developed out of its hardware engineering roots: software was defined in terms of its inputs and outputs, and testing was similarly defined in terms of applied inputs and expected outputs.

However, software testing is more complex than that: this is
because software almost always incorporates "state" or memory that
affects subsequent operations. For instance, the following pseudocode:

> ~~~
> if (VALUE is not defined)
> then
> VALUE := 1.0
> fi
> FRACTION := 1.0 / VALUE
> ~~~
>

In this simple case, the code fragment will always operate correctly
on the first execution, but subsequent executions may fail if VALUE is
zero.

Testing web applications involves planning for this kind of memory,
because in essence a web application runs within a larger program (the
web server and perhaps the application server) and may inherit state
from the environment, or indeed may preserve its own state from one
page reference to the next.

In addition, web applications involve human factors.

- Does the application "display correctly" (whatever that means)?
- Does the page load "quickly enough"?
- Do dynamic elements (e.g. Ajax) respond appropriately?

Such factors are harder to measure than verifying that a sales tax
calculation returns an accurate number.

For these reasons, we turn to web application testing
frameworks. Loosely defined these frameworks provide either a substitute for, or
an interface to, a web browser that is under programmatic control.
So for instance, a test script can invoke the web application via URL
just as a browser would.
Then it can test for page content or metadata (title, etc.), and even
in some cases access embedded media such as image files.
The framework provides a way to operate the web application: through
it, the test script can submit forms, click on objects, respond to
dynamic events such as JavaScript alerts, and even operate the browser
in other ways: navigating via the "Back" button, saving files, etc.

Using such frameworks, the software engineer can automate the testing
process.
The application's performance can be defined in terms of the test
scripts that it passes, so that modifications to the application (new
functionality or bug repairs) can be validated against the existing
tests ([regression testing](http://en.wikipedia.org/wiki/Regression_testing)).

In this article, I'll briefly survey several approaches to web
application testing frameworks that are in use or under study at End
Point.

## WWW::Mechanize

The first framework is a Perl module called [
"WWW::Mechanize"](http://search.cpan.org/~petdance/WWW-Mechanize-1.30/lib/WWW/Mechanize.pm), and its associated extension ["Test::WWW::Mechanize"](http://search.cpan.org/~petdance/Test-WWW-Mechanize-1.14/Mechanize.pm).
This framework provides an object-oriented interface to an HTTP
connection which allows a test script, written in Perl, to perform
operations on a web site much like a browser, and to test the results
in various ways. By way of example, here is a script that operates on
the End Point website:

> ```
> use strict;
> use Test::WWW::Mechanize;
> use Test::More tests => 4;
> my $mech = Test::WWW::Mechanize->new();
> $mech->get_ok('http://www.endpoint.com', 'Home page fetched');
> $mech->title_like(qr/End Point/, 'Page mentions us');
> $mech->follow_link_ok({ text_regex => qr/Team Bios/ }, 'Found team bios');
> $mech->content_contains('Jeff Boes', 'Author was mentioned');
> ```

This test declares that we will run four tests.
It initializes the test framework with a call to the "new" method.
Then it executes the four tests, annotating each one with a message
that lets us identify which test failed by a human-friendly string
rather than a bare number.

The first test just checks that the framework can retrieve the home
page; failure would be caused by a server problem, DNS failure, etc.
The second test just verifies that the page title contains a particular
text pattern (the name of our company).
The third test finds a link (in this case, based on a pattern of text
in the link; we could also locate a link by URL, for example) and
verifies that the framework can follow the link.
The fourth and final test verifies that the author's name appears on
the page.

From simple building blocks like this, more and more complex tests can
be built up. Through the underlying framework, a test script can:

- set and retrieve form field values, including checkboxes and
selectors
- submit forms
- set and retrieve cookie values
- analyze images
- provide credentials for HTTP Basic Authentication (for
password-protected sites)

End Point has used this approach with success.
For example, the order and checkout process on [CityPass](http://www.citypass.com/) uses a
sequence of tests designed to place orders for every product offered,
in various combinations.
The test script makes a connection to the site's PostgreSQL
database allowing it to compare the resulting order receipts with the
matching database entries.

The major failing of the Mechanize family is that JavaScript is not
supported. Thus, this framework is not suitable for testing pages for
which major parts of the functionality are provided through JavaScript.

## HTTP::Recorder

This framework, another Perl module, is really a system for
constructing test scripts for use with WWW::Mechanize. It doesn't
offer any testing facility on its own; instead, it is designed to line
up between a browser and a web application, recording the mouse clicks
and keystrokes made, and emitting a test script that is then fed
through WWW::Mechanize (perhaps after suitable manual adjustment).

Again, this system doesn't recognize, operate on, or record JavaScript
events, so it's not as useful for testing sites with large amounts or critical sections of
JavaScript.

## Selenium

Selenium is a framework rather unlike the previous entries, although
from the view of the programmer developing a test script or suite, it
doesn't seem that much different.
Selenium has several components; the one that interests us most for
this particular survey is ["Selenium RC"](http://www.openqa.org/selenium-rc/) (Remote Control).
This component services requests from a test script written much like
the WWW::Mechanize scripts.
The Selenium RC server will start up a browser and translate test
script requests into actual mouse and keyboard events on the
controlled browser.

Selenium works with several different browsers, such as Firefox and
Microsoft Internet Explorer. For the vast majority of test scripts,
the only change required to switch from testing one browser platform
to another is to change a single line in the initial server request.

Selenium works with JavaScript events and functionality. You can, for
instance, test JavaScript "onmouseover" events, or field validation
through "onchange" or "onsubmit". Your test scripts can check for
JavaScript alerts and respond to them, and behave in nearly every way
just as a real user would, sitting in front of a real browser.

Selenium RC is implemented as a Java application, which means that its environment must include a Java installation (JVM).

The drawback of Selenium is that since it must be run in an
environment that includes a browser and window display system, you'll
almost certainly need to run your test script on a workstation, or a server with all the windowing software installed.

## Other approaches

- [OpenSTA](http://www.opensta.org/) (Open System Testing Architecture) is
more of a heavy-load testing framework, although it does provide a scripted setup.
- Usability testing environments such as [WAUTER](http://wauter.weeweb.com.au/)
are designed to observe and record end-user actions (such as scrolling and mouse clicks)
for later analysis.
