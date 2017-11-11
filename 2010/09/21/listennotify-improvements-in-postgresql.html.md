---
author: Greg Sabino Mullane
gh_issue_number: 351
tags: database, open-source, postgres
title: Listen/Notify improvements in PostgreSQL 9.0
---



Improved listen/notify is one of the new features of Postgres 9.0 I've been waiting for a long time. There are basically two major changes: everything is in shared memory instead of using system tables, and full support for "payload" messages is enabled.

Before I demonstrate the changes, here's a review of what exactly the listen/notify system in Postgres is. Basically, it is an inter-process signalling system, which uses the pg_listener system table to coordinate simple named events between processes. One or more clients connects to the database and issues a command such as:

```sql
LISTEN foobar;
```

The name **foobar** can be replaced by any valid name; usually the name is something that gives a contextual clue to the listening process, such as the name of a table. Another client (or even one of the original ones) will then issue a notification like so:

```sql
NOTIFY foobar;
```

Each client that is listening for the 'foobar' message will receive a notification that the sender has issued the NOTIFY. It also receives the PID of the sending process. Multiple notifications are collapsed into a single notice, and the notification is not sent until a transaction is committed.

Here's some sample code using DBD::Pg that demonstrates how the system works:

```perl
#!/usr/bin/env perl
# -*-mode:cperl; indent-tabs-mode: nil-*-

use strict;
use warnings;
use DBI;

my $dsn = 'dbi:Pg:dbname=test';
my $dbh1 = DBI-&gt;connect($dsn,'test','', {AutoCommit=&gt;0,RaiseError=&gt;1,PrintError=&gt;0});
my $dbh2 = DBI-&gt;connect($dsn,'test','', {AutoCommit=&gt;0,RaiseError=&gt;1,PrintError=&gt;0});

print "Postgres version is $dbh1-&gt;{pg_server_version}\n";

my $SQL = 'SELECT pg_backend_pid(), version()';
my $pid1 = $dbh1-&gt;selectall_arrayref($SQL)-&gt;[0][0];
my $pid2 = $dbh2-&gt;selectall_arrayref($SQL)-&gt;[0][0];
print "Process one has a PID of $pid1\n";
print "Process two has a PID of $pid2\n";

## Process one listens for a notice named "jtx"
$dbh1-&gt;do(q{LISTEN jtx});
$dbh1-&gt;commit();
## Process one checks for any notices received
print show_notices($dbh1);

## Process two sends a notice, but does not commit
$dbh2-&gt;do(q{NOTIFY jtx});
## Process one does not see the notice yet
print show_notices($dbh1);
## Process two sends the same notice again, then commits
$dbh2-&gt;do(q{NOTIFY jtx});
$dbh2-&gt;commit();

sleep 1; ## Ensure the notice has time to get to propogate
## Process two receives a single notice from process one
print show_notices($dbh1);

## Now that it has seen the notice, it reports nothing again:
print show_notices($dbh1);

sub show_notices { ## Function to return any notices received
       my $dbh = shift;
       my $messages = '';
       $dbh-&gt;commit();
       while (my $n = $dbh-&gt;func('pg_notifies')) {
          $messages .= "Got notice '$n-&gt;[0]' from PID $n-&gt;[1]\n";
       }
       return $messages || "No messages\n";
}
```

The output of the above script on a 8.4 Postgres server is:

```nohighlight
Postgres version is 80401
Process one has a PID of 18238
Process two has a PID of 18239
No messages
No messages
Got notice 'jtx' from PID 18239
No messages
```

As expected, we got a notification only after the other process committed.

Note that because this is asychronous and involves the system tables, we added a sleep call to ensure that the notice had time to propagate so that the other processes will see it. Without the sleep, we usually see four "No messages" appear, as the script goes too fast for the pg_listener table to catch up.

Now for the aforementioned payloads. Payloads allow an arbitrary string to be attached to the notification, such that you can have a standard name like before, but you can also attach some specific text that the other processes can see. I added support for payloads to DBD::Pg back in June 2008, so let's modify the script a little bit to demonstrate the new payload mechanism:

```perl
...
## Process two sends two notices, but does not commit
$dbh2-&gt;do(q{NOTIFY jtx, 'square'});
$dbh2-&gt;do(q{NOTIFY jtx, 'square'});
## Process one does not see the notice yet
print show_notices($dbh1);
## Process two sends the same notice again, then commits
$dbh2-&gt;do(q{NOTIFY jtx, 'triangle'});
$dbh2-&gt;commit();
...
 ## This part changes: we get an extra item from our array:
 $messages .= "Got notice '$n-&gt;[0]' from PID $n-&gt;[1] message is '$n-&gt;[2]'\n";
...
```

Here's what the output looks like under version 9.0 of Postgres:

```nohighlight
Postgres version is 90000
Process one has a PID of 19089
Process two has a PID of 19090
No messages
No messages
Got notice 'jtx' from PID 19090 message is 'square'
Got notice 'jtx' from PID 19090 message is 'triangle'
No messages
```

Note that the collapsing of identical messages into a single notification now takes into account the message as well, so we received two notifications in the above example for the three total notifications sent. To add a payload, we simply say NOTIFY, then the name of the notification, add a comma, and specify a payload as a quoted string. Of course, the payload string is still completely optional. If no payload is specified, DBD::Pg will simply treat the payload as an empty string (this is also the behavior when you request the payload using DBD::Pg against a pre-9.0 server, so all combinations should be 100% backwards compatible).

We also got rid of the sleep. Because we are now using shared memory instead of system tables, there is no lag whatsoever, and the other process can see the notices right away.

Another large advantage to removing the pg_listener table is that systems that make heavy use of it (such as the replication systems Bucardo and Slony) no longer have to worry about bloat in these tables.

The use of payloads also means that many application can be greatly simplified: in the past, one had to be creative in the name of your notifications in order to pass meta-information to your listener. For example, [Bucardo](http://bucardo.org/wiki/bucardo) uses a large collection of notifications, meaning that the Bucardo processes had to do the equivalent of things like this:

```perl
$dbh-&gt;do(q{LISTEN bucardo_reload_config});
$dbh-&gt;do(q{LISTEN bucardo_log_message});
$dbh-&gt;do(q{LISTEN bucardo_activate_sync_$sync});
$dbh-&gt;do(q{LISTEN bucardo_deactivate_sync_$sync});
$dbh-&gt;do(q{LISTEN bucardo_kick_sync_$sync});
...
while (my $notice = $dbh-&gt;func('pg_notifies')) {
 my ($name, $pid) = @$notice;
 if ($name eq 'bucardo_reload_config') {
 ...
 }
 elsif ($name =~ /bucardo_kick_sync_(.+)/) {
 ...
 }
...
}
```

We can instead do things like this:

```perl
$dbh-&gt;do(q{LISTEN bucardo});
...
while (my $notice = $dbh-&gt;func('pg_notifies')) {
 my ($name, $pid, $msg) = @$notice;
 if ($msg eq 'bucardo_reload_config') {
 ...
 }
 elsif ($msg =~ /bucardo_kick_sync_(.+)/) {
 ...
 }
...
}
```

I hope to add this support to Bucardo shortly; it's simply a matter of refactoring all the listen and notify calls into a function that does the right thing depending on the server version it is attached to.


