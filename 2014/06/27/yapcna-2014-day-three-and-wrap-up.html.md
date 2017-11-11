---
author: Jeff Boes
gh_issue_number: 1006
tags: conference, perl
title: YAPC::NA 2014, Day Three (and wrap-up)
---

My final day at YAPC::NA (Yet Another Perl Conference, North American flavor) summarized below. (For [Day Two](http://blog.endpoint.com/2014/06/yapcna-2014-day-two.html) and [Day One](http://blog.endpoint.com/2014/06/yapcna-2014-day-one.html), see the links.)

The conference organizers know their audience: day one started at 8 AM, day two at 9 AM, and the final day at 10 AM. (I took advantage of this lenient schedule to go for a swim in the hotel pool and grab a nice off-site breakfast. — Oh, dear, does my boss read this blog? :-)

I attended several medium-sized sessions during the day:

- Designing and Implementing Web Data Services in Perl

Michael McClennen, who programs for the Geology Department at the University of Wisconsin, outlined a flexible approach to providing an API to a complex data store. This supports a [front-end used for displaying](http://paleobiodb.org/navigator/) the location of fossils around the world, which is actually quite impressive. A typical URL for a data request looks like:

> ~~~nohighlight
> http://paleobiodb.org/data1.1/colls/summary.json?lngmin=-180&amp;lngmax=180&amp;latmin=-90&amp;latmax=90&amp;limit=all&amp;show=time&amp;level=3&amp;interval_id=14
> ~~~

(The URL above is wrapped for our blogger format; there should be no whitespace anywhere in it.)

This identifies a specific version of the service ("data1.1"), so that any backwards-incompatible changes to the API won't necessarily bring down a client. The requested format, JSON, is embedded in the request, too.

- Dancer: Getting to Hello, World

R Geoffrey Avery presented this talk, not as a way to get the application code together, but to put in place a fairly complex infrastructure:

        - PSGI
        - Plack
        - nginx
        - gcc
        - starman

as well as setting up appropriate permissions, etc.

Dancer was somewhat incidental to this talk. It's another web framework (a way of connecting structured URLs into a web service so that a given URL runs a given chunk of code, and delivers output in a particular format, HTML, JSON, XML, or what-have you). Setting it up on a bare system can be a chore, especially if you aren't a rugged, fearless [system administrator](http://geekswing.com/wp-content/uploads/2013/07/system-administrator-poster.jpg) type, so Avery gave us mortals a way to brute-force this installation without a lot of experience beforehand.

- Templates as a service – with swig.js

This was a remarkable, rapid tour of an effort by Logan Bell and others at Shutterstock, in which the [swig.js](http://paularmstrong.github.io/swig/) template system is set up to be provided as a web service. In other words, a Dancer application runs JavaScript inside of Perl to fill out HTML templates, which get delivered back to an invoking Perl application (and then, one assumes, served up as the output of that application). I found all this just a bit mind-blowing, and I'm looking forward to giving it a try.

- How Cognitive Linguistics Can Help You Become A (More) Bad-Ass Developer

This was a great place to wind up my technical-talk journey, because it wasn't actually a technical talk at all.

Aside: YAPC has adopted a special track of talks called "Awesome &amp;&amp; !Perl" (awesome and not Perl), in which presenters can talk about pretty much anything they want to. One session featured instruction on how to roast your own coffee. Others were somewhat closer to the spirit of the conference, but all were awesome from what I heard.

I can't do this talk justice in the short space I have, but let me try as follows: when you are thinking about an application, especially in designing it in an object-oriented fashion, you will quite often use a metaphor or a system of them: this object "is" a customer, that object "is" a purchase, etc. Then your system verbs reflect this metaphor:

```perl
$customer-&gt;bill_for_service(@params);
...
$purchase-&gt;refund($amount);
...
```

etc., This process goes on at almost every level of system design, and our ability to understand when we do it and how to do it well is an important insight.

YAPC wound down (if that can be said, given the pace) with a third series of lightning talks.

- Donations for grants to YAPC administration were sought, because the job of organizing the convention has become larger than one person's free time can support.

- How to raise geek children.

- A preview of and invitation to the Netherlands Perl Workshop in 2014.

- And a review of an effort that normalized and centralized all the regular expressions in an enterprise into a Perl module: part numbers, lot numbers, equipment IDs, etc., all served up symbolically.

Finally, we came to not one but two keynote addresses. The first, by Sawyer X of Booking.com, asked us to remember and focus on the joy of what we do. We get bogged down in the details of programming and dealing with users, requirements, and the like, but at heart we are problem-fixers and puzzle-solvers. That should be enough to spur some feelings of joy in our hearts.

John Anderson gave the final address, which returned to the theme of "Perl as a dying language" vs. its maturity, and asked us to be ambassadors of Perl. In particular, he noted that the CPAN site (which shares free software modules to thousands of programmers) has been copied by other communities, but the testing approach used to maintain those modules and their compatibility across versions of Perl has not been so widely adopted.

### Summary Time

YAPC::NA 2014 recorded 366 registered attendees (299 paid or signed up to present), coming from 13 countries and 69 Perl local user groups ("Perl mongers", in the lingo). 127 talks were submitted, 97 accepted. There were * at least* a dozen things I knew of but could not attend due to a conflict. Difficult choices had to be made.

Can I summarize something like 30 hours of experience in a paragraph? No, but I can hope to convey how much fun it was. I came away armed with at least a half-dozen things I want to explore right away, *today* if I can fit it into my schedule. Another half-dozen got tucked away "just in case". I'd like to thank everyone involved in YAPC::NA for a job well done. And thanks to End Point for giving me the opportunity to explore this.

Please visit their website, [yapcna.org](http://www.yapcna.org), for links to the talk slides, and check out their [video library](http://www.youtube.com/user/yapcna) of the talks; I know I will just because I couldn't be everywhere at once!
