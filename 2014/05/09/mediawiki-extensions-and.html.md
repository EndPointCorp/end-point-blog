---
author: Greg Sabino Mullane
gh_issue_number: 980
tags: git, mediawiki, troubleshooting
title: MediaWiki extensions and wfLoadExtensionMessages
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2014/05/09/mediawiki-extensions-and/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/05/09/mediawiki-extensions-and/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/dykcFR">Image</a> by Flickr user <a href="https://www.flickr.com/photos/yukonlife/">Susan Drury</a></small>
</div>

Upgrading MediaWiki can be a challenging task, especially if you use a lot of extensions. 
While the core upgrade process usually goes smoothly, it’s rare you can upgrade a major 
version or two without having to muddle with your collection of extensions. Extensions are bits of code that extend what MediaWiki can do. Only a few are packaged with and maintained alongside MediaWiki itself—​the great majority are written by third-party developers. When the MediaWiki API changes, it is up to those developers to update their extension so it works with the new version of MediaWiki. This does not always happen. Take for example one of the more common errors seen on a MediaWiki upgrade since 1.21 was released:

[Tue May 06 11:21:52 2014] [error] [client 12.34.56.78] PHP Fatal error:  
Call to undefined function wfLoadExtensionMessages() in /home/beckett/mediawiki/extensions/PdfExport/PdfExport.php on line 83, referer: http://test.ziggy.com/wiki/Main_Page

This is because the **wfLoadExtensionMessages** function, which many extensions use, has 
been deprecated since MediaWiki version 1.16 and was finally removed in 1.21, resulting in the 
error seen above. Luckily, this function has been a no-op since 1.16, so it is safe 
to comment it out and/or make a dummy function in your LocalSettings.php file (see below).

