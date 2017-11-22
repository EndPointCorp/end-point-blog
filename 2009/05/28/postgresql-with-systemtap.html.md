---
author: Josh Tolley
gh_issue_number: 155
tags: postgres
title: PostgreSQL with SystemTap
---



Those familiar with PostgreSQL know it has supported [DTrace](http://en.wikipedia.org/wiki/DTrace) since version 8.2. The 8.4beta2 includes support for several new DTrace probes. But for those of us using platforms on which DTrace doesn't exist, this support hasn't necessarily meant much. [SystemTap](http://sourceware.org/systemtap/) is a relatively new, Linux-based package with similar purpose to DTrace, available on Linux, and is under heavy development. As luck would have it, PostgreSQL's DTrace probes work with SystemTap as well.

A few caveats: it helps to run a very new SystemTap version (I used one I pulled from SystemTap's git repository today), and in order for SystemTap to have access to userspace software, your kernel must support utrace. I don't know precisely what kernel versions include the proper patches; my Ubuntu 8.04 laptop didn't have the right kernel, but the Fedora 10 virtual machine I just set up does.

Step 1 was to build SystemTap. This was a straightforward ./configure, make, make install, once I got the correct packages in place. Step 2 was to build PostgreSQL, including the --enable-dtrace option. This also was straightforward. Note that PostgreSQL won't build with the --enable-dtrace option unless you've already installed SystemTap. Finally, I initialized a PostgreSQL database cluster and started the database.

Here's where the fun starts. SystemTap's syntax differs from DTrace syntax. Here's an example probe SystemTap would accept:

```nohighlight
probe process("/usr/local/pgsql/bin/postgres").function("eqjoinsel")
{
        printf ("%d\n", pid())
}
```

This tells SystemTap to print out the process ID (which comes from the SystemTap pid() function) each time the PostgreSQL eqjoinsel function is called. That's the function to estimate join selectivity with most equality operators, and gets called a lot, so it's a decently useful test. It also shows that SystemTap can probe inside programs without an explicitly defined probe. I saved this file as test.d, and ran it like this:

```nohighlight
[josh@localhost ~]$ sudo stap -v test.d
Pass 1: parsed user script and 52 library script(s) in 160usr/220sys/641real ms.
Pass 2: analyzed script: 1 probe(s), 1 function(s), 1 embed(s), 0 global(s) in 40usr/60sys/331real ms.
Pass 3: translated to C into "/tmp/stapDD5a4p/stap_c0b737cdffdb48cec3fd55b631bb0656_1057.c" in 30usr/160sys/211real ms.
Pass 4, preamble: (re)building SystemTap's version of uprobes.
Pass 4: compiled C into "stap_c0b737cdffdb48cec3fd55b631bb0656_1057.ko" in 1510usr/3430sys/8052real ms.
Pass 5: starting run.
4521
4521
4521
4521
```

4521 is the process ID of the PostgreSQL backend I'm connected to, and it gets printed every time I type "\dt" in my psql session.

Now for something more interesting. Although SystemTap lets me probe whatever function I want, it's nice to be able to use the defined DTrace probes, because that way I don't have to find the function name I'm interested in, in order to trace something. Here are some examples I added to my test.d script, pulled more or less at random from the [list of available DTrace probes in the PostgreSQL documentation](http://www.postgresql.org/docs/8.4/static/dynamic-trace.html). Note that whereas the documentation lists the probe names with dashes (or are these hyphens?), to make it work with SystemTap, I needed to use double-underscores, so "transaction-start" in the docs becomes "transaction__start" in my script.

```nohighlight
probe process("/usr/local/pgsql/bin/postgres").mark("transaction__start")
{      
        printf("Transaction start: %d\n", pid())
}

probe process("/usr/local/pgsql/bin/postgres").mark("lwlock__condacquire") {
        printf("lock wait start at %d for process %d on cpu %d\n", gettimeofday_s(), pid(), cpu())
}

probe process("/usr/local/pgsql/bin/postgres").mark("sort__start") {
        printf("transaction abort at %d for process %d on cpu %d\n", gettimeofday_s(), pid(), cpu())
}

probe process("/usr/local/pgsql/bin/postgres").mark("smgr__md__write__done") {
        printf("smgr-md-write-done at %d for process %d on cpu %d\n", gettimeofday_s(), pid(), cpu())
}
```

...which resulted in something like this when I ran pgbench:

```nohighlight
[josh@localhost ~]$ sudo stap -v test.d
Pass 1: parsed user script and 52 library script(s) in 130usr/150sys/286real ms.
Pass 2: analyzed script: 7 probe(s), 4 function(s), 2 embed(s), 0 global(s) in 30usr/30sys/120real ms.
Pass 3: translated to C into "/tmp/stapW9yfAQ/stap_f6f3ffd834ef5b249edcf7d1ca19dce2_3025.c" in 10usr/150sys/163real ms.
Pass 4, preamble: (re)building SystemTap's version of uprobes.
Pass 4: compiled C into "stap_f6f3ffd834ef5b249edcf7d1ca19dce2_3025.ko" in 1380usr/2690sys/4155real ms.
Pass 5: starting run.
Transaction start: 4894
Transaction start: 4894
lock wait start at 1243552147 for process 4907 on cpu 0
Transaction start: 4907
Transaction start: 4907
lock wait start at 1243552147 for process 4907 on cpu 0
Transaction start: 4907
lock wait start at 1243552174 for process 2770 on cpu 0
smgr-md-write-done at 1243552174 for process 2770 on cpu 0
smgr-md-write-done at 1243552174 for process 2770 on cpu 0
smgr-md-write-done at 1243552174 for process 2770 on cpu 0
```

This could be a very interesting way of profiling, performance testing, debugging, troubleshooting, and who knows what else. I'm interested to see SystemTap become more ubiquitous. I should note that I have no idea how SystemTap compares to DTrace or whether it will manage to do for Linux what DTrace can do on other operating systems. Time will tell, I guess.

UPDATE: As has been pointed out in the comments, compiling PostgreSQL with --enable-dtrace is only necessary if I want to use the built-in "taps" (the SystemTap word, apparently, for its equivalent of DTrace probes). Probing by function call, or any of the other probe methods SystemTap supports, works without --enable-dtrace.

UPDATE 2: It's important to note that the defined DTrace probes include sets of useful variables that DTrace and SystemTap scripts might be interested in. For instance, it's possible to get the transaction ID within the transaction__start probe. In SystemTap, these variables are referenced as $arg1, $arg2, etc. So in a transaction__start probe, you could say:

```nohighlight
printf("Transaction with ID %d started\n", $arg1)
```

