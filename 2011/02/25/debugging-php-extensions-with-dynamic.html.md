---
author: Jason Dixon
gh_issue_number: 417
tags: linux, php, tools
title: Debugging PHP extensions with the dynamic linker
---



If you’ve ever had to track down a missing dependency or incompatible libraries, chances are good that you were assisted by the ldd command. This helpful utility reports the list of shared library dependencies required by a binary executable. Or in the typical use case, it will tell you which libraries are *missing* that your application needs to run.

Fortunately most Linux and BSD distributions do a decent job of enforcing dependencies with their respective package managers. But inevitably, there’s the occasional proprietary, closed-binary third-party application or built-from-source utility that skirts the convenience of mainstream distributions. If you’re lucky, the vendor accurately details which software is required, including specific versions theirs was built against. If you’re not, well, you might have to resort to tools like ldd, or even process tracers like strace (Linux), ktrace (OpenBSD) and truss (Solaris).

I recently had the misfortune of troubleshooting a PHP application that was unable to load imagick.so, a [native PHP extension](http://www.php.net/manual/en/intro.imagick.php) to create and modify images using the [ImageMagick](https://www.imagemagick.org/script/index.php) API. The problem manifested itself innocently enough:

```nohighlight
PHP Warning:  PHP Startup: Unable to load dynamic library '/var/www/lib/php/modules
  /imagick.so' - Cannot load specified object in Unknown on line 0
```

Naturally, my first step was to verify the extension was installed.

```nohighlight
$ ls -l /var/www/lib/php/modules/
total 7336
-r--r--r--  1 root  bin       70586 Aug 10  2010 curl.so
-r--r--r--  1 root  bin      395883 Aug 10  2010 gd.so
-rwxr-xr-x  1 root  bin      489386 Aug 10  2010 imagick.so
-r--r--r--  1 root  bin     2105515 Aug 10  2010 mbstring.so
-r--r--r--  1 root  bin       45476 Aug 10  2010 mcrypt.so
-r--r--r--  1 root  bin       63643 Aug 10  2010 mysql.so
```

Knowing that I’d installed the pecl-imagick package using OpenBSD’s pkg_add (which handles dependencies nicely), it seemed unlikely that it was missing any mainstream dependencies. Logically, this started me thinking that it might be a problem with OpenBSD’s default chroot for Apache. Needless to say I was disappointed to see the same error when I ran php -m from the command line:

```nohighlight
$ php -m 2>&1 | grep imagick
PHP Warning:  PHP Startup: Unable to load dynamic library
'/var/www/lib/php/modules/imagick.so' - Cannot load specified object in
Unknown on line 0
```

That was unexpected, but not altogether surprising. Let’s take a quick look with ldd to see what the extension thinks is missing:

```nohighlight
$ ldd /var/www/lib/php/modules/imagick.so
/var/www/lib/php/modules/imagick.so:
Cannot load specified object
```

That’s disturbing... and not much help at all. By contrast, the curl.so extension gives back a full list of shared objects:

```nohighlight
$ ldd /var/www/lib/php/modules/curl.so                                                                              
/var/www/lib/php/modules/curl.so:
        Start            End              Type Open Ref GrpRef Name
        00000002065a3000 00000002069b2000 dlib 1    0   0      /var/www/lib/php/modules/curl.so
        000000020ac30000 000000020b07e000 rlib 0    1   0      /usr/local/lib/libcurl.so.15.0
        000000020f3d4000 000000020f807000 rlib 0    2   0      /usr/local/lib/libidn.so.16.30
        0000000204b21000 0000000204f71000 rlib 0    2   0      /usr/lib/libssl.so.15.1
        0000000204150000 00000002046de000 rlib 0    2   0      /usr/lib/libcrypto.so.18.0
        00000002087f0000 0000000208c05000 rlib 0    2   0      /usr/lib/libz.so.4.1
        0000000209100000 000000020950a000 rlib 0    2   0      /usr/local/lib/libintl.so.5.0
        0000000208c05000 0000000209100000 rlib 0    2   0      /usr/local/lib/libiconv.so.6.0
```

At this point I determine there *has* to be something wrong with imagick.so; the wild goose chase begins. I reinstall the pecl-imagick package from a variety of sources, thinking the original mirror might have a corrupted package. Next I rebuild the package manually from OpenBSD’s ports tree. No change.

Finally, one of the OpenBSD developers suggested the LD_DEBUG environment variable. This tells the run-time link-editor (ld.so) to increase verbosity. The advantage this has over ldd is that it will catch any attempt to load shared objects **after** startup. In the case of PHP, it will look at any shared objects when php tries to load dynamic extensions with **dlopen()**.

```nohighlight
$ sudo LD_DEBUG=1 php -m 2>&1 | more
...
dlopen: loading: /var/www/lib/php/modules/imagick.so
head /var/www/lib/php/modules/imagick.so
obj /var/www/lib/php/modules/imagick.so has /var/www/lib/php/modules/imagick.so as head
linking /var/www/lib/php/modules/imagick.so as dlopen()ed
head [/var/www/lib/php/modules/imagick.so]
examining: '/var/www/lib/php/modules/imagick.so'
loading: libjbig.so.2.0 required by /var/www/lib/php/modules/imagick.so
obj /usr/local/lib/libjbig.so.2.0 has /var/www/lib/php/modules/imagick.so as head
loading: libm.so.5.2 required by /var/www/lib/php/modules/imagick.so
loading: libX11.so.13.0 required by /var/www/lib/php/modules/imagick.so
-->> dlopen: failed to open libX11.so.13.0 <<--
unload_shlib called on /var/www/lib/php/modules/imagick.so
unload_shlib unloading on /var/www/lib/php/modules/imagick.so
dlopen: /var/www/lib/php/modules/imagick.so: done (failed).
PHP Warning:  PHP Startup: Unable to load dynamic library '/var/www/lib/php/modules/imagick.so' - 
   Cannot load specified object in Unknown on line 0
```

And there’s our missing library (libX11.so.13.o). In this case, the dependency *was* installed on the system, but it’s path (/usr/X11R6/lib) wasn’t in the shared library cache. I had remembered to install all of the X11 libraries needed for the ImageMagick and GD libraries, but had forgotten to update the cache with ldconfig. A few seconds and a couple commands later, we were back in business.

```nohighlight
$ sudo ldconfig -m /usr/X11R6/lib
$ php -m | grep imagick
imagick
```

