---
author: Brian J. Miller
gh_issue_number: 119
tags: tips
title: Ack, grep for Developers
---

A relatively new tool in my kit that I’ve come to use very frequently over the last 6 months or so is [Ack](https://beyondgrep.com/). Notwithstanding that it is written in my preferred development language, and is maintained by a developer active in the Perl community working on some important projects, like TAP, it really does just save typing while producing Real Purdy output. I won’t go so far as to say it completely replaces grep, at least not without a learning curve and especially for people doing more “adminesque” tasks, but as a plain old developer I find its default set of configuration and output settings incredibly efficient for my common tasks. I’d go into the benefits myself, but I think the “Top 10 reasons to use ack instead of grep.” from the ack site pretty much covers it. To highlight a couple here,

1. It’s **blazingly fast** because it only searches the stuff you want searched.

1. Searches recursively through directories by default, while ignoring .svn, CVS and other VCS directories. Which would you rather type?
     

    <ul>
      <li><code>$ grep pattern $(find . -type f | grep -v '\.svn')</code></li>
      <li><code>$ ack pattern</code></li>
    </ul>

1. ack ignores most of the crap you don’t want to search
             

    <ul>
      <li>VCS directories</li>
      <li>*blib*, the Perl build directory</li>
      <li>backup files like *foo~* and *#foo#*</li>
      <li>binary files, core dumps, etc</li>
    </ul>

1. Ignoring .svn directories means that **ack is faster than grep** for searching through trees.

1. Lets you specify file types to search, as in --perl or --nohtml. Which would you rather type? (Note that ack’s --perl also checks the shebang lines of files without suffixes, which the find command will not.)

    <ul>
      <li><code>$ grep pattern $(find . -name '*.pl' -or -name '*.pm' -or -name '*.pod' | grep -v .svn)</code></li>
      <li><code>$ ack --perl pattern</code></li>
    </ul>

1. File-filtering capabilities usable without searching with ack -f. This lets you create lists of files of a given type.

1. Color highlighting of search results.

Note that there are actually 13 on their list, but I eliminated the one about that that one OS, the last is basically just for humor, and a couple are mainly relevant only to Perl users/developers.

The next time you need to search a development tree for a particular subroutine, library name, etc. give [Ack](https://beyondgrep.com/) a try.
