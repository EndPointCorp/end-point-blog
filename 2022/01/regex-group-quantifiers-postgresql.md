---
author: "Selvakumar Arumugam"
title: "How to use regular expression group quantifiers in PostgreSQL"
date: 2022-01-27
tags:
- postgres
- sql
- regex
- hl7
github_issue_number: 1828
---

![Side of brick building with windows and protruding roof, tiered shrubs in foreground, with a small corner of blue sky, clouds, and snowy mountaintop](/blog/2022/01/regex-group-quantifiers-postgresql/20220123_222150.webp)

<!-- Photo by Jon Jensen -->

I recently encountered a situation where it was necessary to extract address content from text in HL7 V2 format from a PostgreSQL table's column. The following example is representative:

```plain
||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|
```

In order to manipulate our example, the address section needs to be extracted from the HL7 V2 message PID segment for patient demographic information. The segments have delimiters for fields (`|`), components (`^`), subcomponents (`&`) and repetition (`~`).

Our example has only fields and components delimited by pipe (`|`) and caret (`^`). The address contains nine components delimited by `^`.

I hoped to do this by applying a regular expression (regex) because the address is in a standard format that regex can match with alphanumeric and caret repetition.

Here is my journey figuring out how to match the data I wanted.

### Regex pattern in grep

As a test, I got this regex working with the `grep` command, which successfully extracts the address section from the content:

```bash
$ content='||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|'
$ echo "$content" | grep -Eo "([A-Za-z0-9 #'.,/-]*\^){8}[A-Za-z0-9 ]*"
123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York
```

### PostgreSQL regex attempt

The PostgreSQL `regexp_matches` function supports extraction by pattern-matching data from the content. But when I used the same regex pattern with the `regexp_matches` function, instead of all eight groups, only the eighth value was returned:

```postgres
=# SELECT regexp_matches('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|', '([A-Za-z0-9 #''.,/-]*\^){8}[A-Za-z0-9 ]*', 'g');
 regexp_matches 
----------------
 {^}
(1 row)
```

More generally, our query is returning the *N*th matching group instead of returning all matching groups until the *N*th regex group. So if we try to fetch the text matching with 3 groups, the quantifier will return the third field of all match sections instead of the third group itself.

```postgres
=# SELECT regexp_matches('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|', '([A-Za-z0-9 #''.,/-]*\^){3}[A-Za-z0-9 ]*', 'g');
   regexp_matches   
--------------------
 {^}
 {^}
 {"New York City^"}
 {USA^}
(4 rows)
```

### PL/Perl function

Since that doesn’t satisfy our requirements, I tried using a Perl regex through my own PL/Perl function, and got the expected answer:

```postgres
=# CREATE OR REPLACE FUNCTION perl_regexp_matches (IN str text, IN pattern text) RETURNS text AS $$
    my ($input, $pattern) = @_;
    $output = [$input =~ m/($pattern)/];
    return $output->[0]
$$ LANGUAGE plperl;

=# SELECT perl_regexp_matches('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|', '([A-Za-z0-9 #''.,/-]*\^){8}[A-Za-z0-9 ]*');
                    perl_regexp_matches
------------------------------------------------------------
 123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York
(1 row)
```

But I researched further for a simple solution to achieve the result without using a custom function and the PL/Perl extension.

### PostgreSQL regex solution

In Postgres regex syntax, parentheses `()` create a numbered capture group which leads to returning the contained matching results.

To get the entire matching data, the regex should have a question mark and a colon (`?:`) added at the beginning of the regex pattern to create a non-capturing group. Then because no group is capturing, instead the complete match is returned:

```postgres
=> SELECT regexp_matches('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|', '(?:[A-Za-z0-9 #''.,/-]*\^){8}[A-Za-z0-9 ]*');
                         regexp_matches                         
----------------------------------------------------------------
 {"123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York"}
(1 row)
```

That turns out to be what was happening with my PL/Perl function where `m/($pattern)/` captures the entire match, and what `grep` was doing because of its option `-o` or `--only-matching`, which prints the matching part of the lines rather than its default of printing the entire line.

And we can also use the Postgres function `substring` to return the bare text itself instead of arrays as `regexp_matches` does:

```postgres
=# SELECT substring('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|' FROM '(?:[A-Za-z0-9 #''.,/-]*\^){8}[A-Za-z0-9 ]*');
                         substring
------------------------------------------------------------
 123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York
(1 row)
```

### Reference

* [HL7 International website](https://www.hl7.org/about/)
* [PostgreSQL POSIX regular expressions documentation](https://www.postgresql.org/docs/current/functions-matching.html#FUNCTIONS-POSIX-REGEXP)
