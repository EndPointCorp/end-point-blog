---
author: Emanuele “Lele” Calò
gh_issue_number: 919
tags: apache, linux, php, sysadmin
title: 'phpMemcachedAdmin: Graphical/Web Administration for memcached'
---

Memcached is an awesome tool, though it doesn't offer the best interactive administration experience out there, with its command manually run via a telnet/nc connection.

Well luckily enough there's an alternative to all that pain and its name is *[phpMemcachedAdmin](http://code.google.com/p/phpmemcacheadmin/)*

While the development stopped in the end of 2012 (if we don't consider minor forks) the features offered are quite interesting.

Quoting directly from the main site:

*[...]

This program allows to see in real-time (top-like) or from the start of the server, stats for get, set, delete, increment, decrement, evictions, reclaimed, cas command, as well as server stats (network, items, server version) with googlecharts and server internal configuration

You can go further to see each server slabs, occupation, memory wasted and items (key &amp; value).

Another part can execute commands to any memcached server : get, set, delete, flush_all, as well as execute any commands (like stats) with telnet

[...]*

Which is incredible news, even more considering the complete lack of similar features from the native Memcached code.

Since all the code basically revolves around a PHP file, the setup phase is just a matter of creating a new VirtualHost section inside a working web server which can serve PHP files and placing the uncompressed code tarball inside the docroot. For more details and configuration info, please consult the code homepage.

It's important to highlight that phpMemcachedAdmin has absolutely no layer of security. Unless you're setting up phpMemcachedAdmin just for teaching or testing purposes, it's strongly advisable to protect it with at least a simple Basic Auth mechanism and possibly HTTPS in order to protect your Memcached cluster from potential malicious attackers.

Once you have a working instance you'll see something similar to the following screenshots:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/02/03/phpmemcachedadmin-graphicalweb/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/02/03/phpmemcachedadmin-graphicalweb/image-0.png"/></a></div>

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/02/03/phpmemcachedadmin-graphicalweb/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/02/03/phpmemcachedadmin-graphicalweb/image-1.png"/></a></div>

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/02/03/phpmemcachedadmin-graphicalweb/image-2-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/02/03/phpmemcachedadmin-graphicalweb/image-2.png"/></a></div>

Every Memcached administrator or heavy user have, at least once, wished to have such a powerful tool and now you can finally put your favourite terminal at rest.. at least for the next minute.
