---
author: Josh Williams
gh_issue_number: 567
tags: jquery, json, postgres
title: A Little Less of the Middle
---

<img alt="elephant" border="0" src="http://joshwilliams.name/monitoring/5258954374_52b77c8090_m.jpg"/>[elephant](http://www.flickr.com/photos/34968534@N07/5258954374/) by [esclarabunda](http://www.flickr.com/photos/34968534@N07/) 

I've been meaning to exercise a bit more.  You know, just to keep the mid section nice and trim.  But getting into that habit doesn't seem to be so easy.  Trimming middleware from an app, that's something that can catch my attention.

Something that caught my eye recently is a couple [recent commits](http://git.postgresql.org/pg/commitdiff/5384a73f98d9829725186a7b65bf4f8adb3cfaf1) to Postgres 9.2 that adds a JSON data type.  Or more specifically, the [second commit](http://git.postgresql.org/pg/commitdiff/39909d1d39ae57c3a655fc7010e394e26b90fec9) that adds a couple handy output functions: array_to_json() and row_to_json().  If you want to try it out on 9.1, those have been made available [as a backported extension](http://people.planetpostgresql.org/andrew/index.php?/archives/255-JSON-for-PG-9.2-...-and-now-for-9.1!.html).

Lately I've been doing a bit of work with jQuery, using it for AJAX-y stuff but passing [JSON](http://www.json.org/) around instead. (AJAJ?)  And traditionally that involves something in between the database and the client rewriting rows from one format to another.  Not that it's all that difficult; for example, in Python it's a simple module call:

```python
jsonresult = json.dumps(cursor.fetchall())
```

... assuming I don't have any columns needing processing: *TypeError: datetime.datetime(2012, 3, 09, 18, 34, 20, 730250, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=0, name=None)) is not JSON serializable*  Similarly in PHP I can stitch together a JSON array to pass back to the front end:

```php
while ($row = pg_fetch_assoc($rs))
{
    $rows[] = $row;
}
$jsonresult = json_encode($rows)
```

Now I can trim that out, and embed the encoding right into the database query:

```sql
SELECT row_to_json(pages) FROM pages WHERE page_id = 5;
-- or, to return an array of rows
SELECT array_to_json(array_agg(pages)) FROM pages WHERE page_title LIKE 'A Little Less%';
```

Notice the use of the row-type reference to the table itself after the SELECT, rather than just a single column.  This outputs:

```javascript
[{"page_id":105,"today":"\u03c0 day","page_title":"A Little Less of the Middle","contents":"I've been meaning to exercise a bit more.  You...","published_on":"2012-03-15 03:30:00+00"}]
```

Compare that to the output from json_encode() above, where the database driver treated everything as a string, even the page_id integer.  The other difference is the Postgres code doesn't do any quoting on Unicode characters:

```javascript
[{"page_id":"105","today":"π day","page_title":"A Little Less of the Middle","contents":"I've been meaning to exercise a bit more.  You...","published_on":"2012-03-15 03:30:00+00"}]
```

I'm a bit on the fence about whether it's a real replacement for doing it in middleware, especially in some web use cases where you typically want to do things like anti-XSS type processing on some fields before sending them off to a browser somewhere.  Besides, at the moment at least, there's no built-in way to break JSON back apart in the database.  But I'm sure there's some places getting direct JSON is helpful, and it's certainly an interesting start.


