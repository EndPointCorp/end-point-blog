---
author: Greg Sabino Mullane
gh_issue_number: 1015
tags: bucardo, database, postgres, replication
title: PostgreSQL conflict handling with Bucardo and multiple data sources
---

<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2014/07/24/postgresql-conflict-handling-with/image-0-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/07/24/postgresql-conflict-handling-with/image-0.png"/></a>
<br/><small><a href="https://flic.kr/p/fybbDe">Image</a> by Flickr
user <a href="https://www.flickr.com/photos/grongar/">Rebecca Siegel</a>
(cropped)</small></div>

Bucardo’s much publicized ability to handle multiple data sources often raises questions about conflict resolution. People wonder, for example, what happens when a row in one source database gets updated one way, and the same row in another source database gets updated a different way? This article will explain some of the solutions Bucardo uses to solve conflicts. The recently released [Bucardo 5.1.1](https://bucardo.org/wiki/Bucardo) has some new features for conflict handling, so make sure you use at least that version.

[Bucardo](https://bucardo.org/wiki/Bucardo) does multi-source replication, meaning that 
users can write to more than one source at the same time. (This is also called multi-master
replication, but “source” is a much more accurate description than
“master”). Bucardo deals in primary keys as a way to identify rows. If the same row has changed on one or more sources since the last Bucardo run, a conflict has arisen and Bucardo must be told how to handle it. In other words, Bucardo must decide which row is the “winner” and thus gets replicated to all the other databases.

For this demo, we will again use an Amazon AWS. See the [earlier post about Bucardo 5](
/blog/2014/06/23/bucardo-5-multimaster-postgres-released)
for directions on installing Bucardo itself. Once it is installed (after the
'./bucardo install' step), we can create some test databases for our conflict
testing. Recall that we have a handy database named “shake1”. As this
name can get a bit long for some of the examples below, let’s make a few databases copies with shorter names. We will also teach Bucardo about the databases, and create a sync named “ctest” to replicate between them all:

```nohighlight
createdb aa -T shake1
createdb bb -T shake1
createdb cc -T shake1
bucardo add db A,B,C dbname=aa,bb,cc
## autokick=0 means new data won't replicate right away; useful for conflict testing!
bucardo add sync ctest dbs=A:source,B:source,C:source tables=all autokick=0
bucardo start
```

Bucardo has three general ways to handle conflicts: built in strategies, a
list of databases, or using custom conflict handlers. 
The primary strategy, and also the default one for all syncs, is known as **bucardo_latest**. When
this strategy is invoked, Bucardo scans all copies of the conflicted table across all
source databases, and then orders the databases according to when they were last changed. This generates a list of databases, for example **“B C A”**. For each conflicting row, the database most recently updated—​of all the ones involved in the conflict for that row—​is the winner. The other built in strategy is called “bucardo_latest_all_tables”, which scans all the tables in the sync across all source databases to find a winner.

There may be other built in strategies added as experience/demand
dictates, but it is hard to develop generic solutions to the complex
problem of conflicts, so non built-in strategies are preferred. Before getting into 
those other solutions, let’s see the default strategy (bucardo_latest) in
action:

```
<span class="gsm">## This is the default, but it never hurts to be explicit:
bucardo update sync ctest conflict=bucardo_latest
Set conflict strategy to 'bucardo_latest'
psql aa -c "update work set totalwords=11 where title~'Juliet'"; \
psql bb -c "update work set totalwords=21 where title~'Juliet'"; \
psql cc -c "update work set totalwords=31 where title~'Juliet'"
UPDATE 1
UPDATE 1
UPDATE 1
bucardo kick sync ctest 0
Kick ctest: [1 s] DONE!
## Because cc was the last to be changed, it wins:
for i in {aa,bb,cc}; do psql $i -tc "select current_database(), \
totalwords from work where title ~ 'Juliet'"; done
aa   |   31
bb   |   31
cc   |   31
</span>
```

Under the hood, Bucardo actually applies the list of winning databases to each conflicting row, such that example above of “B C A” means that database B wins in a conflict in which a rows was updated by B and C, or B and A, or B and C and A. However, if B did not change the row, and the conflict is only between C and A, then C will win.

As an alternative to the built-ins, you can set conflict_strategy
to a list of the databases in the sync, ordered from highest priority to lowest, for example “C B A”. The list does not have to include all the databases, but it is a good idea to do so. Let’s see it in action. We will change the conflict_strategy for our test sync and then reload the sync to have it take effect:

```
<span class="gsm">
bucardo update sync ctest conflict='B A C'
Set conflict strategy to 'B A C'
bucardo reload sync ctest
Reloading sync ctest...Reload of sync ctest successful
psql aa -c "update work set totalwords=12 where title~'Juliet'"; \
psql bb -c "update work set totalwords=22 where title~'Juliet'"; \
psql cc -c "update work set totalwords=32 where title~'Juliet'"
UPDATE 1
UPDATE 1
UPDATE 1
bucardo kick sync ctest 10
Kick ctest: [1 s] DONE!
## This time bb wins, because B comes before A and C
for i in {aa,bb,cc}; do psql $i -tc "select current_database(), \
totalwords from work where title ~ 'Juliet'"; done
aa   |   22
bb   |   22
cc   |   22
</span>
```

The final strategy for handling conflicts is to write your own code. Many will argue this is the best approach. It is certaiy the only one that will allow you to embed your business logic into the conflict handling.

Bucardo allows loading of snippets of Perl code known as “customcodes”.
These codes take effect at specified times, such as after triggers are
disabled, or when a sync has failed because of an exception. The specific time we
want is called “conflict”, and it is an argument to the “whenrun”
attribute of the customcode. A customcode needs a name, the whenrun
argument, and a file to read in for its content. They can also be
associated with one or more syncs or tables.

Once a conflict customcode is in place and a conflict is encountered, the code will be invoked, and it will in turn pass information back to Bucardo telling it how to handle the conflict.

The code should expect a single argument, a hashref containing information
about the current sync. This hashref tells the current table, and gives a list of all conflicted rows. The code can tell Bucardo which database to consider the
winner for each conflicted row, or it can simply declare a winning database
for all rows, or even for all tables. It can even modify the data in any of the tables itself. What it cannot do (thanks to the magic of DBIx::Safe) is commit, rollback, or do
other dangerous actions since we are in the middle of an important transaction.

It’s probably best to show by example at this point. Here is a file called ctest1.pl that asks Bucardo to skip to the next applicable customcode if the conflict is in the table “chapter”. Otherwise, it will tell it to have database “C” win all conflicts for this table, and fallback to the database “B” otherwise.

```perl
## ctest1.pl - a sample conflict handler for Bucardo
use strict;
use warnings;

my $info = shift;
## If this table is named 'chapter', do nothing
if ($info->{tablename} eq 'chapter') {
    $info->{skip} = 1;
}
else {
    ## Winning databases, in order
    $info->{tablewinner} = 'C B A';
}
return;
```

Let’s add in this customcode, and associate it with our sync. Then we will reload the sync and cause a conflict.

```
<span class="gsm">bucardo add customcode ctest \
  whenrun=conflict src_code=ctest1.pl sync=ctest
Added customcode "ctest"
bucardo reload sync ctest
Reloading sync ctest...Reload of sync ctest successful
psql aa -c "update work set totalwords=13 where title~'Juliet'"; \
psql bb -c "update work set totalwords=23 where title~'Juliet'"; \
psql cc -c "update work set totalwords=33 where title~'Juliet'"
UPDATE 1
UPDATE 1
UPDATE 1
bucardo kick sync ctest 0
Kick ctest: [1 s] DONE!
## This time cc wins, because we set all rows to 'C B A'
for i in {aa,bb,cc}; do psql $i -tc "select current_database(), \
totalwords from work where title ~ 'Juliet'"; done
aa   |   33
bb   |   33
cc   |   33
</span>
```

We used the “skip” hash value to tell Bucardo to not do anything if the table is named “chapter”. In real life, we would have another customcode that will handle the skipped table, else any conflict in it will cause the sync to stop. Any number of customcodes can be attached to syncs or tables.

The database preference will last for the remainder of this sync’s run,
so any other conflicts in other tables will not even bother to invoke the
code. You can use the hash key “tablewinneralways” to make this decision
sticky, in that it will apply for all future runs by this sync (its KID
technically)—​which effectively means the decision stays until Bucardo
restarts.

One of the important structures sent to the code is a hash
named “conflicts”, which contains all the changed primary keys, and, for
each one, a list of which databases were involved in the sync. A
Data::Dumper peek at it would look like this:

```
<span class="gsm">$VAR1 = {
  'romeojuliet' => {
    'C' => 1,
    'A' => 1,
    'B' => 1,
  }
};
</span>
```

The job of the conflict handling code (unless using one of the “winner” hash keys) is to change each of those conflicted rows from a hash of involved databases into a string describing the preferred order of databases. The Data::Dumper output would thus look like this:

```
<span class="gsm">$VAR1 = {
  'romeojuliet' => 'B'
};
</span>
```

The code snippet would look like this:

```perl
## ctest2.pl - a simple conflict handler for Bucardo.
use strict;
use warnings;

my $info = shift;
for my $row (keys %{ $info->{conflicts} }) {
  ## Equivalent to 'A C B'
  $info->{conflicts}{$row} = exists $info->{conflicts}{$row}{A} ? 'A' : 'C';
}

## We don't want any other customcodes to fire: we have handled this!
$info->{lastcode} = 1;
return;
```

Let’s see that code in action. Assuming the above “bucardo add customcode” command was run, we will need to load an updated version, and then reload the sync. We create some conflicts, and check on the results:

```
<span class="gsm">
bucardo update customcode ctest src_code=ctest2.pl
Changed customcode "ctest" src_code with content of file "ctest2.pl"
bucardo reload sync ctest
Reloading sync ctest...Reload of sync ctest successful
psql aa -c "update work set totalwords=14 where title~'Juliet'"; \
psql bb -c "update work set totalwords=24 where title~'Juliet'"; \
psql cc -c "update work set totalwords=34 where title~'Juliet'"
UPDATE 1
UPDATE 1
UPDATE 1
bucardo kick sync ctest 10
Kick ctest: [2 s] DONE!
## This time aa wins, because we set all rows to 'A C B'
for i in {aa,bb,cc}; do psql $i -tc "select current_database(), \
totalwords from work where title ~ 'Juliet'"; done
aa   |   14
bb   |   14
cc   |   14
</span>
```

That was an obviously oversimplified example, as we picked “A” for no discernible reason! These conflict handlers can be quite complex, and are only limited by your imagination—​and your business logic. As a final example, let’s have the code examine some other things in the database, and as well as jump out of the database itself(!) to determine the resolution to the conflict:

```perl
## ctest3.pl - a somewhat silly conflict handler for Bucardo.
use strict;
use warnings;
use LWP;

my $info = shift;

## What is the weather in Walla Walla, Washington?
## If it's really hot, we cannot trust server A
my $max_temp = 100;
my $weather_url = 'http://wxdata.weather.com/wxdata/weather/rss/local/USWA0476?cm_ven=LWO&cm_cat=rss';
my $ua = LWP::UserAgent->new;
my $req = HTTP::Request->new(GET => $weather_url);
my $response = $ua->request($req)->content();
my $temp = ($response =~ /(\d+) \°/) ? $1 : 75;
## Store in our shared hash so we don't have to look it up every run
## Ideally we'd add something so we only call it if the temp has not been checked in last hour
$info->{shared}{wallawallatemp} = $temp;

## We want to count the number of sessions on each source database
my $SQL = 'SELECT count(*) FROM pg_stat_activity';
for my $db (sort keys %{ $info->{dbinfo} }) {
    ## Only source databases can have conflicting rows
    next if ! $info->{dbinfo}{$db}{issource};
    ## The safe database handles are stored in $info->{dbh}
    my $dbh = $info->{dbh}{$db};
    my $sth = $dbh->prepare($SQL);
    $sth->execute();
    $info->{shared}{dbcount}{$db} = $sth->fetchall_arrayref()->[0][0];
}

for my $row (keys %{ $info->{conflicts} }) {
    ## If the temp is too high, remove server A from consideration!
    if ($info->{shared}{wallawallatemp} > $max_temp) {
        delete $info->{conflicts}{$row}{A}; ## May not exist, but we delete anyway
    }

    ## Now we can sort by number of connections and let the least busy db win
    (my $winner) = sort {
        $info->{shared}{dbcount}{$a} <=> $info->{shared}{dbcount}{$b}
        or
        ## Fallback to reverse alphabetical if the session counts are the same
        $b cmp $a
    } keys %{ $info->{conflicts}{$row} };

    $info->{conflicts}{$row} = $winner;
}

## We don't want any other customcodes to fire: we have handled this!
$info->{lastcode} = 1;
return;
```

We’ll forego the demo: suffice to say that B always won in my tests, as Walla Walla never got over 97, and all my test databases had the same number of connections. Note some of the other items in the $info hash: “shared” allows arbitrary data to be stored across invocations of the code. The “lastcode” key tells Bucardo not to fire any more customcodes. While this example is very impractical, it does demonstrate the power available to you when solving conflicts.

Hopefully this article answers many of the questions about conflict handling
with Bucardo. Suggestions for new default handlers and examples of
real-world conflict handlers are particularly welcome, as well as any other
questions or comments. You can find the mailing list at bucardo-general@bucardo.org, and
subscribe by visiting [the bucardo-general Info Page](https://mail.endcrypt.com/mailman/listinfo/bucardo-general).