Sadly, the release notes for 1.21 make no mention of 
[this fairly major change](https://lists.gt.net/wiki/wikitech/214619). Let’s 
walk through as if we didn’t know anything about it and see how we could solve the 
given error with the help of git. For this example, we’ll use the 
[Pdf Export extension](https://www.mediawiki.org/wiki/Extension:Pdf_Export), 
which allows you to export your wiki pages into PDF form. A pretty handy extension, and 
one which completely fails to work in MediaWiki version 1.21 or better.

First, let’s verify that wfLoadExtensionMessages does not exist at all in version 1.21 of MediaWiki. For 
these examples, I’ve checked out the MediaWiki code via git, and am relying on 
the fact that lightweight git tags were made for all the versions we are interested in.

$ git clone https://github.com/SemanticMediaWiki/SemanticMediaWiki.git mediawiki

$ cd mediawiki

$ git grep wfLoadExtensionMessages 1.21.0

1.21.0:HISTORY:* (bug 12880) wfLoadExtensionMessages does not use $fallback from MessagesXx.php

A nice feature of git-grep is the ability to simply use a tag after the search string. In this 
case, we see that the only mention of wfLoadExtensionMessages in the entire codebase is an 
old mention of it in the history file. Let’s see what version that bug is from:

$ git grep -n wfLoadExtensionMessages 1.21.0

1.21.0:HISTORY:5280:* (bug 12880) wfLoadExtensionMessages does not use $fallback from MessagesXx.php

$ git show 1.21.0:HISTORY | head -5280 | tac | grep '===' -m1

=== Bug fixes in 1.12 ===

That message is from way back in version 1.12, and doesn’t concern us. Let’s take a look at 
what tags exist in the 1.20 branch so we can scan the latest one:

```
<span class="gsm">$ git tag | grep '^1\.20'
1.20.0
1.20.0rc1
1.20.0rc2
1.20.1
1.20.2
1.20.3
1.20.4
1.20.5
1.20.6
1.20.7
1.20.8</span>
```

Now we can peek inside version 1.20.8 and see what that function did before it was removed. 
By using the -A and -B (after and before) arguments to grep, we can see the entire function in 
context:

```
<span class="gsm">$ git grep wfLoadExtensionMessages 1.20.0
1.20.0:HISTORY:* (bug 12880) wfLoadExtensionMessages does not 
  use $fallback from MessagesXx.php
1.20.0:includes/GlobalFunctions.php:function wfLoadExtensionMessages() {
$ git show 1.20.8:includes/GlobalFunctions.php | \
  grep -B6 -A2 LoadExtensionMessages
/**
 * Load an extension messages file
 *
 * @deprecated since 1.16, warnings in 1.18, remove in 1.20
 * @codeCoverageIgnore
 */
function wfLoadExtensionMessages() {
    wfDeprecated( __FUNCTION__, '1.16' );
}
</span>
```

Thus wfLoadExtensionMessages was basically a no-op in MediaWiki version 1.20, with the caveat that it will write 
a deprecation warning to your error log (or, in modern versions, the debug log unless $wgDevelopmentWarnings is set). 
Next we want to find the last time this function did something useful—​which should be version 1.15 according to 
the comment above. Thus:

```
<span class="gsm">$ git show 1.15.0:includes/GlobalFunctions.php | \
  grep -A4 LoadExtensionMessages
function wfLoadExtensionMessages( $extensionName, $langcode = false ) {
    global $wgExtensionMessagesFiles, $wgMessageCache, $wgLang, $wgContLang;

    #For recording whether extension message files have been loaded in a given language.
    static $loaded = array();
</span>
```

So, it’s a pretty safe bet that unless you are upgrading from 1.15.0 or earlier, it should 
be completely safe to remove it. When was 1.16.0 released? There are no dates in the HISTORY 
file (shame), but the date it was tagged should be a good guess:

```
<span class="gsm">$ git show 1.16.0 | grep -m1 Date
Date:   Wed Jul 28 07:11:03 2010 +0000
</span>
```

So what should you do with extensions that are still using this deprecated function? There are 
two quick solutions: comment it out inside the extension, or add a dummy function to your version 
of MediaWiki.

Changing the extension itself is certainly quick and easy. To get the PdfExport extension to work, 
we only have to comments out two calls to wfLoadExtensionMessages inside of the file 
PdfExport.php, and one inside of PdfExport_body.php. The diff:

```
<span class="gsm">$ git difftool -y -x "diff -u1"
--- /tmp/7YqvXv_PdfExport.php 2014-05-08 12:45:03 -0400
+++ PdfExport.php             2014-05-08 12:34:39 -0400
@@ -82,3 +82,3 @@
   if ($img_page > 0 || $img_page === false) {
-        wfLoadExtensionMessages('PdfPrint');
+        //wfLoadExtensionMessages('PdfPrint');
                $nav_urls['pdfprint'] = array(
@@ -92,3 +92,3 @@
 function wfSpecialPdfToolbox (&$monobook) {
-          wfLoadExtensionMessages('PdfPrint');
+          //wfLoadExtensionMessages('PdfPrint');
           if (isset($monobook->data['nav_urls']['pdfprint']))
--- /tmp/7gO8Hz_PdfExport_body.php   2014-05-08 12:45:03 -0400
+++ PdfExport_body.php               2014-05-08 12:34:44 -0400
@@ -44,3 +44,3 @@
            // For backwards compatibility
-             wfLoadExtensionMessages('PdfPrint');
+             //wfLoadExtensionMessages('PdfPrint');
</span>
```

A better way is to add a dummy function to LocalSettings.php. This ensures that any extension 
we add in the future will continue to work unmodified. Just throw this at the bottom 
on your LocalSettings.php:

```
<span class="gsm">function wfLoadExtensionMessages() { }
</span>
```

Probably the best overall solution is to not only add that to your LocalSettings.php, 
but to try to get the extension changed as well. You can notify the author, or try to 
fix it yourself and release a new version if the extension has been abandoned. You might 
also look to see if the extension has been superseded by a different extension, as sometime 
happens.

While there may be other compatibility issues when upgrading MediaWiki, for some extensions 
(such as PdfExport), this is the only change needed to make it work again on newer versions of MediaWiki!


