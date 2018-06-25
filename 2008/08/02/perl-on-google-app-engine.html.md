---
author: Jon Jensen
gh_issue_number: 37
tags: perl, cloud
title: Perl on Google App Engine
---

People are working on getting [Perl support for Google App Engine](https://code.google.com/p/perl-appengine/), led by Brad Fitzpatrick (of Livejournal, memcached, etc. fame) at Google.

They’ve created a new module, [Sys::Protect](https://code.google.com/p/sys-protect/), to simulate the restricted Perl interpreter that would have to exist for Google App Engine. There’s [some discussion](https://brad.livejournal.com/2388824.html) of why they didn’t use [Safe](http://www.cpan.org/modules/by-module/Safe/), but it sounds like it’s based only on rumors of Safe problems, not anything concrete.

Safe is built on Opcode, and Sys::Protect appears to work the same way Safe + Opcode do, by blocking certain Perl opcodes. All the problems I’ve heard of and personally experienced with Safe were because it was working just fine—​but being terribly annoying because many common Perl modules do things a typical Safe compartment disallows. That’s because most Perl module writers don’t use Safe and thus never encounter such problems. It seems likely that Sys::Protect and a hardened Perl Google App Engine environment will have the same problem and will have to modify many common modules if they’re to be used.

Moving on, posters are talking about having support for Moose, Catalyst, CGI::Application, POE, Template::Toolkit, HTML::Template ... well, a lot. I guess that makes sense but it will be a lot of work and complicates the picture compared to the simple Python and custom Django-only initial unveiling of Google App Engine.

If you’re interested in Perl support for Google App Engine, log into your Google account, visit the [“issue” page](https://issuetracker.google.com/issues/35875213), and click on the star by the title to vote in favor of Perl support.
