---
author: Greg Sabino Mullane
title: MediaWiki minor upgrade with patches
github_issue_number: 1039
tags:
- mediawiki
date: 2014-10-02
---



<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2014/10/mediawiki-minor-upgrade-with-patches/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/10/mediawiki-minor-upgrade-with-patches/image-0.jpeg"/></a><br/>
<small><a href="https://flic.kr/p/bTzeNx">Photo</a> by <a href="https://www.flickr.com/photos/31246066@N04/">Ian Sane</a></small></div>

One of the more mundane (but important!) tasks for those running [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) is keeping it updated with the latest version of the software. This is usually a fairly easy process. While the [offical upgrade instructions](http://www.mediawiki.org/wiki/Manual:Upgrading) for MediaWiki are good, they are missing some important items. I will lay out in detail what we do to upgrade MediaWiki installations.

Note that this is for "minor" upgrades to MediaWiki, where minor is defined as not moving more than a couple of actual versions, and not requiring anything other than patching some files. I will cover major upgrades in a future post. For this article, I assume you have full shell access, and not simply FTP, to the server that MediaWiki is running on.

The first step in upgrading is knowing when to upgrade - in other words, making sure you know about new releases. The best way to do this is to subscribe to the low-volume [mediawiki-announce mailing list](https://lists.wikimedia.org/mailman/listinfo/mediawiki-announce). The MediaWiki maintainers have a wonderful new policy of sending out "pre-announcement" emails stating the exact time that the new version will be released. Once we see that announcement, or when the version is actually released, we open a support ticket, which serves the dual purpose of making sure the upgrade does not get forgotten about, and of keeping an official record of the upgrade.

The official announcement should mention the location of a patch tarball, for example 
**http://releases.wikimedia.org/mediawiki/1.23/mediawiki-1.23.5.patch.gz**. If not, you can find the patches in the directory at **http://releases.wikimedia.org/mediawiki/**: look for your version, and the relevant patch. Download the patch, and grab the signature file as well, which will be the same file with "dot sig" appended to it. In the example above, the sig file would be **http://releases.wikimedia.org/mediawiki/1.23/mediawiki-1.23.5.patch.gz.sig**.

It is important to know that these patch files *only* cover patching from the previous version. If you are running version 1.23.2, for example, you would need to download and apply the patches for versions 1.23.3 and 1.23.4, before tackling version 1.23.5. You can also create your own patch file by checking out the MediaWiki git repository and using the version tags. In the previous example, you could run "git diff 1.23.2 1.23.5".

Once the patch is downloaded, I like to give it three sanity checks before installing it. First, is the [PGP](http://en.wikipedia.org/wiki/Pretty_Good_Privacy) signature valid? Second, does this patch look sane? Third, does the patch match what is in the official git repository for MediaWiki?

To check the PGP signature, you use the sig file, which is a small external signature that one of the MediaWiki maintainers has generated for the patch itself. Since you may not have the public PGP key already, you should both verify the file and ask [gpg](http://en.wikipedia.org/wiki/GNU_Privacy_Guard) to download the needed public key in one step. Here's what it looks like when you do:

```
$ gpg --keyserver pgp.mit.edu --keyserver-options auto-key-retrieve --verify mediawiki‑1.23.5.patch.gz.sig 
gpg: Signature made Wed 01 Oct 2014 06:21:47 PM EDT using RSA key ID 5DC00AA7
gpg: requesting key 5DC00AA7 from hkp server pgp.mit.edu
gpg: key 5DC00AA7: public key "Markus Glaser <glaser@hallowelt.biz>" imported
gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model
gpg: depth: 0  valid:   5  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 5u
gpg: Total number processed: 1
gpg:               imported: 1  (RSA: 1)
gpg: Good signature from "Markus Glaser <glaser@hallowelt.biz>"
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 280D B784 5A1D CAC9 2BB5  A00A 946B 0256 5DC0 0AA7
</glaser@hallowelt.biz></glaser@hallowelt.biz>
```

The important line here is the one saying "Good signature". The usage of gpg and PGP is beyond the scope of this article, but feel free to ask questions in the comments. Once verified, the next step is to make sure the patch looks sane. In other words, read through it and see exactly what it does! It helps to read [the release notes](https://git.wikimedia.org/blob/mediawiki%2Fcore.git/REL1_23/RELEASE-NOTES-1.23) right before you do this. Then:

```
$ gunzip -c mediawiki-1.23.5.patch.gz | more
```

While reading through, make note of any files that have been locally patched - you will need to check on them later. If you are not used to reading diff outputs, this may be a little confusing, but give it a shot anyway, so you know what you are patching. Most MediaWiki version upgrades are very small patches, and only alter a few items across a few files. Once that is done, the final sanity check is to make sure this patch matches what it in the canonical MediaWiki git repository.

This is actually a fairly tricky task, as it turns out the patch files are generated from a custom script, and are not just the output of "git diff old_version new_version". Feel free to skip ahead, this is one method I found for making sure the patch file and the git diff match up. By "git diff", I mean the output of "git diff 1.23.4 1.23.5", for example. The biggest problem is that the files are ordered differently. Thus, even if you remove all but the actual diff portions, you cannot easily compare them. Here, "patchfile" is the downloaded and gunzipped patch file, e.g. mediawiki-1.23.5.patch, and "gitfile" is the output of git diff across two different versions, e.g. the output of "git diff 1.23.4 1.23.5". First, we want to ensure that they both have the same group of files being diffed. Then we walk through each file in the order given by the patchfile, and generate a cross-tag diff. This is saved to a file, and then compared to the original patchfile. They will not be identical, but should match up for the actual diff portions of the file.

```
## The -f42 may change from version to version
$ diff -s <(grep diff patchfile | cut -d' ' -f42 | cut -d/ -f2- | sort) <( grep diff gitfile | cut -d' ' -f4 | cut -d/ -f2- | sort)
Files /dev/fd/63 and /dev/fd/62 are identical
$ grep diff patchfile | cut -d' ' -f24 | cut -d/ -f2- | grep -v RELEASE | xargs -L1 git diff 1.23.4 1.23.5 > gitfile2
$ diff -b patchfile gitfile2
```

Okay, we have verified that the patch looks sane. The next step is to make sure your MediaWiki has a clean git status. If you don't have your MediaWiki in [git](http://git-scm.com/), now is the time to do so. It's as simple as:

```
$ cd /your/wiki/directory
$ echo -ne "images/\ncache/\n" > .gitignore
$ git init
$ git add .
$ git commit -a -q -m "Initial import of our MediaWiki directory"
```

Run "git status" and make sure you don't have any changed but uncommitted files. Once that is done, you are ready to apply the patch. Gunzip the patch file first, run the actual patch command in dryrun mode first, then do the final patch:

```
$ gunzip ~/mediawiki-1.23.5.patch.gz
$ patch -p1 --dry-run -i ~/mediawiki-1.23.5.patch
$ patch -p1 -i ~/mediawiki-1.23.5.patch
```

You may not have the "tests" directory installed, in which case it is safe to skip any missing file errors related to that directory. Just answer "Y" when asked if it is okay to skip that file. Here is an example of an actual patch from MediaWiki 1.23.3 to version 1.23.4:

```
$ patch -p1 -i ~/mediawiki-1.23.4.patch
patching file includes/config/GlobalVarConfig.php
patching file includes/db/DatabaseMysqli.php
patching file includes/DefaultSettings.php
patching file includes/libs/XmlTypeCheck.php
patching file includes/Sanitizer.php
patching file includes/upload/UploadBase.php
patching file RELEASE-NOTES-1.23
can't find file to patch at input line 387
Perhaps you used the wrong -p or --strip option?
The text leading up to this was:
--------------------------
|diff -Nruw -x messages -x '*.png' -x '*.jpg' -x '*.xcf' -x '*.gif' -x '*.svg' -x '*.tiff' -x '*.zip' -x '*.xmp' -x '.git*' mediawiki-1.23.3/tests/phpunit/includes/upload/UploadBaseTest.php mediawiki-1.23.4/tests/phpunit/includes/upload/UploadBaseTest.php
|--- mediawiki-1.23.3/tests/phpunit/includes/upload/UploadBaseTest.php 2014-09-24 19:58:10.961599096 +0000
|+++ mediawiki-1.23.4/tests/phpunit/includes/upload/UploadBaseTest.php 2014-09-24 19:55:15.538575503 +0000
--------------------------
File to patch: 
Skip this patch? [y] y
Skipping patch.
2 out of 2 hunks ignored
```

The jump from 1.23.4 to 1.23.5 was much cleaner:

```
$ patch -p1 -i ~/mediawiki-1.23.5.patch
patching file includes/DefaultSettings.php
patching file includes/OutputPage.php
patching file RELEASE-NOTES-1.23
```

Once the patch is applied, immediately check everything into git. This keeps the patch separate from other changes in your git history, and allows us to roll back the patch easily if needed. State the version in your commit message:

```
$ git commit -a -m "Applied mediawiki-1.23.5.patch to move from version 1.23.4 to 1.23.5"
```

The next step is to run the update script. This almost always does nothing for minor releases, but it's a good practice to get into. Running it is simple:

```
$ php maintenance/update.php --quiet --quick
```

The "quick" option prevents the usual five-second warning. The "quiet" option is supposed to turn off any non-error output, but if you are using [Semantic MediaWiki](https://semantic-mediawiki.org/), you will still receive a screen-full of unwanted output. I need to submit a patch to fix that someday. :)

Now that the new version is installed, make sure the wiki is still working! First, visit the Special:Version page and confirm that the new version number appears. Then make sure you can view a random page, that you can edit a page, and that you can upload an image. Finally, load your extension testing page.

You don't have an extension testing page? To make one, create a new page named "Extension_testing". On this page, include as many working examples of your extensions as possible, especially non-standard or heavily-used ones. For each extension, put the name of the extension in a header, describe what the output should be, and then have the extension do something interesting in such a way that a non-working extension will be noticed very quickly when viewing the page!

If you have any locally patched files (we almost always do, especially UserMailer.php!), now is the time to check that the patch did not mess up your local changes. If they did, make adjustments as needed, then make sure to git commit everything.

At this point, your wiki should be up and running the latest version of MediaWiki. Notify the users of the wiki as needed, then close out the support ticket, noting any problems you encountered. Upgrading via patch is a very straightforward procedure, but major upgrades are not! Watch for a future post on that.


