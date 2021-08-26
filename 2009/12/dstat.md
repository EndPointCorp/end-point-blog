---
author: Jon Jensen
title: 'dstat: better system resource monitoring'
github_issue_number: 239
tags:
- environment
- hosting
- monitoring
- redhat
date: 2009-12-19
---



I recently came across a useful tool I hadn’t heard of before: [dstat](http://dag.wiee.rs/home-made/dstat/), by Dag Wieers (of DAG RPM-building fame). He describes it as “a versatile replacement for vmstat, iostat, netstat, nfsstat and ifstat.”

The most immediate benefit I found is the collation of system resource monitoring output at each point in time, removing the need to look at output from multiple monitors. The coloring helps readability too:

% dstat                                                                         

----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system--         

usr sys idl wai hiq siq| read  writ| recv  send|  in   out | int   csw          

  4   1  92   3   0   0|  56k   84k|   0     0 |  94B  188B|1264  1369          

  3   7  43  44   1   1| 368k   11M| 151B  222B|   0   260k|1453  1565          

  3   2  46  48   1   0| 432k 5784k|   0     0 |   0     0 |1421  1584          

  2   2  47  49   0   0| 592k    0 |   0     0 |   0     0 |1513  1763          

  6   2  44  49   1   0| 448k  248k|   0     0 |   0     0 |1398  1640          

  8   4  41  45   3   0| 456k    0 | 135B  222B|   0     0 |1530  2102          

 18   4  38  41   0   0| 408k  128k|   0    47B|   0     0 |1261  1977          

 10   4  44  43   0   0| 728k  208k|   0     0 |   0     0 |1445  2203          

  6   3  39  51   0   0| 648k  256k|3607B 4124B|   0     0 |1496  2180          

  7   7  34  53   0   0|1088k    0 |1234B  582B|   0     0 |1465  2057          

 14   8  28  49   0   0|2856k  104k|   0     0 |   0    52k|1610  2995          

  6   6  43  45   0   0|1992k    0 |5964B 4836B|   0     0 |1493  2391          

  9  14  34  44   0   0|2432k  112k|7854B  726B|   0     0 |1527  2190          

  9  11  40  41   1   0|2680k    0 |1382B  972B|   0     0 |1550  2298          

  5   4  68  22   0   0| 576k 1096k|  12k 4628B|   0     0 |1522  1731 ^C       

(Textual screenshot by script of [util-linux](https://github.com/karelzak/util-linux) and Perl module [HTML::FromANSI](http://search.cpan.org/perldoc?HTML::FromANSI).)

Its default one-line-per-timeslice output makes it good for collecting data samples over time, as opposed to full-screen top-like utilities such as [atop](https://www.atoptool.nl/), which give much more detailed information at each snapshot, but don’t show history.

Since dstat is a standard package available in RHEL/CentOS and Debian/Ubuntu, it is a reasonably easy add-on to get on various systems.

dstat also allows plugins, and just in the most recent release last month were added new plugins “for showing NTP time, power usage, fan speed, remaining battery time, memcache hits and misses, process count, top process total and average latency, top process total and average CPU timeslice, and per disk utilization rates.”

It sounds like it’ll grow even more useful over time and is worth keeping an eye on.


