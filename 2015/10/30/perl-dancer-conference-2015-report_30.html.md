---
author: Josh Lavin
gh_issue_number: 1168
tags: conference, dancer, interchange, perl
title: Perl Dancer Conference 2015 Report—​Conference Days
---

In my [last post](/blog/2015/10/28/perl-dancer-conference-2015-report), I shared about the Training Days from the [Perl Dancer](https://www.perl.dance/) 2015 conference, in Vienna, Austria. This post will cover the two days of the conference itself.

While there were *several* wonderful talks, [Gert van der Spoel](https://www.perl.dance/users/21) did a great job of writing recaps of all of them ([Day 1](https://www.perl.dance/wiki/node/2015%20Day%201%20Summary), [Day 2](https://www.perl.dance/wiki/node/2015%20Day%202%20Summary)), so here I’ll cover the ones that stood out most to me.

### Day One

<div class="separator" style="clear: both; text-align: center; float:right"><a href="/blog/2015/10/30/perl-dancer-conference-2015-report_30/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/10/30/perl-dancer-conference-2015-report_30/image-0.jpeg"/></a>
<br/><br/>
<small><a href="https://twitter.com/sukria/status/657098210989776896">Dancer Conference, by Alexis Sukrieh</a> (used with permission)</small>
</div>

[Sawyer X](https://twitter.com/PerlSawyer) spoke on the *[State of Dancer](https://www.perl.dance/talks/17-state-of-dancer)*. One thing mentioned, which came up again later in the conference, was: **Make the effort, move to Dancer 2! Dancer 1 is frozen.** There have been some recent changes to Dancer:

- Middlewares for static files, so these are handled outside of Dancer
- New [Hash::MultiValue](http://p3rl.org/Hash::MultiValue) parameter keywords (route_parameters, query_parameters, body_parameters; covered in my [earlier post](/2015/10/perl-dancer-conference-2015-report.html))
- [Delayed responses](https://metacpan.org/pod/Dancer2::Manual#Delayed-responses-Async-Streaming) (asynchronous) with delayed keyword:
        - Runs on the server after the request has finished.
        - Streaming is also asynchronous, feeding the user chunks of data at a time.

Items coming soon to Dancer may include: Web Sockets (supported in [Plack](http://p3rl.org/Plack)), per-route [serialization](https://metacpan.org/pod/Dancer2::Manual#Serializers1) (currently enabling a serializer such as JSON affects the entire app—​later on, [Russell](https://twitter.com/veryrusty) [released a module](http://p3rl.org/Dancer2::Plugin::SendAs) for this, which may make it back into the core), Dancer2::XS, and [critic/linter policies](https://github.com/PerlDancer/perl-lint-policy-dancer2).

[Thomas Klausner](https://twitter.com/domm_favors_irc) shared about *[OAuth & Microservices](https://www.perl.dance/talks/18-oauth2%2C-resty-apis%2C-microservices)*. Microservices are a good tool to manage complexity, but you might want to aim for “monolith first”, [according to Martin Fowler](http://martinfowler.com/bliki/MonolithFirst.html), and only later break up your app into microservices. In the old days, we had “fat” back-ends, which did everything and delivered the results to a browser. Now, we have “fat” front-ends, which take info from a back-end and massage it for display. One advantage of the microservice way of thinking is that mobile devices (or even third parties) can access the same APIs as your front-end website.

[OAuth](https://oauth.net/) allows a user to login at your site, using their credentials from another site (such as Facebook or Google), so they don’t need a password for your site itself. This typically happens via JavaScript and cookies. However, to make your back-end “stateless”, you could use [JSON Web Tokens](https://jwt.io/) (JWT). Thomas showed some examples of all this in action, using the [OX Perl module](http://p3rl.org/OX).

One thing I found interesting that Thomas mentioned: *Plack middleware is the correct place to implement most of the generic part of a web app. The framework is the wrong part.* I think this mindset goes along with Sawyer’s comments about *Web App + App* in the Training Days.

[Mickey Nasriachi](https://twitter.com/0xMickey) [shared](https://www.perl.dance/talks/25-ponapi%3A-eliminate-the-bikesheding) his development on [PONAPI](https://github.com/mickeyn/ponapi), which implements the [JSON API](http://jsonapi.org/) specification in Perl. The JSON API spec is a standard for creating APIs. It essentially absolves you from having to make decisions about how you should structure your API.

<div class="separator" style="clear: both; text-align: center; float:right"><a href="/blog/2015/10/30/perl-dancer-conference-2015-report_30/image-1-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/10/30/perl-dancer-conference-2015-report_30/image-1.jpeg"/></a><br/><br/>
<small>Panorama from the south tower of St. Stephen’s cathedral, by this author</small></div>

Gert presented on *[Social Logins & eCommerce](https://www.perl.dance/talks/9-social-logins-for-e-commerce-sites)*. This built on the earlier OAuth talk by Thomas. Here are some of the pros/cons to social login which Gert presented:

- **Pros—​customer:**
    - Alleviates “password fatigue”
    - Convenience
    - Brand familiarity (with the social login provider)
- **Pros—​eCommerce website:**
    - Expected customer retention
    - Expected increase in sales
    - Better target customers
    - “Plug & Play” (if you pay)—​some services exist to make it simple to integrate social logins, where you just integrate with them, and then you are effectively integrated with whatever social login providers they support. These include Janrain and LoginRadius
- **Cons—​customer:**
    - Privacy concerns (sharing their social identity with your site)
    - Security concerns (if their social account is hacked, so are all their accounts where they have used their social login)
    - Confusion (especially on how to leave a site)
    - Usefulness (no address details are provided by the social provider in the standard scope, so the customer still has to enter extra details on your site)
    - Social account hostages (if you’ve used your social account to login elsewhere, you are reluctant to shut down your social account)
- **Cons—​eCommerce website:**
    - Legal implications
    - Implementation hurdles
    - Usefulness
    - Provider problem is your problem (e.g., if the social login provider goes down, all your customers who use it to login are unable to login to your site)
    - Brand association (maybe you don’t want your site associated with certain social sites)
- **Cons—​social provider:**
    - ???

Šimun Kodžoman spoke on *[Dancer + Meteor = mobile app](https://www.perl.dance/talks/22-dancer-%2B-meteor-%3D-mobile-app)*. [Meteor](https://www.meteor.com/) is a JavaScript framework for both server-side and client-side. It seems one of the most interesting aspects is you can use Meteor with the Android or iOS SDK to auto-generate a true mobile app, which has many more advantages than a simple HTML “app” created with [PhoneGap](http://phonegap.com/). Šimun is using Dancer as a back-end for Meteor, because the server-side Meteor aspect is still new and unstable, and is also dependent on [MongoDB](https://www.mongodb.org/), which cannot be used for everything.

End Point’s own Sam Batschelet shared his work on *[Space Camp](https://www.perl.dance/talks/4-space-camp---the-final-frontier)*, a new container-based setup for development environments. This pulls together several pieces, including [CoreOS](https://coreos.com/), [systemd-nspawn](http://www.freedesktop.org/software/systemd/man/systemd-nspawn.html), and [etcd](https://coreos.com/etcd/) to provide a futuristic version of [DevCamps](http://www.devcamps.org/).

### Day Two

<div class="separator" style="clear: both; text-align: center; float:right"><a href="/blog/2015/10/30/perl-dancer-conference-2015-report_30/image-2-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/10/30/perl-dancer-conference-2015-report_30/image-2.jpeg"/></a>
<br/><br/><small><a href="https://twitter.com/sbatschelet/status/657493819135541248">Conference goers, by Sam</a><br/>(used with permission)</small></div>

[Andrew Baerg](https://twitter.com/pullingshots) spoke on *[Taming the 1000-lb Gorilla](https://www.perl.dance/talks/20-taming-a-thousand-pound-gorilla)* that is [Interchange 5](https://www.interchangecommerce.org/). He shared how they have endeavored to manage their Interchange development in more modern ways, such as using unit tests and [DBIC](http://p3rl.org/DBIx::Class). One item I found especially interesting was the use of [DBIx::Class::Fixtures](http://p3rl.org/DBIx::Class::Fixtures) to allow saving bits of information from a database to keep with a test. This is helpful when you have a bug from some database entry which you want to fix and ensure stays fixed, as databases can change over time, and without a “fixture” your test would not be able to run.

[Russell Jenkins](https://twitter.com/veryrusty) shared *[HowTo Contribute to Dancer 2](https://www.perl.dance/talks/24-howto-contributeto-dancer2)*. He went over the use of [Git](https://git-scm.com/), including such helpful commands and tips as:

- git status --short --branch
- Write good commit messages: one line summary, less than 50 characters; longer description, wrapped to 72 characters; refer to and/or close issues
- Work in a branch (you shall not commit to master)
- “But I committed to master” --> branch and reset
- git log --oneline --since=2.weeks
- git add --fixup <SHA1 hash>
- The use of branches named with “feature/whatever” or “bugfix/whatever” can be helpful (this is Russell’s convention)

There are several [Dancer 2 issues tagged “beginner suitable”](https://github.com/PerlDancer/Dancer2/issues?q=is%3Aopen+is%3Aissue+label%3A%22Beginner+Suitable%22), so it is easy for nearly anyone to contribute. The [Dancer website](http://perldancer.org/) is [also on GitHub](https://github.com/PerlDancer/perldancer-website). You can even make simple edits directly in GitHub!

It was great to have the author of Dancer, [Alexis Sukrieh](https://twitter.com/sukria), in attendance. He shared his original vision for Dancer, which filled a gap in the Perl ecosystem back in 2009. The goal for Dancer was to create a DSL ([Domain-specific language](https://en.wikipedia.org/wiki/Domain-specific_language)) to provide a very simple way to develop web applications. The DSL provides “[keywords](https://metacpan.org/pod/Dancer2::Manual#DSL-KEYWORDS)” for use in the Dancer app, which are specific to Dancer (basically extra functionality for Perl). One of the core aspects of keeping it simple was to avoid the use of $self (a standby of object-oriented Perl, one of the things that you just “have to do”, typically).

Alexis mentioned that **Dancer 1 is frozen—​Dancer 2 full-speed ahead!** He also shared some of his learnings along the way:

- Fill a gap (define clearly the problem, present your solution)
- Stick to your vision
- Code is not enough (opensource needs attention; marketing matters)
- Meet in person (collaboration is hard; online collaboration is very hard)
- Kill the ego—​you are not your code

While at the conference, Alexis even wrote a Dancer2 plugin, [Dancer2::Plugin::ProbabilityRoute](https://metacpan.org/pod/Dancer2::Plugin::ProbabilityRoute), which allows you to do [A/B Testing](https://en.wikipedia.org/wiki/A/B_testing) in your Dancer app. (Another similar plugin is [Dancer2::Plugin::Sixpack](https://metacpan.org/pod/Dancer2::Plugin::Sixpack).)

Also check out [Alexis’ recap](https://web.archive.org/web/20151108214937/http://blog.sukria.net/2015/10/22/perl-dancer-2015-report/).

Finally, I was privileged to speak as well, on *[AngularJS & Dancer for Modern Web Development](https://www.perl.dance/talks/11-angularjs-%26-dancer-for-modern-web-development)*. Since this post is already pretty long, I’ll save the details for [another post](/blog/2015/10/30/angularjs-dancer-for-modern-web).

### Summary

In summary, the Perl Dancer conference was a great time of learning and building community. If I had to wrap it all up in one insight, it would be: **Web App + App**—​that is, your **application should be a compilation of: Plack middleware, Web App (Dancer), and App (Perl classes and methods)**.
