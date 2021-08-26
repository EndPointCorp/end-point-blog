---
author: Greg Sabino Mullane
title: RCS vs. Git for quick versioning
github_issue_number: 229
tags:
- git
date: 2009-12-02
---

As a consultant, I’m often called to make changes on production systems—​sometimes in a hurry. One of my rules is to document all changes I make, no matter how small or unimportant they may seem. In addition to local notes, I always check in any files I change, or might change in the future, into version control. In the past, I would always use RCS. However, [Jon Jensen](/team/jon-jensen) challenged me to rethink my automatic use of RCS and give Git a try for this.

This makes sense on some levels. We use Git for most everything here at End Point, and it is our preferred version control system. I still use other systems: there are some clients and projects that require the use of Subversion, Mercurial, and even CVS. The advantage of Git for quick one off checkins is that, similar to RCS, there is no central repository, and setup is extremely easy.

As an example, one of the files I often check into version control is postgresql.conf, the main configuration file for the Postgres database. Before I even edit the file, I’ll check it in, so the sequence of events looks like this:

```nohighlight
mkdir RCS
ci -l postgresql.conf
edit postgresql.conf
```

The creation of the RCS directory is optional but recommended. RCS (which stands for Revision Control System) uses a very simple tracking mechanism. A new file that tracks all changes is created for each file. This new file takes the original name of the file and adds a “,v” to the end of it. However, it’s annoying to have all those “comma vee” files laying around, so RCS has a nice trick that when a directory named RCS exists, all the comma vee files will be placed into that directory. The “ci -l postgresql.conf” checks in (ci) the file, and the “-l” file instructs RCS to immediately check it back out again and lock it (as the current user). This is an RCS specific advisory lock, and only gets in the way if you try to check in the file as a different user. The final command above, “edit postgresql.conf” calls up my editor of choice so I can start modifying the file.

Once the file has been modified, checking in the changes made is as simple as once again doing:

```nohighlight
ci -l postgresql.conf
```

Now that it has been checked in, I can perform other common version control tasks against it. To see the complete log of changes:

```nohighlight
rlog postgresql.conf
```

To see the differences between the current version and the last checkin, or against a specific version:

```nohighlight
rcsdiff postgresql.conf
rcsdiff -r1.3 postgresql.conf
```

To find a string in a specific previous version:

```nohighlight
co -p -r1.3 postgresql.conf | grep foobar
```

Using Git for this purpose is fairly similar. The first steps now become:

```nohighlight
git init
git add postgresql.conf
git commit postgresql.conf
edit postgresql.conf
```

Technically, one more step than before, but not really a big deal. Note that we don’t need to create a special directory to hold the versioning information: by default, Git puts everything in a “.git” directory. Once we’ve made changes to the file, we can commit out changes with:

```nohighlight
git commit postgresql.conf
```

to see the log of changes:

```nohighlight
git log postgresql.conf
```

To see the differences between the current version and the last checkin, or against a specific version:

```nohighlight
git diff postgresql.conf
git diff 11a049bc80fe4a2f4584465fe13d8bb4ee479f23 postgresql.conf
```

To find a string in a specific previous version:

```nohighlight
git show 11a049bc80fe4a2f4584465fe13d8bb4ee479f23:postgresql.conf | grep foobar
```

With Git, there is also quite a bit more than an be done now—​easy branching, grepping, generating diffs, etc. However, most of it is overkill for the simple purpose of tracking local changes. On the downside, Git does not have the simple version numbering that RCS has, and the syntax can be a bit trickier and non-intuitive.

So, did I make the switch? Well, yes and no. I’ve been trying to use Git for simple checkins the last few weeks, and have had mixed results. Here’s my breakdown of areas in which they differ:

### Ease of use

RCS wins this one. All you really need to remember to use RCS is “ci -l filename”. The only other commands you might possibly need is “rlog filename” and “rcsdiff filename”. On the other hand, Git requires a deeper understanding of objects, trees, add vs. commit, and the use of long, hard to type hexadecimal numbers. It’s also not very intuitive, and the command arguments can be complex. To be fair, for this *particular* use case Git is not really that much more complex, but the advantage still goes to RCS.

