---
author: Josh Tolley
title: Creativity with fuzzy string search
github_issue_number: 338
tags:
- open-source
- postgres
- search
date: 2010-08-10
---

<img alt="magnifying glass" border="0" src="/blog/2010/08/creativity-with-fuzzy-string-search/image-0.png" style="float:left; margin:0 10px 10px 0; width:234px; height:320px"/></a>

PostgreSQL provides a useful set of contrib modules for “fuzzy” string searching; that is, searching for something that sounds like or looks like the original search key, but that might not exactly match. One place this type of searching shows up frequently is when looking for peoples’ names. For instance, a receptionist at the dentist’s office doesn’t want to have to ask for the exact spelling of your name every time you call asking for an appointment, so the scheduling application allows “fuzzy” searches, and the receptionist doesn’t have to get it exactly right to find out who you really are. The PostgreSQL documentation provides an excellent introduction to the topic in terms of the available modules; [This blog post](https://www.postgresonline.com/journal/index.php?/archives/158-Where-is-soundex-and-other-warm-and-fuzzy-string-things.html) also demonstrates some of the things they can do.

The [TriSano](https://web.archive.org/web/20100612002539/http://www.trisano.org/) application was originally written to use soundex search alone to find patient names, but that proved insufficient, particularly because common-sounding last names with unusual spellings would be ranked very poorly in the search results. Our solution, which has worked quite well in practice, involved creative use of PostgreSQL’s full-text search combined with the [pg_trgm contrib module](https://www.postgresql.org/docs/current/static/pgtrgm.html).

A trigram is a set of three characters. In the case of pg_trgm, it’s three adjacent characters taken from a given input text. The pg_trgm module provides easy ways to extract all possible trigrams from an input, and compare them with similar sets taken from other inputs. Two strings that generate similar trigram lists are, in theory, similar strings. There’s no particular reason you couldn’t use two, four, or some other number of characters instead of **tri**grams, but you’d trade sensitivity and variability. And as the name implies, pg_trgm only supports trigrams.

Straight trigram search didn’t buy us much on top of soundex, so we got a bit more creative. A trigram is just a set of three characters, which looks pretty much just like a word, so we thought we’d try using PostgreSQL’s full text search on trigram data. Typically full text search has a list of “stop words”: un-indexed words judged too common and too short to contribute meaningfully to an index. Our words would all be three characters long, so we had to create a new text search configuration using a dictionary with an empty stop word list. With that text search configuration, we could index trigrams effectively.

This search helped, but wasn’t quite good enough. We finally borrowed a simplified version of a data mining technique called [“boosting”](https://en.wikipedia.org/wiki/Boosting_(machine_learning)), which involves using multiple “weak” classifiers or searchers to create one relatively good result set. We combined straightforward trigram, soundex, and metaphone searches with a normal full text search of the unmodified name data and a full text search over the trigrams generated from the names. The data sizes in question aren’t particularly large, so this amount of searching hasn’t proven unsustainably taxing on processor power, and it provides excellent results. The code is [on github](https://github.com/csinitiative/trisano/blob/master/webapp/db/name_search.sql); feel free to try it out.

Update: One of the comments suggested a demonstration of the results, which of course makes perfect sense. So I resurrected some of the scripts I used when developing the technique. In addition to the scripts used to install the fuzzystrmatch and pg_trgm modules and the name_search.sql script linked above, I had a script that populated the *people* table with a bunch of fake names. Then, it’s easy to test the search mechanism like this:

```plain
select * from search_for_name('John Doe')
as a(id integer, last_name text, first_name text, sources text[], rank double precision);

 id  |  last_name  | first_name |                     sources                     |        rank        
-----+-------------+------------+-------------------------------------------------+--------------------
 167 | Krohn       | Javier     | {trigram_fts,name_trgm,trigram_fts,trigram_fts} |  0.281305521726608
 228 | Jordahl     | Javier     | {trigram_fts,name_trgm,trigram_fts}             |  0.237995445728302
  59 | Pesce       | Dona       | {trigram_fts}                                   |  0.174265757203102
 185 | Finchum     | Dona       | {trigram_fts}                                   |  0.174265757203102
 104 | Rumore      | Dona       | {trigram_fts}                                   |  0.174265757203102
 250 | Dumond      | Julio      | {name_trgm,trigram_fts,trigram_fts}             |   0.16849160194397
 200 | Dedmon      | Javier     | {name_trgm,trigram_fts,trigram_fts}             |  0.163729697465897
 230 | Dossey      | Malinda    | {name_trgm,trigram_fts}                         |  0.158055320382118
  50 | Dress       | Darren     | {name_trgm,trigram_fts}                         |  0.153293430805206
 136 | Doshier     | Neil       | {name_trgm,trigram_fts}                         |  0.148531511425972
 165 | Donatelli   | Lance      | {name_trgm,trigram_fts}                         |  0.132845237851143
 280 | Dollinger   | Clinton    | {name_trgm,trigram_fts}                         |  0.132845237851143
 273 | Dimeo       | Milagros   | {name_trgm,trigram_fts}                         | 0.0866267532110214
  49 | Dawdy       | Christian  | {name_trgm,trigram_fts}                         | 0.0866267532110214
 298 | Elswick     | Jami       | {trigram_fts}                                   | 0.0845221653580666
```

This isn’t all the results it returned, but it gives an idea what the results look like. The rank value ranks results based on the rankings given by each of the underlying search methods, and the sources column shows which of the search methods found this particular entry. Some search methods may show up twice, because that search method found multiple matches between the input text and the result record. These results don’t look particularly good, because there isn’t really a good match for “John Doe” in the data set. But if I horribly misspell “Jamie Elswick”, the search does a good job:

```plain
select * from search_for_name('Jomy Elswik') as a(id integer, last_name text,                                                 
first_name text, sources text[], rank double precision)

 id  |  last_name  | first_name |                     sources                     |        rank        
-----+-------------+------------+-------------------------------------------------+--------------------
 298 | Elswick     | Jami       | {trigram_fts,name_trgm,trigram_fts,trigram_fts} |  0.480943143367767
 312 | Elswick     | Kurt       | {name_trgm,trigram_fts}                         |  0.381967514753342
 228 | Jordahl     | Javier     | {trigram_fts,name_trgm,trigram_fts}             |  0.197063013911247
 403 | Walberg     | Erik       | {trigram_fts}                                   |  0.145491883158684
 309 | Hammaker    | Erik       | {trigram_fts}                                   |  0.145491883158684
```
