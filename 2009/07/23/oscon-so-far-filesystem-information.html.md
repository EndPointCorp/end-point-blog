---
author: Selena Deckelmann
gh_issue_number: 176
tags: conference, postgres
title: OSCON so far! Filesystem information bonanza on Wednesday
---



Wednesday was the first official day of OSCON, and I spent it elbow deep in filesystems. The morning was kicked off with Val Aurora delivering a great overview of Btrfs, a new fileystem currently in development. [Some of the features](http://btrfs.wiki.kernel.org/index.php/Btrfs_design) include: 

- Copy on write filesystem
- Cheap, easy filesystem snapshots
- Dynamically resizable partitions
- Indexed directory structure
- Very simple administration

Val demonstrated basic functionality, including creating snapshots and creating a Btrfs filesystem on top of an ext3 filesystem. Cool stuff! The filesystem is still under heavy development, but seems very promising.

Next I saw Theodore Ts'o, the primary developer behind ext4, talk about the future of filesystems and storage.  He referenced [a great paper](http://is.gd/1HV7q) that dives deep into the economics behind SSD (solid state drives) and platter hard drive manufacturing. One interesting calculation was that even if we could convert all the silicon fabs to manufacture flash, would only be able to covert about 12% of the world-wide capacity of hard drive production. Because of this, Theodore believes that it is going to be challenging for the cost of SSDs to drop to the point where it becomes cost competitive with hard drives.

Other observations from Theodore concerned the slowing of innovation around hard drives, and companies like Seagate cutting back in their R&D departments. He sees  opportunity for software and filesystem innovation in this environment, and so far that is playing out in the rapid development of new filesystems for Linux (Nilfs2, POMELFS, and EXOFS as three recent new examples). One open issue he brought up is the need for more and better benchmarking tools. 

In the afternoon, I presented [Linux Filesystem Performance for Databases](http://en.oreilly.com/oscon2009/public/schedule/detail/8432).  I've uploaded the slides to the conference site. I talked about the work that the Portland PostgreSQL Performance Pad team did on filesystem testing with some hardware donated from HP. I also included results from some recent DBT-2 tests Mark had run with PostgreSQL, using pgtune and then refining a few key parameters.

There were quite a few interesting questions, and I talked to one of the Wikia admins about a recent change he'd made to use SSDs instead of hard drives in some of their servers. I mentioned that it would be great to see a case study and data from his experience.