### Availability

RCS wins this one as well. On many systems, RCS is already installed by default. Even when it is not, a “yum install rcs” or the equivalent works just fine 100% of the time. RCS has been around a long, long time, and it’s solid, tested, and very available on any system you run into. In contrast, Git is fairly new, does *not* come pre-installed on most systems, and is not even available via all packaging systems. This is one factor that would definitely prevent me from using it everywhere. Maybe years from now when it is a standard tool, this will change, but for now, RCS wins this one.

### Diffs

The rcsdiff command is handy, but very limited. If all you want is the simplest of bare-bones diffs, all is good. However, Git allows you to view diffs in different formats, add color, generate patches, and many other features that can be nice to have.

### Fancy tricks

RCS is designed to be dirt simple and good at what it does: track single files. The design of Git was for a large, distributed project with complex needs. This means that Git has many tricks and features that the designers of RCS did not even dream of. While most of them are not needed when you are simply doing versioning of local files, there are definitely times when the full power of Git is nice to have.

### Grouping

RCS has no concept of projects or trees: everything is simply a file. This means that you cannot track relationships between files. The only possible way to do so is to compare the timestamps that two files were checked in. In contrast, Git does not consider files at all, but simply treats everything as objects in a tree. This allows easy grouping of files together in a single logical commit. It also allows for things such as branching and merging.

### Versioning

While Git uses SHA1 checksums to name each object with a unique identity, RCS simply uses a “single dot” version number, and increments it for you. Thus, the first time you check in a file, it is set as version 1.1. The second version is 1.2, and so on. This is very useful when you are simply tracking a lone file—​you know that version 1.20 is the 20th recorded change, and that comparing or viewing an earlier version is as simple as using the “-r x.y” option. Calling what Git does “versioning” is somewhat of a misnomer—​it has a completely different philosophy about how objects are tracked, which lends itself great to distributed and collaborative projects, but not so well to single files.

### Blame

Here’s one area where Git wins hands down. For RCS, you do a checkin, and the file is locked as the current local user. There is no indication of the actual *person* doing the checkin (as opposed to the account name), unless you add it to the checkin comment each time, and that gets laborious and annoying. With Git, you can set some standard environment variables (even on a shared account), and Git will record who made the change. Not only can you see who made each commit and when, but you can use the awesome “git blame” command to view who made the last change to each line in a file.

As an aside, how do we do the assignment mentioned above in a shared account? Setting the author for Git commits is as simple as setting environment variables like so:

```nohighlight
$ export GIT_AUTHOR_NAME="Greg Sabino Mullane"
$ export GIT_AUTHOR_EMAIL="greg@endpoint.com"
```

On a shared account, just create an alias. For example:

```nohighlight
cat > .gregs_stuff
export GIT_AUTHOR_NAME="Greg Sabino Mullane"
export GIT_AUTHOR_EMAIL="greg@endpoint.com"
<ctrl-D>
cat >> .bashrc
alias greg='source ~/.gregs_stuff'
<ctrl-D>
```

#### Editor support

One of the nice things about RCS is that it has been around for so long that many editors have integrated support for it. For example, calling up a file in emacs that has been checked in via RCS shows a display in the status line at the bottom of the screen showing that the file is controlled by RCS, what the current version number is, whether it is locked or not. While there is Git support as well, it’s only available in very new versions of emacs (and other editors). Advantage, RCS.

### Bloat

Because Git is a real version control system, and a complicated one at that, it carries a lot of setup baggage. Just creating a repository and checking in a single file creates about 37 files underneath the .git directory. This number grows sharply with every commit you do. By contrast, RCS creates a single file (and one additional for each file you track). This means you can easily ship around the “dot vee” files to other systems.

### Final analysis

When looking at all the factors, RCS still wins. It’s simple, gets the job done, and most important of all, is available on all systems. I may revisit this in a few years when Git is more widespread.
