---
author: Greg Sabino Mullane
title: Debugging obscure Postgres problems with strace
github_issue_number: 823
tags:
- postgres
- sysadmin
date: 2013-06-20
---

<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2013/06/debugging-obscure-postgres-problems/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2013/06/debugging-obscure-postgres-problems/image-0.jpeg"/></a><br/><small><a href="https://www.flickr.com/photos/gadl/284995199/in/photolist-rbF9k/">
Image</a> by Flickr user <a href="https://www.flickr.com/photos/gadl/">Alexandre Duret-Lutz</a></small></div>

One of the nice things about being a Postgres consultant is the sheer 
variety of interesting problems you get to solve. Here’s one that 
recently popped up, and a walkthrough of how I solved it. One of 
our clients had this strange error pop up when they were trying 
to start Postgres:

```
FATAL:  too many private dirs demanded
```

This is a very rare and esoteric error. A peek at the source code showed 
that this error only appears in src/backend/storage/file/fd.c, like so:

```
DIR *
AllocateDir(const char *dirname)
{
    DIR        *dir;

    DO_DB(elog(LOG, "AllocateDir: Allocated %d (%s)",
               numAllocatedDescs, dirname));

    /*
     * The test against MAX_ALLOCATED_DESCS prevents us from overflowing
     * allocatedDescs[]; the test against max_safe_fds prevents AllocateDir
     * from hogging every one of the available FDs, which’d lead to infinite
     * looping.
     */
    if (numAllocatedDescs >= MAX_ALLOCATED_DESCS ||
        numAllocatedDescs >= max_safe_fds - 1)
        elog(ERROR, "too many private dirs demanded");
```

So it appeared as if we ran into some sort of safety valve that was meant to
bail out before too many directories were opened. A strange error to suddenly have
appear (this client’s Postgres worked just fine a few days ago—​luckily,
this was not on a production system!).

The client was using Postgres 8.3. In version 9.1, the source code was changed to give
a much less mysterious message, including outputting the name of the
troublesome directory in question as a debugging clue:

```

    if (numAllocatedDescs >= MAX_ALLOCATED_DESCS ||
        numAllocatedDescs >= max_safe_fds - 1)
        elog(ERROR, "exceeded MAX_ALLOCATED_DESCS while trying to open directory \"%s\"",
             dirname);

```

However, I had no such clue. What to do? This was definitely a job for 
the **strace** program. Its job is to show a trace of all system calls 
that a process is making. In this way, you can see at a very low level 
what a particular program is doing. In this case, the program was PostgreSQL, or 
to be precise, the “postmaster” program.

While it’s possible to have strace attach to an already running process, 
that was not possible in this case as Postgres errored out immediately 
after being invoked. The invocation looked like this:

```
pg_ctl start -D /var/lib/pgsql/data -l /tmp/postgres.startup.log
```

To run strace, we can simply add “strace” to the start of the command 
above. However, this will dump the system calls to the screen 
for the pg_ctl command. We need a few flags to make things easier.

The first flag is “-f”, which tells strace to follow forked processes. 
Without this, we would simply strace pg_ctl itself—​and we need to strace 
the postmaster process instead. As we want to be able to look at the output 
in an editor, we also add the “-o” flag to send all strace output to an output 
file. We also take the opportunity to upgrade “-f” to “-ff”, which tells strace to 
send each forked process to a separate file. Very handy, that. Finally, we 
add a “-t” flag, which prepends each line with a timestamp. Not strictly needed in this 
case, but it’s a nice flag to always use. The final command looked like this:

```
strace -o gregtest -ff -t pg_ctl start -D /var/lib/pgsql/data -l /tmp/postgres.startup.log
```

When I actually ran the command, pg_ctl did *not* return as before. Examining the created 
files showed me why:

```
-rw-r--r--  1 postgres postgres     8383 Jun  7 13:44 gregtest.26664
-rw-r--r--  1 postgres postgres     9372 Jun  7 13:44 gregtest.26668
-rw-r--r--  1 postgres postgres     3191 Jun  7 13:44 gregtest.26667
-rw-r--r--  1 postgres postgres     3053 Jun  7 13:44 gregtest.26669
-rw-r--r--  1 postgres postgres    10628 Jun  7 13:44 gregtest.26666
-rw-r--r--  1 postgres postgres 17311855 Jun  7 13:44 gregtest.26670
```

The first PID (26664) is pg_ctl itself, and the rest are the various postgres 
processes that are created. What we need is the main postmaster one, 
which is obvious in this case: not only is it the highest PID, 
but the file size is very large (and growing fast). A peek at the file 
data/postmaster.pid confirmed that the main postmaster PID is indeed 26670.

Why did pg_ctl not return, and not give the expected error? 
The reason is that the strace process adds enough overhead that it takes 
a lot longer to reach the “too many private dirs demanded” error. 
As I suspected this error was related to entering an infinite 
loop of file openings, that delay makes sense.

Taking a peek at the tail end of the giant strace output gives us the 
solution right away. Repeating over and over were calls like this:

```
19:37:38 open("/usr/share/zoneinfo/zoneinfo/zoneinfo/zoneinfo", 
  O_RDONLY|O_NONBLOCK|O_DIRECTORY) = 22
```

The actual call was 16 directories deep, I’m just showing three 
for brevity! So the problem was definitely with the /usr/share/zoneinfo file. 
A look at the file system showed that /usr/share/zoneinfo was a directory, 
which contained a symlink named “zoneinfo” inside of it. Where did that 
symlink point to?

```
lrwxrwxrwx  1 root root    19 Jun  3 05:45 zoneinfo -> /usr/share/zoneinfo
```

Whoops! That explains the problem. Postgres was trying to walk through all the subdirectories 
in the /usr/share/zoneinfo file. Unfortunately, this meant an infinite loop 
as the zoneinfo symlink kept looping back to the current directory.

So the solution was to simply remove that faulty symlink. Once that was done, 
Postgres started without a hitch. Once again, the invaluable strace 
saves the day.
