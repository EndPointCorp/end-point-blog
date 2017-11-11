---
author: Josh Lavin
gh_issue_number: 1246
tags: conference, perl
title: Report on The Perl Conference 2016
---

In June, I traveled to Orlando, Florida to attend the event formerly known as *Yet Another Perl Conference* (or YAPC::NA), now known as [The Perl Conference](http://www.yapcna.org/yn2016/). This was my second time in a row to attend this conference (after my first attendance back in 2007).

Conferences are a great place to learn how others are using various tools, hear about new features, and interact with the community. If you are speaking, it's a great opportunity to brush up on your subject, which was true for me in the extreme, as I was able to give a talk on the PostgreSQL database, which I hadn't used in a long time (more on that later).

### The conference name

The event organizers were able to license the name *The Perl Conference* from O'Reilly Media, as O'Reilly doesn't hold conferences by this name anymore. This name is now preferred over "YAPC" as it is more friendly to newcomers and more accurately describes the conference. [More on the name change.](http://www.yapcna.org/yn2016/news/1397)

### Notes from the conference

Over the three days of the conference, I was able to take in many talks. Here are some of my more interesting notes from various sessions:

<div class="separator" style="clear: both;">
<blockquote class="twitter-tweet" data-lang="en" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;">
    <p dir="ltr" lang="en">
        Yes, this is happening <a href="https://twitter.com/YAPCNA">@YAPCNA</a>
        <br/>
        <a href="https://twitter.com/JayceHall/status/745616157768482816"><img border="0" height="256" src="/blog/2016/07/27/report-on-perl-conference-2016/image-0.jpeg" width="320"/></a>
    </p>
    <cite style="float:right">— Jason Hall (@JayceHall) <a href="https://twitter.com/JayceHall/status/745616157768482816">June 22, 2016</a></cite>
</blockquote>
</div>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

- [MetaCPAN](https://metacpan.org/) is the best way to browse and search for Perl modules. Anyone can help with development of this fine project, via [their GitHub](https://github.com/metacpan/metacpan-web).
- [Ricardo Signes](https://metacpan.org/author/RJBS) says "use [subroutine signatures](http://perldoc.perl.org/perlsub.html#Signatures)!" They are "experimental", but are around to stay.
- Perl6 is written in Perl6 (and something called "[Not Quite Perl](https://github.com/perl6/nqp)"). This allows one to read the source to figure out how something is done. *(There were many talks on Perl6, which is viewed as a different programming language, not a replacement for Perl5.)*
- [jq](https://stedolan.github.io/jq/) is a command-line utility that can pretty-print JSON (non Perl, but nice!)
- Ricardo Signes gave a [talk on encoding](https://www.youtube.com/watch?v=TmTeXcEixEg) that was over my head, but very interesting.
- The presenter of *Emacs as Perl IDE* couldn't attend, so Damian Conway spoke on [VIM as Perl IDE](https://www.youtube.com/watch?v=9u6O0dLuqhI) (photo above)

From [John Anderson's talk](http://www.yapcna.org/yn2016/talk/6599):

- Just say "no" to system Perl. Use [plenv](https://github.com/tokuhirom/plenv) or the like.
- There's a DuckDuckGo [bang command](https://duckduckgo.com/bang) for searching MetaCPAN: !cpan [module]
- Use [JSON::MaybeXS](https://metacpan.org/pod/JSON::MaybeXS) over the plain JSON module.
- Use [Moo](https://metacpan.org/pod/Moo) for object-oriented programming in Perl, or Moose if you must.
- Subscribe to [Perl Weekly](http://perlweekly.com/)
- Submit your module on [PrePAN](http://prepan.org/) first, to receive feedback before posting to CPAN.

Lee Johnson gave a talk called [Battling a legacy schema with DBIx::Class](http://www.yapcna.org/yn2016/talk/6545) ([video](https://www.youtube.com/watch?v=ltckzIJYwHg)). Key takeaways:

- [When should I use DBIC?](https://programmers.stackexchange.com/questions/304520/when-should-i-use-perls-dbixclass/304557#304557)
- Something that has grown organically could be considered "legacy," as it accumulates [technical debt](https://en.wikipedia.org/wiki/Technical_debt)
- With [DBIC](https://metacpan.org/pod/DBIx::Class), you can start to manage that debt by adding relationships to your model, even if they aren't in your database
- RapidApp's [rdbic](https://metacpan.org/pod/Plack::App::RapidApp::rDbic) can help you visualize an existing database

[D. Ruth Bavousett spoke](https://www.youtube.com/watch?v=EXPElOT2fRE) on [Perl::Critic](https://metacpan.org/pod/Perl::Critic), which is a tool for encouraging consistency. Basically, Perl::Critic looks at your source code, and makes suggestions for improvement, etc. These suggestions are known as "policies" and can be configured to enable or disable any of them, or to even write new policies. One suggestion was to create a [Git hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) to run the perlcritic command at the time code is committed to the source code repository (possibly using [App::GitHooks](https://metacpan.org/pod/App::GitHooks)). End Point has its own perlcritic configuration, which I have started trying to use more.

Logan Bell shared [Strategies for leading a remote team](https://www.youtube.com/watch?v=uW4UX8UBAjg). Some of the tools and techniques he uses include:

- [tmate](https://tmate.io/) for terminal sharing
- [HipChat](https://www.hipchat.com/), with a chat room just for complaining called "head to desk"
- Holds one-on-one meetings every Monday for those he works with and directs
- Has new team members work on-site with another team member their first week or so, to help understand personalities that don't often come across well over chat
- Tries to have in-person meetings every quarter or at least twice a year, to bring the team together

### My talk

Finally, my own talk was titled [Stranger in a Strange Land: PostgreSQL for MySQL users](http://www.yapcna.org/yn2016/talk/6631) ([video](https://www.youtube.com/watch?v=sH41r_MOSH0)). I hadn't used Postgres in about seven years, and I wanted to get re-acquainted with it, so naturally, I submitted a talk on it to spur myself into action!

In my talk, I covered:

- the history of MySQL and Postgres
- how to pronounce "PostgreSQL"
- why one might be preferred over the other
- how to convert an existing database to Postgres
- and some tools and tips.

I enjoyed giving this talk, and hope others found it helpful. All in all, The Perl Conference was a great experience, and I hope to continue attending in the future!

[All videos from this year's conference](https://www.youtube.com/user/yapcna/search?query=2016)
