---
author: Josh Williams
gh_issue_number: 846
tags: postgres, unicode
title: The Un-unaccentable Character
---



I typed "Unicode" into an online translator, and it responded saying it had no idea what the language was but it roughly translates to "Surprise!"

Recently a client sent over a problem getting some of their Postgres data through an ASCII-only ETL process.  They only needed to worry about some occasional accent marks, and not any of the more uncommon or odd Unicode characters, thankfully. ☺ Or so we thought.  The [unaccent extension](http://www.postgresql.org/docs/current/interactive/unaccent.html) was a great starting point, but the problem they sent over boiled down to this:

```
postgres=# SELECT unaccent('e é ѐ');
 unaccent 
----------
 e e ѐ
(1 row)
```

unaccent() worked, except for that odd ѐ, which then failed the ETL task.  That's exactly what unnaccent is supposed to handle.  The character è even appears in the unaccent.rules file.  So what gives?

Well, if you're in the habit of piping blog posts through hexdump (and who isn't?) then you probably already know the answer.  But even if not, you may already suspect that we're dealing with a different character that just looks the same.  And you'd be right.  Specifically, the [è in the rules file](http://unicode.org/cldr/utility/character.jsp?a=00E8) is from the more common Latin set, and the [ѐ that doesn't work](http://unicode.org/cldr/utility/character.jsp?a=0450) is from the Cyrillic set.  Pretty much visually identical, but completely separate characters.

### Augmenting the unaccent dictionary:

Speaking more generically, ideally a simple UPDATE statement with a replace() will correct it in the source data.  And a trigger doing the same will keep it tidy from that point forward.

But if you can't or just don't want to go down that path, the unaccent extension dictionary can be edited.  On my system it's found in /usr/share/postgresql/9.3/tsearch_data/unaccent.rules.  It has a very simple format.

1. Make a copy of the file before you edit it.  Updated packages or new deployments if you're compiling from source will wipe out any changes to the unaccent.rules file.

```
root:~# cp /usr/share/postgresql/9.3/tsearch_data/{unaccent,extended}.rules
```

2. Add a line including the character to translate.  To handle our example above, add:

```
ѐ e
```

3. In Postgres, create a new dictionary to load in those rules.

```
db=# CREATE TEXT SEARCH DICTIONARY extended (TEMPLATE=unaccent, RULES='extended');
CREATE TEXT SEARCH DICTIONARY
```

Note that 'extended' above will point to the extended.rules file.

4. Call unaccent() specifying the newly added dictionary:

```
db=# SELECT unaccent('extended', 'e é ѐ');
 unaccent 
----------
 e e e
(1 row)
```

5+. Note that subsequent changes won't automatically appear.  To update the in-database version, after you make any changes to the rules file run:

```
db=# ALTER TEXT SEARCH DICTIONARY extended (RULES='extended');
ALTER TEXT SEARCH DICTIONARY
```

