---
author: Mark Johnson
gh_issue_number: 742
tags: perl
title: Find your Perl in Other Shells
---



Often when programming, it turns out the best tools for the job are system tools, even in an excellent language like Perl. Perl makes this easy with a number of ways you can allocate work to the underlying system: backtick quotes, qx(), system(), exec(), and open(). Virtually anyone familiar with Perl is familiar with most or all of these ways of executing system commands.

What's perhaps less familiar, and a bit more subtle, is what Perl really does when handing these off to the underlying system to execute. The docs for exec() tell us the following:

```
       exec LIST
       exec PROGRAM LIST
[snip]
            If there is more than one argument in LIST, or if LIST is an
            array with more than one value, calls execvp(3) with the
            arguments in LIST.  If there is only one scalar argument or an
            array with one element in it, the argument is checked for shell
            metacharacters, and if there are any, the entire argument is
            passed to the system's command shell for parsing (this is
            "/bin/sh -c" on Unix platforms, but varies on other platforms).
```

That last parenthetical is a key element when we "shell out" and expect certain behavior. Perl is going to use /bin/sh. But I don't; I use /bin/bash. And I am very happy to ignore this divergence ... until I'm not.

Without considering any of these issues, I had leveraged a shell command to do a nifty table comparison between supposedly replicated databases to find where the replication had failed. The code in question was the following:

```
$ diff -u \
&gt; &lt;(psql -c "COPY (SELECT * FROM foo ORDER BY foo_id) TO STDOUT" -U chung chung) \
&gt; &lt;(psql -c "COPY (SELECT * FROM foo ORDER BY foo_id) TO STDOUT" -U chung chung2)
```

The above code produced exactly the results I was looking for, so I integrated it into my Perl code via qx() and ran it. Doing so produced the following surprising result:

```
$ ./foo.pl
sh: -c: line 0: syntax error near unexpected token `('
sh: -c: line 0: `diff -u &lt;(psql -c "COPY (SELECT * FROM foo ORDER BY foo_id) TO STDOUT" -U chung chung) &lt;(psql -c "COPY (SELECT * FROM foo ORDER BY foo_id) TO STDOUT" -U chung chung2)'
```

I worked with an End Point colleague and figured out the problem. <() is supported by bash, but not by Bourne. Further, there is no way to instruct Perl to use /bin/bash for its target shell.

In order to access a different shell and leverage the desired features, I had to use the invocation described for PROGRAM LIST, but identify the shell itself as my program. While I'm unaware of any way to accomplish this with backticks, I was certainly able to do so using Perl's open():

```
my $cmd = q{diff -u &lt;(psql -c "COPY (SELECT * FROM foo ORDER BY foo_id) TO STDOUT" -U chung chung) &lt;(psql -c "COPY (SELECT * FROM foo ORDER BY foo_id) TO STDOUT" -U chung chung2)};

    open (my $pipe, '-|', '/bin/bash', '-c', $cmd)
        or die "Error opening pipe from diff: $!";
    while (&lt;$pipe&gt;) {
        # do my stuff
    }
    close ($pipe);
```

Now results between command line and invocation from Perl are consistent. And now I understand for future reference how to control which shell I find my Perl in.


