---
author: Jon Jensen
gh_issue_number: 403
tags: javascript, json, perl, python, ruby
title: JSON pretty-printer
---

The other day Sonny Cook and I were troubleshooting some YUI JavaScript code and looking at some fairly complex JSON. It would obviously be a lot easier to read if each nested data structure were indented, and spacing standardized.

I threw together a little Perl program based on the JSON man page:

```perl
#!/usr/bin/env perl

use JSON;

my $json = JSON-&gt;new;
undef $/;
while (&lt;&gt;) {
    print $json-&gt;pretty-&gt;encode($json-&gt;decode($_));
}
```

It took all of 2 or 3 minutes and I even left out strictures and warnings. Living on the edge!

It turns a mess like this (sample from json.org):

```javascript
{"glossary":{"title":"example glossary","GlossDiv":{"title":"S","GlossList":
{"GlossEntry":{"ID":"SGML","SortAs":"SGML","GlossTerm":"Standard Generalized Markup Language",
"Acronym":"SGML","Abbrev":"ISO 8879:1986","GlossDef":{"para":
"A meta-markup language,used to create markup languages such as DocBook.",
"GlossSeeAlso":["GML","XML"]},"GlossSee":"markup"}}}}}
```

into this much more readable specimen:

```javascript
{
   "glossary" : {
      "GlossDiv" : {
         "GlossList" : {
            "GlossEntry" : {
               "GlossDef" : {
                  "para" : "A meta-markup language,used to create markup languages such as DocBook.",
                  "GlossSeeAlso" : [
                     "GML",
                     "XML"
                  ]
               },
               "GlossTerm" : "Standard Generalized Markup Language",
               "ID" : "SGML",
               "SortAs" : "SGML",
               "Acronym" : "SGML",
               "Abbrev" : "ISO 8879:1986",
               "GlossSee" : "markup"
            }
         },
         "title" : "S"
      },
      "title" : "example glossary"
   }
}
```

But today I thought back to that and figured surely something like that must already be at hand if I'd just looked for it. Sure enough, there are many easy options that work conveniently from the shell, similarly to that script:

- json_xs (Perl JSON::XS)
- python -mjson.tool (Python 2.6+)
- prettify_json.rb (Ruby json gem)

And those were just the ones that were likely already on the machine I was using! Hooray for convenience.
