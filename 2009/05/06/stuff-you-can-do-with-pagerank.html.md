---
author: Sonny Cook
gh_issue_number: 140
tags: conference, rails, spree
title: Stuff you can do with the PageRank algorithm
---

I've attended several interesting talks so far on my first day of
RailsConf, but the one that got me the most excited to go out and
start trying to shoehorn it into my projects was [Building
Mini Google in Ruby](http://www.slideshare.net/igrigorik/building-mini-google-in-ruby) by Ilya Grigorik.

In terms of doing Google-like stuff (which I'm not especially
interested in doing), there are three steps, which occur in order of
increasing level of interestingness.  They are:

- Crawling (mundane)
- Indexing (sort of interesting)
- Rank (neato)

Passing over crawling, Indexing is sort of interesting.  You can do
it yourself if you care about the problem, or you can hand it over to
something like ferret or sphinx.  I expect it's probably time for me
to invest some time investigating the use of one or more of these,
since I've already gone up and down the do it yourself road.

The interesting bit, and the fascinating focus of Ilya's
presentation were the explanation of the PageRank algorithm and the
implementation details as well as some application ideas.  Hopefully I
don't mess this up too badly, but as I understand it, it simplifies
down to something like this.

A page is ranked to some degree by how many other pages link to
it.  This is a bit too simple, though, and trivially gamed.  So, you
make it a little more complex by modeling the following behavior, a
*random surfer* will surf from one page to another by doing one
of two things.  They will either follow a link or randomly go to a
non-linked page (sort of how I surf Wikipedia).  There is a much
higher probability (.85) that they will follow a link than that thay
will teleport (.15).  If you model this (hand waving here) then you
come up with a nice formula (more hand waving) that can be used to
calculate the page rank for a page in a given data set.  A data set in
this case is a collection of crawled pages.

For large data sets, these calculations can be somewhat intensive,
so we are recommended to the good graces of the Gnu Scientific Library
and the appropriate Ruby wrappers and the NArrary gem to do the
calculations and array management.

One suggestion of a practical applications of this technology is to
apply it to sets of products purchased together in a shopping cart to
provide recommendations of the sort for 'people who bought that also
bought this.'  I'm pretty excited to try to implement this in Spree.  But...

...what really piqued my interest was the idea that this could be
applied to any graph.  The Taxonomies/Taxons/ProductGroups with
products could give me a nice big (depending on the size of the data
set of course) directed graph to play with.  The question, I suppose,
is what the PageRank applied against such a graph means.
