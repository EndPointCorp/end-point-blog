---
author: Greg Sabino Mullane
gh_issue_number: 1139
tags: postgres
title: How fast is pg_upgrade anyway?
---

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2015/07/01/how-fast-is-pgupgrade-anyway/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/07/01/how-fast-is-pgupgrade-anyway/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/db6hGQ">Shark photo</a> by <a href="https://www.flickr.com/people/tomsaint/">Rennett Stowe</a>
</small></div>

Back in the old days, upgrading Postgres required doing a pg_dump and loading 
the resulting logical SQL into the new database. This could be a very slow, 
very painful process, requiring a lot of downtime. While there were other solutions 
(such as [Bucardo](https://bucardo.org/wiki/Bucardo)) that allowed little (or even zero) downtime, setting them 
up was a large complex task. Enter 
[the pg_upgrade program](https://www.postgresql.org/docs/current/static/pgupgrade.html), which attempts to upgrade a 
cluster with minimal downtime. Just how fast is it? I grew tired of answering 
this question from clients with vague answers such as “it depends” and “really, 
really fast” and decided to generate some data for ballpark answers.

Spoiler: it’s either about 3.5 times as fast as pg_dump, or insanely 
fast at a flat 15 seconds or so. Before going further, let’s discuss the methodology used.

I used the venerable pgbench program to generate some sample tables and data, 
and then upgraded the resulting database, going from Postgres version 9.3 to 9.4. The pgbench program comes with Postgres, and simply requires an **--initialize** argument to create the test tables. There is also a **--scale** argument you can provide to increase the amount of initial data—​each increment increases the number of rows in the largest table, pgbench_accounts, by one hundred thousand rows. Here are the scale runs I did, along with the number of rows and overall database size for each level:

<table class="gsm">
<caption>Effect of --scale</caption>
<tbody><tr><th>--scale</th><th>Rows in pgbench_accounts</th><th>Database size</th></tr>
<tr><td>100</td><td>10,000,000</td><td>1418 MB</td></tr>
<tr><td>150</td><td>15,000,000</td><td>2123 MB</td></tr>
<tr><td>200</td><td>20,000,000</td><td>2829 MB</td></tr>
<tr><td>250</td><td>25,000,000</td><td>3535 MB</td></tr>
<tr><td>300</td><td>30,000,000</td><td>4241 MB</td></tr>
<tr><td>350</td><td>35,000,000</td><td>4947 MB</td></tr>
<tr><td>400</td><td>40,000,000</td><td>5652 MB</td></tr>
<tr><td>450</td><td>45,000,000</td><td>6358 MB</td></tr>
<tr><td>500</td><td>50,000,000</td><td>7064 MB</td></tr>
<tr><td>550</td><td>55,000,000</td><td>7770 MB</td></tr>
<tr><td>600</td><td>60,000,000</td><td>8476 MB</td></tr>
</tbody></table>

To test the speed of the pg_dump program, I used this simple command:

```
$ pg_dump postgres | psql postgres -q -p 5433 -f -
```

I did make one important optimization, which was to set 
[
fsync](https://www.postgresql.org/docs/current/static/runtime-config-wal.html#GUC-FSYNC) off on the target database (version 9.4). Although this setting should never be turned off in production—​or anytime you cannot replace all your data, upgrades 
like this are an excellent time to disable fsync. Just make sure you flip it back on 
again right away! There are some other minor optimizations one could make (especially 
boosting [maintenance_work_mem](https://www.postgresql.org/docs/current/static/runtime-config-resource.html#GUC-MAINTENANCE-WORK-MEM)), but for the purposes of this test, I decided that the fsync was enough.

For testing the speed of pg_upgrade, I used the following command:

```
$ pg_upgrade -b $BIN1 -B $BIN2 -d $DATA1 -D $DATA2 -P 5433
```

The speed difference can be understood because pg_dump rewrites the 
entire database, table by table, row by row, and then recreates all the indexes 
from scratch. The pg_upgrade program simply copies the data files, making the 
minimum changes needed to support the new version. Because of this, it will 
always be faster. How much faster depends on a lot of variables, e.g. the number 
and size of your indexes. The chart below shows a nice linear slope for 
both methods, and yielding on average a 3.48 increase in speed of pg_upgrade versus 
pg_dump:

<table class="gsm">
<caption>pg_dump versus pg_upgrade</caption>
<tbody><tr><th>--scale</th><th>Database size</th><th>pg_dump<br/>(seconds)</th><th>pg_upgrade <br/>(seconds)</th><th>Speedup</th></tr>
<tr><td><tt>100</tt></td><td>1.4 GB</td><td>210.0</td><td>74.7</td><td>2.82</td></tr>
<tr><td>150</td><td>2.1 GB</td><td>305.0</td><td>79.4</td><td>3.86</td></tr>
<tr><td>200</td><td>2.8 GB</td><td>457.6</td><td>122.2</td><td>3.75</td></tr>
<tr><td>250</td><td>3.5 GB</td><td>636.1</td><td>172.1</td><td>3.70</td></tr>
<tr><td>300</td><td>4.2 GB</td><td>832.2</td><td>215.1</td><td>3.87</td></tr>
<tr><td>350</td><td>4.9 GB</td><td>1098.8</td><td>320.7</td><td>3.43</td></tr>
<tr><td>400</td><td>5.7 GB</td><td>1172.7</td><td>361.4</td><td>3.25</td></tr>
<tr><td>450</td><td>6.4 GB</td><td>1340.2</td><td>426.7</td><td>3.15</td></tr>
<tr><td>500</td><td>7.1 GB</td><td>1509.6</td><td>476.3</td><td>3.17</td></tr>
<tr><td>550</td><td>7.8 GB</td><td>1664.0</td><td>480.0</td><td>3.47</td></tr>
<tr><td>600</td><td>8.5 GB</td><td>1927.0</td><td>607</td><td>3.17</td></tr>
</tbody></table>

If you graph it out, you can see both of them having a similar slope, but 
with pg_upgrade as the clear winner:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/07/01/how-fast-is-pgupgrade-anyway/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/07/01/how-fast-is-pgupgrade-anyway/image-1.png"/></a></div>

I mentioned earlier that there were some other optimizations that could be done to make the pg_dump slightly faster. As it turns out, pg_upgrade can also be made faster. Absolutely, beautifully, insanely faster. All we have to do is add the **--link** argument. What this does is rather than copying the data files, it simply links them via the filesystem. Thus, each large data file that makes up the majority of a database’s size takes a fraction of a second to link to the new version. Here are the new numbers, generated simply by adding a **--link** to the pg_upgrade command from above:

<table class="gsm">
<caption>pg_upgrade --link is crazy fast</caption>
<tbody><tr><th>--scale</th><th>Database size</th><th>pg_upgrade --link<br/>(seconds)</th></tr>
<tr><td>100</td><td>1.4 GB</td><td>12.9</td></tr>
<tr><td>150</td><td>2.1 GB</td><td>13.4</td></tr>
<tr><td>200</td><td>2.8 GB</td><td>13.5</td></tr>
<tr><td>250</td><td>3.5 GB</td><td>13.2</td></tr>
<tr><td>300</td><td>4.2 GB</td><td>13.6</td></tr>
<tr><td>350</td><td>4.9 GB</td><td>14.4</td></tr>
<tr><td>400</td><td>5.7 GB</td><td>13.1</td></tr>
<tr><td>450</td><td>6.4 GB</td><td>13.0</td></tr>
<tr><td>500</td><td>7.1 GB</td><td>13.2</td></tr>
<tr><td>550</td><td>7.8 GB</td><td>13.1</td></tr>
<tr><td>600</td><td>8.5 GB</td><td>12.9</td></tr>
</tbody></table>

No, those are not typos—​an average of thirteen seconds despite the size of the database! The only downside to this method is that you cannot access the old system once the new system starts up, but that’s a very small price to pay, as you can easily backup the old system first. There is no point in graphing these numbers out—​just look at the graph above and imagine a nearly flat line traveling across the bottom of the graph :)

Are there any other options that can affect the time? While pgbench has a handy **--foreign-keys** argument I often use to generate a more “realistic” test database, both pg_dump and pg_upgrade are unaffected by any numbers of foreign keys. One limitation of pg_upgrade is that it cannot change the **--checksum** attribute of a database. In other words, if you want to go from a non-checksummed version of Postgres to a checksummed version, you need to use pg_dump or some other method. On the plus side, my testing found negligible difference between upgrading a checksummed versus a non-checksummed version.

Another limitation of the pg_upgrade method is that all internal stats are blown away by the upgrade, so the database starts out in a completely unanalyzed state. This is not as much an issue as it used to be, as pg_upgrade will generate a script to regenerate these stats, using the handy **--analyze-in-stages** argument to vacuum. There are a few other minor limitations to pg_upgrade: read [the documentation](https://www.postgresql.org/docs/current/static/pgupgrade.html#AEN165408) for a complete list. In the end, pg_upgrade is extraordinarily fast and should be your preferred method for upgrading. Here is a final chart showing the strengths and weaknesses of the major upgrade methods.

<table class="gsm">
<caption>Postgres upgrade methods compared</caption>
<tbody><tr><th>Method</th><th>Strengths</th><th>Weaknesses</th></tr>
<tr><td>pg_dump</td><td><ul><li>Always works</li><li>Battle tested</li></ul></td><td><ul><li>Slowest method</li><li>Maximum downtime</li><li>Requires lots of disk space</li></ul></td></tr>
<tr><td>pg_upgrade</td><td><ul><li>Very fast</li><li>--link mode super fast</li></ul></td><td><ul><li>Cannot always be used (finicky)</li><li>Stats are lost</li><li>Minimal but non-zero downtime</li></ul></td></tr>
<tr><td>Bucardo</td><td><ul><li>Handles complex cases</li><li>Zero-downtime possible</li></ul></td><td><ul><li>Complex to setup</li><li>Requires primary keys on large tables</li><li>Requires lots of disk space</li></ul></td></tr>
</tbody></table>

(As an addendum of sorts, pg_upgrade is fantastic, but the Holy Grail is still out of sight: true in-place upgrades. This would mean dropping in a new major version (similar to the way revisions can be dropped in now), and this new version would be able to read both old and new data file formats, and doing an update-on-write as needed. Someday!)
