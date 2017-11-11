---
author: David Christensen
gh_issue_number: 411
tags: postgres
title: Pausing Hot Standby Replay in PostgreSQL 9.0
---



When using a PostgreSQL Hot Standby master/replica pair, it can be
useful to temporarily pause WAL replay on the replica.  While future
versions of Postgres will include the ability to pause recovery using
administrative SQL functions, the current released version does not
have this support.  This article describes two options for pausing
recovery for the rest of us that need this feature in the present.
These two approaches are both based around the same basic idea:
utilizing a "pause file", whose presence causes recovery to pause
until the file has been removed.

### Option 1: patched pg_standby

pg_standby is a fairly standard tool that is often used as
a restore_command for WAL replay.  I wrote a patch for it
(available at [my github repo](https://github.com/machack666/postgres/commit/77dc38a63f72f3d63f80a344aa357bfe6ebb1dc3)) to support the "pause
file" notion.  The patch adds a -p path/to/pausefile optional
argument, which if present will check for the pausefile and wait until
it is removed before proceeding with recovery.

The benefit of patching pg_standby is that the we're
building on mature production-level code, adding a functionality at
its most relevant place.  In particular, we know that signal handling
is already sensibly handled; (this was something I was less than
positive about with when it comes to the wrapper shell script
described later).  The downside here is that you need to compile your
own version of pg_standby in order to take advantage of it.  However,
it may be considered useful enough of a patch to accept in the 9.0
tree, so future releases could support it out-of-the-box.

After patching, compiling, and installing the modified version of
pg_standby the only change to an existing
restore_command already using pg_standby would be
the addition of the -p /path/to/pausefile argument; e.g.:

```nohighlight
restore_command = 'pg_standby -p /tmp/pausefile /path/to/archive %f %p'
```

After restarting the standby, simply touching the
/tmp/pausefile file will pause recovery until the file is
subsequently removed.

### Option 2: a shell script

The pause-while script is a simple wrapper script I wrote
which can be used to gate the invocation of any command by checking if
the "pause file" (a file path passed as the first argument) exists.
If the pause file exists, we loop in a sleep cycle until it is
removed.  Once the pause file does not exist (or if it did not exist
in the first place), we execute the rest of the provided command
string.

Sample invocation:

```bash
[user@host&lt;1&gt;] $ touch /tmp/pausefile; pause-while /tmp/pausefile echo hi
... # pauses, notifying of status

[user@host&lt;2&gt;] $ rm /tmp/pausefile
... # shell 1 will now output "hi"
```

Here's the script:

pause-while:

```bash
#!/bin/bash

# we're trapping this signal
trap 'exit 1' INT;

PAUSE_FILE=$1;
shift;

while [ -f $PAUSE_FILE ]; do
 echo "'$PAUSE_FILE' present; pausing. remove to continue" &gt;&amp;2
 sleep 1;
 PAUSED=1
done

[ "$PAUSED" ] &amp;&amp; echo "'$PAUSE_FILE' removed; " &gt;&amp;2

# untrap so we don't block the invoked command's expected signal handling
trap INT;

# now we know the pause file doesn't exist, proceed to execute our
# command as normal

exec $@;
```

We need to trap SIGINT to prevent the wrapped command from executing if the sleep cycle is interrupted.

Putting this to use in our Hot Standby case, we will want to use
pause-while as a wrapper for the existing
restore_command, thus adjusting recovery.conf to
something like this:

```nohighlight
restore_command = 'pause-while /tmp/standby.pause pg_standby ... &lt;args&gt;'
```

With this configuration, when you want to pause WAL replay on the
replica simply touch the /tmp/standby.pause pause file and
the next invocation of restore_command will wait until that file is
removed before proceeding.

The wrapper script approach has the benefit of working with any
defined restore_command and is not limited to just working
with pg_standby.

### Limitations

- Since this is based on WAL archive restoration, this has a very
coarse granularity; recovery can only pause between WAL files, which
are 16MB.  It is likely that future SQL support functions will support
this at arbitrary transaction boundaries and will not have this
specific limitation.

- Neither of these options will work with Streaming Replication.
Streaming Replication uses a non-zero exit status of the
restore_command as the "End of Archive" marker to flip from
archive restoration/catchup mode to WAL Streaming mode.
pg_standby's default behavior (even before this patch) is to
wait for the next archive file to appear before returning a zero exit
status, and returning a non-zero exit status only on error, signal, or
because its failover trigger file now exists.  This means that if you
use pg_standby as the restore_command with Streaming
Replication enabled, you will never actually flip over into WAL
streaming mode, and will stay pointlessly in rechive restoration mode.
(Technically speaking you could touch the failover trigger file; that
would get you out of the archive mode, and into WAL streaming mode,
but would not result in actually failing over.)  It is likely that
future SQL support functions for pausing recovery will not have this
same dependency/limitation, and will be able to pause recovery when
utilizing Streaming Replication.

- While reviewed/manually tested, these programs have **not**
been production-tested.  I've done basic testing on both the shell
script and pg_standby patch, however this has not been battle-tested,
and likely has some corner cases that haven't been considered (I'm
particularly concerned about the shell script's signal handling
interactions.)

- pg_standby has been deprecated and removed in future
releases of PostgreSQL.  I believe it would still be possible to
compile/use pg_standby for future releases based on the
version in the 9.0 source tree, but I believe it was removed because
of the issues in conjunction with Streaming Replication.  Presumably
it (and this approach) would still be relevant if people wanted to
utilize a traditional log-shipping standby with Hot Standby.

Comments/improvements welcome/appreciated!


