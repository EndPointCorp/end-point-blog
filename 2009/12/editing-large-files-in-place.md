---
author: Greg Sabino Mullane
title: Editing large files in place
github_issue_number: 237
tags:
- database
- postgres
- tips
date: 2009-12-13
---



Running out of disk space seems to be an all too common problem lately, especially when dealing with large databases. One situation that came up recently was a client who needed to import a large Postgres dump file into a new database. Unfortunately, they were very low on disk space and the file needed to be modified. Without going into all the reasons, we needed the databases to use template1 as the template database, and not template0. This was a very large, multi-gigabyte file, and the amount of space left on the disk was measured in megabytes. It would have taken too long to copy the file somewhere else to edit it, so I did a low-level edit using the Unix utility **dd**. The rest of this post gives the details.

To demonstrate the problem and the solution, we’ll need a disk partition that has little-to-no free space available. In Linux, it’s easy enough to create such a thing by using a RAM disk. Most Linux distributions already have these ready to go. We’ll check it out with:

```bash
$ ls -l /dev/ram*
brw-rw---- 1 root disk 1,  0 2009-12-14 13:04 /dev/ram0
brw-rw---- 1 root disk 1,  1 2009-12-14 22:27 /dev/ram1
```

From the above, we see that there are some RAM disks available (there are actually 16 of them available on my box, but I only showed two). Here’s the steps to create a usable partition from /dev/ram1, and to then check the size:

```bash
$ mkdir /home/greg/ramtest

$ sudo mke2fs /dev/ram1
mke2fs 1.41.4 (27-Jan-2009)
Filesystem label=
OS type: Linux
Block size=1024 (log=0)
Fragment size=1024 (log=0)
4096 inodes, 16384 blocks
819 blocks (5.00%) reserved for the super user
First data block=1
Maximum filesystem blocks=16777216
2 block groups
8192 blocks per group, 8192 fragments per group
2048 inodes per group
Superblock backups stored on blocks:
        8193

Writing inode tables: done
Writing superblocks and filesystem accounting information: done

This filesystem will be automatically checked every 29 mounts or
180 days, whichever comes first.  Use tune2fs -c or -i to override.

$ sudo mount /dev/ram1 /home/greg/ramtest

$ sudo chown greg:greg /home/greg/ramtest

$ df -h /dev/ram1
Filesystem            Size  Used Avail Use% Mounted on
/dev/ram1              16M  140K   15M   1% /home/greg/ramtest
```

