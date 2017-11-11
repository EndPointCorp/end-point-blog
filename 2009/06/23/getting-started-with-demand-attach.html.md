---
author: Steven Jenkins
gh_issue_number: 160
tags: openafs
title: Getting Started with Demand Attach
---



As OpenAFS moves towards a 1.6 release that has Demand Attach
Fileservers (DAFS), there is a need to thoroughly test Demand Attach.
Getting started can be tricky, so this article highlights the important
steps to configuring a Demand Attach fileserver.

OpenAFS CVS HEAD does not come with Demand Attach enabled by default,
so you'll need to build your own binaries.  You should consult the
official documentation, but the major requirement is to pass the
--enable-demand-attach-fs option to configure.
You should also note that DAFS is only supported on namei fileservers,
not inode.

Once you've built and installed the binaries, you need to be careful
to remove your existing fileserver's bos configuration (i.e., fs)
and put a dafs one in place; e.g.,

```nohighlight
$ bos stop localhost fs -localauth
$ bos delete localhost fs -localauth
```

Once the fs bnode is deleted, you need to install the new
binaries and create the dafs entry.  You should pass your
normal command line arguments to the fileserver and volserver processes:

```nohighlight
$ bos create localhost dafs dafs "/usr/afs/bin/fileserver -my-usual-options" \
    /usr/afs/bin/volserver \
    /usr/afs/bin/salvageserver /usr/afs/bin/salvager
```

Once the entry is created, the bosserver will automatically bring up the processes, so you should check the logfiles to make sure everything is ok. Note that a vos listvol will show volumes as online, even if they are only pre-attached (*pre-attached* means that the fileserver was able to read the volume header, but has not yet brought the volume fully
online).  You can watch the FileLog to see when the fileserver requests a salvage be done.

After initial configure, build, and bos configuration, your Demand Attach fileserver is  not significantly different from your normal fileserver.  You create, move, back up, restore, and move volumes just as with a traditional fileserver.

For more details about DAFS, take a look at the [OpenAFS wiki entry](http://www.dementia.org/twiki/bin/view/AFSLore/DemandAttach).  Be sure to give feedback to the [mailing list](mailto:openafs-info@openafs.org).


