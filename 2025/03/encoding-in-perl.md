---
author: "Marco Pessotto"
date: 2025-03-05
title: "Handling text encoding in Perl"
tags:
 - perl
 - web
 - encoding
 - utf8
 - unicode
---

![Hieroglyphics](/blog/2025/03/encoding-in-perl/hieroglyphics-1246926-pxhere-com.webp)

<!-- Photo https://pxhere.com/en/photo/1246926 CC0 Public Domain -->


When we are dealing with legacy applications, it's very possible
that the code we are looking at does not have a clear understanding of
the problems related to plain text handling.

In this article we are going to focus on Perl, but the other languages
face the same problems.

In 2025, after more than 30 years since Unicode was born, how is that
possible that our old application survived ignoring or working around
the whole issue?

Well, if your audience is mainly English speaking, it's possible that
you just experience glitches sometimes, with some characters like
typographical quotes, non breaking spaces, etc. which are not really
mission-critical.

If, on the contrary, you need to deal every day with diacritics or
even different languages (say, Italian and Slovenian), your
application simply won't survive without a good understanding of
encoding.

### Back to the bytes

As we know, machines work with numbers and bytes. A string of text is
made of bytes, and each of them is 8 bits (a 0 or a 1). So one byte
allows 256 possible combinations.

Plain ASCII is made by 128 characters (7 bits), so it fits nicely in
one byte, leaving room for more. One character is exactly one byte,
and one byte carries a character.

However, ASCII is not enough for most of the languages based on the
Latin alphabet, because usually they use diacritics like these: é à č
ž.

