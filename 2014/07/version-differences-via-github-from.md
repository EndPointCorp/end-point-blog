---
author: Greg Sabino Mullane
title: Version differences via GitHub from the command line
github_issue_number: 1009
tags:
- git
- mediawiki
- postgres
- shell
date: 2014-07-09
---

<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2014/07/version-differences-via-github-from/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/07/version-differences-via-github-from/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/7pSEW1">Photo</a> by <a href="https://www.flickr.com/photos/bensonkua/">Benson Kua</a></small></div>

I work with a lot of open source projects, and I use the command-line for almost everything. It often happens that I need to examine a file from a project, and thanks to bash, [Github](https://github.com/), and curl, I can do so easily, without even needing to have the repo handy. One of the things I do sometimes is compare a file across versions to see what has changed. For example, I needed to see what changes were made between versions 1.22 and 1.23 to the file includes/UserMailer.php which is part of the [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) project. For this trick to work, the project must be on Github, and must label their versions in a consistent manner, either via git branches or git tags.

MediaWiki exists on Github as [wikimedia/mediawiki-core](https://github.com/wikimedia/mediawiki-core). The MediaWiki project tags all of their releases in the format X.Y.Z, so in this example we can use the git tags **1.22.0** and **1.23.0**. Github is very nice because you can view a specific file at a certain commit (aka a tag), and even grab it over the web as a plain text file. The format is:

```plain
https://raw.githubusercontent.com/PROJECTNAME/BRANCH-OR-TAG/FILE
```

Note that you can use a tag ***OR*** a branch! So to compare these two files, we can use one of these pairs:

```plain
https://raw.githubusercontent.com/wikimedia/mediawiki-core/REL1_21/includes/UserMailer.php
https://raw.githubusercontent.com/wikimedia/mediawiki-core/REL1_22/includes/UserMailer.php

https://raw.githubusercontent.com/wikimedia/mediawiki-core/1.21.0/includes/UserMailer.php
https://raw.githubusercontent.com/wikimedia/mediawiki-core/1.22.0/includes/UserMailer.php
```

All that is left is to treat git as a web service and compare the two files at the command line ourselves. The program **curl** is a great tool for downloading the files, as it dumps to stdout by default. We will add a **-s** flag (for “silent”) to prevent it from showing the progress meter as it usually does. The last bit of the puzzle is to use <(), bash’s process substitution feature, to trick diff into comparing the curl outputs as if they were files. So our final command is:

```plain
diff <(curl -s https://raw.githubusercontent.com/wikimedia/mediawiki-core/1.21.0/includes/UserMailer.php) \
<(curl -s https://raw.githubusercontent.com/wikimedia/mediawiki-core/1.22.0/includes/UserMailer.php) \
| more
```

Voila! A quick and simple glance at what changed between those two tags. This should work for any project on Github. You can also replace the branch or tag with the word “master” to see the current version. For example, the PostgreSQL project lives on github as postgres/postgres. They use the format RELX_Y_Z in their tags. To see what has changed since release 9.3.4 in the psql help file (as a context diff), run:

```sql
diff -c <(curl -s https://raw.githubusercontent.com/postgres/postgres/REL9_3_4/src/bin/psql/help.c) \
<(curl -s https://raw.githubusercontent.com/postgres/postgres/master/src/bin/psql/help.c)
```

You are not limited to diff, of course. For a final example, let’s see how many times Tom Lane is mentioned in the version 9 release notes:

```plain
for i in {0,1,2,3,4}
do grep -Fc 'Tom Lane' \
<(curl -s https://raw.githubusercontent.com/postgres/postgres/master/doc/src/sgml/release-9.$i.sgml)
done
272
206
174
115
16
```

The last number is so low relative to the rest because 9.4 is still under development. Rest assured Tom’s contributions have not slowed down! :) Thanks to Github for providing such a useful service for so many open source projects, and for providing the raw text to allow useful hacks like this.
