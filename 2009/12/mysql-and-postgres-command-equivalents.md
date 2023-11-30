---
author: Greg Sabino Mullane
title: MySQL and PostgreSQL command equivalents (mysql vs. psql)
github_issue_number: 242
tags:
- database
- mysql
- open-source
- postgres
- tips
date: 2009-12-24
---

Users toggling between the MySQL and PostgreSQL command-line clients are often confused by the equivalent commands to accomplish basic tasks. Here’s a chart listing some of the differences between the command line client for MySQL (simply called **mysql**), and the command line client for Postgres (called **psql**).

<style> td, th { vertical-align: top } </style>
<table cellpadding="0" cellspacing="0" id="toggle" style="border: medium none"><tbody>
<tr class="alt"><th style="white-space: nowrap;" width="30%">MySQL (using mysql)</th><th style="white-space: nowrap;" width="30%">Postgres (using psql)</th><th>Notes</th></tr>
<tr><td><b>\c</b>
<br>Clears the buffer</td><td><b>\r</b>
<br>(same)</td><td>
</td></tr>
<tr class="alt">
<td><b>\d <em>string</em></b>
<br>Changes the delimiter</td><td>No equivalent</td><td>
</td></tr>
<tr><td><b>\e</b>
<br>Edit the buffer with external editor</td><td><b>\e</b>
<br>(same)</td><td>Postgres also allows <b>\e <em>filename</em></b> which will become the new buffer</td></tr>
<tr class="alt"><td><b>\g</b>
<br>Send current query to the server</td><td><b>\g</b>
<br>(same)</td><td>
</td></tr>
<tr><td><b>\h</b>
<br>Gives help — general or specific</td><td><b>\h</b>
<br>(same)</td><td>
</td></tr>
<tr class="alt"><td><b>\n</b>
<br>Turns the pager off</td><td><b>\pset pager off</b>
<br>(same)</td><td>The pager is only used when needed based on number of rows; to force it on, use <span style="font-weight: bold; white-space: nowrap;">\pset pager always</span></td></tr>
<tr><td><b>\p</b>
<br>Print the current buffer</td><td><b>\p</b>
<br>(same)</td><td>
</td></tr><tr class="alt"><td><b>\q</b>
<br>Quit the client</td><td><b>\q</b>
<br>(same)</td><td>
</td></tr><tr><td><span style="font-weight: bold;">\r</span> <code><em>[dbname] [dbhost]</em></code>
<br>Reconnect to server</td><td><span style="font-weight: bold;">\c</span> <code><em>[dbname] [dbuser]</em></code>
<br>(same)</td><td>
</td></tr><tr class="alt"><td><b>\s</b>
<br>Status of server</td><td>No equivalent</td><td>Some of the same info is available from the <code>pg_settings</code> table</td></tr><tr><td><b>\t</b>
<br>Stop teeing output to file</td><td>No equivalent</td><td>However, <span style="font-weight: bold;">\o</span> (without any argument) will stop writing to a previously opened outfile</td></tr><tr class="alt"><td><b>\u <em>dbname</em></b>
<br>Use a different database</td><td><b>\c <em>dbname</em></b>
<br>(same)</td><td>
</td></tr><tr><td><b>\w</b>
<br>Do not show warnings</td><td>No equivalent</td><td>Postgres always shows warnings by default</td></tr><tr class="alt"><td><b>\C <em>charset</em></b>
<br>Change the charset</td><td><b>\encoding <em>encoding</em></b>
<br>Change the encoding</td><td>Run <span style="font-weight: bold;">\encoding</span> with no argument to view the current one</td></tr><tr><td><b>\G</b>
<br>Display results vertically (one column per line)</td><td><b>\x</b>
<br>(same)</td><td>Note that <span style="font-weight: bold;">\G</span> is a one-time effect, while <span style="font-weight: bold;">\x</span> is a toggle from one mode to another. To get the exact same effect as <span style="font-weight: bold;">\G</span> in Postgres, use <span style="font-weight: bold;">\x\g\x</span></td></tr><tr class="alt"><td><b>\P <em>pagername</em></b>
<br>Change the current pager program</td><td>Environment variable <span style="font-weight: bold;">PAGER</span> or <span style="font-weight: bold;">PSQL_PAGER</span></td><td>
</td></tr><tr><td><b>\R <em>string</em></b>
<br>Change the prompt</td><td><b>\set PROMPT1 <em>string</em></b>
<br>(same)</td><td>Note that the Postgres prompt cannot be reset by omitting an argument. A good prompt to use is: \set PROMPT1 <span style="white-space: nowrap;">'%n@%\`hostname\`:%>%R%#%x%x%x '</span></td></tr><tr class="alt"><td><b>\T <em>filename</em></b>
<br>Sets the tee output file</td><td>No direct equivalent</td><td>Postgres can output to a pipe, so you can do: <b><span style="white-space: nowrap;">\o | tee <em>filename</em></span></b></td></tr><tr><td><b>\W</b>
<br>Show warnings</td><td>No equivalent</td><td>Postgres shows warnings by default</td></tr><tr class="alt"><td><b>\?</b>
<br>Help for internal commands</td><td><b>\?</b>
<br>(same)</td><td>
</td></tr><tr><td><b>\#</b>
<br>Rebuild tab-completion hash</td><td>No equivalent</td><td>Not needed, as tab-completion in Postgres is always done dynamically</td></tr><tr class="alt"><td><b>\! <em>command</em></b>
<br>Execute a shell command</td><td><b>\! <em>command</em></b>
<br>(same)</td><td>If no command is given with Postgres, the user is dropped to a new shell (<span style="font-weight: bold;">exit</span> to return to psql)</td></tr><tr><td><b>\. <em>filename</em></b>
<br>Include (“source”) a file as if it were typed in</td><td><b>\i <em>filename</em></b>
<br>(same)</td><td>
</td></tr><tr class="alt"><td>Timing is always on</td><td><b>\timing</b>
<br>Toggles timing on and off</td><td>
</td></tr><tr><td>No equivalent</td><td><b>\t</b>
<br>Toggles “tuple only” mode</td><td>This shows the data from select queries, with no headers or footers</td></tr><tr class="alt"><td><b>show tables;</b>
<br>List all tables</td><td><b>\dt</b>
<br>(same)</td><td>Many also use just <span style="font-weight: bold;">\d</span>, which lists tables, views, and sequences</td></tr><tr><td><b>desc <em>tablename;</em></b>
<br>Display information about the given table</td><td><b>\d <em>tablename</em></b>
<br>(same)</td><td>
</td></tr><tr class="alt"><td><b>show index from <em>tablename;</em></b>
<br>Display indexes on the given table</td><td><b>\d <em>tablename</em></b>
<br>(same)</td><td>The bottom of the <span style="font-weight: bold; white-space: nowrap;">\d <em>tablename</em></span> output always shows indexes, as well as triggers, rules, and constraints</td></tr><tr><td><b>show triggers from <em>tablename</em>;</b>
<br>Display triggers on the given table</td><td><b>\d <em>tablename</em></b>
<br>(same)</td><td>See notes on <span style="font-weight: bold; white-space: nowrap;">show index</span> above</td></tr><tr class="alt"><td><b>show databases;</b>
<br>List all databases</td><td><b>\l</b>
<br>(same)</td><td>
</td></tr><tr><td>No equivalent</td><td><b>\dn</b>
<br>List all schemas</td><td>MySQL does not have the concept of schemas, but uses databases as a similar concept</td></tr><tr class="alt"><td><b>select version();</b>
<br>Show backend server version</td><td><b>select version();</b>
<br>(same)</td><td>
</td></tr><tr><td><b>select now();</b>
<br>Show current time</td><td><b>select now();</b>
<br>(same)</td><td>Postgres gives fractional seconds in the output</td></tr><tr class="alt"><td><b>select current_user;</b>
<br>Show the current user</td><td><b>select current_user;</b>
<br>(same)</td><td>
</td></tr><tr><td><b>select database();</b>
<br>Show the current database</td><td><b>select current_database();</b>
<br>(same)</td><td>
</td></tr><tr class="alt"><td><b>show create table <em>tablename;</em></b>
<br>Output a CREATE TABLE statement for the given table</td><td>No equivalent</td><td>The closest you can get with Postgres is to use <span style="font-weight: bold; white-space: nowrap;">pg_dump --schema-only -t <em>tablename</em></span></td></tr><tr><td><b>show engines;</b>
<br>List all server engines</td><td>No equivalent</td><td>Postgres does not use separate engines</td></tr><tr class="alt"><td><b>CREATE <em>object ...</em></b>
<br>Create an object: database, table, etc.</td><td><b>CREATE <em>object ...</em></b>
<br>Mostly the same</td><td>Most CREATE commands are similar or identical. Lookup specific help on commands (for example: <span style="font-weight: bold; white-space: nowrap;">\h CREATE TABLE</span>)</td></tr></tbody></table>

If there are any commands not listed you would like to see, or if there are errors in the above, please let me know. There are differences in how you invoke **mysql** and **psql**, and in the flags that they use, but that’s a topic for another day.

**Updates:** Added **PSQL_PAGER** and <b>\o |tee *filename*</b>, thanks to the Davids in the comments section. Added **\t** back in, per Joe’s comment.