To address this problem, the
[ISO 8859](https://en.wikipedia.org/wiki/ISO/IEC_8859) encoding
standards appeared (there are others, like the Windows code pages,
using the same idea, but of course using different code points...),
which use the free combinations not occupied by the ASCII encoding,
but still using a single byte for each character and allowing 256
possible characters. That's better, but not great. It suffices to
handle text in a couple of languages if they share the same
characters, but not more. For this reason, there are the various IS0
8859 encoding standards (8859-1, 8859-2, etc.), one for each group of
related languages (e.g. 8859-1 is for Western Europe, 8859-2 for
Central Europe and so on, and even revisions of the same encoding,
like 8859-15 and 8859-16).

The problem is that if you have a random string, you have to guess
which is the correct encoding. Is this character a "È" or "Č"? You
need to look at the context (which language is this?) or search for
an encoding declaration. Most important, you are simply not able to
type È and Č in the same plain text document. If your company works in
Italy using the 8859-15 encoding, it means you can't even accept the
correct name of a customer from, say, Slovenia, a neighbour country,
because the encoding simply doesn't have a place for those characters
with the caron like "č", and you have to work around this real
problem.

So finally came the [Unicode](https://en.wikipedia.org/wiki/) age.
This standard allows for more than a million characters, which
should be enough. You can finally type English, Italian, Russian,
Arabic and Emojis all in the same plain text. This is truly great, but
it creates a complication for the programmer: the assumption that one
byte is one character is not true anymore. The common encoding is
UTF-8, which is also backward compatible with ASCII. This means that
if you have an ASCII text, it is also valid UTF-8. Any other character
which is not ASCII, will instead take from two to three bytes and the
programming language needs to be aware of this.

### Into the language and back to the world

Text manipulation is a very common task. If you need to process a
string, say "ÈČ", like in this document, you should be able to tell
that it is a string with two characters representing two letters. You
want to be able to use regular expression on it, and so on.

Now, if we read it as a string of bytes, we get 4 of them and the
newline, which is not what we want.

Let's see an example:

```perl
#!/usr/bin/env perl

use strict;
use warnings;
use Data::Dumper::Concise;

# sample.txt contains ÈČ and a new line

{
    open my $fh, '<', 'sample.txt';
    while (my $l = <$fh>) {
        print $l;
        if ($l =~ m/\w\w/) {
            print "Found two characters\n"
        }
        print Dumper($l);
    }
    close $fh;
}
      
{
    open my $fh, '<:encoding(UTF-8)', 'sample.txt';
    while (my $l = <$fh>) {
        print $l;
        if ($l =~ m/\w\w/) {
            print "Found two characters\n"
        }
        print Dumper($l);
    }
    close $fh;
}
```

This is the output:

```
ÈČ
"\303\210\304\214\n"
Wide character in print at test.pl line 24, <$fh> line 1.
ÈČ
Found two characters
"\x{c8}\x{10c}\n"
```

In the first block the file is read verbatim, without any decoding.
The regular expression doesn't work, we have basically 4 bytes which
don't seem to mean much.

In the second block we decoded the input, converting it in the Perl
internal representation. Now we can use regular expressions and have a
consistent approach to text manipulation.

However, we got a warning:

```
Wide character in print at test.pl line 25, <$fh> line 1
```

That's because we printed something to the screen, but given that the
string is now made by characters (decoded for internal use), Perl
warns us that we need to encode it back to bytes (for the outside
world to consume). A wide character is basically a character which
needs to be encoded.

This can be done either with:

```perl
use strict;
use warnings;
use Encode;
print encode("UTF-8", "\x{c8}\x{10c}\n");
```

Or, better, declaring the global encoding for the standard output:

```perl
use strict;
use warnings;
binmode STDOUT, ":encoding(UTF-8)";
print "\x{c8}\x{10c}\n";
```

So, the golden rule is:

 - decode the string on input and get characters out of bytes
 - work with it in your program as a string of characters
 - encode the string on output
 
Any other approach is going to lead to double encoded characters (when
you see things like Ã and Ä in English text, that's a clear symptom of
this), corrupted text, confusion.
 
### Encoding strategies

If you are dealing with standard input/output on the shell, you should
have this in your script:

```
binmode STDIN,  ":encoding(UTF-8)";
binmode STDOUT, ":encoding(UTF-8)";
binmode STDERR, ":encoding(UTF-8)";
```

So you're decoding on input and encoding on output automatically.

For files, you can add the layer in the second argument of `open` like
in the sample script above, or use a more handy module like
`Path::Tiny`, which provides methods like `slurp_utf8` and `spew_utf8`
to read and write files using the correct encoding.

The interactions with web frameworks should always happen with the
internal Perl representation. When you receive the input from a form,
it *should be considered already decoded*. It's also responsibility of
the framework to handle the encoding on output. Here at End Point we
have many Interchange applications. Interchange *can* support this,
via the `MV_UTF8` variable.

The same rules applies to databases. It's responsibility of the driver
to take your strings and encode/decode them when talking to the
database. E.g. [DBD::Pg](https://metacpan.org/pod/DBD::Pg) has the
`pg_enable_utf8` option, while
[DBD::mysql](https://metacpan.org/pod/DBD::mysql) has
`mysql_enable_utf8`. These options should usually be turned on or off
explicitly. Not specifying the option is usually source of confusion
because of the heuristic approach they take.

### Debugging strategies

It may not be the most correct approach, but that's what I've been
using for more than a decade and it works, and it's simple to use
`Data::Dumper` or `Data::Dumper::Concise` and call `Dumper` on the
string you want to examine.

If you see the hexadecimal codepoints like `\x{c8}\x{10c}`, it means
the string is decoded and you're working with the characters, if you
see the raw bytes or characters with diacritics (the terminal is
interpreting the bytes and showing you the characters), you're dealing
with an encoded string. If you see weird characters in English
context, it probably means the text has been encoding more than once.

### Migrate a web application to Unicode

If you're still using legacy encoding systems like 8859 or the similar
Windows code pages, or worse, you simply don't know and you're relying
on the browsers' heuristics (they're quite good at that) you need to
handle the input and the output correctly along the whole application:

 - convert the templates from the encoding you are using to UTF-8
   (`iconv` should do the trick).
 - inspect and possibly convert the existing DB data
 - make sure the DB drivers handle the I/O correctly
 - make sure the web framework is decoding the input and encoding the output
 - make sure the files you read and write are correctly handled
 - clean up any workaround you may have had in place to make it so far
 
This can look, and is, a challenging task, but it's totally worth
it, as fancy characters nowadays are the norm. Typographical quotes
like “this” and ‘this’ are very common and inserted by word processors
automatically. So are Emojis. People and customers simply expect them
to work.

### Band-aids

If your client is on a budget or can't deal with a large upgrade like
this one, which has the potential to be disruptive and expose bugs
which are lurking around, you can try to degrade the Unicode
characters to ASCII with tools like
[Text::Unidecode](https://metacpan.org/pod/Text::Unidecode) (which, by
the way, has been ported to other languages as well). So typographical
quotes will became the ASCII plain ones, diacritics will be stripped,
and even various characters will get their ASCII representation. Not
great, but better than nothing!
