---
author: "Jon Jensen"
title: "Git PostgreSQL mirror"
tags: git, postgres, development
gh_issue_number: 1672
---

I’ve been using the excellent <a href="https://git-scm.com/">Git</a> version control system for a while now, and while it’s been great for my personal and work projects (not to forget <a href="https://bucardo.org/Bucardo/">Bucardo</a>!), I’m finding it even nicer for working with the PostgreSQL source code, thanks to the <a href="https://git.postgresql.org/gitweb/?p=postgresql.git">PostgreSQL Git repository</a> (which started as a mirror but eventually became the canonical source).</p>

From time to time I run `git pull` to update my local mirror, and without any further network access I’m able to find when a section of code changed, browse recent changes in general or to a particular section, grab the code from any particular release via the tags, etc. All with much less fuss and time than CVS.

I realize those are all basic operations and taken for granted in the distributed version control world, and I’m used to them now, but I guess I appreciate it all the more when dealing with a large and long-running codebase like PostgreSQL.

For anyone who hasn’t tried Git before, I think playing with the PostgreSQL mirror may actually be an easier place to start than with your own code.

(My co-worker Greg goes into this a bit more <a href="https://web.archive.org/web/20071128024559/http://people.planetpostgresql.org/greg/index.php?/archives/115-Postgres-cvs,-subversion,-and-git.html">in his blog entry</a>.)</p>

<!-- original version is at https://web.archive.org/web/20071104013932/http://people.planetpostgresql.org/jjensen/index.php?/archives/2-Git-PostgreSQL-mirror.html -->
