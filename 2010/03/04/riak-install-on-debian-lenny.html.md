---
author: Ethan Rowe
gh_issue_number: 273
tags: database, hosting, nosql
title: Riak Install on Debian Lenny
---



I'm doing some comparative analysis of various distributed non-relational databases and consequently wrestled with the installation of [Riak](http://riak.basho.com/) on a server running Debian Lenny.

I relied upon the standard "erlang" debian package, which installs cleanly on a basically bare system without a hitch (as one would expect).  However, the latest Riak's "make" tasks fail to run; this is because the rebar script on which the make tasks rely chokes on various bad characters:

```nohighlight
riak@nosql-01:~/riak$ make all rel
./rebar compile
./rebar:2: syntax error before: PK
./rebar:11: illegal atom
./rebar:30: illegal atom
./rebar:72: illegal atom
./rebar:76: syntax error before: ��n16
./rebar:79: syntax error before: ','
./rebar:91: illegal integer
./rebar:149: illegal atom
./rebar:160: syntax error before: Za��ze
./rebar:172: illegal atom
./rebar:176: illegal atom
escript: There were compilation errors.
make: *** [compile] Error 127
```

Delicious.

Ultimately, I came across this article describing issues [getting Riak to install on Ubuntu 9.04](http://onerlang.blogspot.com/2009/10/fighting-with-riak.html), and ultimately determined that the Erlang version mentioned seemed to apply here.  Following the article's instructions for building Erlang from source worked out fine, and so far I've been able to start, ping, and stop the local Riak server without incident.

Since a true investigation requires running these kinds of tools in a cluster, and that means automation of the installation/configuration is desirable, I've been scripting out the configuration steps (putting things into a configuration management tool like [Puppet](http://reductivelabs.com/trac/puppet/) will come later when we're farther along and closer to picking the right solution for the problem in question).  So, here's the script I've been running to build these things from my local machine (relying upon SSH); these are rough, a work in progress, and are not intended as examples of excellence, elegance, or beauty -- they simply get the job done (so far) for me and may help somebody else.

```bash
#!/bin/sh

hostname=$1
erlang_release=otp_src_R13B04
riak_release=riak-0.8.1

ssh root@$hostname "
# necessary for Erlang build
apt-get install build-essential libncurses5-dev m4
apt-get install openssl libssl-dev
# standard from-source build
mkdir erlang-build
cd erlang-build
wget http://ftp.sunet.se/pub/lang/erlang/download/$erlang_release.tar.gz
tar xzf $erlang_release.tar.gz
cd $erlang_release
./configure
make
make install
# put all of riak in a riak user
useradd -m riak
su -c 'wget http://bitbucket.org/basho/riak/downloads/$riak_release.tar.gz' - riak
su -c 'tar xzf $riak_release.tar.gz' - riak
su -c 'cd $riak_release &amp;&amp; make all rel' - riak
su -c 'mv $riak_release/rel riak' - riak
"
```

(I have other scripts for preparing the box post-OS-install, but I don't think they impact this particular part of the process.)


