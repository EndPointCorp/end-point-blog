---
author: Jon Jensen
gh_issue_number: 276
tags: database, perl, postgres
title: PostgreSQL UTF-8 Conversion
---

It’s becoming increasingly common for me to be involved in conversion of an old version of PostgreSQL to a new one, and at the same time, from an old “SQL_ASCII” encoding (that is, undeclared, unvalidated byte soup) to UTF-8.

Common ways to do this are to run pg_dumpall and then pipe the output through iconv or recode. When your source encoding is all pure ASCII, you don’t need to do even that. When it’s really all Windows-1252 (a superset of Latin-1 aka ISO-8859-1) it’s easy.

But often, the data is stored in various unknown encodings from several sources over the course of years, including some that’s already in UTF-8. When you convert with iconv, it dies with an error at the first problem, whereas recode will let you ignore encoding problems, but that leaves you with junk in your output.

The case I’m often encountering is fairly easy, but not perfect: Lots of ASCII, some Windows-1252, and some UTF-8. Since both pure ASCII and UTF-8 can be mechanistically detected, I put together this script to do the detection. It’s Perl and uses the nice [IsUTF8 module](https://metacpan.org/pod/IsUTF8) to do its character encoding detection:

<script src="https://gist.github.com/327332.js"></script>

Pipe input to the script. It handles one line at a time. When run with any arguments (such as --test) it will swallow pure ASCII lines, write lines it thinks are valid UTF-8 to stderr, and will convert the remaining presumed Windows-1252 lines to stdout, for manual examination.

If its guesses look correct, run it again with no arguments, and it will write all 3 types of encoding to stdout, ready for input to psql in your new UTF-8 encoded database.

(Don’t forget to munge your pg_dump file to remove any hardcoded declarations of “SQL_ASCII” encoding from CREATE DATABASE statements, or otherwise make sure your database actually is created with UTF-8 encoding!)
