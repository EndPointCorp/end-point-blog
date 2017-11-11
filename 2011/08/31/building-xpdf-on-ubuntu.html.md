---
author: Jon Jensen
gh_issue_number: 490
tags: graphics, open-source, tips, ubuntu
title: Building Xpdf on Ubuntu
---



It may happen that you need to use [Xpdf](http://foolabs.com/xpdf/), even though it no longer ships with [Ubuntu](http://www.ubuntu.com/) and is considered ... outdated? buggy? insecure? In any case, it still renders some PDFs that [Poppler](http://poppler.freedesktop.org/)-based viewers such as [Evince](http://projects.gnome.org/evince/) don't, or allows some troublesome PDFs to print as fonts and line art instead of a rasterized mess.

Here's how I built and installed xpdf 3.02 on Ubuntu 11.04 (Natty Narwhal) x86_64:

```bash
sudo apt-get install libfreetype6-dev libmotif-dev
wget ftp://ftp.foolabs.com/pub/xpdf/xpdf-3.02.tar.gz  # now 3.03 is current
tar xzpf xpdf-3.02.tar.gz
cd xpdf-3.02
./configure --with-freetype2-library=/usr/lib/x86_64-linux-gnu \
    --with-freetype2-includes=/usr/include/freetype2 \
    --with-Xm-library=/usr/lib \
    --with-Xm-includes=/usr/include/Xm
make
# see lots of warnings!
sudo make install
```

That's it. Not as nice as the old native Debian/Ubuntu packages, but gets the job done.


