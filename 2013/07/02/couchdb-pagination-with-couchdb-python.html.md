---
author: Miguel Alatorre
gh_issue_number: 827
tags: couchdb, python
title: CouchDB pagination with couchdb-python
---

I’ve been working with couchdb-python v0.8 to meet some of a project’s CouchDB needs and ran into an unfortunate shortcoming.

Retrieving database rows is as easy as:

```python
for row in db.view(mapping_function):
    print row.key
```

However, all the rows will be loaded into memory. Now, for small databases this is not a problem but lucky me is dealing with a 2.5 million+ document database. Long story short: kaboom!

There is an excellent blog post by [Marcus Brinkmann](https://web.archive.org/web/20131009233304/http://blog.marcus-brinkmann.de/2011/09/17/a-better-iterator-for-python-couchdb/) that details the memory issue and also provides a pagination solution. However, couchdb-python v0.9 (released 2013-04-25) does provide its own solution: the [iterview](http://couchdb-python.readthedocs.io/en/latest/client.html#couchdb.client.Database.iterview) method. If you’ve been able to manage small databases with v0.8 but are anticipating larger and larger databases, be sure to upgrade!
