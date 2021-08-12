---
author: "Marco Pessotto"
title: "Adding full-text search to a site on a budget: Xapian"
tags:
- search
- xapian
---

Over the years I've seen and implemented different full-text search
solutions in different installations: plain SQL-based ones,
[PostgreSQL-based](https://www.postgresql.org/docs/13/textsearch.html),
[Elastic Search](https://www.elastic.co/elasticsearch/),
[Solr](https://solr.apache.org/) and finally
[Xapian](https://xapian.org/).

While Solr and Elastic are very well known, Xapian, despite the fact
that it's available and packaged in all the major GNU/Linux
distributions, doesn't seem to be so famous, at least not among the
project managers.

But Xapian is fast, advanced, can be configured to do faceted search
(so the user can filter the search results), and, my favorite, is fast
to build and has virtually no maintenance overhead.

Its main feature is that it's not a stand-alone application, like Solr
or Elastic Search, but instead it's a library written in C++ which has
bindings for all the major languages (as advertised on its homepage).
It has also great [documentation](https://github.com/xapian/xapian-docsprint).

Now, being in the e-commerce business, my typical use-case is that the
client's shop needs something more fast and advanced than a search
with an SQL query in the products table. And beware, even implementing
a non-trivial SQL-based search could burn more hours than setting up
Xapian.

With Xapian you can prototype very quickly, without losing hours in
a gazillion of obscure options, and still you have something which you
can build upon all the features a typical full-text search needs.

I'm a Perl guy, so I will refer to Perl code, but the procedure is the
same for the other languages. Even the
[documentation](https://github.com/xapian/xapian-docsprint) can be
build specifically for your language!

Typically, to add a search engine to your site you need two pieces: an
indexer to which you feed the data (from static files or databases or
even fetching remote pages or whatever you want) and the search itself
in the site.

Both the indexer and the search code need to load the Xapian library
and point to the same Xapian database, which is usually a directory
(or a file pointing to a directory).

Now, stripped down to the minimum, this is how an indexer code looks
like:

```
#!/usr/local/bin/perl
use utf8;
use strict;
use warnings;
use Search::Xapian (':all');
use JSON qw/encode_json/;

my $dblocation = "xapiandb";
my $xapian = Search::Xapian::WritableDatabase->new($dblocation, DB_CREATE_OR_OPEN);
my $indexer = Search::Xapian::TermGenerator->new;
$indexer->set_database($xapian);
$indexer->set_stemmer(Search::Xapian::Stem->new("english"));
my @entries = ({ uri => '/blog/1', title => 'T1', text => '.....' },
               { uri => '/blog/2', title => 'T2', text => '.....' });
foreach my $data (@entries) {
    my $doc = Search::Xapian::Document->new;
    my $qterm = 'Q' . $data->{uri};
    $doc->add_term($qterm);
    $doc->set_data(encode_json({ uri => $data->{uri}, title => $data->{title}));
    $indexer->set_document($doc);
    $indexer->index_text(data->{text});
    $xapian->replace_document_by_term($qterm, $doc);
}
```

This code will create a `xapiandb` directory with the Xapian database,
indexing the blog posts in the `@entries` array. In a real script,
they would come from the database.

Still, there are a couple of things worth noting in this minimal code.

We set the [stemmer](https://en.wikipedia.org/wiki/Stemming) for the
given language, so the text we pass to the indexer via the
`index_text` call is actually parsed.

Then we store the data structure we want to retrieve later with
`set_data`. The best thing to do is probably to serialize it with
JSON, in this case I'm excluding the full text, which we don't need in
the output (but it would be wise to add a teaser).

Also, we use the [Q prefix](https://xapian.org/docs/omega/termprefixes.html)
to produce an unique key which we use to update the entry if it
already exists.

Of course the indexer will need to grow if you need more power and
more structured data (like filtering or searching a specific field),
but at this point we want just to show something to our client.

So let's call it done and move to the next part, the searcher.











