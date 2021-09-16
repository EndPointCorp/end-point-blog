---
author: Greg Sabino Mullane
title: Broken wikis due to PHP and MediaWiki “namespace” conflicts
github_issue_number: 1178
tags:
- mediawiki
- php
date: 2015-11-09
---

<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2015/11/broken-wikis-due-to-php-and-mediawiki/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/11/broken-wikis-due-to-php-and-mediawiki/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/79LtQP">Photo</a> by <a href="https://www.flickr.com/people/mothernaturephotos/">Elliot Gilfix</a></small></div>

I was recently tasked with resurrecting an ancient wiki. In this case, a wiki last 
updated in 2005, running [MediaWiki](https://mediawiki.org/) version 1.5.2, and that needed to get transformed 
to something more modern (in this case, version 1.25.3). The old settings and extensions were not important, 
but we did want to preserve any content that was made.

The items available to me were a tarball of the mediawiki directory (including the 
LocalSettings.php file), and a MySQL dump of the wiki database. To import the items 
to the new wiki (which already had been created and was gathering content), an 
XML dump needed to be generated. MediaWiki has two simple command-line scripts 
to export and import your wiki, named dumpBackup.php and 
importDump.php. So it 
was simply a matter of getting the wiki up and running enough to run dumpBackup.php.

My first thought was to simply bring the wiki up as it was—​all the files were in 
place, after all, and specifically designed to read the old version of the schema. 
(Because the database scheme changes over time, newer MediaWikis cannot run against 
older database dumps.) So I unpacked the MediaWiki directory, and prepared to 
resurrect the database.

Rather than MySQL, the distro I was using defaulted to using the freer and 
arguably better [MariaDB](https://mariadb.org/), which installed painlessly.

```
## Create a quick dummy database:
$ echo 'create database footest' | sudo mysql

## Install the 1.5.2 MediaWiki database into it:
$ cat mysql-acme-wiki.sql | sudo mysql footest

## Sanity test as the output of the above commands is very minimal:
echo 'select count(*) from revision' | sudo mysql footest
count(*)
727977
```

Success! The MariaDB instance was easily able to parse and load the 
old MySQL file. The next step was to unpack the old 1.5.2 mediawiki directory 
into Apache’s docroot, adjust the LocalSettings.php file to point to the 
newly created database, and try and access the wiki. Once all that was done, however, both the 
browser and the command-line scripts spat out the same error:

```
Parse error: syntax error, unexpected 'Namespace' (T_NAMESPACE), 
  expecting identifier (T_STRING) in 
  /var/www/html/wiki/includes/Namespace.php on line 52
```

What is this about? Turns out that some years ago, someone added a class to 
MediaWiki with the terrible name of “Namespace”. Years later, PHP finally 
caved to user demands and added some non-optimal support for namespaces, which 
means that (surprise), “namespace” is now a reserved word. In short, older 
versions of MediaWiki cannot run with modern (5.3.0 or greater) versions 
of PHP. Amusingly, a web search for this error on DuckDuckGo revealed not 
only many people asking about this error and/or offering solutions, but 
many results were actual wikis that are currently not working! 
Thus, their wiki was working fine one moment, and then PHP was (probably automatically) 
upgraded, and now the wiki is dead. But DuckDuckGo is happy to show you 
the wiki and its now-single page of output, the error above. :)

There are three groups to blame for this sad situation, as well as 
three obvious solutions to the problem. The first group to share the 
blame, and the most culpable, is the MediaWiki developers who chose 
the word “Namespace” as a class name. As PHP has always had very 
non-existent/poor support for packages, namespaces, and scoping, it is 
vital that all your PHP variables, class names, etc. are as unique as possible. 
To that end, the name of the class was changed at some point  
to “MWNamespace”—​but the damage has been done. The second group to share the 
blame is the PHP developers, both for not having namespace support for 
so long, and for making it into a reserved word full knowing that one of 
the poster children for “mature” PHP apps, MediaWiki, was using “namespace”. 
Still, we cannot blame them too much for picking what is a pretty obvious 
word choice. The third group to blame is the owners of all those wikis 
out there that are suffering that syntax error. They ought to be repairing their 
wikis. The fixes are pretty simple, which leads us to the three solutions to the problem.

<div class="separator" style="clear: both; padding: 0em 0em 2em 2em; float:right; text-align: center;"><a href="/blog/2015/11/broken-wikis-due-to-php-and-mediawiki/image-1-big.png" id="gtsm.com/mediawiki_flower.png" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/11/broken-wikis-due-to-php-and-mediawiki/image-1.png"/></a><br/><small>MediaWiki’s cool install image</small></div>

The quickest (and arguably worst) solution is to downgrade PHP to 
something older than 5.3. At that point, the wiki will probably work 
again. Unless it’s a museum (static) wiki, and you do not intend to 
upgrade anything on the server ever again, this solution will not 
work long term. The second solution is to upgrade your MediaWiki! The upgrade process is actually very 
robust and works well even for very old versions of MediaWiki (as 
we shall see below). The third solution is to make some quick edits 
to the code to replace all uses of “Namespace” with “MWNamespace”. 
Not a good solution, but ideal when you just need to get the wiki up 
and running. Thus, it’s the solution I tried for the original problem.

However, once I solved the Namespace problem by renaming to MWNamespace, 
some other problems popped up. I will not run through them here—​although they were 
small and quickly solved, it began to feel like a neverending whack-a-mole 
game, and I decided to cut the Gordian knot with a completely different 
approach.

As mentioned, MediaWiki has an upgrade process, which means that 
you can install the software and it will, in theory, transform your 
database schema and data to the new version. However, version 
1.5 of MediaWiki was released in October 2005, almost exactly 
10 years ago from the current release (1.25.3 as of this writing). 
Ten years is a really, really long time on the Internet. 
Could MediaWiki really convert something that old? (spoilers: yes!). 
Only one way to find out. First, I prepared the old database for the upgrade. 
Note that all of this was done on a private local machine where security was not 
an issue.

```
## As before, install mariadb and import into the 'footest' database
$ echo 'create database footest' | sudo mysql test
$ cat mysql-acme-wiki.sql | sudo mysql footest
$ echo "set password for 'root'@'localhost' = password('foobar')" | sudo mysql test
```

Next, I grabbed the latest version of MediaWiki, verified it, put it in place, and 
started up the webserver:

```
$ wget http://releases.wikimedia.org/mediawiki/1.25/mediawiki-1.25.3.tar.gz
$ wget http://releases.wikimedia.org/mediawiki/1.25/mediawiki-1.25.3.tar.gz.sig

$ gpg --verify mediawiki-1.25.3.tar.gz.sig 
gpg: assuming signed data in `mediawiki-1.25.3.tar.gz'
gpg: Signature made Fri 16 Oct 2015 01:09:35 PM EDT using RSA key ID 23107F8A
gpg: Good signature from "Chad Horohoe <chad@wikimedia.org>"
gpg:                 aka "keybase.io/demon <demon@keybase.io>"
gpg:                 aka "Chad Horohoe (Personal e-mail) <innocentkiller@gmail.com>"
gpg:                 aka "Chad Horohoe (Alias for existing email) <chadh@wikimedia.org>"
## Chad's cool. Ignore the below.
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 41B2 ABE8 17AD D3E5 2BDA  946F 72BC 1C5D 2310 7F8A</chadh@wikimedia.org></innocentkiller@gmail.com></demon@keybase.io></chad@wikimedia.org>

$ tar xvfz mediawiki-1.25.3.tar.gz
$ mv mediawiki-1.25.3 /var/www/html/
$ cd /var/www/html/mediawiki-1.25.3
## Because "composer" is a really terrible idea:
$ git clone https://gerrit.wikimedia.org/r/p/mediawiki/vendor.git 
$ sudo service httpd start
```

Now, we can call up the web page to install MediaWiki.

- Visit http://localhost/mediawiki-1.25.3, see the familiar yellow flower
- Click “set up the wiki”
- Click next until you find “Database name”, and set to “footest”
- Set the “Database password:” to “foobar”
- Aha! Looks what shows up: “Upgrade existing installation” and “There are MediaWiki tables in this database. To upgrade them to MediaWiki 1.25.3, click Continue”

It worked! Next messages are: “Upgrade complete. You can now start using your wiki. If you want to regenerate your LocalSettings.php file, click the button below. This is not recommended unless you are having problems with your wiki.” That message is a little misleading. You almost certainly *do* want to generate a new LocalSettings.php file when doing an upgrade like this. So say yes, leave the database choices as they are, and name your wiki something easily greppable like “ABCD”. Create an admin account, save the generated LocalSettings.php file, and move it to your mediawiki directory.

At this point, we can do what we came here for: generate a XML dump of the wiki content in the database, so we can import it somewhere else. 
We only wanted the actual content, and did not want to worry about the history of the pages, so the command was:

```
$ php maintenance/dumpBackup.php --current > acme.wiki.2005.xml
```

It ran without a hitch. However, close examination showed that it had an amazing amount of unwanted stuff from the 
“MediaWiki:” namespace. While there are probably some clever solutions that could be devised to cut them out of the 
XML file (either on export, import, or in between), sometimes quick beats clever, and I simply opened the file in an 
editor and removed all the “page” sections with a title beginning with “MediaWiki:”. Finally, the file was shipped 
to the production wiki running 1.25.3, and the old content was added in a snap:

```
$ php maintenance/importDump.php acme.wiki.2005.xml
```

The script will recommend rebuilding the “Recent changes” page by running rebuildrecentchanges.php (can we 
get consistentCaps please MW devs?). However, this data is at least 10 years old, and Recent changes only goes back 
90 days by default in version 1.25.3 (and even shorter in previous versions). So, one final step:

```
## 20 years should be sufficient
$ echo '$wgRCMAxAge = 20 * 365 * 24 * 3600;' >> LocalSettings.php
$ php maintenance/rebuildrecentchanges.php
```

Voila! All of the data from this ancient wiki is now in place on a modern wiki!
