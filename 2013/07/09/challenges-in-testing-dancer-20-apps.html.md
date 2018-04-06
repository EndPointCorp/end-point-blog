---
author: Jeff Boes
gh_issue_number: 831
tags: dancer, perl, testing
title: Challenges in testing Dancer 2.0 apps
---



I’ve been dabbling in Dancer, and I managed to put together a moderately complex re-hosting of a web application with Dancer 1.0, including a preliminary package of unit tests via Test::More.

Spoiler alert: I don’t yet have a solution, but I thought maybe this blog post would organize my thoughts to where someone else might peek in and spot my problem.

A bit of introduction follows for those who may not have been down this path before.

Testing a web application can take one of two general approaches:

1. Test the underlying code by calling it directly, one program to another, with no web server involved. This is pretty straightforward, although you may have to rig up some replacements for the environment (such as if your code expects CGI parameters, or reacts to things in the web server environment such as cookies, remote IP address, etc.). In any case, you have to recognize that you are now testing the code logic, not the actual interaction of your code as a subsystem in the web server.
1. Test the web application in its “native environment”, by issuing requests to its associated web server and examining the responses (as web pages, JSON, what-have-you). This is much preferred, as it will catch all sorts of subtle bugs, if you haven’t exactly reproduced the environment (for instance, “correctly” spelling HTTP_REFERRER in your rigged-up environment, whereas the misspelled HTTP_REFERER is actually in use).

The module [Dancer2::Test](https://metacpan.org/pod/Dancer2::Test) provides a small set of routines for supporting this second approach. For instance, you can verify that your routes are set up correctly via “route_exists”:

```perl
route_exists [ GET => '/index.html' ], "We can get the home page";
```

This behaves like the various test-helper routines in [Test::More](http://search.cpan.org/~exodist/Test-Simple-1.302136/lib/Test/More.pm). If the test succeeds (in this case, a route is defined that matches the path), great; if not, an error message is reported using the string parameter.

You can also verify that the correct page has been delivered without errors:

```perl
my $response = dancer_response GET => '/something';
is $response->{status}, 200, '/something returns OK';
like $response->{content}, qr{Something from the /something page};
```

dancer_response is the preferred way to go about this, because it captures status, headers, and content in one operation, saving you time but also avoiding the potential for disturbing the state of your application by subsequent requests.

Now, this article’s title starts with “Challenge”, so I should let the other shoe drop. The Dancer2::Test setup doesn’t seem to have a way to preserve “state” on the server between requests. So if your application supports, for instance, a “login” page and a “modify my account” page, you don’t really have a way to test the latter page, as you can’t remain logged in.


