---
author: Greg Sabino Mullane
title: 'Postgres WAL files: best compression methods'
github_issue_number: 1294
tags:
- postgres
- compression
date: 2017-03-28
---

<div class="separator" style="clear: both; text-align: center; float:right"><a href="/blog/2017/03/postgres-wal-files-best-compression/image-0.jpeg" imageanchor="1" style="clear:float; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2017/03/postgres-wal-files-best-compression/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/9sa2bM">Turtle turtle</a> by WO1 Larry Olson from <a href="https://www.flickr.com/people/familymwr/?rb=1">US Army</a></small>
</div>

The [PostgreSQL database system](https://postgresql.org) uses the write-ahead logging method to ensure that
a log of changes is saved before being applied to the actual data. The log
files that are created are known as [WAL (Write Ahead Log) files](https://www.postgresql.org/docs/current/static/wal-intro.html), and by default
are 16 MB in size each. Although this is a small size, a busy system can generate hundreds
or thousands of these files per hour, at which point disk space becomes an issue.
Luckily, WAL files are extremely compressible. I examined different programs to
find one that offered the best compression (as indicated by a smaller size)
at the smallest cost (as indicated by wall clock time). All of the methods tested worked
better than the venerable gzip program, which is suggested in the Postgres
documentation for the [archive_command option](https://www.postgresql.org/docs/9.6/static/continuous-archiving.html). The best overall solution was using the [pxz program](http://manpages.ubuntu.com/manpages/trusty/man1/pxz.1.html) inside the [archive_command setting](https://www.postgresql.org/docs/current/static/runtime-config-wal.html#GUC-ARCHIVE-COMMAND), followed closely by use of the [7za program](http://manpages.ubuntu.com/manpages/trusty/man1/7z.1.html). Use of the built-in [wal_compression](https://www.postgresql.org/docs/current/static/runtime-config-wal.html#GUC-WAL-COMPRESSION) option was an excellent solution as well, although not as
space-saving as using external programs via archive_command.

-----------

A database system is a complex beast, involving many trade-offs. An important issue is speed:
waiting for changes to get written to disk before letting the client proceed can be a
very expensive solution. Postgres gets around this with the use of the Write Ahead Log, which
generates WAL files indicating what changes were made. Creating these files is much faster than
performing the actual updates on the underlying files. Thus, Postgres is able to tell the client
that the work is “done” when the WAL file has been generated. Should the system crash before
the actual changes are made, the WAL files are used to replay the changes. As these
WAL files represent a continuous unbroken chain of all changes to the database, they can also
be used for Point in Time Recovery—​in other words, the WAL files can be used to rewind the database
to any single point in time, capturing the state of the database at a specific moment.

Postgres WAL files are exactly 16 MB in size (although this size may be changed at compilation time,
it is extremely unheard of to do this). These files primarily sit around taking up disk space
and are only accessed when a problem occurs, so being able to compress them is a good
one-time exchange of CPU effort for a lower file size. In theory, the time to decompress
the files should also be considered, but testing revealed that all the programs
decompressed so quickly that it should not be a factor.

WAL files can be compressed in one of two ways. As of Postgres 9.5, the wal_compression
feature can be enabled, which instructs Postgres to compress parts of the WAL file
in-place when possible, leading to the ability to store much more information per 16 MB WAL file,
and thus reducing the total number generated. The second way is to compress with an external
program via the free-form archive_command parameter. Here is the canonical example
from the Postgres docs, showing use of the gzip program for archive_command:

```
archive_command = 'gzip < %p > /var/lib/pgsql/archive/%f'
```

It is widely known that gzip is no longer the best compression option for most tasks,
so I endeavored to determine which program was the best at WAL file compression—​in terms
of final file size versus the overhead to create the file. I also wanted to examine how these
fared versus the new wal_compression feature.

-----------

To compare the various compression methods, I examined all of the compression programs that
are commonly available on a Linux system, are known to be stable, and which perform at least
as good as the common utility gzip. The contenders were:

- **gzip** — the canonical, default compression utility for many years
- **pigz** — parallel version of gzip
- **bzip2** — second only to gzip in popularity, it offers better compression
- **lbzip2** — parallel version of bzip
- **xz** — an excellent all-around compression alternative to gzip and bzip
- **pxz** — parallel version of xz
- **7za** — excellent compression, but suffers from complex arguments
- **lrzip** — compression program targeted at “large files”

For the tests, 100 random WAL files were copied from a busy production Postgres system. Each of
those 100 files were compressed nine times by each of the programs above: from the “least compressed”
option (e.g. -1) to the “best compressed” option (e.g. -9).
The tests were performed on a 16-core system, with plenty of free RAM and nothing else running on the server.
Results were gathered by wrapping
each command with /usr/bin/time -verbose, which produces a nice breakdown of results.
To gather the data, the “Elapsed (wall clock) time” was used, along with size of
the compressed file. Here is some sample output of the time command:

```text
  Command being timed: "bzip2 -4 ./0000000100008B91000000A5"
  User time (seconds): 1.65
  System time (seconds): 0.01
  Percent of CPU this job got: 99%
  Elapsed (wall clock) time (h:mm:ss or m:ss): 0:01.66
  Average shared text size (kbytes): 0
  Average unshared data size (kbytes): 0
  Average stack size (kbytes): 0
  Average total size (kbytes): 0
  Maximum resident set size (kbytes): 3612
  Average resident set size (kbytes): 0
  Major (requiring I/O) page faults: 0
  Minor (reclaiming a frame) page faults: 938
  Voluntary context switches: 1
  Involuntary context switches: 13
  Swaps: 0
  File system inputs: 0
  File system outputs: 6896
  Socket messages sent: 0
  Socket messages received: 0
  Signals delivered: 0
  Page size (bytes): 4096
  Exit status: 0
```

The wal_compression feature was tested by creating a new Postgres 9.6 cluster, then
running the [pgbench program](https://www.postgresql.org/docs/current/static/pgbench.html) twice to generate WAL files—​once with wal_compression enabled,
and once with it disabled. Then each of the resulting WAL files was compressed using each of the programs above.

-----------

<style><!--
table.gsmt { font-family: Monospace; padding: 0 0 3em 0; margin-left: auto; margin-right: auto; }
table.gsmt table td { padding: 0 0.5em 0 0.2em ; color: #222200; white-space: nowrap; font-size: smaller;}
table.gsmt table th { padding: 0em 0.5em 0em 0.5em; color: black; font-size: smaller; }
--></style>

<table border="0" class="gsmt" style="padding: 0 0 3em 0"><caption><b>Table 1.</b><br/>
Results of compressing 16 MB WAL files—​average for 100 files</caption>
<tbody><tr>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th></tr>
 <tr><td>gzip -1</td><td>0.271</td><td>4.927</td></tr>
 <tr><td>gzip -2</td><td>0.292</td><td>4.777</td></tr>
 <tr><td>gzip -3</td><td>0.366</td><td>4.667</td></tr>
 <tr><td>gzip -4</td><td>0.381</td><td>4.486</td></tr>
 <tr><td>gzip -5</td><td>0.492</td><td>4.318</td></tr>
 <tr><td>gzip -6</td><td>0.734</td><td>4.250</td></tr>
 <tr><td>gzip -7</td><td>0.991</td><td>4.235</td></tr>
 <tr><td>gzip -8</td><td>2.042</td><td>4.228</td></tr>
 <tr><td>gzip -9</td><td>3.626</td><td>4.227</td></tr>
</tbody></table></td>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th></tr>
 <tr><td>bzip2 -1</td><td>1.540</td><td>3.817</td></tr>
 <tr><td>bzip2 -2</td><td>1.531</td><td>3.688</td></tr>
 <tr><td>bzip2 -3</td><td>1.570</td><td>3.638</td></tr>
 <tr><td>bzip2 -4</td><td>1.625</td><td>3.592</td></tr>
 <tr><td>bzip2 -5</td><td>1.667</td><td>3.587</td></tr>
 <tr><td>bzip2 -6</td><td>1.707</td><td>3.566</td></tr>
 <tr><td>bzip2 -7</td><td>1.731</td><td>3.559</td></tr>
 <tr><td>bzip2 -8</td><td>1.752</td><td>3.557</td></tr>
 <tr><td>bzip2 -9</td><td>1.784</td><td>3.541</td></tr>
</tbody></table></td>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th></tr>
 <tr><td>xz -1</td><td>0.962</td><td>3.174</td></tr>
 <tr><td>xz -2</td><td>1.186</td><td>3.066</td></tr>
 <tr><td>xz -3</td><td>5.911</td><td>2.711</td></tr>
 <tr><td>xz -4</td><td>6.292</td><td>2.682</td></tr>
 <tr><td>xz -5</td><td>6.694</td><td>2.666</td></tr>
 <tr><td>xz -6</td><td>8.988</td><td>2.608</td></tr>
 <tr><td>xz -7</td><td>9.194</td><td>2.592</td></tr>
 <tr><td>xz -8</td><td>9.117</td><td>2.596</td></tr>
 <tr><td>xz -9</td><td>9.164</td><td>2.597</td></tr>
</tbody></table></td>
</tr>
</tbody></table>

<table border="0" class="gsmt"><caption><b>Table 2.</b><br/>
Results of compressing 16 MB WAL file—​average for 100 files</caption>
<tbody><tr>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th>
 </tr><tr><td>lrzip<br/> -l -L1</td><td>0.296</td><td>5.712</td></tr>
 <tr><td>lrzip<br/> -l -L2</td><td>0.319</td><td>5.686</td></tr>
 <tr><td>lrzip<br/> -l -L3</td><td>0.341</td><td>5.645</td></tr>
 <tr><td>lrzip<br/> -l -L4</td><td>0.370</td><td>5.639</td></tr>
 <tr><td>lrzip<br/> -l -L5</td><td>0.389</td><td>5.627</td></tr>
 <tr><td>lrzip<br/> -l -L6</td><td>0.901</td><td>5.501</td></tr>
 <tr><td>lrzip<br/> -l -L7</td><td>2.090</td><td>5.462</td></tr>
 <tr><td>lrzip<br/> -l -L8</td><td>2.829</td><td>5.471</td></tr>
 <tr><td>lrzip<br/> -l -L9</td><td>5.983</td><td>5.463</td></tr>
</tbody></table></td>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th></tr>
 <tr><td>lrzip<br/> -z -L1</td><td>3.582</td><td>3.353</td></tr>
 <tr><td>lrzip<br/> -z -L2</td><td>3.577</td><td>3.342</td></tr>
 <tr><td>lrzip<br/> -z -L3</td><td>3.601</td><td>3.326</td></tr>
 <tr><td>lrzip<br/> -z -L4</td><td>11.971</td><td>2.799</td></tr>
 <tr><td>lrzip<br/> -z -L5</td><td>11.890</td><td>2.741</td></tr>
 <tr><td>lrzip<br/> -z -L6</td><td>11.971</td><td>2.751</td></tr>
 <tr><td>lrzip<br/> -z -L7</td><td>12.861</td><td>2.750</td></tr>
 <tr><td>lrzip<br/> -z -L8</td><td>30.080</td><td>2.483</td></tr>
 <tr><td>lrzip<br/> -z -L9</td><td>33.171</td><td>2.482</td></tr>
</tbody></table></td>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th></tr>
 <tr><td>7za -bd -mx=1<br/> a test.7za</td><td>0.128</td><td>3.182</td></tr>
 <tr><td>7za -bd -mx=2<br/> a test.7za</td><td>0.139</td><td>3.116</td></tr>
 <tr><td>7za -bd -mx=3<br/> a test.7za</td><td>0.301</td><td>3.059</td></tr>
 <tr><td>7za -bd -mx=4<br/> a test.7za</td><td>1.251</td><td>3.001</td></tr>
 <tr><td>7za -bd -mx=5<br/> a test.7za</td><td>3.821</td><td>2.620</td></tr>
 <tr><td>7za -bd -mx=6<br/> a test.7za</td><td>3.841</td><td>2.629</td></tr>
 <tr><td>7za -bd -mx=7<br/> a test.7za</td><td>4.631</td><td>2.591</td></tr>
 <tr><td>7za -bd -mx=8<br/> a test.7za</td><td>4.671</td><td>2.590</td></tr>
 <tr><td>7za -bd -mx=9<br/> a test.7za</td><td>4.663</td><td>2.599</td></tr>
</tbody></table></td></tr>
</tbody></table>

<table border="0" class="gsmt"><caption><b>Table 3.</b><br/>
Results of compressing 16 MB WAL file—​average for 100 files</caption>
<tbody><tr>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th></tr>
 <tr><td>pigz -1</td><td>0.051</td><td>4.904</td></tr>
 <tr><td>pigz -2</td><td>0.051</td><td>4.755</td></tr>
 <tr><td>pigz -3</td><td>0.051</td><td>4.645</td></tr>
 <tr><td>pigz -4</td><td>0.051</td><td>4.472</td></tr>
 <tr><td>pigz -5</td><td>0.051</td><td>4.304</td></tr>
 <tr><td>pigz -6</td><td>0.060</td><td>4.255</td></tr>
 <tr><td>pigz -7</td><td>0.081</td><td>4.225</td></tr>
 <tr><td>pigz -8</td><td>0.140</td><td>4.212</td></tr>
 <tr><td>pigz -9</td><td>0.251</td><td>4.214</td></tr>
</tbody></table></td>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th></tr>
 <tr><td>lbzip2 -1</td><td>0.135</td><td>3.801</td></tr>
 <tr><td>lbzip2 -2</td><td>0.151</td><td>3.664</td></tr>
 <tr><td>lbzip2 -3</td><td>0.151</td><td>3.615</td></tr>
 <tr><td>lbzip2 -4</td><td>0.151</td><td>3.586</td></tr>
 <tr><td>lbzip2 -5</td><td>0.151</td><td>3.562</td></tr>
 <tr><td>lbzip2 -6</td><td>0.151</td><td>3.545</td></tr>
 <tr><td>lbzip2 -7</td><td>0.150</td><td>3.538</td></tr>
 <tr><td>lbzip2 -8</td><td>0.151</td><td>3.524</td></tr>
 <tr><td>lbzip2 -9</td><td>0.150</td><td>3.528</td></tr>
</tbody></table></td>
<td><table border="1">
<tbody><tr><th>Command</th><th>Wall clock time (s)</th><th>File size (MB)</th></tr>
 <tr><td>pxz -1</td><td>0.135</td><td>3.266</td></tr>
 <tr><td>pxz -2</td><td>0.175</td><td>3.095</td></tr>
 <tr><td>pxz -3</td><td>1.244</td><td>2.746</td></tr>
 <tr><td>pxz -4</td><td>2.528</td><td>2.704</td></tr>
 <tr><td>pxz -5</td><td>5.115</td><td>2.679</td></tr>
 <tr><td>pxz -6</td><td>9.116</td><td>2.604</td></tr>
 <tr><td>pxz -7</td><td>9.255</td><td>2.599</td></tr>
 <tr><td>pxz -8</td><td>9.267</td><td>2.595</td></tr>
 <tr><td>pxz -9</td><td>9.355</td><td>2.591</td></tr>
</tbody></table></td></tr>
</tbody></table>

<table border="0" class="gsmt"><caption><b>Table 4.</b><br/>Results of Postgres wal_compression option</caption>
<tbody><tr>
<td><table border="1">
<tbody><tr><th>Modifications</th><th>Total size of WAL files (MB)</th></tr>
<tr><td>No modifications</td><td>208.1</td></tr>
<tr><td>wal_compression enabled</td><td>81.0</td></tr>
<tr><td>xz -2</td><td>8.6</td></tr>
<tr><td>wal_compression enabled PLUS xz -2</td><td>9.4</td></tr>
</tbody></table>
</td></tr></tbody></table>

-----------

Table 1 shows some baseline compression values for the three popular programs
gzip, bzip2, and xz. Both gzip and bzip2 show little change in the file sizes as the
compression strength is raised. However, xz has a relatively large jump when going
from -2 to -3, although the time cost increases to an unacceptable 5.9 seconds. As a starting
point, something well under one second is desired.

Among those three, xz is the clear winner, shrinking the file to 3.07 MB with a compression
argument of -2, and taking 1.2 seconds to do so. Both gzip and bzip2 never even reach this
file size, even when using a -9 argument. For that matter, the best compression gzip can
ever achieve is 4.23 MB, which the other programs can beat without breakng a sweat.

Table 2 demonstrates two ways of invoking the lrzip program: the -l option (lzo compression -
described in the lrzip documentation as “ultra fast”) and the -z option (zpaq compression -
“extreme compression, extreme slow”). All of those superlatives are supported by the data. The -l
option runs extremely fast: even at -L5 the total clock time is still only .39 seconds. Unfortunately,
the file size hovers around an undesirable 5.5 MB, no matter what compression level is used. The -z
option produces the smallest file of all the programs here (2.48 MB) at a whopping cost of over 30
seconds! Even the smallest compression level (-L1) takes 3.5 seconds to produce a 3.4 MB file. Thus,
lrzip is clearly out of the competition.

<div class="separator" style="clear: both; text-align: center; padding-bottom:1em;"><a href="/blog/2017/03/postgres-wal-files-best-compression/image-1.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" id="jA0EBAMCQV4Upc7MVzZgycARvnUd7ZPBWXA9iXj+1nagDqP0bIKB3vspSuKJKLudmKh2tPgjwLFfxFkN34sgCWCeyYnxTt/zDAR3GpmBoiPQbMmxJO2QBdjcFr6e3R5/tMNH5MsIQklNNOM/EBtZid0PshHrOEooRj4xhSO74FtVZiXNR/hx0tr1QdPHs8XS5qWaKCG4PG69JN/k74CevdILYAAdhENPNZV48aOJwZq5D2A3+65ZYcNWfBXpHrnecboKT607iQUBC7zUnzqPCl31RVmQ0EmRX7zElgin3B3jwho==9+3U" src="/blog/2017/03/postgres-wal-files-best-compression/image-1.jpeg"/></a><br/>Compression in action <small>(<a href="https://flic.kr/p/9sgf6f">photo</a> by <a href="https://www.flickr.com/people/familymwr/?rb=1">Eric Armstrong</a>)</small></div>

The most interesting program is without a doubt 7za. Unlike the others, it is organized around
creating archives, and thus doesn’t do in-place compression as the others do. Nevertheless,
the results are quite good. At the lowest level, it takes a mere 0.13 seconds to produce a
3.18 MB file. As it takes xz 1.19 seconds to produce a nearly equivalent 3.10 MB file, 7za
is the clear winner ... if we had only a single core available. :)

It is rare to find a modern server with a single processor, and a crop of compression programs have
appeared to support this new paradigm. First up is the amazing pigz, which is a parallel
version of gzip. As Table 3 shows, pigz is extraordinarily fast on our 16 core box, taking
a mere 0.05 seconds to run at compression level -1, and only 0.25 seconds to run at
compression level -9. Sadly, it still suffers from the fact that gzip is simply not good
at compressing WAL files, as the smallest size was 4.23 MB. This rules out pigz from
consideration.

The bzip2 program has been nipping at the heels of gzip for many years, so naturally it
has its own parallel version, known as lbzip2. As Table 3 shows, it is also amazingly fast.
Not as fast as pigz, but with a speed of under 0.2 seconds—​even at the highest compression level!
There is very little variation among the compression levels used, so it is fair to simply state
that lbzip2 takes 0.15 seconds to shrink the WAL file to 3.5 MB. A decent entry.

Of course, the xz program has a parallel version as well, known as pxz. Table 3 shows that
the times still vary quite a bit, and reach into the 9 second range at higher compression levels,
but does very well at -2, taking a mere 0.17 seconds to produce a 3.09 MB file. This is
comparable to the previous winner, 7za, which took 0.14 seconds to create a 3.12 MB
file.

So the clear winners are 7za and pxz. I gave the edge to pxz, as (1) the file size was
slightly smaller at comparable time costs, and (2) the odd syntax for 7za for both compressing
and decompressing was annoying compared with the simplicity of “xz -2” and “xz -d”.

Now, what about the built-in compression offered by the wal_compression option?
As Table 4 shows, the compression for the WAL files I tested went from 208 MB to
81 MB. This is a significant gain, but only equates to compressing a single WAL
file to 6.23 MB, which is a poor showing when compared to the compression programs above.
It should be pointed out that the wal_compression option is sensitive to
your workload, so you might see reports of greater and lesser compressions.

Of interest is that the WAL files generated by turning on wal_compression are
capable of being further compressed by the archive_command option, and doing
a pretty good job of it as well—​going from 81 MB of WAL files to 9.4 MB of
WAL files. However, using just xz in the archive_command without wal_compression
on still yielded a smaller overall size, and means less CPU because the data is only
compressed once.

It should be pointed out that wal_compression has other advantages, and that
comparing it to archive_command is not a fair comparison, but this article was
primarily about the best compression option for storing WAL files long-term.

Thus, the overall winner is “pxz -2”, followed closely by 7za and its bulky
arguments, with honorable mention given to wal_compression. Your particular
requirements might guide you to another conclusion, but hopefully nobody shall
simply default to using gzip anymore.

-----------

Thanks to my colleague Lele for encouraging me to try pxz, after I was already happy with xz. Thanks to the authors of xz, for providing an amazing program that has an incredible number of knobs for tweaking. And a final thanks to the authors of the wal_compression feature, which is a pretty nifty trick!
