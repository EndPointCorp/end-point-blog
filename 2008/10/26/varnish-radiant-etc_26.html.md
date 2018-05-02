---
author: Ethan Rowe
gh_issue_number: 73
tags: hosting, postgres, rails, performance, cms
title: Varnish, Radiant, etc.
---

As my colleague [Jon mentioned](/blog/2008/10/22/walden-university-presidential-youth), the Presidential Youth Debates launched its [full debate content this week](http://www.youthdebate2008.org/).  And, as Jon also mentioned, the mix of tools involved was fairly interesting:

- [Radiant](http://radiantcms.org/), a simple Rails-based CMS
- [Varnish](http://varnish.projects.linpro.no/), a high-performance reverse proxy server
- [Amazon Simple Storage Service](http://aws.amazon.com/s3/), a scalable storage layer
- [PostgreSQL](http://www.postgresql.org/), the truly marvelous open-source relational database management system that End Point loves so well

Our use of Postgres for this project was not particularly special, and is simply a reflection of our using Postgres by default.  So I won't discuss the Postgres usage further (though it pains me to ignore my favorite piece of the software stack).

## Radiant

Dan Collis-Puro, who has done a fair amount of CMS-focused work throughout his career, was the initial engineer on this project and chose Radiant as the backbone of the site.  He organized the content within Radiant, configured the [Page Attachments extension](http://github.com/radiant/radiant-page-attachments-extension/tree/master) for use with Amazon's S3 (Simple Storage Service), and designed the organization of videos and thumbnails for easy administration through the standard Radiant admin interface.  Furthermore, prior to the release of the debate videos, Dan built a question submission and moderation facility as a Radiant extension, through which users could submit questions that might ultimately get passed along to the candidates for the debate.

In the last few days prior to launch, it fell to me to get the new debate materials into production, and we had to reorganize the way we wanted to lay out the campaign videos and associated content.  Because the initial implementation relied purely on conventions in how page parts and page attachments are used, accomplishing the reorganization was straightforward and easily achieved; it was not the sort of thing that required code tweaks and the like, managed purely through the CMS.  It ended up being quite -- dare I say it? -- an agile solution.  (Agility!  Baked right in!  Because it's opinionated software!  Where's my Mac?  It just works!  [Think Same.](http://www.flickr.com/photos/twylo/173895378/))

For managing small, simple, straightforward sites, Radiant has much to recommend it.  For instance:

- the hierarchical management of content/pages is quite effective and intuitive
- a pretty rich set of extensions (such as page attachments)
- the "filter" option on content is quite handy (switch between straight text, fckeditor, etc.) and helpful
- the Radiant tag set for basic templating/logic is easy to use and understand
- the general resources available for organizing content (pages, layouts, snippets) enables and readily encourages effective reuse of content and/or presentation logic

That said, there are a number of things for which one quickly longs within Radiant:

- In-place editing user interface: an adminstrative mode of viewing the site in which editing tools would show in-place for the different components on a given page.  This is not an uncommon approach to content management.  The fact that you can view the site in one window/tab and the admin in another mitigates the pain of not having this feature to a healthy extent, but the ease of use undoubtedly suffers nevertheless.
- Radiant offers different publishing "states" for any given page ("draft", "published", "hidden", etc.), and only publicly displays pages in the "published" state in production.  This is certainly helpful, but it is ultimately insufficient.  This is no substitute for versioning of resources; there is no way to have a staging version of a given page, in which the staging version is exposed to administrative users only at the same URL as the published version.  To get around this, one needs to make an entirely different page that will replace the published page when you're ready.  While it's possible to work around the problem in this manner, it clutters up the set of resources in the CMS admin UI, and doesn't fit well with the hierarchical nature of the system; the staging version of a page can't have the same children as the published version of the page, so any staging involving more than one level of edits is problematic and awkward.  That leaves quite a lot to be desired: any engineer who has ever done all development on a production site (no development sites) and moved to version-controlled systems knows full well that working purely against a live system is extremely painful.  Content management is no different.
- The page attachments extension, while quite handy in general, has configuration information (such as file size limits and the attachment_fu storage backend to use) hard-coded into its PageAttachment model class definition, rather than abstracting that configuration information into YAML files.  Furthermore, it's all or nothing: you can only use one storage backend, apparently, rather than having the flexibility of choosing different storage backends by the content type of the file attached, or choosing manually when uploading the file, etc.  The result in our case is that all page attachments go to Amazon S3, even though videos were the only thing we really wanted to have in S3 (bandwidth on our server is not a concern for simple images and the like).

The in-place editing UI features could presumably be added to Radiant given a reasonable degree of patience.  The page attachment criticisms also seem achievable.  The versioning, however, is a more fundamental issue.  Many CMSes attempt to solve this problem many different ways, and ultimately things tend to get unpleasant.  I tend to think that CMSes would do well to learn from version control systems like [Git](http://git-scm.com/) in their design; beyond that, **integrate** with Git: dump the content down to some intelligent serialized format and integrate with git branching, checkin, checkout, pushing, etc.   That dandy, glorious future is not easily realized.

To be clear: Radiant is a very useful, effective, straightforward tool; I would be remiss not to emphasize that the things it does well are more important than the areas that need improvement.  As is the case with most software, it could be better.  I'd happily use/recommend it for most content management cases I've encountered.

## Amazon S3

I knew it was only a matter of time before I got to play with Amazon S3.  Having read about it, I felt like I pretty much knew what to expect.  And the expectations were largely correct: it's been mostly reliable, fairly straightforward, and its cost-effectiveness will have to be determined over time.  A few things did take me by surprise, though:

- The documentation on certain aspects, particularly the logging is, fairly uninspiring.  It could be a lot worse.  It could also be a lot better.  Given that people pay for this service, I would expect it to be documented extremely well.  Of course, given the kind of documentation Microsoft routinely spits out, this expectation clearly lacks any grounding in reality.
- Given that the storage must be distributed under the hood, making usage information aggregation somewhat complicated, it's nevertheless disappointing that Amazon doesn't give any interface for capping usage for a given bucket. It's easy to appreciate that Amazon wouldn't want to be on the hook over usage caps when the usage data comes in from multiple geographically-scattered servers, presumably without any guarantee of serialization in time.  Nevertheless, it's a totally lame problem.  I have reason to believe that Amazon plans to address this soon, for which I can only applaud them.

So, yeah, Amazon S3 has worked fine and been fine and generally not offended me overmuch.

## Varnish

The Presidential Youth Debate project had a number of high-profile sponsors potentially capable of generating significant usage spikes.  Given the simplicity of the public-facing portion of the site (read-only content, no forms to submit), scaling out with a caching reverse proxy server was a great option.  Fortunately, [Varnish](http://varnish-cache.org/) makes it pretty easy; basic Varnish configuration is simple, and putting it in place took relatively little time.

Why go with Varnish?  It's designed from the ground up to be fast and scalable (check out the [architecture notes](http://www.varnish-cache.org/trac/wiki/ArchitectNotes) for an interesting technical read).  The time-based caching of resources is a nice approach in this case; we can have the cached representations live for a couple of minutes, which effectively takes the load off of Apache/Rails (we're running Rails with [Phusion Passenger](http://www.modrails.com/)) while refreshing frequently enough for little CMS-driven tweaks to percolate up in a timely fashion.  Furthermore, it's not a custom caching design, instead relying upon the [fundamentals of caching in HTTP itself](http://www.w3.org/Protocols/rfc2616/rfc2616-sec13.html#sec13).  Varnish, with its Varnish Configuration Language ([VCL](http://www.varnish-cache.org/trac/wiki/VCLExamples)), is extremely flexible and configurable, allowing us to easily do things like ignore cookies, normalize domain names (though I ultimately did this in Apache), normalize the annoying Accept-Encoding header values, etc.  Furthermore, if the cache interval is too long for a particular change, Varnish gives you a straightforward, expressive way of [purging cached representations](http://www.varnish-cache.org/trac/wiki/VCLExamplePurging), which came in handy on a number of occasions close to launch time.

A number of us at End Point have been interested in Varnish for some time. We've made some core patches: JT Justman tracked down a caching bug when using [Edge-Side Includes](http://en.wikipedia.org/wiki/Edge_Side_Includes) (ESI), and Charles Curley and JT have done some work to add native gzip/deflate support in Varnish, though that remains to be released upstream. We've also prototyped a system relying on ESI and message-driven cache purging for an up-to-date, high-speed, extremely scalable architecture. (That particular project hasn't gone into production yet due to the degree of effort required to refactor much of the underlying app to fit the design, though it may still come to pass next year -- I hope!)

Getting Varnish to play nice with Radiant was a non-issue, because the relative simplicity of the site feature set and content did not require specialized handling of any particular resource: one cache interval was good for all pages.  Consequently, rather than fretting about having Radiant issue Cache-Control headers on a per-page basis (which may have been fairly unpleasant, though I didn't look into it deeply; eventually I'll need to, though, having gotten modestly hooked on Radiant and less-modestly hooked on Varnish), the setup was refreshingly simple:

- The public site's domain disallows all access to the Radiant admin, meaning it's effectively a read-only site.
- The public domain's Apache container always issues a couple of cache-related headers:
```
Header always set Cache-Control "public; max-age=120"
Header always set Vary "Accept-Encoding"
```

    The Cache-Control header tells clients (Varnish in this case) that it's acceptable to cache representations for 120 seconds, and that all representations are valid for all users ("public").  We can, if we want, use VCL to clean this out of the representation Varnish passes along to clients (i.e. browsers) so that browsers don't cache automatically, instead relying on conditional GET.  The Vary header tells clients that cache (again, primarily concerned with Varnish here) to consider the "Accept-Encoding" header value of a request when keying cached representations.
- An entirely separate domain exists that is not fronted by Varnish and allows access to the Radiant admin.  We could have it fronted by Varnish with caching deactivated, but the configuration we used keeps things clean and simple.

- We use some simple VCL to tell Varnish to ignore cookies (in case of Rails sessions on the public site), to normalize the Accept-Encoding header value to one of "gzip" or "deflate" (or none at all) to avoid caching different versions of the same representation due to inconsistent header values submitted by competing browsers.

Getting all that sorted was, as stated, refreshingly easy.  It was a little less easy, surprisingly, to deal with logging.  The main Varnish daemon (varnishd) logs to a shared memory block.  The logs just sit there (and presumably eventually get overwritten) unless consumed by another process.  A varnishlog utility, which can be run as a one-off or as a daemon, reads in the logs and outputs them in various ways.  Furthermore, a varnishncsa utility outputs logging information in an Apache/NCSA-inspired "combined log" format (though it includes full URLs in the request string rather than just the path portion, presumably due to the possibility of Varnish fronting many different domains).  Neither one of these is particularly complicated, though the varnishlog output is reportedly quite verbose and may need frequent rotation, and when run in daemon mode, both will re-open the log file to which they write upon receiving SIGHUP, meaning they'll play nice with log rotation routines.  I found myself repeatedly wishing, however, that they both interfaced with syslog.

So, I'm very happy with Varnish at this point.  Being a jerk, I must nevertheless publicly pick a few nits:

- Why no syslog support in the logging utilities?  Is there a compelling argument against it (I haven't encountered one, but admittedly I haven't looked very hard), or is it simply a case of not having been handled yet?
- The VCL snippet we used for normalizing the Accept-Encoding header came right off the Varnish FAQ, and seems to be a pretty common case.  I wonder if it would make more sense for this to be part of the default VCL configuration requiring explicit deactivation if not desired.  It's not a big deal either way, but it seems like the vast majority of deployments are likely to use this strategy.

That's all I have to whine about, so either I'm insufficiently observant or the software effectively solves the problem it set out to address.  These options are not mutually exclusive.

I'm definitely looking forward to further work with Varnish.  This project didn't get into ESI support at all, but the native ESI support, combined with the high-performance caching, seems like a real win, potentially allowing for simplification of resource design in the application server, since documents can be constructed by the edge server (Varnish in this case) from multiple components.  That sort of approach to design calls into question many of the standard practices seen in popular (and unpopular) application servers (namely, high-level templating with "pages" fitting into an overall "layout") but could help engineers keep maintain component encapsulation, think through more effectively the URL space, resource privacy and scoping considerations (whether or not a resource varies per user, by context, etc.), etc.  But I digress.  Shocking.
