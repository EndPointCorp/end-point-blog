---
author: Greg Sabino Mullane
gh_issue_number: 1192
tags: mediawiki
title: MediaWiki major upgrade process
---



<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2016/01/13/mediawiki-major-upgrade-process/image-0-big.jpeg" id="jA0ECgMCAgq+j/dF5fVg0p8B+8AMgSoFokDOSe5KCFaxWZJhpt3VCeVufE4QxYsVo4JdJsN/neWFX+7wvaOGwJ4PWGvCJkIhTWbhp40tAbTL4uxmK3Qn7vru5vFtQvwJab4uSmKNp+lG4rTqWrHU2gi0wLlpFCKQ7WabVQ5cAdwwUInGP/13zrBj9J0Cg9FAZVjb5M9qFDNl6kip6Gg8dl5IXp+PKyhRd09Nng4yBKM==zRAb" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/01/13/mediawiki-major-upgrade-process/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/26krAr">Flower photo</a> by <a href="https://www.flickr.com/photos/mayrace/">May Race</a></small></div>

Keeping your MediaWiki site up to date with the latest version is, like many sysadmin tasks, 
a never-ending chore. In a previous article I covered how to [
upgrade minor revisions of MediaWiki with patches.](/blog/2014/10/02/mediawiki-minor-upgrade-with-patches) In this one, I'll cover 
my solution to doing a "major" upgrade to MediaWiki. While the [official upgrade instructions](https://www.mediawiki.org/wiki/Manual:Upgrading) are good, they don't cover everything.

MediaWiki, like Postgres, uses a three-section version number in which the first two 
numbers combined give the major version, and the number on the end the revision of 
that branch. Thus, version 1.26.2 is the third revision (0, then 1, then 2) of the 
1.26 version of MediaWiki. Moving from one major version to another (for example 1.25 
to 1.26) is a larger undertaking than updating the revision, as it involves significant 
software changes, whereas a minor update (in which only the revision changes) simply 
provides bug fixes.

The first step to a major MediaWiki upgrade is to try it on a cloned, test version of your wiki.
See [this article](/blog/2015/06/06/mediawiki-complete-test-wiki-via-cloning) on how to make such a clone. Then run through the steps below to find any problems 
that may crop up. When done, run through again, but this time on the actual live site.
For this article, we will use MediaWiki installed in **~intranet/htdocs/mediawiki**, and 
going from version 1.25.3 to 1.26.2

### Preparation

Before making any changes, make sure everything is up to date in 
[git](https://rogerdudler.github.io/git-guide/). You do have your MediaWiki 
site controlled by git, right? If not, go do so right now. Then check you are on the main branch 
and have no outstanding changes. It should look like this:

```
<span class="gsm">$ cd ~/htdocs/mediawiki
$ git status
# On branch master
nothing to commit, working directory clean
</span>
```

### Download

Time to grab the new major version. Always get the latest revision in the current 
branch. For this example, we want the highest in the 1.26 branch, which as of this 
writing is 1.26.2. You can always find a prominent link on [mediawiki.org](https://mediawiki.org/). Make sure you 
grab both the tarball (tar.gz) and the signature (.tar.gz.sig) file, then use gnupg to verify it:

```
<span class="gsm">$ wget https://releases.wikimedia.org/mediawiki/1.26/mediawiki-1.26.2.tar.gz
$ wget https://releases.wikimedia.org/mediawiki/1.26/mediawiki-1.26.2.tar.gz.sig
$ gpg mediawiki-1.26.2.tar.gz.sig 
gpg: assuming signed data in `mediawiki-1.26.2.tar.gz'
gpg: Signature made Sun 20 Dec 2015 08:13:14 PM EST using RSA key ID 23107F8A
gpg: please do a --check-trustdb
gpg: Good signature from "Chad Horohoe <chad@wikimedia.org>"
gpg:                 aka "keybase.io/demon <demon@keybase.io>"
gpg:                 aka "Chad Horohoe (Personal e-mail) <innocentkiller@gmail.com>"
gpg:                 aka "Chad Horohoe (Alias for existing email) <chadh@wikimedia.org>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 41B2 ABE8 17AD D3E5 2BDA  946F 72BC 1C5D 2310 7F8A
</span>
```

Copy the tarball to your server, and untar it in the same base directory as your 
mediawiki installation:

```
<span class="gsm">$ cd ~/htdocs
$ tar xvfz ~/mediawiki-1.26.2.tar.gz
</span>
```

### Copy files

Copy the LocalSettings.php file over, as well as any custom images (e.g. the logo, which I like 
to keep nice and visible at the top level):

```
<span class="gsm">$ cp mediawiki/LocalSettings.php mediawiki-1.26.2/
$ cp mediawiki/Wiki_logo.png mediawiki-1.26.2/
</span>
```

Setup the images directory. The tarball comes with a dummy directory containing a few unimportant files. We want to replace 
that with our existing one. I keep the images directory a level up from the actual mediawiki 
directory, and symlink it in. This allows for easy testing and upgrades:

```
<span class="gsm">$ cd ~/htdocs/mediawiki-1.26.2
$ rm -fr images/ ## Careful, make sure you are in the right directory! :)
$ ln -s ../images/ .
</span>
```

### Copy extensions

Now it is time to copy over the extensions. MediaWiki bundles a number of extensions in 
the tarball, as they are considered "core" extensions. We do not want to overwrite these 
with our old versions. We do want to copy any extensions that exist in our old 
mediawiki directory, yet not in our newly created one. To help keep things straight and 
reduce typing, let's make some symlinks for the existing (old) MediaWiki and for the 
current (new) MediaWiki, naming them "aa" and "bb" respectively. Then we use "diff" to help 
us copy the right extensions over:

```
<span class="gsm">$ cd ~/htdocs
$ ln -s mediawiki aa
$ ln -s mediawiki-1.26.2 bb
## Visually check things over with:
$ diff aa/extensions bb/extensions | grep 'Only in aa' | awk '{print $4}' | more
## Do the copying:
$ diff aa/extensions bb/extensions | grep 'Only in aa' | awk '{print $4}' | xargs -iZ cp -r aa/extensions/Z bb/extensions/Z
</span>
```

Extensions may not be the only way you have modified your installation. There could 
be skins, custom scripts, etc. Copy these over now, being sure to only copy what is 
truly still needed. Here's one way to check on the differences:

```
<span class="gsm">$ cd ~/htdocs
$ diff -r aa bb | grep 'Only in aa' | more
</span>
```

### Check into git

Now that everything is copied over, we can check the 1.26.2 changes into git. To do 
so, we will move the git directory from the old directory to the new one. Remember to let anyone who might 
be developing in that directory know what you are doing first!

```
<span class="gsm">$ mv aa/.git bb/
## Don't forget this important file:
$ mv aa/.gitignore bb/
$ cd mediawiki-1.26.2
$ git add .
$ git commit -a -m "Upgrade to version 1.26.2"
$ git status
# On branch master
nothing to commit, working directory clean
</span>
```

### Extension modifications

This is a good time to make any extension changes that are needed for the new version. 
These should have been revealed in the first round, using the cloned test wiki. In our case, 
we needed an updated and locally hacked version of the [Auth_remoteuser extension](https://www.mediawiki.org/wiki/Extension:Auth_remoteuser):

```
<span class="gsm">$ cd ~/htdocs/mediawiki-1.26.2/extensions
$ rm -fr Auth_remoteuser/
$ tar xvfz ~/Auth_remoteuser.tgz
$ git add Auth_remoteuser
$ git commit -a -m "New version of Auth_remoteuser extension, with custom fix for wpPassword problem"
</span>
```

### Core modifications

One of the trickiest part of major upgrades is the fact that all the files are simply replaced. 
Normally not a problem, but what if you are in the habit of modifying the core files because sometimes 
extensions cannot do what you want? My solution is to tag the changes prominently - using a PHP comment 
that contains the string "END POINT". This makes it easy to generate a list of files that may 
need the local changes applied again. After using "git log" to find the commit ID of the 1.26.2 
changes (message was "Upgrade to version 1.26.2"), we can grep for the unique string and 
figure out which files to examine:

```
<span class="gsm">$ git log 1a83a996b9d00444302683fb6de6e86c4f4006e7 -1 -p | grep -E 'diff|END POINT' | grep -B1 END
diff --git a/includes/mail/EmailNotification.php b/includes/mail/EmailNotification.php
-        // END POINT CHANGE: ignore the watchlist timestamp when sending notifications
-        // END POINT CHANGE: send diffs in the emails
diff --git a/includes/search/SearchEngine.php b/includes/search/SearchEngine.php
-       // END POINT CHANGE: Remove common domain suffixes
</span>
```

At that point, manually edit both the new and old version of the files and make the 
needed changes. After that, remember to commit all your changes into git.

### Final changes

Time to make the final change, and move the live site over. The goal is to minimize the downtime, 
so we will move the directories around and run the update.php script on one line. This is an excellent 
time to notify anyone who may be using the wiki that there may be a few bumps.

```
<span class="gsm">## Inform people the upgrade is coming, then:
$ mv mediawiki old_mediawiki; mv mediawiki-1.26.2 mediawiki; cd mediawiki; php maintenance/update.php --quick
$ rm ~/htdocs/aa ~/htdocs/bb
</span>
```

### Testing

Hopefully everything works! Time to do some testing. First, visit your wiki's Special:Version page and 
make sure it says 1.26.2 (or whatever version you just installed). Next, test that most things are still 
working by:

- Logging in, and...
 - Editing a page, then...
 - Upload an image, plus...
 - Test all your extensions.

For that last bullet, having an extension testing page is very handy. This is simply an unused page on the 
wiki that tries to utilize as many active extensions as possible, so that reloading the page should quickly 
allow a tally of working and non-working extensions. I like to give each extension a header with its name, 
a text description of what should be seen, and then the actual extension in action.

That's the end of the major upgrade for MediaWiki! Hopefully in the future the upgrade process will 
be better designed (I have ideas on that - but that's the topic of another article). One final check you can do is to 
open a screen and tail -f the httpd error log for your site. After the upgrade, this is a helpful 
way to spot any issues as they come up.


