---
author: Jason Dixon
gh_issue_number: 412
tags: environment, perl, ruby
title: Managing Perl environments with perlbrew
---



As a Perl hobbyist, I’ve gotten used to the methodical evolution of Perl 5 over the years. Perl has always been a reliable language, not without its faults, but with a high level of flexibility in syntactical expression and even deployment options. Even neophytes quickly learn how to install their own Perl distribution and CPAN libraries in $HOME. But the process can become unwieldy, particularly if you want to test across a variety of Perl versions.

To contrast, Ruby core development frequently experiences ABI breakages, even between minor releases. In spite of the wide adoption of Ruby as a Web development language (thanks to Ruby on Rails), Ruby developers are able to plod along unconcerned, where these incompatibilities would almost certainly lead to major bickering within the Perl or PHP communities. How do they do it? The [Ruby Version Manager](https://rvm.io/).

Ruby Version Manager (RVM) allows users to install Ruby and RubyGems within their own self-contained environment. This allows each user to install all (or only) the software that their particular application requires. Particularly for Ruby developers, this provides them with the flexibility to quickly test upgrades for regressions, ABI changes and enhancements without impacting system-wide stability. Thankfully a lot of the ideas in RVM have made their way over to the Perl landscape, in the form of [perlbrew](https://github.com/gugod/App-perlbrew).

Perlbrew offers many of the same features found in RVM for Ruby. It’s easy to install. It isolates different Perl versions and CPAN installations in your $HOME and helps you switch between them. It automates your environment setup and teardown. And most importantly, using perlbrew means not having to clutter your default system Perl with application-specific CPAN dependencies.

Getting started with perlbrew couldn’t be easier. A quick one-liner is all it takes to install perlbrew in your home directory.

```nohighlight
$ curl -L http://xrl.us/perlbrewinstall | bash
```

If you need to install perlbrew somewhere other than your home directory, just download the installer and pass it the PERLBREW_ROOT environment variable.

```nohighlight
$ curl -LO http://xrl.us/perlbrew
$ chmod +x perlbrew
$ PERLBREW_ROOT=/mnt/perlbrew ./perlbrew install
```

Follow the instructions on screen and you’ll be ready to use perlbrew in no time. The perlbrew binary will be installed in ~/perl5/perlbrew/bin, so make sure to adjust your login $PATH accordingly.

Once you’re done installing perlbrew there are a couple commands you’ll want to run before installing your own Perl versions or CPAN modules. The perlbrew init command is mandatory; this initializes your perlbrew directory. It can also be used later if you need to modify your PERLBREW_ROOT setting. The perlbrew mirror is optional (but recommended) to help you select a preferred CPAN mirror.

```nohighlight
$ perlbrew init
$ perlbrew mirror
```

Next comes the fun part. Start off by verifying the Perl version(s) that perlbrew sees.

```nohighlight
$ perlbrew list
* /usr/bin/perl (5.10.1)
```

Install a newer version of Perl.

```nohighlight
$ perlbrew install 5.12.3
```

Now switch to the newer Perl.

```nohighlight
$ perlbrew list
* /usr/bin/perl (5.10.1)
perl-5.12.3

$ perlbrew switch perl-5.12.3

$ perlbrew list
/usr/bin/perl (5.10.1)
* perl-5.12.3

$ perl -v

This is perl 5, version 12, subversion 3 (v5.12.3) built for x86_64-linux

Copyright 1987-2010, Larry Wall

Perl may be copied only under the terms of either the Artistic License or the
GNU General Public License, which may be found in the Perl 5 source kit.

Complete documentation for Perl, including FAQ lists, should be found on
this system using “man perl” or “perldoc perl”. If you have access to the
Internet, point your browser at http://www.perl.org/, the Perl Home Page.
```

Alternatively, if you only want to test a different Perl version, try the perlbrew use command (note: this only works in bash and zsh). Unlike the switch command, use is only active for the current shell.

```bash
$ perlbrew use system

$ perlbrew list
* /usr/bin/perl (5.10.1)
perl-5.12.3
```

A quick peek behind the curtain reveals much of the simplicity behind perlbrew.

```nohighlight
$ ls -l ~/perl5/perlbrew/
total 2680
-rw-r--r--  1 testy  users      408 Feb 10 23:58 Conf.pm
drwxr-xr-x  2 testy  users      512 Feb 10 23:46 bin
drwxr-xr-x  4 testy  users      512 Feb 11 09:59 build
-rw-r--r--  1 testy  users  1333196 Feb 11 10:33 build.log
drwxr-xr-x  2 testy  users      512 Feb 11 09:59 dists
drwxr-xr-x  2 testy  users      512 Feb 10 23:47 etc
drwxr-xr-x  4 testy  users      512 Feb 11 10:32 perls

$ ls -l ~/perl5/perlbrew/perls/
total 8
drwxr-xr-x  5 testy  users  512 Feb 11 00:38 perl-5.12.3
drwxr-xr-x  5 testy  users  512 Feb 11 10:32 perl-5.13.6
```

If you’re a Perl developer, the [perlbrew](https://github.com/gugod/App-perlbrew) project may help alleviate a lot of the pain associated with team development or multi-tenant programming environments. Suddenly it becomes much easier to manage your own software requirements, resulting in faster development and testing cycles for you, and fewer headaches for your System Administrators.


