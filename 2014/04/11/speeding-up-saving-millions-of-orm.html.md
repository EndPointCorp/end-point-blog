---
author: Szymon Lipiński
gh_issue_number: 961
tags: performance, postgres, python
title: Speeding Up Saving Millions of ORM Objects in PostgreSQL
---

## The Problem

Sometimes you need to generate sample data, like random data for tests. Sometimes you need to generate it with
huge amount of code you have in your ORM mappings, just because an architect decided that all the logic needs to be
stored in the ORM, and the database should be just a dummy data container. The real reason is not important - the problem
is: let’s generate lots of, millions of rows, for a sample table from ORM mappings.

Sometimes the data is read from a file, but due to business logic kept in ORM, you need to load the data from file to ORM and then save the millions of ORM objects to database.

This can be done in many different ways, but here I will concentrate on making that as fast as possible.

I will use PostgreSQL and SQLAlchemy (with psycopg2) for ORM, so all the code will be implemented in Python. I will create a couple of functions, each implementing another solution for saving the data to the database, and I will test them using 10k and 100k of generated ORM objects.

## Sample Table

The table I used is quite simple, just a simplified blog post:

```sql
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  payload TEXT NOT NULL
);
```

## SQLAlchemy Mapping

I'm using SQLAlchemy for ORM, so I need a mapping, I will use this simple one:

```python
class BlogPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    body = Column(Text)
    payload = Column(Text)
```

The payload field is just to make the object bigger, to simulate real life where objects can be much more complicated, and thus slower to save to the database.

## Generating Random Object

The main idea for this test is to have a randomly generated object, however what I really check is the database speed,
and the whole randomness is used at the client side, so having a randomly generated object doesn’t really matter at
this moment.
The overhead of a fully random function is the same regardless of the method of saving the data to the database. So
instead of randomly generating the object, I will use a static one, with static data, and I will use the function below:

```python
TITLE   = "title"      * 1764
BODY    = "body"       * 1764
PAYLOAD = "dummy data" * 1764

def generate_random_post():
    "Generates a kind of random blog post"
    return BlogPost(title=TITLE, body=BODY, payload=PAYLOAD)
```

## Solution Ideas

Generally there are two main ideas for such a bulk inserting of multiple ORM objects:

- Insert them one-by-one with autocommit
- Insert them one-by-one in one transaction

## Save One By One

This is the simplest way. Usually we don’t save just one object, but instead we save
many different objects in one transaction, and making a couple of related changes in multiple transactions is a great
way leading to a database with bad data.

For generating millions of unrelated objects this shouldn’t cause data inconsistency, but this is highly inefficient.
I’ve seen this multiple times in code: create an object, save it to the database, commit, create another object and so on. It works,
but is quite slow. Sometimes it is fast enough, but for the cost of making a very simple change in this algorithm we
can make it 10 times faster.

I’ve implemented this algorithm in the function below:

```python
def save_objects_one_by_one(count=MAX_COUNT):
    for i in xrange(1, MAX_COUNT+1):
        post = generate_random_post()
        session.add(post)
        session.commit()
```

## Save All in One Transaction

This solution is as simple as: create objects, save them to the database, commit the transaction at the end, so do
everything in one huge transaction.

The implementation differs only by four spaces from the previous one, just run commit() once, after adding all
objects:

```python
def save_objects_one_transaction(count=MAX_COUNT):
    for i in xrange(1, MAX_COUNT+1):
        post = generate_random_post()
        session.add(post)
    session.commit()
```

## Time difference

I ran the tests multiple times, truncating the table each time. The average results of saving 10k objects were quite predictable:

- Multiple transactions - 268 seconds
- One transaction - 25 seconds

The difference is not surprising, the whole table size is 4.8MB, but after each transaction the database needs to write the
changes on disk, which slows the procedure a lot.

## Copy

So far, I’ve described the most common methods of generating and storing many ORM objects. I was wondering about
another, which may seem surprising a little bit at the beginning.

PostgreSQL has a great COPY command which can copy data between a table and a file. The file format is simple: one table
row per one file row, fields delimited with a defined delimiter etc. It can be a normal csv or tsv file.

