---
author: Josh Tolley
title: PostgreSQL 9.0 Admin Cookbook
github_issue_number: 385
tags:
- postgres
date: 2010-11-29
---



I’ve been reading through the recently published book [PostgreSQL 9.0 Admin Cookbook](https://www.packtpub.com/big-data-and-business-intelligence/postgresql-9-administration-cookbook-second-edition) of late, and found that it satisfies an itch for me, at least for now. Every time I get involved in a new project, or work with a new group of people, there’s a period of adjustment where I get introduced to new tools and new procedures. I enjoy seeing new (and not uncommonly, better) ways of doing the things I do regularly. At conferences I’ll often spend time playing “What’s on your desktop” with people I meet, to get an idea of how they do their work, and what methods they use. Questions about various peoples’ favorite window manager, email reader, browser plugin, or IRC client are not uncommon. Sometimes I’m surprised by a utility or a technique I’d never known before, and sometimes it’s nice just to see minor differences in the ways people do things, to expand my toolbox somewhat. This book did that for me.

As the title suggests, authors Simon Riggs and Hannu Krosing have organized their book similarly to a cookbook, made up of simple “recipes” organized in subject groups. Each recipe covers a simple topic, such as “Connecting using SSL”, “Adding/Removing tablespaces”, and “Managing Hot Standby”, with detail sufficient to guide a user from beginning to end. Of course in many of the more complex cases some amount of detail must be skipped, and in general this book probably won’t provide its reader with an in depth education, but it will provide a framework to guide further research into a particular topic. It includes a description of the manuals, and locations of some of the mailing lists to get the researcher started.

I’ve used PostgreSQL for many different projects and been involved in the community for several years, so I didn’t find anything in the book that was completely unfamiliar. But PostgreSQL is an open source project with a large community. There exists a wide array of tools, many of which I’ve never had occasion to use. Reading about some of them, and seeing examples in print, was a pleasant and educational experience. For instance, one recipe describes “Selective replication using [Londiste](https://wiki.postgresql.org/wiki/Skytools#Londiste)”. My tool of choice for such problems is generally [Bucardo](https://bucardo.org), so I’d not been exposed to Londiste’s way of doing things. Nor have I used [pgstatspack](http://pgfoundry.org/projects/pgstatspack/), a project for collecting various statistics and metrics from database views which is discussed under “Collecting regular statistics from pg_stat_* views”.

In short, the book gave me the opportunity to look over the shoulder of experienced PostgreSQL users and administrators to see how they go about doing things, and compare to how I’ve done them. I’m glad to have had the opportunity.


