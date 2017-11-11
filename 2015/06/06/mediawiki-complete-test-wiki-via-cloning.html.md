---
author: Greg Sabino Mullane
gh_issue_number: 1132
tags: mediawiki
title: MediaWiki complete test wiki via cloning
---



<div class="separator" style="clear: both; float:right; padding-left: 2em; padding-bottom: 1em; text-align: center;"><a href="/blog/2015/06/06/mediawiki-complete-test-wiki-via-cloning/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" id="jA0EAgMCshiJ2sWFNg5gyVkDpsZvh+IoZdIClG04/TSA8gqRN8ct" src="/blog/2015/06/06/mediawiki-complete-test-wiki-via-cloning/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/eavCXg">Liska</a> by <a href="https://www.flickr.com/photos/tambako/">Tambako The Jaguar</a></small></div>

Being able to create a quick copy of your [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) site is an important skill that has many benefits. Any time you are testing an upgrade, whether major or [minor](http://blog.endpoint.com/2014/10/mediawiki-minor-upgrade-with-patches.html), it is great to be able to perform the upgrade on a test site first. Tracking down bugs becomes a lot easier when you can add all the debugging statements you need and not worry about affecting any of the users of your wiki. Creating and modifying extensions also goes a lot smoother when you can work with an identical copy of your production wiki. I will outline the steps I use to create such a copy, also known as a "test wiki".

Before creating a copy, there are two things that should be done to an existing MediaWiki installation: [use git](http://sixrevisions.com/resources/git-tutorials-beginners/), and move the **images** directory. By "use git", I mean to put your existing mediawiki directory (e.g. where your LocalSettings.php file lives) into version control. Because the MediaWiki software is not that large, it is simplest to just add nearly everything into git, with the exception of the images and the cache information. Here is a recipe to do just that:

```
$ cd /var/www/mediawiki
$ git init .
<span class-"gsm_o"="">Initialized empty Git repository in /var/www/mediawiki/.git/</span>
$ echo /cache/ &gt;&gt; .gitignore
$ echo /images/ &gt;&gt; .gitignore
$ git add --force .
$ git commit -a -m "Initial MediaWiki commit, version 1.24"
[master (root-commit) bd7db2b] Initial MediaWiki commit, version 1.24
 10024 files changed, 1910576 insertions(+)
 create mode 100644 .gitignore
...
```

Replace that commit message with your specific version, of course, or whatever you like, although I highly recommend your git commits always mention the version on major changes.

The second thing that should be done is to move the images directory and use a symlink to the new location. The "images" directory in MediaWiki is special in many ways. It is the only directory (except 'cache') directly written by MediaWiki (all other changes are stored in the database, not on disk). It is the only directory that comes pre-populated in the MediaWiki tarballs and is always a pain to upgrade. Finally, it invariably contains a large collection of static files that are not well suited for version control, and are usually better backed up and stored  in ways different than the rest of MediaWiki. For all these reasons, I recommend making images into a symlink. The simplest recipe is to just move the images directory "up a level". This will also help us below when cloning the wiki.

```
$ cd /var/www/mediawiki
$ mv images ..
$ ln -s ../images .
```

Now that those two important prerequisites are out of the way, let's get a quick overview of the steps to create a clone of your wiki:

- Make a backup of your existing wiki (files and database)
- Make a copy of your database
- Create a new directory, and copy the mediawiki files into it
- Create a new git branch
- Adjust the LocalSettings.php file
- Mark it clearly as a test wiki
- Do a git commit
- Adjust your web server

The first step is to make a backup of your existing wiki. You can never have too many backups, and right before you go copying a lot of files is a great time to create one. 
Before backing up, make sure everything is up to date in git with "git status". Make a backup of the mediawiki directory, for example with tar, making sure the resulting backup file is well labeled:

```
$ tar cfz /backups/mediawiki.backup.20150601.tar.gz --exclude=mediawiki/cache --anchored mediawiki/
```

If your images directory is somewhere else, make sure you back that up as well. 
Backing up your database is dead simple if you are using Postgres:

```
$ pg_dump wikidb | gzip --fast &gt; /backups/mediawiki.database.backup.wikidb.20150601.pg.gz
```

The next step is to create a new copy of the database for your cloned wiki to access:

```
$ dropdb test_wikidb
$ createdb -T wikidb test_wikidb
$ psql test_wikidb -c 'alter database test_wikidb owner to wikiuser'
```

Now we want to create a new directory for the cloned wiki, and populate it with files from the production wiki. For this example, the existing production wiki lives in /var/www/mediawiki, and the new cloned test wiki will live in /var/www/test_mediawiki.

```
$ cd /var/www
$ mkdir test_mediawiki
$ rsync -a -W --exclude=/images/ mediawiki/ test_mediawiki/
## rsync will copy symlinks as well - such as the images directory!
```

I like to create a new git branch right away, to avoid any confusion with the "actual" git 
repository in the production mediawiki directory. If you do end up making any changes in the test directory, it's easy enough to roll them into the other git repo. 
Branch names should be short and clearly indicate why you have created this copy of the wiki. Doing this means the name shows up as the first line whenever you do a "git status", which is nice.

```
$ cd /var/www/test_mediawiki
$ git checkout -b testing_version_1.25.2
Switched to a new branch 'testing_version_1.25.2'
```

The next step is critical: editing the LocalSettings.php file! 
As this was copied from the production wiki, we need to make sure it points back to itself via paths, and that it connects to our newly created database. Add all these to the bottom of your test_mediawiki/LocalSettings.php file:

```
## Change important paths:
$wgArticlePath          = '/testwiki/$1';
$wgScriptPath           = '/test_mediawiki';
## Point to the correct database:
$wgDBname               = 'test_wikidb';
## The logo may be hardcoded, so:
$wgLogo                 = '/test_mediawiki/End_Point_logo.png';
## Disable all email notifications:
$wgUsersNotifiedOnAllChanges = array();
```

It's also a good idea to make this wiki read-only until needed. Also important if you symlinked the images directory is to disallow any uploads. If you need to enable uploads, and thus writes to the images directory, make sure you remove the symlink and create a new images directory! You can either copy all the files from the production wiki, or simply leave it empty and expect to see a lot of "missing file" errors, which can safely be ignored.

```
$wgReadOnly       = 'Test wiki: upgrading to MediaWiki 1.25.2';
$wgEnableUploads  = false;
```

The $wgReadOnly message will appear when people try to edit a page, but we want to make it very visible to all users so as soon as they see the wiki that "here be Danger" (and edits will be lost). To that end, there are four additional steps you can take. First, you can set a sitewide message. This will appear near the top of every page. You can add HTML to this, and it is set in your LocalSettings.php file as $wgSiteNotice. You can also change the $wgSiteName parameter, which will appear in the title of every page.

```
$wgSiteNotice  = '&lt;strong&gt;TEST WIKI ONLY!&lt;/strong&gt;';
$wgSitename    = 'TEST WIKI';
```

The third additional step is to change the CSS of every page. I use this to slightly change the background color of every page. This requires that the $wgUseSiteCss setting is enabled. It is on by default, but there is no harm setting it to true explicitly. 
Getting it to work on all pages, including the login page, requires enabling $wgAllowSiteCSSOnRestrictedPages as well.

```
$wgUseSiteCss                     = true;
$wgAllowSiteCSSOnRestrictedPages  = true;
```

Once the above is done, navigate to MediaWiki:Common.css and add the text below. Note that you may need to wait until "making the wiki active" step below - and comment out the $wgReadOnly variable.

```
* { background-color: #ddeeff !important }
```

The last method to mark the wiki as test only is to change the wiki logo. You can replace it with a custom image, or you can modify the existing logo. I like the latter approach. 
Annotating text is easy from the command line by using ImageMagick. Use the "polaroid" feature to give it a nice effect (use "-polaroid 0" to avoid the neat little rotation). The command and the 
result:

```
$ convert End_Point.logo.png -caption "TEST WIKI ONLY\!" -gravity center -polaroid 20 End_Point.tilted.testonly.png
```

<table border="1" class="gsm">
<tbody><tr><td><a href="/blog/2015/06/06/mediawiki-complete-test-wiki-via-cloning/image-1.png" imageanchor="1"><img border="0" id="DpGxzTyk3O8za1Aig6jaLjob/evsLLg9TQpoLlnHUm2xImQk" src="/blog/2015/06/06/mediawiki-complete-test-wiki-via-cloning/image-1.png"/></a></td>
<td><a href="/blog/2015/06/06/mediawiki-complete-test-wiki-via-cloning/image-2.png" imageanchor="1"><img border="0" id="v/+S6fL1Nz6M3/jqUNUM8l4Pub/Ewg44E61hvYvcxQ===D/fO" src="/blog/2015/06/06/mediawiki-complete-test-wiki-via-cloning/image-2.png"/></a></td></tr>
<tr><th>Original</th><th>Captioned</th></tr>
</tbody></table>

At this point, all of the changes to the test wiki are complete, so we/you should commit all your changes:

```
$ git commit -a -m "Changes for the test wiki"
```

The final step is to make your test wiki active by adjusting your web server. 
Generally this is easy and basically means copying the existing wiki parameters. For Apache, it can be as simple as adding a new Alias directive to your http.conf file:

```
Alias /testwiki /var/www/test_mediawiki/index.php
```

Reload the web server, and Bob's your uncle. You now have a fully functional, safely sandboxed, magnificently marked-up 
copy of your production wiki. The above may seem like a lot of work, but this was an overly-detailed post - the actual work only takes around 10 minutes (or much less if you script it!)


