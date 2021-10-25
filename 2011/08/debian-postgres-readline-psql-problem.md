---
author: Greg Sabino Mullane
title: Debian Postgres readline psql problem and the solutions
github_issue_number: 481
tags:
- open-source
- postgres
date: 2011-08-02
---



<a href="/blog/2011/08/debian-postgres-readline-psql-problem/image-0-big.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5636297890565452370" src="/blog/2011/08/debian-postgres-readline-psql-problem/image-0.gif" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 320px; height: 208px;"/></a>

There was a bit of [a controversy](https://petereisentraut.blogspot.com/2011/02/squeeze-postgresql-broken.html) back in February as Debian decided to replace libreadline with libedit, which affected a number of apps, the most important of which for Postgres people is the psql utility. They did this because psql links to both OpenSSL and readline, and although psql is compatible with both, they are not compatible with each other!

By compatible, I mean that the licenses they use (OpenSSL and readline) are not, in one strict interpretation, allowed to be used together. Debian attempts to live by the letter and spirit of the law as close as possible, and thus determined that they could not bundle both together. Interestingly, Red Hat does still ship psql using OpenSSL and readline; apparently their lawyers reached a different conclusion. Or perhaps they, as a business, are being more pragmatic than strictly legal, as it’s very unlikely there would be any consequence for violating the licenses in this way.

While libreadline (the library for [GNU readline](https://en.wikipedia.org/wiki/GNU_Readline)) is a feature rich, standard, mature, and widely used library, [libedit](https://www.cs.utah.edu/~bigler/code/libedit.html) (sadly) is not as developed and has some important bugs and shortcomings (including no home page, apparently, and no Wikipedia page!). This resulted in frustration for many Debian users, who found that their command-line history commands in psql no longer worked, and worse, psql no longer supported non-ASCII input! Since I came across this problem recently on a client machine, I thought I would lay out the current solutions.

The first and easiest solution is to simply upgrade. Debian has made a “workaround” by forcing psql to use the readline library when it is invoked.

The next best solution, for those rare cases when you cannot upgrade, is to apply Debian’s solution yourself by patching the ‘pg_wrapper’ program that Debian uses. In order to support running different versions of Postgres on the same box in a sane and standard fashion, Debian uses some wrapper scripts around some of the Postgres command-line utilities such as psql. Thus, the psql command in /usr/bin/psql is actually a symlink to the shell script pg_wrapper, which parses some arguments and then calls the **actual** psql binary, which is no longer in the default path. So, to apply the Debian fix, just patch your pg_wrapper file like so:

```plain
*** pg_wrapper  2011/07/18 03:46:49     1.1
--- pg_wrapper  2011/07/18 03:48:23
***************
*** 94,100 ****
  }
  
  error 'Invalid PostgreSQL cluster version' unless -d "/usr/lib/postgresql/$version";
! my $cmd = get_program_path (((split '/', $0)[-1]), $version);
  error 'pg_wrapper: invalid command name' unless $cmd;
  unshift @ARGV, $cmd;
  exec @ARGV;
--- 94,110 ----
  }
  
  error 'Invalid PostgreSQL cluster version' unless -d "/usr/lib/postgresql/$version";
! my $cmdname = (split '/', $0)[-1];
! my $cmd = get_program_path ($cmdname, $version);
! 
! # libreadline is a lot better than libedit, so prefer that                                                                  
! if ($cmdname eq 'psql') {
!     my @readlines = sort();
!     if (@readlines) {
!       $ENV{'LD_PRELOAD'} = ($ENV{'LD_PRELOAD'} or '') . ':' . $readlines[-1];
!     }
! }
! 
  error 'pg_wrapper: invalid command name' unless $cmd;
  unshift @ARGV, $cmd;
  exec @ARGV;
```

As you can see, what Debian has done is set the LD_PRELOAD environment variable to point to the libreadline shared object, which means that when psql is started, it uses the libreadline library instead of libedit. This is great news for Debian users. I’m unconvinced of how “legal” this is per Debian’s standards, but then I’m in the camp that think they are interpreting all the licensing around this in the wrong way, and should have just left libreadline alone.

The second best solution, after patching pg_wrapper, is to simply define LD_PRELOAD yourself, either globally or per user.

Another solution is to use the ‘rlwrap’ program, which is a wrapper around some arbitrary program (in this case, psql) which routes the user input through readline. So a quick alias would be:

```plain
alias p='rlwrap psql --no-readline'
```

(Yes, we could also use -n, but it’s an alias and thus we don’t have to type it out each time, so it’s better to be more verbose). The rlwrap solution is a quick hack, and I do not recommend it, as it still leaves out many psql features, such as autocompletion and ctrl-c support.

All of this is not strictly Debian’s fault. If you read [the various Debian bug reports](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=608442) as well as some of the [Postgres mailing list threads](https://web.archive.org/web/20110825004319/http://postgresql.1045698.n5.nabble.com/Debian-readline-libedit-breakage-td3380317.html) about this topic, you will find there is plenty of finger pointing going around. It seems to me the least guilty party here is readline itself, whose only fault is that it is GPL and not a better license ;). Debian should take a little blame, both for being too strict in what is obviously a very uncharted legal licensing mess, and for making this change so quickly without any announcement and apparently without realizing how many things would break. The worst offender appears to be OpenSSL, which apparently is being stubborn about changing its license to allow linking with the GPL readline. I’ll throw a little bit of blame towards libedit as well, merely for its inability to keep up with 20th century ideas like Unicode (because whose database doesn’t need more 麟?).

The current Debian “solution” has stilled the waters a little bit, but we (Postgres) really need a long-term solution. Or solutions, as the case may be. As with [my previous post](/blog/2011/05/postgres-bug-tracking-help-wanted), the big question there is “who shall put the bell on the cat”? I’d like to see Debian itself fund some work into improving libedit, since they are strongly encouraging use of it over libreadline. That’s solution one: improve libedit such that it becomes a decent readline replacement. This is nice because as great as libreadline is, it’s one of the only pieces of Postgres that used the GPL, and it would be nice to get rid of it for that reason alone (the other big one is PostGIS).

Another solution is to replace [OpenSSL](https://www.openssl.org/), since they apparently are never going to change their license, despite it being in everyone’s best interest. [GnuTLS](https://gnutls.org/) is an oft-mentioned replacement, which seems to be production ready, unlike libedit. The problem here is that psql has a lot of “openssl-isms” in the code. However, that is something that can be accomplished by the Postgres community.

Another option is to get readline to make an exception so it can play nicely with OpenSSL. Not only is this unlikely to happen, I think it’s a band-aid and I’d rather see the above two actions happen instead.

So, in summary, there are really two ways out of this mess: fix up libedit (hello Debian community) and allow Postgres support for GnuTLS (or other non-OpenSSL system for that matter) (hello Postgres community).

For those wanting to dig into this some more, Greg Smith’s excellent summation in [this thread](https://web.archive.org/web/20110825004319/http://postgresql.1045698.n5.nabble.com/Debian-readline-libedit-breakage-td3380317.html) is a great read.


