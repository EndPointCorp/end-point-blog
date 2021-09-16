---
author: Greg Sabino Mullane
title: Finding the PostgreSQL version — without logging in!
github_issue_number: 306
tags:
- database
- postgres
- security
date: 2010-05-17
---

<a href="/blog/2010/05/finding-postgresql-version-without/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5472376552703238962" src="/blog/2010/05/finding-postgresql-version-without/image-0.jpeg" style="margin: 0pt 0pt 10px 10px; float: right; cursor: pointer; width: 180px; height: 239px;"/></a>

Metasploit used the error messages given by a PostgreSQL server to find out the version without actually having to log in and issue a “SELECT version()” command. The original article is at [http://blog.metasploit.com/2010/02/postgres-fingerprinting.html](https://web.archive.org/web/20100619074143/http://blog.metasploit.com/2010/02/postgres-fingerprinting.html) and is worth a read. I’ll wait.

The basic idea is that because version 3 of the Postgres protocol gives you the file and the line number in which the error is generated, you can use the information to figure out what version of Postgres is running, as the line numbers change from version to version. In effect, each version of Postgres reveals enough in its error message to fingerprint it. This was a neat little trick, and I wanted to explore it more myself. The first step was to write a quick Perl script to connect and get the error string out. The original Metasploit script focuses on failed login attempts, but after some experimenting I found an easier way was to send an invalid protocol number (Postgres expects “2.0” or “3.0”). Sending a startup packet with an invalid protocol of “3.1” gave me back the following string:

```perl
E|SFATALC0A000Munsupported frontend protocol 3.1:
server supports 1.0 to 3.0Fpostmaster.cL1507RProcessStartupPacket
```

The important part of the string was the parts indicating the file and line number:

```perl
Fpostmaster.cL1507
```

In this case, we can clearly see that line 1507 of postmaster.c was throwing the error. After firing up a few more versions of Postgres and recording the line numbers, I found that all versions since 7.3 were hitting the same chunk of code from postmaster.c:

```nohighlight
/* Check we can handle the protocol the frontend is using. */

if (PG_PROTOCOL_MAJOR(proto) <> PG_PROTOCOL_MAJOR(PG_PROTOCOL_LATEST) ||
  (PG_PROTOCOL_MAJOR(proto) == PG_PROTOCOL_MAJOR(PG_PROTOCOL_LATEST) &&
   PG_PROTOCOL_MINOR(proto) > PG_PROTOCOL_MINOR(PG_PROTOCOL_LATEST)))
  ereport(FATAL,
  (errcode(ERRCODE_FEATURE_NOT_SUPPORTED),
    errmsg("unsupported frontend protocol %u.%u: server supports %u.0 to %u.%u",
      PG_PROTOCOL_MAJOR(proto), PG_PROTOCOL_MINOR(proto),
      PG_PROTOCOL_MAJOR(PG_PROTOCOL_EARLIEST),
      PG_PROTOCOL_MAJOR(PG_PROTOCOL_LATEST),
      PG_PROTOCOL_MINOR(PG_PROTOCOL_LATEST))));
```

Line numbers were definitely different across major versions of Postgres (e.g. 8.2 vs. 8.3), and were even different sometimes across revisions. Rather than fire up every possible revision of Postgres and run my program against it, I simply took advantage of the cvs tags (aka symbolic names) and did this:

```bash
cvs update -rREL8_3_0 -p postmaster.c | grep -Fn 'LATEST))))'
```

This showed me that the string occurred on line 1497 of postmaster.c. I created a Postgres instance and verified that the line number was the same. At that point, it was a simple matter of making a bash script to grab all releases since 7.3 and build up a comprehensive list of when that line changed from version to version.

Once that was done, I rolled the whole thing up into a new Perl script called “detect_postgres_version.pl”. Here’s the script, broken into pieces for explanation. A link to the entire script is at the bottom of the post.

First, we do some standard Perl script things and read in the __DATA__ section at the bottom of the script, which lists at which version the message has changed:

```perl
#!/usr/bin/env perl

## Quickly and roughly determine what version of Postgres is running
## greg@endpoint.com

use strict;
use warnings;
use IO::Socket;
use Data::Dumper;
use Getopt::Long;

## __DATA__ looks like this: filname / line / version when it changed
## postmaster.c 1287 7.4.0
## postmaster.c 1293 7.4.2
## postmaster.c 1293 7.4.29
##
## postmaster.c 1408 8.0.0
## postmaster.c 1431 8.0.2

## Build our hash of file-and-line to version matches
my %map;
my ($last,$lastmin,$lastline) = ('',0,0);
while (<data>) {
   next if $_ !~ /(\w\S+)\s+(\d+)\s+(.+)/;
   my ($file,$line,$version) = ($1,$2,$3);
   die if $version !~ /(\d+)\.(\d+)\.(\d+)/;
   my ($vmaj,$vmin,$vrev) = ($1,$2,$3);
   my $current = "$file|$vmaj|$vmin";
   if ($current eq $last) {
       my ($lfile,$lmaj,$lmin) = split /\|/ => $last;
       for (my $x = $lastmin+1 ; $x<$vrev; $x++) {
           push @{$map{$file}{$lastline}}
             => ["$lmaj.$lmin","$lmaj.$lmin.$x"];
       }
   }
   push @{$map{$file}{$line}} => ["$vmaj.$vmin",$version];
   $last = $current;
   $lastmin = $vrev;
   $lastline = $line;
}
</data>
```

Next, we allow a few options to the script: port and host. We’ll default to a Unix socket if the host is not set, and default to port 5432 if none is given:

```perl
## Read in user options and set defaults
my %opt;
GetOptions(\%opt,
          'port=i',
          'host=s',
);

my $port = $opt{port} || 5432;
my $host = $opt{host} || '';
```

We’re ready to connect, using the very standard IO::Socket module. If the host starts with a slash, we assume this is the unix_socket_directory and replace the default ‘/tmp’ location:

```perl
## Start the connection, either unix or tcp
my $server;
if (!$host or !index $host, '/') {
   my $path = $host || '/tmp';
   $server = IO::Socket::UNIX->new(
       Type => IO::Socket::SOCK_STREAM,
       Peer => "$path/.s.PGSQL.$port",
   ) or die "Could not connect!: $@";
}
else {
   $server = IO::Socket::INET->new(
       PeerAddr => $host,
       PeerPort => $port,
       Proto    => 'tcp',
       Timeout  => 3,
   ) or warn "Could not connect!: $@";
}
```

Now we’re ready to actually send something over our new socket. Postgres expects the startup packet to be in a certain format. We’ll follow that format, but send it an invalid protocol number, 3.1. The rest of the information does not really matter, but we’ll also tell it we’re connecting as user “pg”. Finally, we read back in the message, extract the file and line number, and spit them back out to the user:

```perl
## Build and sent the packet
my $packet = pack('nn', 3,1) . "user\0pg\0\0";
$packet = pack('N', length($packet) + 4). $packet;
$server->send($packet, 0);

## Get the message back and extract the filename and line number
my $msg;
recv $server, $msg, 1000, 0;
if ($msg !~ /F([\w\.]+)\0L(\d+)/) {
   die "Could not find a file and line from error message: $msg\n";
}

my ($file,$line) = ($1,$2);

print "File: $file Line: $line\n";
```

Finally, we try to map the file name and line number we received back to the version of PostgreSQL it came from. If the file is not recognized, or the line number is not known, we bail out early:

```perl
$map{$file}
   or die qq{Sorry, I do not know anything about the file "$file"\n};

$map{$file}{$line}
   or die qq{Sorry, I do not know anything about line $line of file "$file"\n};

```

If there is only one result for this line and file number, we can state what it is and exit.

```perl
my $result = $map{$file}{$line};

if (1 == @$result) {
   print "Most likely Postgres version $result->[0][1]\n";
   exit;
}
```

In most cases, though, we don’t know the exact version down to the revision after the second dot, so we’ll state what the major version is, and all the possible revisions:

```perl
## Walk through and figure out which versions it may be.
## For now, we know that the major version does not overlap
print "Most likely Postgres version $result->[0][0]\n";
print "Specifically, one of these:\n";

for my $row (@$result) {
   print "  Postgres version $row->[1]\n";
}

exit;
```

The only thing left is the DATA section, which I’ll show here to be complete:

```nohighlight
__DATA__

## Format: filename line version

postmaster.c 1167 7.3.0
postmaster.c 1167 7.3.21

postmaster.c 1287 7.4.0
postmaster.c 1293 7.4.2
postmaster.c 1293 7.4.29

postmaster.c 1408 8.0.0
postmaster.c 1431 8.0.2
postmaster.c 1441 8.0.5
postmaster.c 1445 8.0.6
postmaster.c 1439 8.0.7
postmaster.c 1443 8.0.9
postmaster.c 1445 8.0.14
postmaster.c 1445 8.0.25

postmaster.c 1449 8.1.0
postmaster.c 1450 8.1.1
postmaster.c 1454 8.1.2
postmaster.c 1448 8.1.3
postmaster.c 1452 8.1.4
postmaster.c 1448 8.1.9
postmaster.c 1454 8.1.10
postmaster.c 1454 8.1.21

postmaster.c 1432 8.2.0
postmaster.c 1437 8.2.1
postmaster.c 1440 8.2.5
postmaster.c 1432 8.2.17

postmaster.c 1497 8.3.0
postmaster.c 1507 8.3.8
postmaster.c 1507 8.3.11

postmaster.c 1570 8.4.0
postmaster.c 1621 8.4.1
postmaster.c 1621 8.4.4

postmaster.c 1664 9.0.0
```

(Because version 9.0 is not released yet, its line number may still change.)

I found this particular protocol error to be a good one because there is no overlap of line numbers across major versions. Of the approximately 125 different versions released since 7.3.0, only 6 are unique enough to identify to the exact revision. That’s okay for this iteration of the script. If you wanted to know the exact revision, you could try other errors, such as an invalid login, as the metasploit code does.

The complete code can be read here: [detect_postgres_version.pl](http://gtsm.com/detect_postgres_version.pl)

I’ll be giving [a talk](http://www.pgcon.org/2010/schedule/events/238.en.html) later on this week at [PgCon 2010](http://www.pgcon.org/2010/), so say hi if you see me there. I’ll probably be giving a [lightning talk](http://www.pgcon.org/2010/schedule/events/267.en.html) as well.
