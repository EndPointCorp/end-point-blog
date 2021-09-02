---
author: Jeff Boes
title: Use ZIP+4, except when you shouldn’t
github_issue_number: 440
tags:
- perl
date: 2011-04-12
---

The USPS provides a handy [API](https://www.usps.com/business/web-tools-apis/rate-calculator-api.pdf) for looking up postal rates on the fly. Recently it started failing for code that had been working for a while, so I investigated. I found a couple of different problems with it:

- First, the “service description” field had been “augmented” by including copyright symbols via HTML mark-up. That meant internal comparisons started to fail, so I “canonicalized” all the responses by stripping out various things from both sides of my comparison.

```perl
    $string =~ s{&(?:[a-z/;&])+}{}gis;
    $string =~ s/[^a-z]//gis;
    $string =~ s/^\s+//;
    $string =~ s/\s+$//;
    $string =~ s/\s+/ /gis;
```

- Second, I found that the API inexplicably rejects 9-digit ZIP codes, the “ZIP+4” format. That’s right, you can’t look up a domestic shipping rate for a 9-digit ZIP. The documentation linked above specifically calls for 5-digit ZIPs. If you pass a 9-digit ZIP to the API, it doesn’t smartly recognize that you’ve given it too much info and just use what it needs. Instead, it throws an error.

So the API got too clever in one regard, and not clever enough where it counts.
