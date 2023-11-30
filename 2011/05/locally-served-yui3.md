---
author: Brian J. Miller
title: Locally served YUI3
github_issue_number: 449
tags:
- javascript
date: 2011-05-11
---

For the vast majority of sites serving static JS and CSS files such as those required by YUI (or jQuery etc.) from a CDN makes great sense: improved performance through caching and geography, reduced load, improved uptime, leveraging some large corporations’ resources, etc.

Unfortunately as soon as you hit an SSL secured page you can’t use a CDN’s resources securely, a common thing with e-commerce sites and administration panels. In the YUI case that means doing at least a little bit of extra configuration and maintenance of an installed library base, an all-too-common task in typical server-side development that’s becoming more common as libraries are maintained for client-side usage as well.

Toss in “combo loading” and all of a sudden it feels like the software development cycle can’t just be discarded ’cause you are working on the web. Maybe this is really what they meant by Web 2.0. But I digress...

Since I’m familiar with and working on YUI3, here is how we have it working for non-CDN based serving for an administration panel developed for a newer generation of an Interchange site. Our custom application uses YUI3 (core), modules from the [YUI3 Gallery](https://clarle.github.io/yui3/gallery-archive/gallery/index.html), and a few modules that are pulled in using the YUI 2in3 version compatibility layer. Now, down to business...

Each of the libraries is [provided by the YUI team on GitHub](https://github.com/yui/). Since our project has Git under it (you are using Git, right?) we can set up submodules to help us with tracking new versions as they are released (or really be on the bleeding edge ahead of releases). To start we choose a location to serve the files. This is fairly arbitrary and I happened to choose /vendor. Then set up new submodules for each of the libraries in use:

- git submodule add http://github.com/yui/yui3 vendor/yui3
- git submodule add http://github.com/yui/yui3-gallery vendor/yui3-gallery
- git submodule add http://github.com/yui/2in3 vendor/yui-2in3

Follow that with the normal `git submodule init`, `git submodule update` cycle to pull down the HEAD version of each library. At this point the library files are available for local serving, and the current version is pegged against the superproject.

With the files locally stored they can be served locally. To do so we need to adjust the “seed” file for the YUI core, the loader, and any CSS files loaded on the page. For instance,

```
<!-- YUI Seed, Loader, and our primary source -->
<script type="text/javascript" src="/combo?vendor/yui3/build/yui/yui.js&vendor/yui3/build/loader/loader.js"></script>
```

(For now ignore the “/combo” portion of this. More on that later.)

With the yui.js and loader.js files loading from a local resource YUI will automatically know where to look for other YUI3 core files. But for non-core files (such as gallery modules or 2in3 loaded modules) we need to provide more information to the loader through the YUI_config global variable.

<script src="https://gist.github.com/934486.js"></script>

The above configuration has parameters for both combo and non-combo loading.

Lines 4–7 tell the loader where to find core modules explicitly, though the loader should default to these based on the location of the seed file.

Starting on line 9 there are definitions for the additional groups of files that we now want locally served. The first group, lines 11–20, are needed to load our local gallery files.

Lines 25–44, as the comment above them indicates, are for loading specific CSS files that were not properly handled by the first group, though I’ve yet to track down why (more robust skin support may fix this issue).

Lines 46–62 bring in YUI 2-in-3, note the specific minor version of 2 is pegged in line 47 and 50.

With this configuration in place, and properly located files on the filesystem you should be able to use any core, gallery, or 2in3 modules loaded from your local system.

But what about “combo loading”? That allows us to reduce the number of round-trip requests made to pull down the dependencies by concatenating a set of files together (either JS or CSS but not mixed together), when serving from the CDN you get this because Yahoo! has provided a combo loading service.

You can see a PHP-based loading service provided by the YUI team in [the phploader project](https://github.com/yui/phploader/). Because we are working with Interchange and aren’t using PHP, I’ve written [a similar script to be used as plain ol' boring CGI](https://github.com/brianjmiller/cgi-combo/blob/master/combo).

In the example code this script would be set up to run at the root of our URL space, specifically as `/combo` and the script itself will need to know where to find the local root `vendor` on the physical file system.

It is important to note that combo loading CSS files takes some special parsing to make images and other referenced files work correctly. Also note that my version does not work with includes in the CSS.

Finally, one of the biggest benefits to this set up is being able to test literally any commit in any of the modules while leaving all else the same. This can allow you to determine when a bug first entered the picture (see `git bisect`) or test against development branches ahead of releases. To test against the latest and greatest between releases, you simply have to go to one of the submodule paths, fetch any recent updates, then check out a branch, merge from the origin branch, and test. If all your tests pass, then you `git add` the submodule path in the superproject, `git commit`, and know that your stack is now up to date.

Hopefully some day the gallery modules themselves will be Git submodules so that maintaining a local gallery will not involve pulling down all modules and an application can peg (or update) a specific module as needed by the application. Essentially you’d have your own gallery.
