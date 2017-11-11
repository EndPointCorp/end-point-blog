---
author: Jon Jensen
gh_issue_number: 214
tags: open-source, perl, redhat
title: ImageMagick EPS bug workaround
---

Sometimes software is buggy, and even with the malleability of open source software, upgrading to fix a problem may not be an immediate option due to lack of time, risks to production stability, or problems caused by other incompatible changes in a newer version of the software.

[ImageMagick](http://www.imagemagick.org/) is a widely used open source library and set of programs for manipulating images in many ways. It's very useful and I'm grateful it exists and has become so powerful. However, many longtime ImageMagick users like me can attest that it has had a fair number of bugs, and upgrades sometimes don't go very smoothly as APIs change, or new bugs creep in.

Recently my co-worker, Jeff Boes, had the misfortune, or opportunity, of encountering just such a scenario. Our friends at [CityPass](http://www.citypass.com/) have several site features that use ImageMagick for resizing, rotating, and otherwise manipulating or gathering data about images.

The environment specifics (skip if you're not troubleshooting an ImageMagick problem of your own!): [RHEL 5](http://www.redhat.com/rhel/server/) with its standard RPM of ImageMagick-6.2.8.0-4.el5_1.1.x86_64. The application server is [Interchange](http://www.icdevgroup.org/), running on our local-perl-5.10.0 nonthreaded Perl build, using the local-ImageMagick-perl-6.2.8.0-4.1 library. Those custom builds are available in the [packages.endpoint.com endpoint Yum repository](https://packages.endpoint.com/).

CityPass reported problems with some EPS (Encapsulated PostScript) images failing to process correctly by ImageMagick. In fact, the bug prevented any subsequent image processing jobs from completing in the same OS process. Upgrading ImageMagick would fix the bug, but we can't currently do that on the production server due to other compatibility problems.

After some trial and error, Jeff determined that the ImageMagick bug only kicks in when the **first** image processed is an EPS file. If it's any other image type, it works fine. This explained why code that had been unchanged in a year or so suddenly stopped working: Before now, no EPS file had happened to come first.

At first Jeff hacked the system to process the non-EPS files first, then sorted the results as originally desired. Then we realized there may be some rare scenarios where no non-EPS files at all were in the batch, which would trigger the bug. Jeff then had ImageMagick always first process a trivial small JPEG file which was known to work.

That worked, but Jeff then came across the idea of processing an empty image file so we didn't have a dependency on an image that might later be deleted. He tinkered a bit and came up with something suprising but even better. This is his Perl code:

```perl
my $first_im = Image::Magick->new;
$first_im->read('');
# (then process all images in any order as originally intended)
```

I wouldn't have expected an initial read of an empty string filename to solve the problem, but it did. Accompanied by a suitable comment noting the history of the kludge for future software archaeologists, closed the case.

Software's funny, but it's nice when there's a simple -- if counterintuitive -- solution to work around a bug. And I think Jeff has mostly recovered his sanity in the meantime!
