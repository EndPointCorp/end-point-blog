---
author: Greg Sabino Mullane
gh_issue_number: 1130
tags: database, perl, postgres
title: Postgres "unsupported frontend protocol" mystery
---



<div class="separator" style="clear: both; float: right; text-align: center; padding-left: 4em;"><a href="/blog/2015/05/28/postgres-unsupported-frontend-protocol/image-0-big.png" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/05/28/postgres-unsupported-frontend-protocol/image-0.png"/></a><br/><small>"<a href="https://flic.kr/p/bWd997">Koala Portrait</a>" by <a href="https://www.flickr.com/photos/bareego/">James Niland</a></small></div>

The wonderful [tail_n_mail program](https://bucardo.org/wiki/Tail_n_mail) continues to provide me with new mysteries from our [Postgres](http://www.postgresql.org/) clients. One of the main functions it provides is to send an immediate email to us when an unexpected FATAL (or ERROR or PANIC) message appears in the Postgres logs. While these are often simple application errors, or deeper problems such as running out of disk space, once in a blue moon you see something completely unexpected. Some time  ago, I saw a bunch of these messages appear in an email from a tail_n_mail email:

```
[1] From files A to B Count: 2
First: [A] 2015-12-01T06:30:00 server1 postgres[1948]
Last:  [B] 2015-12-01T06:30:00 server2 postgres[29107]
FATAL: unsupported frontend protocol 65363.19778: server supports 1.0 to 3.0
```

I knew what caused this error in general, but decided to get to the bottom of the 
problem. Before we go into the specific error, let's review what causes this 
particular message to appear. When a Postgres client (such as psql or [DBD::Pg](https://metacpan.org/pod/DBD::Pg)) 
connects to Postgres, the first thing it does is to issue a [startup message](http://www.postgresql.org/docs/current/static/protocol-flow.html). 
One of the things included in this request is the 
version of the Postgres protocol the client wishes to use. Since 
[2003](https://bucardo.org/postgres_all_versions.html#version_7.4), 
Postgres servers have been using version 3.1. It is very rare to see a client 
or server that uses anything else. Because this protocol number request occurs 
at the very start of the connection request, non-Postgres programs often 
trigger this error, because the server is expecting a number at the start of 
the request.

We can verify this by use of a small [Perl](http://www.perl.org/) script that connects to the server, 
and sends an invalid protocol request:

```
#!/usr/bin/env perl

use strict;
use warnings;
use IO::Socket;

my $server = IO::Socket::UNIX->new('/tmp/.s.PGSQL.5432')
  or die "Could not connect!: $@";

my $packet = pack('nn', 1234,56789) . "user\0pg\0\0";
$packet = pack('N', length($packet) + 4). $packet;
$server->send($packet, 0);
```

After running the above program, a new error pops up in the Postgres logs as 
expected:

```
$ tail -1 /var/lib/pgsql/data/pg_log/postgres-2015-05-20.log
2015-05-21 12:00:00 EDT [unknown]@[unknown] [10281] FATAL:  unsupported frontend protocol 1234.56789: server supports 1.0 to 3.0
```

There is our error, as expected. The "unknown"s are because my log_line_prefix looks like this: **%t %u@%d [%p]**. While the timestamp (%t) and the process ID (%p) are easily filled in, the login failed, so both the user (%u) and database (%d) are still unknown.

Now on to our specific error, which you will recall is "unsupported frontend protocol 65363.19778". 
The above program shows that the protocol number is sent in a specific format. Let's use Perl to display the 
numbers 65363.19778 and see if there are any clues buried within it:

```
$ perl -e 'print pack "nn", 65363,19778'
�SMB
```

Some sort of unprintable character in there; let's take a deeper look just for 
completeness:

```
$ perl -e 'print pack "nn", 65363,19778' | hd
00000000  ff 53 4d 42                                       |.SMB|
00000004
```

Aha! **SMB** is not just a random placement of three letters, it is a big clue as to what is 
causing this message. SMB stands for [Server Message Block](https://en.wikipedia.org/wiki/Server_Message_Block), and is used by a variety of things. We can guess that this is either some program randomly hitting 
the Postgres port without realizing what it is, or some sort of purposeful port scanner. Why would something 
want to connect to the port but not log in? For one, you can [determine the version of Postgres 
without logging in](/blog/2010/05/17/finding-postgresql-version-without).

To cut to the chase, the culprit is the [nmap](http://nmap.org/) program. In addition to simply 
scanning ports, it has the ability to do a [deeper inspection](http://nmap.org/book/man-version-detection.html) to determine not only what is running on each port, but what version it is as well (with the "**-sV**" argument). Let's see nmap in action. We will use a non-standard Postgres port so as not to give it any additional hints about what is on that port:

```
$ nmap -p 5930 localhost -sV
Starting Nmap 6.40 ( http://nmap.org ) at 2015-05-20 12:00 EDT
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000088s latency).
PORT     STATE SERVICE    VERSION
5930/tcp open  postgresql PostgreSQL DB
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at http://www.insecure.org/cgi-bin/servicefp-submit.cgi :
SF-Port5930-TCP:V=6.40%I=7%D=5/21%Time=504C5445%P=i686-pc-linux-emu%r(Kerb
SF:eros,85,"E\0\0\0\x84SFATAL\0C0A000\0Munsupported\x20frontend\x20protoco
SF:l\x2027265\.28208:\x20server\x20supports\x201\.0\x20to\x203\.0\0Fpostma
SF:ster\.c\0L1834\0RProcessStartupPacket\0\0")%r(SMBProgNeg,85,"E\0\0\0\x8
SF:4SFATAL\0C0A000\0Munsupported\x20frontend\x20protocol\x2065363\.19778:\
SF:x20server\x20supports\x201\.0\x20to\x203\.0\0Fpostmaster\.c\0L1834\0RPr
SF:ocessStartupPacket\0\0");

Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.73 seconds
```

It looks like it triggered the "unsupported protocol" message, based on what 
was returned. Taking a peek at the Postgres 9.3 logs shows our mystery message:

```
$ tail -1 /var/lib/pgsql/pg9.3/pg_log/postgres-2015-05-20.log
2015-05-21 12:00:00 EDT [unknown]@[unknown] [2318] FATAL:  unsupported frontend protocol 65363.19778: server supports 1.0 to 3.0
```

As a final check, let's confirm that nmap is using SMB when it runs the version check:

```
$ nmap localhost -p 5930 -sV --version-trace 2>/dev/null | grep SMB
Service scan sending probe SMBProgNeg to 127.0.0.1:5930 (tcp)
Service scan match (Probe SMBProgNeg matched with SMBProgNeg line 10662): 127.0.0.1:5930 is postgresql.  Version: |PostgreSQL DB|||
SF:ster\.c\0L1834\0RProcessStartupPacket\0\0")%r(SMBProgNeg,85,"E\0\0\0\x8
```

Bingo. Mystery solved. If you see that error in your logs, it is most likely caused by someone running nmap 
in version detection mode.