My crazy idea was: how about using the COPY for loading all the generated ORM objects? To do that, I need to
serialize them to a text representation, to create a text file with all of them. So I created a simple function, which
does that. This function is made outside the BlogPost class, so I don't need to change the data model.

```python
def serialize_post_to_out_stream(post, out):
    import csv
    writer = csv.writer(out, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
    writer.writerow([post.title, post.body, post.payload])
```

The function above gets two parameters:

- post - the object to be serialized
- out - the output stream where the row with the post object will be saved, in Python it is a file-like object, so an
object with all the functions a file object has

Here I use a standard csv module, which supports reading and writing csv files. I really don’t want to write my own
function for escaping all the possible forms of data I could have - this usually leads to many tricky bugs.

The only thing left is to use the COPY command. I don’t want to create a file with data and load that later; the
generated data can be really huge, and creating temporary files can just slow things down. I want to keep the whole
procedure in Python, and use pipes for data loading.

I will use the psql program for accessing the PostgreSQL database. Psql has a different command called \COPY, which can read the csv file from psql's standard input. This can be done using e.g.: cat file.csv | psql database.

To use it in Python, I’m going to use the subprocess module, and create a psql process with stdin=subprocess.PIPE
which will give me write access to the pipe psql reads from. The function I’ve implemented is:

```python
def save_objects_using_copy(count=MAX_COUNT):
    import subprocess
    p = subprocess.Popen([
        'psql', 'pgtest', '-U', 'pgtest',
        '-c', '\COPY posts(title, body, payload) FROM STDIN',
        '--set=ON_ERROR_STOP=true'
        ], stdin=subprocess.PIPE
    )
    for i in xrange(1, MAX_COUNT+1):
        post = generate_random_post()
        serialize_post_to_out_stream(post, p.stdin)
    p.stdin.close()
```

## Results

I’ve also tested that on the same database table, truncating the table before running it. After that I’ve also checked
this function, and the previous one (with one transaction) on a bigger sample - 100k of BlogPost objects.

The results are:

<table>
<colgroup>
<col style="text-align:right;"/>
<col style="text-align:right;"/>
<col style="text-align:right;"/>
<col style="text-align:right;"/>
</colgroup>

<thead>
<tr>
 <th style="text-align:right;">Sample size</th>
 <th style="text-align:right;">Multiple Transactions</th>
 <th style="text-align:right;">One Transaction</th>
 <th style="text-align:right;">COPY</th>
</tr>
</thead>

<tbody>
<tr>
 <td style="text-align:right;">10k</td>
 <td style="text-align:right;">268 s</td>
 <td style="text-align:right;">25 s</td>
 <td style="text-align:right;">5 s</td>
</tr>
<tr>
 <td style="text-align:right;">100k</td>
 <td style="text-align:right;">—</td>
 <td style="text-align:right;">262 s</td>
 <td style="text-align:right;">51 s</td>
</tr>
</tbody>
</table>

I haven’t tested the multiple transactions version for 100k sample, as I just didn’t want to wait multiple hours for
finishing that (as I run each of the tests multiple times to get more reliable results).

As you can see, the COPY version is the fastest, even 5 times faster than the full ORM version with one huge
transaction. This version is also memory friendly, as no matter how many objects you want to generate, it always needs
to store one ORM object in memory, and you can destroy it after saving.

## The Drawbacks

Of course using psql poses a couple of problems:

- you need to have psql available; sometimes that’s not an option
- calling psql creates another connection to the database; sometimes that could be a problem
- you need to set up a password in ~/.psql file; you cannot provide it in the command line

You could also get the pcycopg2 cursor directly from the SQLAlchemy connection, and then use the copy_from() function, but this method needs to have all the data already prepared in memory, as it reads from a file-like object, e.g. StringIO. This is not a good solution for inserting millions of objects, as they can be quite huge - streaming is much better in this case.

Another solution to this is to write a generator, which is a file like object, and the copy_from() method can read from it directly. This function calls the file's read() method trying to read 8192 bytes per call. This can be a good idea when you don't have access to the psql, however due to the overhead for generating the 8192 bytes strings, it should be slowever than the psql version.
