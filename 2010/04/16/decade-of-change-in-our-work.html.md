---
author: Jon Jensen
gh_issue_number: 288
tags: community, ecommerce
title: A decade of change in our work
---



Lately I’ve been looking back a bit at how things have changed in our work during the past decade. Maybe I’m a little behind the times since this is a little like a new year’s reflection.

Since 2000, in our world of open source/free software ecommerce and other Internet application development, many things have stayed the same or become more standard.

The Internet is a completely normal part of people’s lives now, in the way TV and phones long have been.

Open source and free software is a widely-used and accepted part of the software ecosystem, used on both servers and desktops, at home and in companies of all sizes. Software licensing differences are still somewhat arcane, but the more popular options are now fairly widely-known.

Many of today’s major open source software systems key to Internet infrastructure and application development were already familiar in 2000:

- the GNU toolset, Linux (including Red Hat and Debian), FreeBSD, OpenBSD

- Apache, mod_ssl (the RSA patent expired in September 2000, making it freely usable)

- PostgreSQL, MySQL, *DBM

- Perl and CPAN, Python, PHP, Ruby (though little known then)

- Interchange (just changed from MiniVend)

- JavaScript

- Sendmail, Postfix

- OpenSSH (brand new!), GnuPG, Nmap, Nagios (originally NetSaint), BIND, rsync

- zip, gzip, bzip2

- screen, Vim, Emacs, IRC, Pine (and now Alpine), mutt

- X.org (from XFree86), KDE, GNOME

- proprietary Netscape became open-source Mozilla became very popular Firefox

- OpenOffice.org, the GIMP, Ghostscript, etc.

- and many others

Also worth mentioning: Java was (eventually) released as open source.

All of these projects have improved dramatically over the past decade and they’ve become a core part of many people’s lives, even though invisibly in many cases. Time invested in learning, developing software based on, and contributing to these projects has been well-rewarded.

However, my hand-picked list of open source “survivor” projects reveals just as much by what’s not listed there.

Take version control systems: A decade ago, Subversion was in its infancy, its developers aiming to improve on the de facto standard CVS. Now Subversion is a legacy system, still used but overshadowed by a new generation of version control systems that have distributed functionality at their core. Git, Mercurial, and Bazaar are the norm in free software and much business development now.

And countless smaller open source libraries, frameworks, and applications have come and gone.

Now, in contrast to the things that have stayed much the same, consider some of the upheavals that we’ve adapted to, or are still adapting to:

- migration from 32-bit to 64-bit: hardware, operating systems, libraries, applications, and binary data formats

- from a huge number of character sets to Unicode

- and from a variety of mostly fixed 8- and 16-bit character set encodings to Internet standard variable-length UTF-8

- reignited browser competition and finally somewhat standard and usable CSS and JavaScript

- a proliferation of new frameworks in every language, including JavaScript’s Prototype.js, script.aculo.us, MooTools, Rico, Dojo, YUI, Ext JS, Google Web Toolkit, jQuery

- widespread adoption object/relational mappers to interact with databases instead of hand-written SQL queries

- necessity of email spam filtering for survival, and coping with spam blacklists interfering with legitimate business

- search engine optimization (SEO) and adapting to Google’s search dominance

- leased dedicated server hosting price wars: where all servers once cost at least $500/month, price competition brought us < $100/month options

- server virtualization and cloud computing

- configuration management: from obscure cfengine to widely-used Puppet and Chef

- Microsoft’s introduction of XmlHttpRequest and the transformation of dynamic HTML into Ajax

- multi-core CPUs and languages to take advantage (Erlang, Scala, etc.)

- and so on.

The first of these changes, moving to 64-bit platforms and UTF-8 encoding, were mostly quiet behind-the-scenes migration work on the server. I think they’re two of the more important changes, though of course the transition still is underway.

Thanks to UTF-8, new projects typically give little thought to character set encoding concerns, which once were a major problem as soon as any non-ASCII or non-Latin-1 text came into play. Just mixing, say, Japanese, Chinese, and Hungarian in a single data set was a real challenge. But anyone asked to display all three in a single browser screen knows how valuable UTF-8 is as a standard.

Moving to 64-bit architecture removed the ~3 GB memory barrier from applications and operating systems. It gave us lots of room to grow, and take advantage of cheaper memory, with the next limit not really in sight.

Other changes in the larger Internet ecosystem are more visible and have been more widely discussed, but still bear mentioning:

- online advertising as a major industry

- affiliate marketing

- social networks

- wikis as a standard fixture in society, from the overwhelmingly popular Wikipedia, to private wikis used in business and community projects

- prepackaged free software-style licenses have spread to other areas, for example via the Creative Commons

- free-of-charge email and other services

- mobile computing, from laptops to netbooks to phones

- rebirth of the Walkman as a little computer, and MP3 and other digital audio purchases now eclipse CDs

- DVRs, Hulu, HD TV

- wifi Internet widely available

- broadband Internet access in many homes

I don’t mean to say that the preceding decades were any less noteworthy. Those working with the Internet should expect a lot of change, as it’s still a young industry.

It’s interesting to look back and consider the journey, and a little daunting to realize how much work has gone into adapting to each wave of change, and how much work remains to upgrade, migrate, and adapt the large amount of legacy code and infrastructure we’ve created. That, in addition to working on the next improvements we see a need for. Lots to learn, and lots to do!


