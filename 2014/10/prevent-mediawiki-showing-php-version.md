---
author: Greg Sabino Mullane
title: 'Prevent MediaWiki showing PHP version with new extension: ControlSpecialVersion'
github_issue_number: 1047
tags:
- mediawiki
date: 2014-10-29
---



<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2014/10/prevent-mediawiki-showing-php-version/image-0-big.png" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/10/prevent-mediawiki-showing-php-version/image-0.png"/></a><br/>Sok Kwu Wan</div>

I recently created a new [MediaWiki extension](https://www.mediawiki.org/wiki/Manual:Extensions) named **ControlSpecialVersion** whose purpose is to allow some control over what is shown on MediaWiki’s “special” page Special:Version. The latest version of this extension can be [downloaded from Mediawiki.org](https://www.mediawiki.org/wiki/Extension:ControlSpecialVersion).
The primary purpose of the module is to prevent showing the PHP and database versions to the public.

As with most MediaWiki extensions, installation is easy: download the tarball, unzip it into your **extensions** directory, and add this line to your LocalSettings.php file:

```plain
require_once( "$IP/extensions/ControlSpecialVersion/ControlSpecialVersion.php" );
```

By default, the extension removes the PHP version information from the page. It also changes the PostgreSQL reported version from its revision to simply the major version, and changes the name from the terrible-but-official “PostgreSQL” to the widely-accepted “Postgres”. Here is what the **Software** section of bucardo.org looks like before and after the extension is used:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/10/prevent-mediawiki-showing-php-version/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/10/prevent-mediawiki-showing-php-version/image-1.png"/></a></div>

<div class="separator" style="clear: both; text-align: center; padding-bottom: 1em"><a href="/blog/2014/10/prevent-mediawiki-showing-php-version/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/10/prevent-mediawiki-showing-php-version/image-2.png"/></a></div>

Note that we are also eliding the git revision information (sha and date). You can also do things such as hide the revision information from the extension list, remove the versions entirely, or even remove an extension from showing up at all. All the configuration parameters can be found on the [extension’s page on mediawiki.org](https://www.mediawiki.org/wiki/Extension:ControlSpecialVersion).

It should be noted that there are typically two other places in which your PHP version may be exposed, both in the HTTP headers. If you are running Apache, it may show the version as part of the **Server** heading. To turn this off, edit you httpd.conf file and change the **ServerTokens** directive to **ProductOnly**. The other header is known as **X-Powered-By** and is added by PHP to any pages it serves (e.g. MediaWiki pages). To disable this header, edit your php.ini file and make sure **expose_php** is set to **Off**.

While these methods may or may not make your server safer, there really is no reason to expose certain information to the world. With this extension, you at least have the choice now.


