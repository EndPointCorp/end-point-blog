---
author: Jeff Boes
title: Interchange Form Testing with WWW::Mechanize
github_issue_number: 853
tags:
- automation
- interchange
- perl
- testing
date: 2013-09-17
---

Recently, I encountered a testing challenge that involved making detailed comparisons between the old and new versions of over 200 separate form-containing HTML (Interchange) pages.

Because the original developers chose to construct 200+ slightly-different pages, rather than a table-driven Interchange flypage (curses be on them forever and ever, amen), an upgrade to change how the pages prepared the shopping cart meant making over 200 similar edits. (Emacs macros, yay!) Then I had to figure out how to verify that each of the 200 new versions did something at least *close* to what the 200 old versions did.

Fortunately, I had easy ways to identify which pages needed testing, construct URLs to the new and old pages, and even a way to “script” how to operate on the page-under-test. And I had WWW::Mechanize, which has saved my aft end more than once.

WWW::Mechanize is a pretty mature (originally 2008) “browser-like” system for fetching and acting on web pages. You can accept and store cookies, find and follow links, handle redirection, forms, you name it—​but not Javascript. Sorry, but there are other tools in the box that can help you if you are working with more interactive pages.

In my case, lack of JS wasn’t an issue. I just needed a way to fetch a page, tweak a form element or two, and submit the page’s POST for server processing. Then if I could capture the server-side state of my session, I’d be golden.

```perl
 1 #!/usr/local/bin/perl
 2 use strict;
 3 use warnings;
 4 use WWW::Mechanize;
 5 use Test::More;
 6 
 7 our $BASE = 'http://www.example.com/';
 8 
 9 my %common = (
10     agent => 'compare-pages',
11     autocheck => 1,
12     cookie_jar => { },
13     quiet => 1,
14     redirect_ok => 1,
15     timeout => 15,
16 );
17 my $old = WWW::Mechanize->new(
18     %common,
19 );
20 my $new = WWW::Mechanize->new(
21     %common,
22 );
23 
24 for my $page (@ARGV ? @ARGV : <>) {
25     print $page;
26     chomp $page;
27     $new->get( $BASE . 'newstuff/' . $page . '?mv_pc=RESET');
28     my $new_form = $new->form_with_fields('last_product');
29     $new->submit();
30     $new->form_with_fields('mv_todo');
31     $new->submit();
32     $new->get( $BASE . 'show-the-dump' );
33     $new->content =~ m/#+\s+SESSION\s+#+\n(.+)\n#+\s+END SESSION\s+#+/s;
34     my $new_session = eval $1;
35     delete $new_session->{carts}{main}[0]{$_} for qw(some fields);
36 
37     $old->get( $BASE . $page . '?mv_pc=RESET' );
38     my $old_form = $old->form_with_fields('order_item', 'mv_order_deliverydate');
39     $old->select('mv_order_deliverydate', {n => 2});
40     $old->submit();
41     $old->get( $BASE . 'show-the-dump' );
42     $old->content =~ m/#+\s+SESSION\s+#+\n(.+)\n#+\s+END SESSION\s+#+/s;
43     my $old_session = eval $1;
44     delete $old_session->{carts}{main}[0]{$_} for qw(other fields);
45 
46     is_deeply($old_session->{carts}{main}, $new_session->{carts}{main}, "$page : carts match") or exit;
47 }
48 
49 done_testing;
50 exit;
```

- 2-5: Very few external modules are needed for this. WWW::Mechanize is quite complete (but it has a slew of prerequisites). Test::More is used just to make our comparisons easier.

- 7: This will be the URL base for our requests.
- 9-22: we set up two separate user agents so that they don’t share cookies, history, or any state information that would confuse our comparisons.
- 27, 37: retrieving the pages under test. Note that in my case, “newstuff/” distinguished the new version from the original.
- 28, 38: specifying which form on the retrieved page is to be considered the “current” one. Note that I’m not using the returned value here (although it came in handy during debugging). “form_with_fields” lets you pick a form based on one or more fields named within it. In the event that there’s more than one, you get the first (and Mechanize complains with a warning—​but we’ve turned that off via the “quiet” option, above).
- 32, 41: In the interests of security, I’ve not shown the actual page we use to dump the session internals. However, for Interchange users it’s just a page with a “[dump]” tag. You might write something that produces plain text, or CSV, or JSON. In my case, the session dump contains Data::Dumper-style output that I can feed into Perl’s “eval” function.
- 35, 44: The two data structures resulting from the “old” and “new” pages aren’t exactly alike, so I remove the bits I don’t care about.
- 46: And Test::More to the rescue, saving me from having to re-invent the code that will compare a possibly-complex data structure down to the scalar members. I have it exit after a failure, since in my case one error usually meant a whole family of corrections that needed to be applied to several related pages.

And that’s all! My testing now consists of:

```bash
$ grep "some pattern that identifies my 200" *.html | perl compare_pages.pl
```

I also had to adjust my Interchange configuration so my script would be accepted as a “robot”:

```nohighlight
RobotUA compare-pages
```

As a result of this testing, I identified at least a few pages where the “old” and “new” forms did not result in the same cart configuration, so I was able to fix that before it went live and caused untold confusion.

I hope this excursion into page-testing has proven interesting.


