---
author: Jeff Boes
gh_issue_number: 853
tags: automation, interchange, perl, testing
title: Interchange Form Testing with WWW::Mechanize
---



Recently, I encountered a testing challenge that involved making detailed comparisons between the old and new versions of over 200 separate form-containing HTML (Interchange) pages.

Because the original developers chose to construct 200+ slightly-different pages, rather than a table-driven Interchange flypage (curses be on them forever and ever, amen), an upgrade to change how the pages prepared the shopping cart meant making over 200 similar edits. (Emacs macros, yay!) Then I had to figure out how to verify that each of the 200 new versions did something at least *close* to what the 200 old versions did.

Fortunately, I had easy ways to identify which pages needed testing, construct URLs to the new and old pages, and even a way to "script" how to operate on the page-under-test. And I had WWW::Mechanize, which has saved my aft end more than once.

WWW::Mechanize is a pretty mature (originally 2008) "browser-like" system for fetching and acting on web pages. You can accept and store cookies, find and follow links, handle redirection, forms, you name it -- but not Javascript. Sorry, but there are other tools in the box that can help you if you are working with more interactive pages.

In my case, lack of JS wasn't an issue. I just needed a way to fetch a page, tweak a form element or two, and submit the page's POST for server processing. Then if I could capture the server-side state of my session, I'd be golden.

```perl
#!/usr/local/bin/perl
use strict;
use warnings;
use WWW::Mechanize;
use Test::More;

our $BASE = 'http://www.example.com/';

my %common = (
    agent =&gt; 'compare-pages',
    autocheck =&gt; 1,
    cookie_jar =&gt; { },
    quiet =&gt; 1,
    redirect_ok =&gt; 1,
    timeout =&gt; 15,
);
my $old = WWW::Mechanize-&gt;new(
    %common,
);
my $new = WWW::Mechanize-&gt;new(
    %common,
);

for my $page (@ARGV ? @ARGV : &lt;&gt;) {
    print $page;
    chomp $page;
    $new-&gt;get( $BASE . 'newstuff/' . $page . '?mv_pc=RESET');
    my $new_form = $new-&gt;form_with_fields('last_product');
    $new-&gt;submit();
    $new-&gt;form_with_fields('mv_todo');
    $new-&gt;submit();
    $new-&gt;get( $BASE . 'show-the-dump' );
    $new-&gt;content =~ m/#+\s+SESSION\s+#+\n(.+)\n#+\s+END SESSION\s+#+/s;
    my $new_session = eval $1;
    delete $new_session-&gt;{carts}{main}[0]{$_} for qw(some fields);

    $old-&gt;get( $BASE . $page . '?mv_pc=RESET' );
    my $old_form = $old-&gt;form_with_fields('order_item', 'mv_order_deliverydate');
    $old-&gt;select('mv_order_deliverydate', {n =&gt; 2});
    $old-&gt;submit();
    $old-&gt;get( $BASE . 'show-the-dump' );
    $old-&gt;content =~ m/#+\s+SESSION\s+#+\n(.+)\n#+\s+END SESSION\s+#+/s;
    my $old_session = eval $1;
    delete $old_session-&gt;{carts}{main}[0]{$_} for qw(other fields);

    is_deeply($old_session-&gt;{carts}{main}, $new_session-&gt;{carts}{main}, "$page : carts match") or exit;
}

done_testing;
exit;
```

- 2-5: Very few external modules are needed for this. WWW::Mechanize is quite complete (but it has a slew of prerequisites). Test::More is used just to make our comparisons easier.

- 7: This will be the URL base for our requests.
- 9-22: we set up two separate user agents so that they don't share cookies, history, or any state information that would confuse our comparisons.
- 27, 37: retrieving the pages under test. Note that in my case, "newstuff/" distinguished the new version from the original.
- 28, 38: specifying which form on the retrieved page is to be considered the "current" one. Note that I'm not using the returned value here (although it came in handy during debugging). "form_with_fields" lets you pick a form based on one or more fields named within it. In the event that there's more than one, you get the first (and Mechanize complains with a warning -- but we've turned that off via the "quiet" option, above).
- 32, 41: In the interests of security, I've not shown the actual page we use to dump the session internals. However, for Interchange users it's just a page with a "[dump]" tag. You might write something that produces plain text, or CSV, or JSON. In my case, the session dump contains Data::Dumper-style output that I can feed into Perl's "eval" function.
- 35, 44: The two data structures resulting from the "old" and "new" pages aren't exactly alike, so I remove the bits I don't care about.
- 46: And Test::More to the rescue, saving me from having to re-invent the code that will compare a possibly-complex data structure down to the scalar members. I have it exit after a failure, since in my case one error usually meant a whole family of corrections that needed to be applied to several related pages.

And that's all! My testing now consists of:

```bash
$ grep "some pattern that identifies my 200" *.html | perl compare_pages.pl
```

I also had to adjust my Interchange configuration so my script would be accepted as a "robot":

```nohighlight
RobotUA compare-pages
```

As a result of this testing, I identified at least a few pages where the "old" and "new" forms did not result in the same cart configuration, so I was able to fix that before it went live and caused untold confusion.

I hope this excursion into page-testing has proven interesting.


