---
author: Greg Sabino Mullane
gh_issue_number: 1317
tags: postgres, unicode, perl
title: Postgres migrating SQL_ASCII to UTF-8 with fix_latin
---

<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2017/07/21/postgres-migrating-sqlascii-to-utf-8/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" data-original-height="395" data-original-width="500" src="/blog/2017/07/21/postgres-migrating-sqlascii-to-utf-8/image-0.jpeg"/></a><br/><small>(<a href="https://flic.kr/p/fZRp6G">photograph</a> by <a href="https://www.flickr.com/people/usoceangov/">NOAA National Ocean Service</a>)</small></div>

Upgrading [Postgres](https://www.postgresql.org/) is not quite as painful as it used to be, thanks
primarily to the [pg_upgrade program](https://www.postgresql.org/docs/current/static/pgupgrade.html), but there are times when it simply cannot be used.
We recently had an existing End Point client come to us requesting help upgrading from their current
Postgres database (version 9.2) to the latest version (9.6 — but soon to be 10). They also wanted
to finally move away from their SQL_ASCII encoding to [UTF-8](https://en.wikipedia.org/wiki/UTF-8). As this meant
that pg_upgrade could not be used, we also took the opportunity to enable
checksums as well (this change cannot be done via pg_upgrade). Finally, they
were moving their database server to new hardware. There were many lessons learned and bumps
along the way for this migration, but for this
post I’d like to focus on one of the most vexing problems, the database encoding.

When a Postgres database is created, it is set to a specific encoding. The most
common one (and the default) is “UTF8”.  This covers
99% of all user’s needs. The second most common one is the
poorly-named “SQL_ASCII” encoding, which should be named
“DANGER_DO_NOT_USE_THIS_ENCODING”, because it causes nothing but trouble.
The SQL_ASCII encoding basically means no encoding at all, and simply stores
any bytes you throw at it. This usually means the database ends up containing a
whole mess of different encodings, creating a “byte soup” that will be
difficult to sanitize by moving to a real encoding (i.e. UTF-8).

Many tools exist which convert text from one encoding to another. One of the
most popular ones on Unix boxes is “iconv”. Although this program works great
if your source text is using one encoding, it fails when it encounters
byte soup.

For this migration, we first did a [pg_dump](https://www.postgresql.org/docs/current/static/app-pgdump.html) from the old database to
a newly created UTF-8 test database, just to see which tables had encoding problems.
Quite a few did — but not all of them! — so we wrote a script to import tables
in parallel, with some filtering for the problem ones. As mentioned above,
iconv was not particularly helpful: looking at the tables closely showed
evidence of many different encodings in each one: Windows-1252, ISO-8859-1,  Japanese,
Greek, and many others. There were even large bits that were plainly
binary data (e.g. images) that simply got shoved into a text field somehow.
This is the big problem with SQL_ASCII: it accepts *everything*, and does no
validation whatsoever. The iconv program simply could not handle these tables,
even when adding the //IGNORE option.

To better explain the problem and the solution, let’s create a small text
file with a jumble of encodings. Discussions of how UTF-8 represents
characters, and its interactions with Unicode, are avoided here, as
Unicode is a dense, complex subject, and this article is dry enough already. :)

First, we want to add some items using the encodings ‘Windows-1252’ and ‘Latin-1’. These encoding
systems were attempts to extend the basic ASCII character set to include more characters. As these encodings
pre-date the invention of UTF-8, they do it in a very inelegant (and incompatible)
way. Use of the “echo” command is a great way to add arbitrary bytes to a file as it
allows direct hex input:

```
$ echo -e "[Windows-1252]   Euro: \x80   Double dagger: \x87" > sample.data
$ echo -e "[Latin-1]   Yen: \xa5   Half: \xbd" >> sample.data
$ echo -e "[Japanese]   Ship: \xe8\x88\xb9" >> sample.data
$ echo -e "[Invalid UTF-8]  Blob: \xf4\xa5\xa3\xa5" >> sample.data
```

This file looks ugly. Notice all the “wrong” characters when we simply view the file directly:

```
$ cat sample.data
[Windows-1252]   Euro: �   Double dagger: �
[Latin-1]   Yen: �   Half: �
[Japanese]   Ship: 船
[Invalid UTF-8]  Blob: ����
```

Running iconv is of little help:

```text
## With no source encoding given, it errors on the Euro:
$ iconv -t utf8 sample.data >/dev/null
iconv: illegal input sequence at position 23

## We can tell it to ignore those errors, but it still barfs on the blob:
$ iconv -t utf8//ignore sample.data >/dev/null
iconv: illegal input sequence at position 123

## Telling it the source is Window-1252 fixes some things, but still sinks the Ship:
$ iconv -f windows-1252 -t utf8//ignore sample.data
[Windows-1252]   Euro: €   Double dagger: ‡
[Latin-1]   Yen: ¥   Half: ½
[Japanese]   Ship: èˆ¹
[Invalid UTF-8]  Blob: ô¥£¥
```

After testing a few other tools, we discovered the nifty [Encoding::FixLatin](https://metacpan.org/pod/Encoding::FixLatin), a Perl module which provides a command-line program called “fix_latin”. Rather than being authoritative like iconv, it tries its best to fix things up with educated guesses. Its documentation gives a good summary:

>  The script acts as a filter, taking source data which may contain a mix of
>  ASCII, UTF8, ISO8859-1 and CP1252 characters, and producing output will be
>  all ASCII/UTF8.
>
>  Multi-byte UTF8 characters will be passed through unchanged (although
>  over-long UTF8 byte sequences will be converted to the shortest normal
>  form). Single byte characters will be converted as follows:
>
>  0x00 - 0x7F   ASCII - passed through unchanged
>  0x80 - 0x9F   Converted to UTF8 using CP1252 mappings
>  0xA0 - 0xFF   Converted to UTF8 using Latin-1 mappings


While this works great for fixing the Windows-1252 and Latin-1 problems (and
thus accounted for at least 95% of our table’s bad encodings), it still allows
“invalid” UTF-8 to pass on through. Which means that Postgres will still refuse
to accept it. Let’s check our test file:

```text
$ fix_latin sample.data
[Windows-1252]   Euro: €   Double dagger: ‡
[Latin-1]   Yen: ¥   Half: ½
[Japanese]   Ship: 船
[Invalid UTF-8]  Blob: ����

## Postgres will refuse to import that last part:
$ echo "SELECT E'"  "$(fix_latin sample.data)"  "';" | psql
ERROR:  invalid byte sequence for encoding "UTF8": 0xf4 0xa5 0xa3 0xa5

## Even adding iconv is of no help:
$ echo "SELECT E'"  "$(fix_latin sample.data | iconv -t utf-8)"  "';" | psql
ERROR:  invalid byte sequence for encoding "UTF8": 0xf4 0xa5 0xa3 0xa5
```

The [UTF-8 specification](https://tools.ietf.org/html/rfc3629) is rather dense and puts many requirements on
encoders and decoders. How well programs implement these requirements (and optional
bits) varies, of course. But at the end of the day, we needed that data to go
into a UTF-8 encoded Postgres database without complaint. When in doubt, go
to the source! The relevant file in the Postgres source code responsible for
rejecting bad UTF-8 (as in the examples above) is src/backend/utils/mb/wchar.c
Analyzing that file shows a small but elegant piece of code whose job is
to ensure only “legal” UTF-8 is accepted:

```
bool
pg_utf8_islegal(const unsigned char *source, int length)
{
  unsigned char a;

  switch (length)
  {
    default:
      /* reject lengths 5 and 6 for now */
      return false;
    case 4:
      a = source[3];
      if (a < 0x80 || a > 0xBF)
        return false;
      /* FALL THRU */
    case 3:
      a = source[2];
      if (a < 0x80 || a > 0xBF)
        return false;
      /* FALL THRU */
    case 2:
      a = source[1];
      switch (*source)
      {
        case 0xE0:
          if (a < 0xA0 || a > 0xBF)
            return false;
          break;
        case 0xED:
          if (a < 0x80 || a > 0x9F)
            return false;
          break;
        case 0xF0:
          if (a < 0x90 || a > 0xBF)
            return false;
          break;
        case 0xF4:
          if (a < 0x80 || a > 0x8F)
            return false;
          break;
        default:
          if (a < 0x80 || a > 0xBF)
            return false;
          break;
      }
      /* FALL THRU */
    case 1:
      a = *source;
      if (a >= 0x80 && a < 0xC2)
        return false;
      if (a > 0xF4)
        return false;
      break;
  }
  return true;
}
```

Now that we know the UTF-8 rules for Postgres, how do we ensure our data follows it?
While we could have made another standalone filter to run after fix_latin, that would
increase the migration time. So I made a quick patch to the fix_latin program itself, rewriting
that C logic in Perl. A new option “--strict-utf8” was added. Its job is to simply enforce the
rules found in the Postgres source code. If a character is invalid, it is replaced with
a question mark (there are other choices for a replacement character, but we decided simple
question marks were quick and easy — and the surrounding data was unlikely to be read or even used anyway).

Voila! All of the data was now going into Postgres without a problem. Observe:

```text
$ echo "SELECT E'"  "$(fix_latin  sample.data)"  "';" | psql
ERROR:  invalid byte sequence for encoding "UTF8": 0xf4 0xa5 0xa3 0xa5

$ echo "SELECT E'"  "$(fix_latin --strict-utf8 sample.data)"  "';" | psql
                   ?column?
----------------------------------------------
  [Windows-1252]   Euro: €   Double dagger: ‡+
 [Latin-1]   Yen: ¥   Half: ½                +
 [Japanese]   Ship: 船                       +
 [Invalid UTF-8]  Blob: ????
(1 row)
```

What are the lessons here? First and foremost, ***never*** use SQL_ASCII. It’s outdated,
dangerous, and will cause much pain down the road. Second, there are an amazing number
of client encodings in use, especially for old data, but the world has pretty much standardized
on UTF-8 these days, so even if you are stuck with SQL_ASCII, the amount of Windows-1252 and
other monstrosities will be small. Third, don’t be afraid to go to the source. If Postgres
is rejecting your data, it’s probably for a very good reason, so find out exactly why.
There were other challenges to overcome in this migration, but the encoding was certainly
one of the most interesting ones. Everyone, the client and us, is very happy to finally
have everything using UTF-8!
