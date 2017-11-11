---
author: Greg Sabino Mullane
gh_issue_number: 1201
tags: apache, bcrypt, mediawiki, performance, security, sysadmin
title: Bonked By Basic_auth Because Bcrypt
---



<div class="separator" style="clear: both; float: right; padding: 0 1em 1em 2em; text-align: center;"><a href="/blog/2016/02/09/bonked-by-basicauth-because-bcrypt/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2016/02/09/bonked-by-basicauth-because-bcrypt/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/xUswo">Alligator photo</a> by <a href="https://www.flickr.com/people/johnjack/">Random McRandomhead</a></small></div>

**tl;dr - don't use a high bcrypt cost with HTTP basic auth!**

Recently we had a client approach us with reports of a slow wiki experience. This was 
for a [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki) we recently installed for them; 
there were no 
[fancy extensions](https://www.mediawiki.org/wiki/Manual:Extensions), and the hardware, the OS, and the 
[Apache web server](https://en.wikipedia.org/wiki/Apache_HTTP_Server) were solid, perfectly normal choices. 
I was tasked to dive in and solve this issue.

The first step in any troubleshooting is to verify and duplicate the problem. While the 
wiki did feel a bit sluggish, it was not as bad as the reports we were getting of taking 
over 15 seconds to view a page. A side-by-side comparison with a similar wiki seemed a 
good place to start. I called up the main wiki page on both the client wiki and End Point's 
internal wiki. Both were running the latest version of MediaWiki, had the same type of 
servers (located a similar distance from me), were using the same version of Apache, and 
had roughly the same 
[server load](https://en.wikipedia.org/wiki/Load_%28computing%29). While both 
wiki's pages had roughly the same amount of content, the client one loaded noticeably slower. 
It took less than a second for the End Point wiki, and around ten seconds for the client one!

The first possible culprit was MediaWiki itself. Perhaps something was misconfigured there, or 
some extension was slowing everything down? MediaWiki has 
[good debugging tools](https://www.mediawiki.org/wiki/Manual:How_to_debug). Inside the both wiki's **LocalSettings.php** file I 
turned on debugging temporarily with:

```
$wgDebugLogFile         = '/tmp/mediawiki.debug';
$wgDebugDBTransactions  = true;
$wgDebugDumpSql         = true;
$wgDebugTimestamps      = true;
```

I reloaded the page, then commented out the $wgDebugLogFile line to stop it from 
growing large (the debug output can be quite verbose!). Here's some snippets from 
the generated log file:

```
0.9151   4.2M  Start request GET /wiki/Main_Page
...
[caches] main: SqlBagOStuff, message: SqlBagOStuff, parser: SqlBagOStuff
[caches] LocalisationCache: using store LCStoreDB
0.9266   9.2M  Implicit transaction open enabled.
0.9279   9.2M  Query wikidb (1) (slave): SET /* DatabasePostgres::open  */ client_encoding='UTF8'
0.9282   9.2M  Resource id #127: Transaction state changed from IDLE -&gt; ACTIVE
0.9268   9.2M  Query wikidb (2) (slave): SET /* DatabasePostgres::open  */ datestyle = 'ISO, YMD'
...
0.9587   9.2M  Query wikidb (11) (slave): SELECT /* LCStoreDB::get  */  lc_value  FROM "l10n_cache"   WHERE lc_lang = 'en' AND lc_key = 'deps'  LIMIT 1
0.9573   9.5M  Query wikidb (12) (slave): SELECT /* LCStoreDB::get  */  lc_value  FROM "l10n_cache"   WHERE lc_lang = 'en' AND lc_key = 'list'  LIMIT 1
0.9567  10.8M  Query wikidb (13) (slave): SELECT /* LCStoreDB::get  */  lc_value  FROM "l10n_cache"   WHERE lc_lang = 'en' AND lc_key = 'preload'  LIMIT 1
0.9572  10.8M  Query wikidb (14) (slave): SELECT /* LCStoreDB::get  */  lc_value  FROM "l10n_cache"   WHERE lc_lang = 'en' AND lc_key = 'preload'  LIMIT 1
...
0.9875  21.2M  Query wikidb (195) (slave): SELECT /* LCStoreDB::get Greg */  lc_value  FROM "l10n_cache"   WHERE lc_lang = 'en' AND lc_key = 'messages:accesskey-pt-mycontris'  LIMIT 1
0.9873  21.2M  Query wikidb (196) (slave): SELECT /* LCStoreDB::get Greg */  lc_value  FROM "l10n_cache"   WHERE lc_lang = 'en' AND lc_key = 'messages:tooltip-pt-logout'  LIMIT 1
0.9868  21.2M  Query wikidb (197) (slave): SELECT /* LCStoreDB::get Greg */  lc_value  FROM "l10n_cache"   WHERE lc_lang = 'en' AND lc_key = 'messages:accesskey-pt-logout'  LIMIT 1
0.9883  21.2M  Query wikidb (198) (slave): SELECT /* LCStoreDB::get Greg */  lc_value  FROM "l10n_cache"   WHERE lc_lang = 'en' AND lc_key = 'messages:vector-more-actions'  LIMIT 1
```

Just to load a simple page, there were 194 SELECT statements! And 137 of those were trying to look in the l10n_cache table, one 
row at a time. Clearly, there is lots of room for improvement there. Someday, I may even jump in and tackle that. But for now, 
despite being very inefficient, it is also very fast. Because of the $wgDebugTimestamps, it was easy to compute how much 
time both wikis spent actually creating the page and sending it back to Apache. In this case, the difference was minimal, 
which meant MediaWiki was not the culprit.

I then turned my attention to Apache. Perhaps it was compiled differently? Perhaps there was some 
obscure 
[SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security) bug slowing things down for everyone? These were unlikely, but it was worth checking the Apache logs 
(which were in /var/log/httpd). There are 
two main logs Apache uses: access and error. The latter revealed nothing at all when I loaded the 
main wiki page. The access logs looked fairly normal:

```
85.236.207.120 - greg [19/Jan/2016:12:23:21 -0500] "GET /wiki/Main_Page HTTP/1.1" 200 23558 "-" "Mozilla/5.0 Firefox/43.0"
85.236.207.120 - greg [19/Jan/2016:12:23:22 -0500] "GET /mediawiki/extensions/balloons/js/balloon.config.js HTTP/1.1" 200 4128 "https://wiki.endpoint.com/wiki/Main_Page
" "Mozilla/5.0 Firefox/43.0"
...
85.236.207.120 - greg [19/Jan/2016:12:23:22 -0500] "GET /mediawiki/load.php?debug=false&amp;lang=en&amp;modules=mediawiki.legacy.commonPrint%2Cshared%7Cmediawiki.sectionAnchor%7Cmediawiki.skinning.interface%7Cskins.vector.styles&amp;only=styles&amp;skin=vector HTTP/1.1" 200 58697 "https://wiki.endpoint.com/wiki/Main_Page" "Mozilla/5.0 Firefox/43.0"
85.236.207.120 - greg [19/Jan/2016:12:23:22 -0500] "GET /mediawiki/resources/assets/poweredby_mediawiki_88x31.png HTTP/1.1" 200 3525 "https://wiki.endpoint.com/wiki/Main_Page" "Mozilla/5.0 Firefox/43.0"
```

Still nothing out of the ordinary. What to do next? When all else fails, go to the system calls. It's about as close to bare metal as you can easily get on a Linux system. In this case, I decided to run 
[strace](https://en.wikipedia.org/wiki/Strace) on the Apache 
[daemon](https://en.wikipedia.org/wiki/Daemon_%28computing%29) to see exactly where the time was being spent. As expected, there were a large handful of httpd processes already 
spawned and waiting for a connection. While there was no way to know which one would field my requests, some shell-fu allowed me 
to strace them all at once:

```
## The -u prevents us from picking the parent httpd process, because it is owned by root!
$ strace -o greg.httpd.trace -tt -ff `pgrep -u apache httpd | xargs -n 1 echo -p | xargs`
Process 5148 attached
Process 4848 attached
Process 5656 attached
Process 4948 attached
Process 5149 attached
Process 5148 attached
Process 4858 attached
Process 5657 attached
Process 4852 attached
Process 4853 attached
^CProcess 5148 detached
Process 4848 detached
Process 5656 detached
Process 4948 detached
Process 5149 detached
Process 5148 detached
Process 4858 detached
Process 5657 detached
Process 4852 detached
Process 4853 detached
```

Looking at one of the output of one of these revealed some important clues:

```
$ head greg.httpd.trace.4948
13:00:28.799807 read(14, "\27\3\3\2\221\0\0\0\0\0\0\0\1\35-\332\3123(\200\302\"\251'g\256\363b5"..., 8000) = 666
13:00:28.799995 stat("/wiki/htdocs/mediawiki/load.php", {st_mode=S_IFREG|0644, st_size=1755, ...}) = 0
13:00:28.800126 open("/wiki/htpasswd.users", O_RDONLY|O_CLOEXEC) = 15
13:00:28.800176 fstat(15, {st_mode=S_IFREG|0640, st_size=947, ...}) = 0
13:00:28.800204 read(15, "alice:{SHA}jA0EAgMCMEpo4Wa3n/9gy"..., 4096) = 2802
13:00:28.800230 close(15)               = 0
13:00:29.496369 setitimer(ITIMER_PROF, {it_interval={0, 0}, it_value={60, 0}}, NULL) = 0
13:00:29.496863 rt_sigaction(SIGPROF, {0x7fc962da7ab0, [PROF], SA_RESTORER|SA_RESTART, 0x7fc970605670}, {0x7fc962da7ab0, [PROF], SA_RESTORER|SA_RESTART, 0x7fc970605670
```

Aha! If you look close at those timestamps, you will notice that the time gap from the call to close() and the subsequent setitimer() is quite large at .69 seconds. That's a long time for Apache to be waiting around for something. The second clue is the file it just opened: "htpasswd.users". Seeing the top of the file, with the {SHA} in quotes, made me realize the problem - htpasswd files now support bcrypt as an authentication method, and bcrypt is designed to be secure - and slow. Sure enough, the htpasswd file had bcrypt entries with a high cost for the people that were having the most issues with the speed. This is what the file looked like (names and values changed):

```
alice:{SHA}jA0EAgMCMEpo4Wa3n/9gybBBsDPa
greg:$2y$13$+lE6+EwgtzP0m8K8VQDnYMRDRMf6rNMRZsCzko07QQpskKI9xbb/y9
mallory:$2y$15$ww8Q4HMI1Md51kul2Hiz4ctetPqJ95cmspH8T81JHfqRvmg===rVgn
carol:7RnEKJWc38uEO
bob:$apr1$uKX9Z63CqPOGX4lD1R4yVZsloJyZGf+
jon:$2y$08$SUe3Z8sgEpyDWbWhUUUU5wtVTwlpEdc7QyXOg3e5WBwM4Hu35/OSo1
eve:$apr1$I/hv09PcpU0VfXhyG7ZGaMz7Vhxi1Tm
```

I recognized the bcrypt format right away ($2y$13$). The people who were complaining the most (e.g. mallory in the example above) about the speed of the wiki had the highest costs, while those with low costs (e.g. jon), and those using something other than bcrypt (everyone else above), were not complaining at all!

The 'cost' is the number after the second dollar sign: as you can see, some of them had a cost of **15**, which is much more expensive than a cost of **13**, which is what my user ("greg") was using. This was a smoking gun, but one more step was needed for proof. I adjusted the cost of my password to something low using the [htpasswd program](https://httpd.apache.org/docs/current/programs/htpasswd.html):

```
$ htpasswd -B -C 6 /wiki/htpasswd.users greg
New password: 
Re-type new password: 
Updating password for user greg
```

Voila! The page loaded in a flash. I then changed the cost to 15 and suddenly the wiki was even slower than before - taking 
upwards of 15 seconds to load the main page of the wiki. Mystery solved. All those high cost bcrypt requests are also not good 
for the server: not only does it use a lot of CPU, but ends up keeping the Apache daemon tied up waiting for the bcrypt to 
finish, rather than simply finishing up quickly and going back to the main pool.

You may be asking a few questions at this point, however. Why would htpasswd offer a footgun like this? Why such a radical 
difference in effect for slightly different costs? Is bcrypt a good practice for a htpasswd file? Let's attempt to answer 
those. Before we do, we have to learn a little bit about bcrypt and passwords in general. Some of this is purposefully 
oversimplified, so be gently in the comments. :)

Passwords themselves are never stored on a server (aka the machine doing the authentication). Instead, the server stores 
a hash of the password. This is created by what is known as a "one-way" function, that creates a unique fingerprint of your 
password. If this fingerprint (aka hash) is discovered, there is no direct way to see the password that created it. When 
you login to a site, it creates a hash of the password you give it, then compares that hash to the one it has stored. Thus, 
it can verify that you have given it the correct password without actually having to store the password.

For a long time, very simple algorithms were used to create these hashes. However, as computers became more powerful, 
and as the field of cryptography advanced, it became easier to "crack" these hashes and determine the password that 
was used to create them. This was an important problem, and one of the solutions that people came up with was the 
[bcrypt algorithm](https://en.wikipedia.org/wiki/Bcrypt), which makes the computation of the hash very expensive, in terms of computer speed. Furthermore, that 
speed is adjustable, and determined by the "cost" given at creation time. You may have noticed the **-C** option I 
used in the htpasswd example above. That number indicates the number of rounds the algorithm must go through. However, the cost 
given leads to 2^code rounds, which means that the cost is exponential. In other words, a cost of 13 means that bcrypt runs 
2 to the 13th power rounds, or 8,192 rounds. A cost of 14 is 2 to the 14th power, or 16,384 rounds - twice as slow as 
a cost of 13! A cost of 15 is 32,768 rounds, etc. Thus, one can see why even a cost of 15 would be much slower than a cost of 13.

A web page usually returns more than just the requested HTML. There are commonly images, CSS, and JavaScript that must also be 
loaded from the webserver to fully render the page. Each of these requests must go through basic auth, and thus get slowed down 
by bcrypt. This is why even though each basic authentication via bcrypt of 15 only takes a couple of seconds, the entire web 
page can take much longer.

What encryption options are available for htpasswd program? The bcrypt option was introduced without much fanfare in 
[version 2.4.4 of Apache](https://httpd.apache.org/docs/2.4/new_features_2_4.html#programs), which was released on February 25, 2013. So, it's been around a while. The output of --help shows 
us that bcrypt is the only secure one, but allows for other legacy ones to be used. Also note that the range of costs for 
bcrypt range from 4 to 31:

```
 -m  Force MD5 encryption of the password (default).
 -B  Force bcrypt encryption of the password (very secure).
 -C  Set the computing time used for the bcrypt algorithm
     (higher is more secure but slower, default: 5, valid: 4 to 31).
 -d  Force CRYPT encryption of the password (8 chars max, insecure).
 -s  Force SHA encryption of the password (insecure).
 -p  Do not encrypt the password (plaintext, insecure).
```

So should you use bcrypt for your htpasswd? Absolutely yes. Even a lower cost bcrypt is incredibly 
more secure than using MD5, CRYPT, or SHA. A cost of 10 is roughly the same speed as those, 
but a much, much better choice. You can measure the time it takes to create or update your password via 
the command-line htpasswd command to get a rough idea of how much impact it will have on your 
website. You can use the time it takes to run the htpasswd command as rough proxy for the total 
page load time. Here are some numbers I generated on my local box. Numbers represent the average 
of a few runs:

<table border="1" class="gsm">
<tbody><tr>
<th>Bcrypt cost</th>
<th>htpasswd creation time</th>
<th>Web page load time</th>
</tr>
<tr><td>10</td><td>0.079</td><td>5.68 seconds</td></tr>
<tr><td>12</td><td>0.268</td><td>6.77 seconds</td></tr>
<tr><td>14</td><td>0.979</td><td>10.78 seconds</td></tr>
<tr><td>16</td><td>3.684</td><td>25.72 seconds</td></tr>
<tr><td>18</td><td>14.683</td><td>88.85 seconds</td></tr>
<tr><td>20</td><td>58.680</td><td>358.80 seconds</td></tr>
<tr><td>22</td><td>236.369</td><td>1357.82 seconds</td></tr>
<tr><td>31</td><td>186,173 seconds<br/>(51 hours and 42 minutes!!)</td><td>Ah...no</td></tr>
</tbody></table>

There are times where you really do want a higher bcrypt cost. The basic auth usage in this 
scenario is really the exception, and not the norm. In most cases, a password will be used to log in 
to something, and you will either create a persistent connection (e.g. SSH), or a cookie with a 
temporary token will be issued (e.g. almost every website in the world). In those cases, a few 
seconds delay are quite acceptable, as it is a rare event.

So why do we even care about passwords so much, especially for something like basic auth and 
a htpasswd file? After all, if someone can view the contents of the htpasswd file, they can 
also more than likely view whatever material on the web server it was designed to protect. 
These days, however, it's important to view strong hashes such as bcrypt as not just 
protecting data, but protecting the password as well. Why? Password reuse. 
It's very common for people to use the same (or very similar) password on all the sites 
they visit. The danger is thus not that an attacker can view the file contents protected 
by the htpasswd file, but that an attacker can use that password on the user's email accounts, or 
on other sites the user may have visited and used the same password.

What bcrypt cost should you use? The general answer is to use the highest possible cost 
you can get away with. Take something with such a high cost that is causes discomfort 
to the users, then dial it back a tiny bit. Measure it out and see what your server 
can handle. For general bcrypt use, start with 13, but don't be afraid to keep going up until it takes a 
wall clock second or two to run. For basic auth, use something very fast: perhaps 9 or less. Anything 
that takes over a second to create via htpasswd will slow a site down noticeably!


