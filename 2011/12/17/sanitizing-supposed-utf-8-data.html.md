---
author: Jon Jensen
gh_issue_number: 528
tags: perl, postgres, tips, tools, unicode
title: Sanitizing supposed UTF-8 data
---



As time passes, it's clear that Unicode has won the character set encoding wars, and UTF-8 is by far the most popular encoding, and the expected default. In a few more years we'll probably find discussion of different character set encodings to be arcane, relegated to "data historians" and people working with legacy systems.

But we're not there yet! There's still lots of migration to do before we can forget about everything that's not UTF-8.

Last week I again found myself converting data. This time I was taking data from a PostgreSQL database with no specified encoding (so-called "SQL_ASCII", really just raw bytes), and sending it via JSON to a remote web service. JSON uses UTF-8 by default, and that's what I needed here. Most of the source data was in either UTF-8, ISO Latin-1, or Windows-1252, but some was in non-Unicode Chinese or Japanese encodings, and some was just plain mangled.

At this point I need to remind you about one of the most unusual aspects of UTF-8: It has limited valid forms. Legacy encodings typically used all or most of the 255 code points in their 8-byte space (leaving point 0 for traditional ASCII NUL). While UTF-8 is compatible with 7-bit ASCII, it does not allow any possible 8-bit byte in any position. See [the Wikipedia summary of invalid byte sequences](http://en.wikipedia.org/wiki/UTF-8#Invalid_byte_sequences) to know what can be considered invalid.

We had no need to try to fix the truly broken data, but we wanted to convert everything possible to UTF-8 and at the very least guarantee no invalid UTF-8 strings appeared in what we sent.

I previously wrote about [converting a PostgreSQL database dump to UTF-8](http://blog.endpoint.com/2010/03/postgresql-utf-8-conversion.html), and used the Perl CPAN module [IsUTF8](http://search.cpan.org/perldoc?IsUTF8).

I was going to use that again, but looked around and found an even better module, exactly targeting this use case: [Encoding::FixLatin](http://search.cpan.org/dist/Encoding-FixLatin/), by Grant McLean. Its documentation says it "takes mixed encoding input and produces UTF-8 output" and that's exactly what it does, focusing on input with mixed UTF-8, Latin-1, and Windows-1252.

It worked as advertised, very well. We would need to use a different module to convert some other legacy encodings, but in this case this was good enough and got the vast majority of the data right.

There's even a standalone [fix_latin](http://search.cpan.org/dist/Encoding-FixLatin/script/fix_latin) program designed specifically for processing Postgres pg_dump output from legacy encodings, with some nice examples of how to use it.

One gotcha is similar to a catch that David Christensen reported with the Encode module in a [blog post here about a year ago](http://blog.endpoint.com/2010/12/character-encoding-in-perl-decodeutf8.html): If the Perl string already has the UTF-8 flag set, Encoding::FixLatin immediately returns it, rather than trying to process it. So it's important that the incoming data be a pure byte stream, or that you otherwise turn off the UTF-8 flag, if you expect it to change anything.

Along the way I found some other CPAN modules that look useful for cases where I need more manual control than Encoding::FixLatin gives:

- [Search::Tools::UTF8](http://search.cpan.org/perldoc?Search::Tools::UTF8) - test for and/or fix bad ASCII, Latin-1, Windows-1252, and UTF-8 strings
- [Encode::Detect](http://search.cpan.org/perldoc?Encode::Detect) - use Mozilla's universal charset detector and convert to UTF-8
- [Unicode::Tussle](http://search.cpan.org/perldoc?Unicode::Tussle) - ridiculously comprehensive set of Unicode tools that has to be seen to be believed

Once again Perl's thriving open source/free software community made my day!


