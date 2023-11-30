---
author: Jeff Boes
title: Cleaner redirection in Perl Dancer
github_issue_number: 1072
tags:
- dancer
- perl
date: 2015-01-21
---



Recently I worked on a project using the Perl web application framework [Dancer](http://www.perldancer.org) that had multiple paths to order a product:

```plain
 /product => /cart => /checkout => /receipt
```

That’s the standard approach. Then there was a “phone order” approach:

```plain
 /create_order => /checkout => /receipt
```

A “phone order” is one taken down (usually by phone), where the user who is logged in is not the same as the user who “owns” the order. Thus, one user is ordering on behalf of another: the order must be recorded as part of the second user’s order history, the various shipping and billing information must come from that user’s stored information, and even the product pricing has to be calculated as though that customer were doing the ordering rather than the logged-in user.

As a consequence, the phone order page flow actually ended up as:

```plain
 get /create_order => post /create_order => /checkout
```

The submission of the /create_order page was processed in an environment that knew about this “proxy” ordering arrangement, thus could do some particularly special-case processing, and then the idea was to pass off to the /checkout page, which would finalize the order including payment information.

All well and good, but when it came time to implement this, I was faced with a minor inconvenience and a bad choice:

Since /checkout was itself a POSTed page, I needed to reach that page with a set of form parameters in hand. So my original plan was:

```perl
 post '/create_order' => sub {
   ... # do my special-case processing, and then:
   forward '/checkout', { param1 => $value1, ... };
 };
```

While this works, the problem is that “forward” as a Dancer directive doesn’t interact with the browser: it just interrupts your path handling of “/create_order” and resumes at “/checkout”. So the browser, innocent of these shenanigans, remains on “/create_order”. It would be so much cleaner (darn my OCD!) if the browser ended up at “/checkout”.

That means you need to redirect the request, though. I.e.,

```perl
 post '/create_order' => sub {
   ... # do my special-case processing, and then:
   redirect '/checkout';  # hmm, something's missing here
 };
```

Hmm, redirect doesn’t support a parameter hash. Oh, well, no problem:

```perl
   redirect url_for('/checkout', { param1 => $value1, ... });
```

That gets the job done, but at a price: now instead of a nice, clean URL at my final destination, I get:

```plain
   .../checkout?param1=value1&param2=...
```

So, still not right. Some research and mailing-list inquiries led me to:

[
Why doesn’t HTTP have POST redirect?
](https://programmers.stackexchange.com/questions/99894/why-doesnt-http-have-post-redirect)

Short version: you can’t get there from here. Redirection is supposed to be “idempotent”, meaning you can repeat them without harm. That’s why when you refresh the page after a form submission, browsers will ask for permission to re-submit the form rather than just silently refreshing the page.

So what’s the option? Well, I can think of two approaches here:

One: instead of redirecting with parameters, store the parameters in the session:

```perl
 post '/create_order' => sub {
   ... # do my special-case processing
   session 'create_order_for_checkout' => { param1 => $value1, ... };
   redirect '/checkout';
 };
 post '/checkout' => sub {
   my $params = (session 'create_order_for_checkout')
     || params();
   ...
 };
```

Two: do away with the post handler for ‘/create_order’ altogether, and move the processing inside the post handler for ‘/checkout’. The merits of that depend on how complex the /create_order handler is.

I’m leaning toward the first approach, definitely.


