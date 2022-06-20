---
author: Josh Tolley
title: Bucardo, and Coping with Unicode
github_issue_number: 944
tags:
- bucardo
- perl
- postgres
- replication
- unicode
date: 2014-03-12
---

Given the [recent DBD::Pg 3.0.0 release](/blog/2014/02/dbdpg-utf-8-perl-postgresql/), with its improved Unicode support, it seemed like a good time to work on a [Bucardo bug](https://github.com/bucardo/bucardo/issues/47) we’ve wanted fixed for a while. Although [Bucardo](https://bucardo.org) will replicate Unicode data without a problem, it runs into difficulties when table or column in the database include non-ASCII characters. Teaching Bucardo to handle Unicode data has been an interesting exercise.

Without information about its encoding, string data at its heart is meaningless. Programs that exchange string information without paying attention to the encoding end up with problems exactly like that described in the bug, with nonsense characters all over. Further, it’s impossible even to compare two different strings reliably. So not only would Bucardo’s logs and program output contain junk data, Bucardo would simply fail to find database objects that clearly existed, because it would end up querying for the wrong object name, or the keys of the hashes it uses internally would be meaningless. Even communication between different Bucardo processes needs to be decoded correctly. The recent DBD::Pg 3.0.0 release takes care of decoding strings sent from PostgreSQL, but other inputs, such as command-line arguments, must be treated individually. All output handles, such as STDOUT, STDERR, and the log file output, must be told to expect data in a particular encoding to ensure their output is handled correctly.

The first step is to build a test case. Bucardo’s test suite is quite comprehensive, and easy to use. For starters, I’ll make a simple test that just creates a table, and tries to tell Bucardo about it. The test suite will already create databases and install Bucardo for me; I can talk to those databases with handles $dbhA and $dbhB. Note that in this case, although the table and primary key names contain non-ASCII characters, the relgroup and sync names do not. That will require further programming. The character in the primary key name, incidentally, is a [staff of Aesculapius](https://en.wikipedia.org/wiki/Rod_of_Asclepius), which I don’t recommend people include in the name of a typical primary key.

```perl
for my $dbh (($dbhA, $dbhB)) {
    $dbh->do(qq/CREATE TABLE test_büçárđo ( pkey_\x{2695} INTEGER PRIMARY KEY, data TEXT );/);
    $dbh->commit;
}

like $bct->ctl('bucardo add table test_büçárđo db=A relgroup=unicode'),
    qr/Added the following tables/, "Added table in db A";
like($bct->ctl("bucardo add sync test_unicode relgroup=unicode dbs=A:source,B:target"),
    qr/Added sync "test_unicode"/, "Create sync from A to B")
    or BAIL_OUT "Failed to add test_unicode sync";
```

Having created database objects and configured Bucardo, the next part of the test starts Bucardo, inserts some data into the master database “A”, and tries to replicate it:

```perl
$dbhA->do("INSERT INTO test_büçárđo (pkey_\x{2695}, data) VALUES (1, 'Something')");
$dbhA->commit;

## Get Bucardo going
$bct->restart_bucardo($dbhX);

## Kick off the sync.
my $timer_regex = qr/\[0\s*s\]\s+(?:[\b]{6}\[\d+\s*s\]\s+)*/;
like $bct->ctl('kick sync test_unicode 0'),
    qr/^Kick\s+test_unicode:\s+${timer_regex}DONE!/,
    'Kick test_unicode' or die 'Sync failed, no point continuing';

my $res = $dbhB->selectall_arrayref('SELECT * FROM test_büçárđo');
ok($#$res == 0 && $res->[0][0] == 1 && $res->[0][1] eq 'Something', 'Replication worked');
```

Given that DBD::Pg handles the encodings for strings from the database, I only need to make a few other changes. I added a few lines to the preamble of some files, to deal with UTF8 elements in the code itself, and to tell input and output pipes to expect UTF8 data.

```perl
use utf8;
use open qw( :std :utf8 );
```

In some cases, I also had to add a couple more modules, and explicitly decode incoming values. For instance, the test suite repeatedly runs shell commands to configure and manage test instances of Bucardo. There, too, the output needs to be decoded correctly:

```perl
    debug("Script: $ctl Connection options: $connopts Args: $args", 3);
-   $info = qx{$ctl $connopts $args 2>&1};
+   $info = decode( locale => qx{$ctl $connopts $args 2>&1} );
    debug("Exit value: $?", 3);
```

And with that, now Bucardo accepts non-ASCII table names.

```plain
[~/devel/bucardo]$ prove t/10-object-names.t 
t/10-object-names.t .. ok     
All tests successful.
Files=1, Tests=20, 24 wallclock secs ( 0.01 usr  0.01 sys +  2.01 cusr  0.22 csys =  2.25 CPU)
Result: PASS
```
