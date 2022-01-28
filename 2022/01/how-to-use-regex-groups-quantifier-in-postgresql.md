---
author: "Selvakumar Arumugm"
title: "How to use regex groups quantifier in PostgreSQL"
date: 2022-01-27
tags:
- postgres
- sql
- regex
- hl7
github_issue_number: 
---

I recently encountered a situation where it was necessary to extract address content from a
specific format (HL7 V2) of text on a PostgreSQL table column. This became possible through applying a regex as the address contains a standard format that regex can match. The following example will be used to demonstrate the process: 

```
||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|
```
### Perl Regex Pattern

In order to manipulate our example, the address section needs to be extracted from the table. HL7 have PID segment for the patient demographic information in HL7 V2 message. The segments have delimiters for fields (|), components(^), subcomponents(&) and repetition(~). The following sample data have only fields and components delimited by pipe (|) and caret (^). Uniquely, the address contains nine components(^). Therefore, a regex group with alphanumeric and caret repetition is required in order to match our address. The regex is tested through the grep command perl regex option (-P, --perl-regexp) and successfully extracts the address section from the content.

```bash
$ content='||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|'

$ echo $content | grep -Po '([A-Za-z0-9 ]*\^){8}'
123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^
```

### PostgreSQL Regex

PostgreSQL's `regexp_matches` function supports the pattern extraction by matching data from the content. While the same perl regex pattern was added to the `regexp_matches` function, instead of all eight groups, only the eighth value was returned. 

```postgres
=# SELECT REGEXP_MATCHES('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|', E'([A-Za-z0-9 #''.,/-]*\\^){8}[A-Za-z0-9 ]*', 'g');
 regexp_matches 
----------------
 {^}
(1 row)
```

More generally, our query is returning the Nth matching group instead of returning all matching groups until the Nth regex group. So if we try to fetch the text matching with 3 groups, the quantifier three will return the third field of all match sections instead of the third group itself.

```postgres
=# SELECT REGEXP_MATCHES('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|', E'([A-Za-z0-9 #''.,/-]*\\^){3}[A-Za-z0-9 ]*', 'g');
   regexp_matches   
--------------------
 {^}
 {^}
 {"New York City^"}
 {USA^}
(4 rows)
```

### PLPERL Function

Since the regexp_matches function doesn’t satisfy our requirements, I have attempted to use perl regex through the plperl function. The plperl function is created with the perl regex pattern and the plperl regex function produced expected answer.

```postgres
=# CREATE OR REPLACE FUNCTION perl_regexp_matches (IN str text, IN pattern text) RETURNS text AS $$
    # PL/Perl function body
    my ($input, $pattern) = @_;
    $output = [$input =~ m/($pattern)/];
    return $output->[0]
$$ LANGUAGE plperl;

=# SELECT perl_regexp_matches('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|', '([A-Za-z0-9 #''.,/-]*\^){8}[A-Za-z0-9 ]*');
                    perl_regexp_matches
 perl_regexp_matches 
                    perl_regexp_matches
------------------------------------------------------------
 123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York
(1 row)
```

But researched for simple solution to achieve the result without using function and plperl extension.

### Solution

In regular Postgres expressions, parentheses ( ) create a numbered capture group which leads to returning the quantitative matching results. To get the entire matching data, the regex should have a question mark (?) and a colon (:) added at the beginning of the regex pattern to create a non-capturing group to receive the complete matching group.

```postgres
=# SELECT substring('||121212^^^2^ID 1|676767||SELVA^KUMAR^^^^|19480203|M||B||123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York||123456-7890|||M|NON|4000|' FROM '(?:[A-Za-z0-9 #''.,/-]*\^){8}[A-Za-z0-9 ]*');
                         substring
------------------------------------------------------------
 123456 SAMPLE ROAD^^New York City^NY^12345^USA^H^^New York
(1 row)
```

The regex quantifiers can be skipped by using ?: to return the matching regex group.
