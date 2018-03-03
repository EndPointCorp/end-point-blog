---
author: Jon Jensen
gh_issue_number: 905
tags: perl, redhat
title: Building ImageMagick on RHEL/CentOS 6 with Perl 5.18.1
---



This is a quick tip for anyone in the exact same situation I was recently, and everyone else can probably just skip it!

RHEL 6 and CentOS 6 and other derivatives come with ImageMagick-6.5.4.7-6.el6_2.x86_64, which is a bit dated but still reasonable. They also come with Perl 5.10.1, which has grown very old. We wanted to use the latest version of Perl (5.18.1) with [plenv](https://github.com/tokuhirom/plenv), but the latest version of the Perl libraries for ImageMagick (PerlMagick) does not work with the older ImageMagick 6.5.4.7.

The first task, then, was to locate the matching older version of PerlMagick from [BackPAN](http://backpan.perl.org/), the archive of historical CPAN modules: [http://backpan.perl.org/authors/id/J/JC/JCRISTY/PerlMagick-6.54.tar.gz](http://backpan.perl.org/authors/id/J/JC/JCRISTY/PerlMagick-6.54.tar.gz), and try to build that.

However, that fails to build without applying a patch to make it compatible with newer versions of Perl. The patch is available from [http://trac.imagemagick.org/changeset?format=diff&new=4950](http://trac.imagemagick.org/changeset?format=diff&new=4950), or you can just create a file called typemap in the root of the unpacked directory, with one line:

```nohighlight
Image::Magick T_PTROBJ
```

Then build, test, and install as usual. That’s it.


