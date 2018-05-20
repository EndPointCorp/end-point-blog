---
author: Greg Sabino Mullane
gh_issue_number: 623
tags: database, monitoring, postgres, security
title: Detecting Postgres SQL Injection
---



<a href="/blog/2012/06/10/detecting-postgres-sql-injection/image-0-big.png" imageanchor="1" style="clear:right; float:right; margin-left:1em; margin-bottom:1em"><img border="0" height="206" src="/blog/2012/06/10/detecting-postgres-sql-injection/image-0.png" width="200"/></a>

SQL injection attacks are often treated with scorn among seasoned 
DBAs and developers—​“oh it could never happen to **us**!”. Until it does, 
and then it becomes a serious matter. It can, and most likely will eventually 
happen to you or one of your clients. It’s prudent to not just avoid them in 
the first place, but to be proactively looking for attacks, to know what to do 
when they occur, and know what steps to take after you have cleaned up the mess.

What is a SQL injection attack? Broadly speaking, it is a malicious 
user entering data to subvert the nature of your original query. This is 
almost always through a web interface, and involves an “unescaped” parameter 
that can be used to change the data returned or perform other database 
actions. The user “injects” their own SQL into your original SQL statement, 
changing the query from its original intent.

For example, you have a page in which the a logged-in customer can look up 
their orders by an order_number, a text field on a web form. The query thus 
looks like this in your code:

```
$order_id = cgi_param('order_number');

$sql = "SELECT * FROM order WHERE order_id = $order_id AND order_owner = '$username'";

$results = run_query($sql);
```

Because there is nothing to limit what the user enters in the order_number 
field, they can inject their own SQL into to the middle of your SQL query 
by creating a non-standard order_number such as:

```
12345 --
```

This would return information on anyone’s order, without checking the order_owner 
column, as the SQL sent to the database would become:

```

SELECT * FROM order WHERE order_id = <span class="i">12345 -- </span>AND order_owner = 'alice'
```

Much more creative (and destructive) choices are available to the attacker as well, 
such as:

```
SELECT * FROM order WHERE order_id = <span class="i">12345; UPDATE user 
  SET admin=TRUE WHERE username = 'alice'; --</span>AND order_owner = 'alice';

SELECT * FROM order WHERE order_id = <span class="i">12345; TRUNCATE TABLE invoices; 
  SELECT * FROM order WHERE order_id = 12345</span> AND order_owner = 'alice';
```

The above is a very simplistic generic-language example, but there are many ways for 
SQL injection attacks to work, including software out of your direct control 
(anything in your chain, from database driver to language to the database 
itself) and non-obvious angles (such as getting creative with multi-byte 
languages).

The correct approach to the above would be to use placeholders:

```
$order_id = cgi_param('order_number');

$sql = 'SELECT * FROM order WHERE order_id = ? AND order_owner = ?';

$results = run_query($sql, $order_id, $username);
```

### Reaction

So you’ve just detected a SQL injection attack. Don’t panic! Okay, perhaps 
panic a little bit. The first order of business is to, as quickly as possible, 
disable access and prevent the attacker from doing anything else. Their next 
injected SQL statement could be a DROP TABLE. Do as much as is needed to stop it 
right away—​don’t worry about fixing the hole yet. Stop Apache, disable all CGI, 
shut down your database, whatever it takes. Yes, this will cause a loss of business 
for a busy site but so will that potential DROP TABLE command! Once things are disabled, 
start patching up the holes. If it is a well isolated, obvious fix, bring things back up. 
If not, look for similar code with the same problem, then bring things back up. There 
are now some important steps to take:

- Double check all similar code for any other problems.
- Check your logs carefully to see if this was an isolated event, or if the hole had 
been used before. If you are relying on SQL errors for detection, a careful attacker 
may have already successfully injected some SQL. See below for forensic tactics.
- Learn why this happened in the first place. Didn’t update a driver? Someone just 
wrote some bad code? Something else? Fix it at both the immediate technical and 
long-term procedural level.

### Detection

Detection is the most important part of this article. If someone were to start a 
SQL injection attack against your site right now, would you even know? How quickly?

