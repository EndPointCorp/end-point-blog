---
author: Greg Sabino Mullane
title: Gathering server information with boxinfo
github_issue_number: 254
tags:
- database
- mysql
- open-source
- perl
- postgres
date: 2010-01-15
---

I’ve just publicly released another Postgres-related script, this one called “boxinfo”. Basically, it gathers information about a box (server), hence the catchy and original name. It outputs the information it finds into an HTML page, or into a MediaWiki formatted page.

The goal of boxinfo is to have a simple, single script that quickly gathers important information about a server into a web page, so that you can get a quick overview of what is installed on the server and how things are configured. It’s also useful as a reference page when you are trying to remember which server was it that had Bucardo version 4.5.0 installed and was running pgbouncer.

As we use MediaWiki internally here at End Point (running with a Postgres backend, naturally), the original (and default) format is HTML with some MediaWiki specific items inside of it.

Because it is meant to run on a wide a range of boxes as possible, it’s written in Perl. While we’ve run into a few boxes over the years that did not have Perl installed, the number that had any other language you choose (except perhaps sh) is much greater. It requires no other Perl modules, and simply makes a lot of system calls.

Various information about the box is gathered. System wide things such as mount points, disk space, schedulers, packaging systems are gathered first, along with versions of many common Unix utilities. We also gather information on some programs where more than just the version number is important, such as puppet, heartbeat, and lifekeeper. Of course, we also go into a great amount of detail about all the installed Postgres clusters on the box as well.

The program tries its best to locate every active Postgres cluster on the box, and then gathers information about it, such as where pg_xlog is linked to, any contrib modules installed, any interesting configuration variables from postgresql.conf, the size of each database, and lots of detailed information about any Slony or Bucardo configurations it finds.

The main page for it is on the Bucardo wiki at [https://bucardo.org/wiki/Boxinfo](https://bucardo.org/wiki/Boxinfo). That page details the various command line options and should be considered the canonical documentation for the script. The latest version of boxinfo can be downloaded from that page as well. For any enhancement requests or problems to report, please submit an issue at [https://github.com/bucardo/bucardo/issues](https://github.com/bucardo/bucardo/issues).

What exactly does the output look like? We’ve got an example on the wiki showing the sample output from a run against my laptop. Some of the items were removed, but it should give you an idea of what the script can do, particularly with regards to the Postgres information: [https://bucardo.org/Boxinfo/Example/](https://bucardo.org/Boxinfo/Example/)

The script is still a little rough, so we welcome any patches, bug reports, requests, or comments. The development version can be obtained by running: **git clone git://bucardo.org/boxinfo.git**
