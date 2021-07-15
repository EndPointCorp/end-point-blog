---
author: Greg Sabino Mullane
title: Postgres searchable release notes—​one page with all versions
github_issue_number: 1098
tags:
- database
- postgres
date: 2015-03-11
---

The inability to easily search the Postgres release notes has been a long-standing annoyance of mine, and a recent thread on the pgsql-general mailing list showed that others share the same frustration. One common example when a  new client comes to End Point with a mysterious Postgres problem. Since it is rare that a client is running the latest Postgres revision (sad but true), the first order of business is to walk through all the revisions to see if [a simple Postgres update](https://www.postgresql.org/docs/current/static/upgrading.html) will cure the problem. Currently, the release notes are arranged on the postgresql.org web site as a [
series of individual HTML pages](https://www.postgresql.org/docs/current/static/release.html), one per version. Reading through them can be very painful—​especially if you are trying to search for a specific item. I whipped up a Perl script to gather all of the information, reformat it, clean it up, and summarize everything on one giant HTML page. This is the result: [https://bucardo.org/postgres_all_versions.html](https://bucardo.org/postgres_all_versions.html)

Please feel free to use this page however you like. It will be updated as new versions are released. You may notice there are some differences from the original separate pages:

- All 270 versions are now on a single page. Create a local greppable version with: 
`links -dump https://bucardo.org/postgres_all_versions.html > postgres_all_versions.txt`
- All version numbers are written clearly. The confusing “E.x.y” notation was stripped out
- A table of contents at the top allows for jumping to each version (which has the release date next to it).
- Every bulleted feature has the version number written right before it, so you never have to scroll up or down to see what version you are currently reading.
- If a feature was applied to more than one version, all the versions are listed (the current version always appears first).
- All CVE references are hyperlinks now.
- All “mailtos” were removed, and other minor cleanups.
- Replaced single-word names with the full names (e.g. “Massimo Dal Zotto” instead of “Massimo”) (see below)

Here’s a screenshot showing the bottom of the table of contents, and some of the items for Postgres 9.4:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/03/postgres-searchable-release-notes-one/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/03/postgres-searchable-release-notes-one/image-0.png"/></a></div>

The name replacements took the most time, as some required a good bit of detective work. Most were unambiguous: “Tom” became “Tom Lane”, “Bruce” became “Bruce Momjian”, and so on. For the final document, 3781 name replacements were performed! Some of the trickier ones were “Greg”—​both myself (“Greg Sabino Mullane”) and “Greg Stark” had single-name entries. Similar problems popped up with “Ryan”, and with “Peter” *not* being the familiar Peter Eisentraut (but Peter T. Mount) threw me off for a second. The only one I was never able to figure out was “Clark”, who is attributed (via Bruce) with “Fix tutorial code” in version 6.5. Pointers or corrections welcome.

Hopefully this page will be of use to others. It’s a very large page, but not remarkably wasteful of space,  like many HTML pages these days. Perhaps some of the changes will make their way to the official docs over time.