Fortunately, SQL injection attacks almost always generate some SQL errors as the 
attacker tries to work around your SQL. This is the number one way to detect 
an attack while it is happening. We recommend the invaluable 
[tail_n_mail](https://bucardo.org/tail_n_mail/) for this task.
For our clients, we have tail_n_mail running via cron every minute, 
scanning for new and interesting errors and mailing them out to us. Thus, 
detection is usually within minutes.

In addition to pure SQL errors, permission errors often occur as well, as 
the attacker tries to do something not allowed by the current database 
user, such as creating a table or running the COPY command. Remember to 
never treat a strange error as an unintersting isolated event, or assume 
that it is probably one of your developers making a typo. Follow up on everything.

Sometimes, when the attacker is very good, no SQL errors are generated, and the 
problems have to be detected in other ways. One way is to scan for common 
SQL injection items. The trick is filtering out valid SQL while finding 
injected ones. In most cases, attacker access to your database is fairly limited without 
knowing the names of your tables, columns, functions, and views, so one thing 
to look for is references to system tables such as pg_class and pg_attribute, 
system views such as pg_tables and pg_stat_activity, the pg_sleep() function, 
and the information_schema schema. (pg_sleep() is often used in “blind SQL” 
attacks, to let the attacker know if something worked or not by the inclusion 
of a delay, when there may be no other direct feedback from their injection).
While looking for these items is not as easy to setup as looking 
for errors, it can be fairly easy to develop and exclude a whitelist of things that should 
be accessing those items.

Another thing to watch out for strange offsets. Because the information an attacker 
can get back is often limited to a row at a time due to the limitations of 
the original query, SQL injections often pull back the same information from, 
say, information_schema.tables, with a “LIMIT 1 OFFSET 1” tacked on, Then 
they call the page again and inject their SQL, but with an offset of 2, then an 
offset of 3, etc. Nothing says SQL injection like seeing an OFFSET 871 in your logs.

Speaking of logs, you may have noticed that the above checks will only work 
if you are logging all statements, by adjusting **log_statement** in 
your postgresql.conf file. Setting this parameter to **'all'** is *highly* 
recommended, and SQL injection detection (and forensics!) are merely two of the 
many reasons for doing so.

If you don’t have log_statement set to ‘all’, your only hope of direct detection is 
if one of the queries happens to get logged for some other reason, such 
as going over your log_min_duration_statement setting. Good luck with that. 
/sarcasm.

There are other methods of detecting SQL injection, but they can all be 
classified as reacting to side effects. Your logs may grow larger, 
a sysadmin on your team may notice some odd network patterns, your 
business intelligence people may come across some unexplained buying 
patterns, etc. Intuition from experienced people is a powerful tool: follow 
up on those hunches and nagging feelings!

### Prevention

Preventing SQL injection is mostly a matter of following some 
standard software development practices. Basically, you want your 
code up to date, well vetted, and easy to read and revert. Here are some 
guidelines:

#### Use version control

More specifically, use 
[git](https://git-scm.com/). For everything related to your site. Application code, 
HTML pages, system configurations. There are many advantages to git, but it is particularly 
useful when you are (quickly!) trying to figure out how some bad code (e.g. with SQL injection 
holes) got into your app, and what safe version you can replace it with. The powers of 
git log -p, git bisect, git blame, and git checkout will make you wonder how you ever 
lived without them.

#### More than one set of eyes

 

Never commit code that hasn’t been looked at by at least one other person not involved 
in its writing. This can be as informal as leaning over and asking someone else to look 
at the patch, to setting up a complex enforcement system via something like 
[gerrit](https://www.gerritcodereview.com/). The most important thing is to 
have it reviewed by someone qualified, and to note the review in your commit message.

Email is a great way to do this, especially if you have a list of people qualified to 
give a review of the code in question. So, database changes could go to a “dbgroup” 
list, and one or more people on the list will review and reply.

Another nice thing is a post-commit hook that mails committed code as a diff to a wide 
audience, such as all engineers in the company. Sure, most people may ignore it, 
but the more eyes the better. On that note, make sure the age-old appeal of heavily 
commenting code is followed, especially code that is trying to fetch information 
from a database.

#### Teach people about SQL injection

Using placeholders is the only truly safe way to write code. Make sure everyone 
knows this, and show some examples of SQL injection problems to new hires so they 
know what to look out for and what the consequences will be.

#### Never assume any database input is safe.

Never, ever assume database input is safe, or will remain safe. Always 
use prepared statements aka placeholders. You say you scrubbed that 
variable with a regular expression above the SQL call? Someone **will** 
tweak that regex someday.

#### Be proactive in looking for problems

See the section about about using tail_n_mail. There are also companies / tools 
that will attempt to find SQL injection problems in your application. While not 
foolproof, these can be useful, particularly if you have a very large website 
with a very large codebase.

#### Keep your software up to date

Sure, your software is free of all problems, but what about the framework 
you are using? The language? The database? And the database drivers? 
They may have a SQL injection problem, and, more importantly, they may 
have already patched it. Run the most recent version, and make sure you 
are on all the relevant announcement lists so you hear about new problems 
and new releases of everything important in your tool chain.

#### Compartmentalize

In these days of complex frameworks and multiple levels of abstraction, 
direct SQL access is often hard or impossible to do. Which can be a very 
good thing, as this is often a good protection against SQL injection. 
Keep in mind however that there are always other ways to reach your database, 
such as the boss’s daughter or son whipping up a quick PHP script so he can 
run some reports from home against the production database.

#### Use the least privileges possible

Make sure you are taking full advantage of roles and users in your database. 
This means an application should have the bare minimum rights it needs to 
do its job. No creating of functions, no creating tables, and explicit 
GRANTs to the tables/views/functions it truly needs. Limit severely what 
runs as a superuser. If something really needs to run as a superuser, 
consider wrapping the data/logic in a SECURITY DEFINER function. Having 
separate “readonly” and “readwrite” versions of each application’s user is 
a great idea as well, and may even help you to scale by being able to send 
your readonly user to a different database (via hot standby or a Bucardo/Slony slave), 
or even send them to different pg_bouncer ports with different pooling methods.

Access can be further limited by the use of views, which can limit which 
columns and rows are visible to a user, or you could even limit all 
application user access to going through stored procedures.

#### URLs are public

Never assume an application, URL, or API will remain internal. It will end 
up accessible to an attacker someday, somehow. Treat everything with 
the same careful, paranoid, care and always use placeholders.

### Forensics

So you’ve just closed a SQL injection hole, and carefully audited your code to 
ensure no other holes exist. Now what? Forensics! Which means, a careful 
examination after the crime. In this case, we want to see what damage the 
intruder managed to cause.

The first thing to do is figure out what **potential** harm there is. You can 
do this by assuming the worst case scenario. What database user was used 
in the attack, and what rights does it have? Could tables have been updated? 
Data deleted? Were tables dropped or views altered? This may be a good time to 
run something like 
[same_schema in historical mode](/blog/2011/10/05/viewing-schema-changes-over-time-with) to find out the answer to that last question.

Now comes the hard part: seeing what was changed. If you do not have 
**log_statment='all'** set in your postgresql.conf (as I will once again 
highly recommend you should have) finding what has changed becomes a 
very, very difficult task. Your best bet at this point is to go to your backups and 
start comparing things, and perhaps running some sanity checks on your data 
(e.g. unusually low prices on things you sell, new mega-useful coupons, 
users with elevated rights). If you know about when the attack started, 
you could, in theory, look on disk to see which relations may have been 
altered to narrow the list of changed data. You will also have to assume that 
the attacker captured all the possible data the database user was allowed 
to see.

Enough about the worst case scenario above—​what about those of us 
with **log_statment='all'**? Well, now we go through the logs to see 
what exact SQL was injected, and what commands have been succesfully run. At this point, 
you should know what the SQL involved in the attack looks like, and more to the point, 
where in your code it came from. Now its a matter of filtering out the good stuff 
from the bad. Luckily, this is a pretty easy task.

What you will need to do is write a quick script to parse your logs, find the type of query 
that had the hole, and determine the “bad” ones. Then you can look closer 
and have it report exactly what commands the attacker ran.

Most SQL injection results in a string of additional SQL in place of where 
a single value should be, with an adding of quotes. So, for example, if someone 
forgot to escape an OFFSET at the end of the query, your program could simply 
look for any variations of the query that ended in something other than 
OFFSET \d$. If the unescaped value was in the middle of the query, I find that 
a simple but reliable test is to look for whitespace or a ‘*’ character. This assumes 
that whitespace or ‘*’ would not normally appear for that value, but as long as it’s 
not common, it should still work. (The ‘*’ is needed because one can use SQL comments 
as a means of whitespace, for example **SELECT/**/*/*foo*/FROM/**/pg_tables**). 
Your script should ignore any queries in which the value has no whitespace or ‘*’ character, 
and focus on the ones that do. Then normalize the queries (for example collapse ones that 
differ only by the OFFSET value), and generate a report. Of course, the exact method to 
differentiate between “good” and “bad” queries will vary. Find your best Perl hacker and 
set them on it.

I should point out that a script is almost always necessary, for three reasons. 
First, manually reading logs is a time-wasting and error-prone bore. Second, 
log_statment='all' leads to some really, really big logs. Third, SQL injection 
attacks usually involve some sort of scripted attack, which can mean a **lot** 
of entries. For example, a client recently had over 8000 lines from a SQL injection 
attack spread out over 20 GB of log files. (This one had a happy ending: the 
attacker was both not very competent and the database user was fairly locked down, 
so no damage was done.)

So remember: SQL injection can happen to you. Make sure you are able to detect it, 
recognize it, fix it, and inspect the damage!


