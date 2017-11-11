---
author: Greg Sabino Mullane
gh_issue_number: 450
tags: dbdpg, open-source, perl, postgres
title: DBD::Pg and the libpq COPY bug
---

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5606309124510069138" src="/blog/2011/05/13/dbdpg-and-libpq-copy-bug/image-0.jpeg"/>(image by [kvanhorn](http://www.flickr.com/photos/kvh/))

Version 2.18.1 of [DBD::Pg](http://search.cpan.org/search?query=DBD%3A%3APg), the Perl driver for Postgres, was just released. This was to fix [a serious bug](https://rt.cpan.org/Ticket/Display.html?id=68041) in which we were not properly clearing things out after [performing a COPY](http://www.postgresql.org/docs/current/interactive/sql-copy.html). The only time the bug manifested, however, is if [an asynchronous query](http://search.cpan.org/~turnstep/DBD-Pg-2.18.1/Pg.pm#Asynchronous_Queries) was done immediately after a COPY finished. I discovered this while working on the [new version of Bucardo](https://mail.endcrypt.com/pipermail/bucardo-general/2011-May/001000.html). The failing code section was this (simplified):

```perl
## Prepare the source
my $srccmd = "COPY (SELECT * FROM $S.$T WHERE $pkcols IN ($pkvals)) TO STDOUT";
$fromdbh->do($srccmd);

## Prepare each target
for my $t (@$todb) {
    my $tgtcmd = "COPY $S.$T FROM STDIN";
    $t->{dbh}->do($tgtcmd);
}

## Pull a row from the source, and push it to each target
while ($fromdbh->pg_getcopydata($buffer) >= 0) {
    for my $t (@$todb) {
        $t->{dbh}->pg_putcopydata($buffer);
    }
}

## Tell each target we are done with COPYing
for my $t (@$todb) {
    $t->{dbh}->pg_putcopyend();
}

## Later on, run an asynchronous command on the source database
$sth{track}{$dbname}{$g} = $fromdbh->prepare($SQL, {pg_async => PG_ASYNC});
$sth{track}{$dbname}{$g}->execute();
```

This gave the error "**another command is already in progress**". This error did not come from Postgres or DBD::Pg, but from **libpq**, the underlying C library which DBD::Pg uses to talk to the database. Strangely enough, taking out the async part and running the exact same command produced no errors.

After tracking back through the libpq code, it turns out that DBD::Pg was only calling PQresult a single time after the copy ended. I can see why this was done: the [docs for PQputCopyEnd](http://www.postgresql.org/docs/current/static/libpq-copy.html) state: "*After successfully calling PQputCopyEnd, call PQgetResult to obtain the final result status of the COPY command. One can wait for this result to be available in the usual way. Then return to normal operation.*" What's not explicitly stated is that you need call PQgetResult again, and keep calling it, until it returns null, to "clear out the message queue". In this case, PQresult pulled back a 'c' message from Postgres, via the frontend/backend protocol, indicating that the copy command was complete. However, what it really needed was to call PQresult two more times, once to get back a 'C' (indicating the COPY statement was complete), and a 'Z' (indicating the backend was ready for a new query). Technically, there was nothing stopping libpq from sending a fresh query except that its own internal flag, conn->asyncStatus, is not reset on a simple end of copy, but only when 'Z' is encountered. Thus, DBD::Pg 2.18.1 now calls PQresult until it returns null.

If your application is encountering this bug and you cannot upgrade to 2.18.1 yet, the solution is simple: perform a non-asynchronous query between the end of the copy and the start of the asynchronous query. It can be any query at all, so the above code could be cured with:

```perl
...
## Tell each target we are done with COPYing
for my $t (@$todb) {
    $t->{dbh}->pg_putcopyend();
    $t->{dbh}->do('SELECT 123');
}

## Later on, run an asynchronous command on the source database
$fromdbh->do('SELECT 123');
$sth{track}{$dbname}{$g} = $fromdbh->prepare($SQL, {pg_async => PG_ASYNC});
$sth{track}{$dbname}{$g}->execute();
```

Why does the non-asynchronous command work? Doesn't it check the conn->asyncStatus as well? The secret is that PQexecstart has this bit of code in it:

```perl
    /*
     * Silently discard any prior query result that application didn't eat.
     * This is probably poor design, but it's here for backward compatibility.
     */
    while ((result = PQgetResult(conn)) != NULL)
```

Wow, that code looks familiar! So it turns out that the only reason this was not spotted earlier is that non-asynchronous commands (e.g. those using PQexec) were silently clearing out the message queue, kind of as a little favor from libpq to the driver. The async function, PQsendQuery, is not as nice, so it does the correct thing and fails right away with the error seen above (via PQsendQueryStart).


