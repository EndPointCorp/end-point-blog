---
author: "Marco Pessotto"
title: "Full-text search on a budget: Xapian"
tags:
- search
- xapian
---

![searching](/blog/2021/08/12/searching.jpg)

Over the years I’ve seen and implemented different full-text search
applications using various technologies: plain SQL,
[PostgreSQL](https://www.postgresql.org/docs/13/textsearch.html),
[Elastic Search](https://www.elastic.co/elasticsearch/),
[Solr](https://solr.apache.org/) and finally
[Xapian](https://xapian.org/).

While Solr and Elastic are very well known, Xapian, despite the fact
that it’s available and packaged in all the major GNU/Linux
distributions, doesn’t seem to be so popular, at least not among the
project managers.

But Xapian is fast, advanced, can be configured to do faceted search
(so the user can filter the search results), and, my favorite, is fast
to build and has virtually no maintenance overhead.

Its main feature is that it’s not a stand-alone application, like Solr
or Elastic Search, but instead it’s a library written in C++ which has
bindings for all the major languages (as advertised on its
[homepage](https://xapian.org/)). It has also great
[documentation](https://github.com/xapian/xapian-docsprint).

Now, being in the e-commerce business, my typical use-case is that the
client’s shop needs something faster and better than a search using a
SQL query against the products table. And beware, even implementing a
non-trivial SQL-based search could burn more hours than setting up
Xapian.

With Xapian you can prototype very quickly, without losing hours
wading through obscure options, setting up services and configuring
firewalls. And yet, the prototype will allow you to build more
advanced features once you need them.

I’m a Perl guy, so I will show you some Perl code, but the procedure
is the same for the other languages. Even the
[documentation](https://github.com/xapian/xapian-docsprint) can be
built specifically for your language!

Typically, to add a search engine to your site you need two pieces: an
indexer to which you feed the data (from static files or databases or
even fetching remote pages or whatever you need) and the search itself
in the site.

Both the indexer and the search code need to load the Xapian library
and point to the same Xapian database, which is usually a directory
(or a file pointing to a directory).

Now, stripped down to the minimum, this is how an indexer code looks
like:

```perl
#!/usr/bin/env perl
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
my @entries = ({ uri => '/blog/1', title => 'T1', text => 'Marco loves pizza' },
               { uri => '/blog/2', title => 'T2', text => 'They love chapati' });
foreach my $data (@entries) {
    my $doc = Search::Xapian::Document->new;
    my $qterm = 'Q' . $data->{uri};
    $doc->add_term($qterm);
    $doc->set_data(encode_json({ uri => $data->{uri}, title => $data->{title} }));
    $indexer->set_document($doc);
    $indexer->index_text($data->{text});
    $xapian->replace_document_by_term($qterm, $doc);
}
```

This code will create a `xapiandb` directory with the Xapian database,
indexing the blog posts in the `@entries` array. In a real script,
they would come from the database.

Still, there are a couple of things worth noting in this minimal code.

We set the [stemmer](https://en.wikipedia.org/wiki/Stemming) for the
given language, so the text passed to the indexer via the `index_text`
call is parsed.

Then we store the data structure we want to retrieve later with
`set_data`. The best thing to do is probably to serialize it with
JSON, in this case I’m excluding the full text, which we don’t need in
the output (but it would be wise to add a teaser).

Also, we use a `Q`
[prefix](https://xapian.org/docs/omega/termprefixes.html) to produce
an unique term to update the entry when it already exists.

Of course the indexer will need to grow if you need more power and
more structured data (like filtering or searching a specific field),
but at this point we want just to show something to our hypothetical
client.

The database can be inspected very easily. Xapian comes with a tool
called `delve` (or `xapian-delve`):

```
$ xapian-delve xapiandb -a -v -1
All terms in database (termfreq):
Q/blog/1 1
Q/blog/2 1
Zchapati 1
Zlove 2
Zmarco 1
Zpizza 1
Zthey 1
chapati 1
love 1
loves 1
marco 1
pizza 1
they 1
```

And you can also try a search from the command line with `quest`:

```
$ quest -d xapiandb "loves NOT chapati"
Parsed Query: Query((Zlove@1 AND_NOT Zchapati@2))
Exactly 1 matches
MSet:
1: [0.0953102]
{"title":"T1","uri":"/blog/1"}

$ quest -d xapiandb "pizza OR chapati" 
Parsed Query: Query((Zpizza@1 OR Zchapati@2))
Exactly 2 matches
MSet:
1: [0.405465]
{"title":"T1","uri":"/blog/1"}
2: [0.405465]
{"uri":"/blog/2","title":"T2"}
```

As the example above shows, it should be clear that:

 - search works as you would expect (with logical operators) out of
   the box

 - the stemming works, searching for "loves" and "love" is the same.

 - the results give us back the JSON we stored in the index.

So let’s call it done and move to the next part, the searcher.

Now, while the indexer is a single script, the search needs to be
plugged into the live code of your site. For the purposes of this
article, I will provide a script instead, which does basically the
same thing as `quest`. Plugging it into the web application is left as
an exercise for the reader. I would also suggest to put both the
indexing and searching code in a single shared module, keeping the
logic in a single location.

```perl
#!/usr/bin/env perl
use utf8;
use strict;
use warnings;
use Search::Xapian ':all';
use JSON;

my ($cgi) = join(' ', @ARGV);
my $dblocation = "xapiandb";
my $database = Search::Xapian::Database->new($dblocation);
my $enquire = Search::Xapian::Enquire->new($database);
my $qp = Search::Xapian::QueryParser->new;
$qp->set_database($database);
$qp->set_stemmer(Search::Xapian::Stem->new("english"));
$qp->set_stemming_strategy(STEM_SOME);
$qp->set_default_op(OP_AND);
my $query = $qp->parse_query($cgi, FLAG_PHRASE|FLAG_BOOLEAN|FLAG_WILDCARD);
$enquire->set_query($query);

# fetch the first 50 results
my $mset = $enquire->get_mset(0, 50);
print "Total results: " . $mset->get_matches_estimated . "\n";

my $json_pretty = JSON->new->pretty(1)->utf8(1)->canonical(1);
foreach my $m ($mset->items) {
    my $data = decode_json($m->get_document->get_data);
    # decode and reencode the json in a human-readable fashion
    print $json_pretty->encode($data);
}
```

If you’re wondering what those constants are and where to look for
more, they are in the module’s
[documentation](https://metacpan.org/pod/Search::Xapian#EXPORT), in
plain sight (we asked for them when loading the module with the `:all`
argument).

Most of the code shown here is boilerplate, but that could change once
you build up. Notably we set the stemmer for the current language and
the query parser options, so we can use wildcard (e.g. `piz*`), the
`AND`/`OR` operators, and quoting.

Let’s see the script in action.

Wildcard:

```
$ ./search.pl 'piz'              
Total results: 0
$ ./search.pl 'piz*'
Total results: 1
{
   "title" : "T1",
   "uri" : "/blog/1"
}
```

Operators:

```
$ ./search.pl 'pizza OR chapati'
Total results: 2
{
   "title" : "T1",
   "uri" : "/blog/1"
}
{
   "title" : "T2",
   "uri" : "/blog/2"
}
$ ./search.pl 'pizza AND chapati'
Total results: 0
```

Quoting (beware here the double quotes to escape the shell):

```
$ ./search.pl '"loves chapati"'
Total results: 0
$ ./search.pl '"love chapati"' 
Total results: 1
{
   "title" : "T2",
   "uri" : "/blog/2"
}
```

The whole thing already looks pretty good. Way better (and way faster
to code and to execute) than a home-baked SQL search.

As already noted, this is just scratching the surface. Xapian can
do [much more](https://getting-started-with-xapian.readthedocs.io/en/latest/howtos/index.html):
filtering, range queries, facets, sorting, even spelling corrections!

I don’t doubt that Solr&C. have their use-cases, but for the common
scenario of a small/mid-sized e-shop or site, I think that this
solution is more affordable and maintainable than having whole
separate application (like a Solr server) to maintain, upgrade and
secure. Don’t forget that here we haven’t done a single HTTP request.
We didn’t have to manage daemons, opening/closing ports, and alike. We
didn’t have to configure a schema and a tokenizer in a separate
application (and keep that aligned with the handling code). It’s all
there in our (Perl) code in two files (as already noted, the logic
should live in a single module).

We just installed a library (big chances are that it’s already
installed) and a Perl module.

The Xapian database lives on the disk and your code has full control
over it. Also it’s normally your GNU/Linux distribution taking care of
the security upgrades.

If your client is on a budget, building a full-text search Xapian can
be the right choice, and you can scale it up on the go, once more
features are required.

