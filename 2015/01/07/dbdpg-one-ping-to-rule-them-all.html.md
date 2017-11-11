---
author: Greg Sabino Mullane
gh_issue_number: 1066
tags: database, dbdpg, postgres
title: 'DBD::Pg: one ping to rule them all'
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="https://flic.kr/p/25b8Ch" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/01/07/dbdpg-one-ping-to-rule-them-all/image-0.jpeg"/></a>
<br/><small><a href="https://flic.kr/p/25b8Ch">Yellow Submarine</a> by <a href="https://www.flickr.com/photos/bolfster/">Wolfgang Metzner</a></small></div>

How can you tell if your database connection is still valid? One way, when using Perl, is to use the ping() method.
Besides backslash-escaped placeholders, a revamped ping() method is the major change in the recently released version 3.5.0 of [DBD::Pg](http://search.cpan.org/dist/DBD-Pg/), the Perl/[DBI](http://search.cpan.org/dist/DBI/DBI.pm#ping) interface to 
[Postgres](https://postgres.org/). Before 3.5.0, there was a chance of false positives when using this method. In particular, if you were inside of a transaction, DBD::Pg did not actually attempt to contact the Postgres backend. This was definitely an oversight, and DBD::Pg now does the right thing.

Detecting a dead backend is a little trickier than it sounds. While libpq stores some state information for us, the only way to be sure is to issue a command to the backend. Additionally, we check the value of PQstatus in case libpq has detected a problem. Realistically, it would be far better if the Postgres protocol supported some sort of ping itself, just a simple answer/response without doing anything, but there is nothing like that yet. Fortunately, the command that is issued, **/* DBD::Pg ping test, v3.5.0 */**, is very lightweight.

One small side effect is that the ping() method (and its stronger cousin, the [pg_ping() method](http://search.cpan.org/dist/DBD-Pg/Pg.pm#pg_ping)) will both cancel any COPY that happens to be in progress. Really, you should not be doing that anyway! :) Calling the next copy command, either pg_getline() or pg_putline(), will tell you if the connection is valid anyway. Since the copy system uses a completely different backend path, this side effect is unavoidable.

Even this small change may cause some problems for applications, which relied on the previous false positive behavior. Leaving as a basic no-op, however, was not a good idea, so check if your application is using ping() sanely. For most applications, simple exception handling will negate to use ping() in the first place.


