---
author: Steph Skardal
gh_issue_number: 586
tags: tips
title: 'Three Things: Photography, Facebook on WordPress, and the watch command'
---

### 1. Photography News

There’s been some recent news in the photography space. [Adobe](http://www.adobe.com/) announced Photoshop CS6, and [Lightroom 4](http://www.adobe.com/products/photoshop-lightroom.html), and [Adobe Photoshop Touch](http://www.adobe.com/products/photoshop-touch.html) recently. The [Lytro](http://www.lytro.com/) [Light Field] camera has picked up recognition lately. The new [Nikon D4](http://imaging.nikon.com/lineup/dslr/d4/) recently became available, as well as the [Canon 5D MK III](http://usa.canon.com/cusa/consumer/products/cameras/slr_cameras/eos_5d_mark_iii), both high end DSLRs.

### 2. Facebook Comments for WordPress

Last week, I was working on WordPress development for [The Best Game Apps](http://www.thebestgameapps.com/), and I came across a strange Facebook integration error about compatibility mode, show in the screen below:

<img border="0" src="/blog/2012/04/11/three-things-photography-facebook-on/image-0.png"/>

The site uses the WordPress plugin [Facebook Comments for WordPress](http://wordpress.org/extend/plugins/facebook-comments-for-wordpress/). After some research, I decided to dig into the Facebook documentation and the code to make the following change myself to specify the post URL as the href attribute in the facebook markup:

```diff
219c219
-    echo "\t&lt;fb:comments xid='$xid' url='$postUrl' $siteisdark ",
+    echo "\t&lt;fb:comments xid='$xid' href='$postUrl' url='$postUrl' $siteisdark ",
```

In the context of:

```php
219                     echo "\t&lt;fb:comments xid='$xid' href='$postUrl' url='$postUrl' $siteisdark ",
220                         "numposts='{$fbc_options['numPosts']}' ",
221                         "width='{$fbc_options['width']}' ",
222                         "publish_feed='$publishToWall' ",
223                         "migrated='1'&gt;&lt;/fb:comments&gt;";
```

With this change, the Facebook error message disappeared and all appeared to be working as expected. I’m surprised that this hasn’t been fixed in the plugin itself, and the documentation wasn't extremely helpful. Sometimes the best option is to go right to the code. And of course, I'm recording this so I can revisit it if it breaks again with a WordPress plugin upgrade.

### 3. The watch Command

I was talking to [Jon](/team/jon_jensen) recently about monitoring disk usage and he mentioned the [watch](http://linux.about.com/library/cmd/blcmdl1_watch.htm) command. Specifically, the watch command might be a good tool to monitor disk usage if you expect to see the disk fill up quickly while you are actively developing on it. I'm always learning random tips from End Point's sysadmin experts, and this one may come in handy at some point.
