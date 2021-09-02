---
author: Szymon Lipiński
title: Pretty Printing JSONs in PostgreSQL
github_issue_number: 839
tags:
- postgres
- python
date: 2013-07-25
---

PostgreSQL has huge support for JSON type, [ like I wrote recently](/2013/06/postgresql-as-nosql-with-data-validation.html). It also has some operators for converting data to and from JSON, and the JSON type itself is great for ensuring that the JSON stored in database is always valid.

### Pretty Printing JSON

#### The Problem

JSONs can be quite complicated and can have multiple levels. Look at them as normal strings: printing the values can increase their readability. Let’s use a sample JSON like:

```
{"a":42, "d":{"a":10, "b":[1,2,3], "c":"x2"}, "x":"test", "p":[1,2,3,4,5]}
```

I think it would be much readable in the form:

```
 {
     "a": 42,
     "d": {
         "a": 10,
         "b": [
             1,
             2,
             3
         ],
         "c": "x2"
     },
     "p": [
         1,
         2,
         3,
         4,
         5
     ],
     "x": "test"
 }
```

#### The Solution

To generate this kind of format, I created a very simple Python function:

```
CREATE FUNCTION pp_json(j JSON, sort_keys BOOLEAN = TRUE, indent TEXT = '    ')
RETURNS TEXT AS $$
  import simplejson as json
  return json.dumps(json.loads(j), sort_keys=sort_keys, indent=indent)
$$ LANGUAGE PLPYTHONU;
```

It uses Python’s module simplejson for parsing the JSON from string to dictionary. The dictionary then is converted to JSON again, but this time in quite nicer format.

The function arguments allow to sort the JSON keys and set the string used for indentation, i.e. number of spaces.

This function can be used as:

```
x=# SELECT pp_json('{"a":42, "d":{"a":10, "b":[1,2,3], "c":"x2"}, "x":"test", "p":[1,2,3,4,5]}');
      pp_json
-------------------
 {                +
     "a": 42,     +
     "d": {       +
         "a": 10, +
         "b": [   +
             1,   +
             2,   +
             3    +
         ],       +
         "c": "x2"+
     },           +
     "p": [       +
         1,       +
         2,       +
         3,       +
         4,       +
         5        +
     ],           +
     "x": "test"  +
 }
```

### Logging Pretty JSON

Sometimes it can be needed not to get the JSON from a function, but write it to logs. For this I have another function:

```
CREATE FUNCTION pp_log_json(j JSON, sort_keys BOOLEAN = TRUE, indent TEXT = '    ')
RETURNS VOID AS $$
BEGIN
  RAISE NOTICE '%', pp_json(j, sort_keys, indent);
END;
$$ LANGUAGE PLPGSQL;
```

It uses the previous function for formatting the JSON and raises a notice, which should be stored in logs, depending on PostgreSQL logging settings.