First we created a new directory to server as the mount point, then we used the **mke2fs** utility to create a new file system (ext2) on the RAM disk at /dev/ram1. It’s a fairly verbose program by default, but there is nothing in the output that’s really important for this example. Then we mounted our new filesystem to the directory we just created. Finally, we reset the permissions on the directory such that an ordinary user (e.g. 'greg’) can read and write to it. At this point, we’ve got a directory/filesystem that is just under 16 MB large (we could have made it much closer to 16 MB by specifying a -m 0 to mke2fs, but the actual size doesn’t matter).

To simulate what happened, let’s create a database dump and then bloat it until there it takes up all available space:

```bash
$ cd /home/greg/ramtest

$ pg_dumpall > data.20091215.pg

$ ls -l data.20091215.pg
-rw-r--r-- 1 greg greg 3685 2009-12-15 10:42 data.20091215.pg

$ dd seek=3685 if=/dev/zero of=data.20091215.pg bs=1024 count=99999
dd: writing 'data.20091215.pg': No space left on device
13897+0 records in
13896+0 records out
14229504 bytes (14 MB) copied, 0.0814188 s, 175 MB/s

$ df -h .
Filesystem            Size  Used Avail Use% Mounted on
/dev/ram1              16M   15M     0 100% /home/greg/ramtest
```

First we created the dump, then we found the size of it, and told dd via the **‘seek’** argument to start adding data to it at the 3685 byte mark (in other words, we appended to the file). We used the special file **/dev/zero** as the **‘if’** (input file), and our existing dump as the **‘of’** (output file). Finally, we told it to chunk the inserts into 1024 bytes at a time, and to attempt to add 999,999 of those chunks.  Since this is approximately 100MB, we ran out of disk space quickly, as we intended. The filesystem is now at 100% usage, and will refuse any further writes to it.

To recap, we need to change the first three instances of template0 with template1. Let’s use grep to view the lines:

```bash
$ grep --text --max-count=3 template data.20091215.pg
CREATE DATABASE greg WITH TEMPLATE = template0 OWNER = greg ENCODING = 'UTF8';
CREATE DATABASE rand WITH TEMPLATE = template0 OWNER = greg ENCODING = 'UTF8';
CREATE DATABASE sales WITH TEMPLATE = template0 OWNER = greg ENCODING = 'UTF8';
```

We need the **--text** argument here because grep correctly surmises that we’ve changed the file from text-based to binary with the addition of all those zeroes on the end. We also used the handy **--max-count** argument to stop processing once we’ve found the lines we want. Very handy argument when the actual file is gigabytes in size!

There are two major problems with using a normal text editor to change the file. First, the file (in the real situation, not this example!) was very, very large. We only needed to edit something at the very top of the file, so loading the entire thing into an editor is very inefficient. Second, editors need to save their changes somewhere, and there just was not enough room to do so.

Attempting to edit with emacs gives us: emacs: IO error writing /home/greg/ramtest/data.20091215.pg: No space left on device

An attempt with vi gives us: vi: Write error in swap file on startup. "data.20091215.pg" E514: write error (file system full?)

Although emacs gives the better error message (why is vim making a guess and outputting some weird E514 error?), the advantage always goes to vi in cases like this as emacs has a [major bug](https://www.emacswiki.org/emacs/EmacsFileSizeLimit) in that it cannot even open very large files.

What about something more low-level like **sed**? Unfortunately, while sed is more efficient than emacs or vim, it still needs to read the old file and write the new one. We can’t do that writing as we have no disk space! More importantly, in sed there is no way (that I could find anyway) to tell it stop processing after a certain number of matches.

What we need is something *really* low-level. The utility **dd** comes to the rescue again. We can use dd to truly edit the file in place. Basically, we’re going to overwrite some of the bytes on disk, without needing to change anything else. First though, we have to figure out exactly which bytes to change. The grep program has a nice option called **--byte-offset** that can help us out:

```bash
$ grep --text --byte-offset --max-count=3 template data.20091215.pg
301:CREATE DATABASE greg WITH TEMPLATE = template0 OWNER = greg ENCODING = 'UTF8';
380:CREATE DATABASE rand WITH TEMPLATE = template0 OWNER = greg ENCODING = 'UTF8';
459:CREATE DATABASE sales WITH TEMPLATE = template0 OWNER = greg ENCODING = 'UTF8';
```

This tells us the offset for each line, but we want to replace the number ‘0’ in ‘template0’ with the number ‘1’. Rather than count it out manually, let’s just use another Unix utility, **hexdump**, to help us find the number:

```bash
$ grep --text --byte-offset --max-count=3 template data.20091215.pg | hexdump -C
00000000  33 30 31 3a 43 52 45 41  54 45 20 44 41 54 41 42  |301:CREATE DATAB|
00000010  41 53 45 20 67 72 65 67  20 57 49 54 48 20 54 45  |ASE greg WITH TE|
00000020  4d 50 4c 41 54 45 20 3d  20 74 65 6d 70 6c 61 74  |MPLATE = templat|
00000030  65 30 20 4f 57 4e 45 52  20 3d 20 67 72 65 67 20  |e0 OWNER = greg |
00000040  45 4e 43 4f 44 49 4e 47  20 3d 20 27 55 54 46 38  |ENCODING = 'UTF8|
...
```

Each line is 16 characters, so the first three lines comes to 48 characters, then we add two for the ‘e0’, subtract four for the ‘301:’, and get 301+48+2-4=347. We subtract one more as we want to seek to the point just before that character, and we can now use our dd command:

```bash
$ echo 1 | dd of=data.20091215.pg seek=346 bs=1 count=1 conv=notrunc
1+0 records in
1+0 records out
1 byte (1 B) copied, 0.00012425 s, 8.0 kB/s
```

Instead of an input file (the ‘if’ argument), we simply pass the number ‘1’ via stdin to the dd command. We use our calculated seek, tell it to copy a single byte (bs=1), one time (count=1), and (this is very important!) tell dd NOT to truncate the file when it is done (conv=notrunc). Technically, we are sending two characters to the dd program, the number one and a newline, but the bs=1 argument ensures only the first character is being copied. We can now verify that the change was made as we expected:

```bash
$ grep --text --byte-offset --max-count=3 TEMPLATE data.20091215.pg
301:CREATE DATABASE greg WITH TEMPLATE = template1 OWNER = greg ENCODING = 'UTF8';
380:CREATE DATABASE rand WITH TEMPLATE = template0 OWNER = greg ENCODING = 'UTF8';
459:CREATE DATABASE sales WITH TEMPLATE = template0 OWNER = greg ENCODING = 'UTF8';
```

Now for the other two entries. From before, the magic number is 45, so we now add 380 to 45 to get 425. For the third line, the name of the database is 1 character longer so we add 459+45+1 = 505:

```bash
$ echo 1 | dd of=data.20091215.pg seek=425 bs=1 count=1 conv=notrunc
1+0 records in
1+0 records out
1 byte (1 B) copied, 0.000109234 s, 9.2 kB/s

$ echo 1 | dd of=data.20091215.pg seek=505 bs=1 count=1 conv=notrunc
1+0 records in
1+0 records out
1 byte (1 B) copied, 0.000109932 s, 9.1 kB/s

$ grep --text --byte-offset --max-count=3 TEMPLATE data.20091215.pg
301:CREATE DATABASE greg WITH TEMPLATE = template1 OWNER = greg ENCODING = 'UTF8';
380:CREATE DATABASE rand WITH TEMPLATE = template1 OWNER = greg ENCODING = 'UTF8';
459:CREATE DATABASE sales WITH TEMPLATE = template1 OWNER = greg ENCODING = 'UTF8';
```

Success! On the real system, the database was loaded with no errors, and the large file was removed. If you’ve been following along and need to cleanup:

```bash
$ cd ~
$ sudo umount /home/greg/ramtest
$ rmdir ramtest
```

Keep in mind that dd is a very powerful and thus very dangerous utility, so treat it with care. It can be invaluable for times like this however!


