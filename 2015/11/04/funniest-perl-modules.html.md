---
author: Jeff Boes
gh_issue_number: 1172
tags: perl
title: Top 7 Funniest Perl Modules
---



And now for something completely different ...

Programmers in general, and Perl programmers in particular, seem to have excellent, if warped, senses of humor. As a result, the CPAN library is replete with modules that have oddball names, or strange and wonderful purposes, or in some delightful cases—​both!

Let’s take a look.

### 1. [Bone::Easy](http://search.cpan.org/~mschwern/Bone-Easy-0.04/lib/Bone/Easy.pm)
  
  I’m going to take the coward’s way out on this one right away. Go see for yourself, or don’t.
  
### 2. [Acme::EyeDrops](http://search.cpan.org/~asavige/Acme-EyeDrops-1.62/lib/Acme/EyeDrops.pm)
  
  Really, anything in the Acme::* (meaning “perfect”) namespace is just programmer-comedy gold, depending on what you find amusing and what is just plain forehead-smacking stupid to you. This one allows you to transform your Perl programs (small ones work better) from this:
  ```perl
  print "hello world\n";
  ```
  
  to this:
  <img src="/blog/2015/11/04/funniest-perl-modules/image-0.png"/>
  
  Oh, that’s not just a picture of a camel. That’s actual Perl code; you can run that, and it executes in the exact same way as the original one-liner. So much more stylish. Plus, you can impress your boss/cow-orker/[heroic scientist boyfriend](http://nightvale.wikia.com/wiki/Carlos).
  
### 3. [common::sense](http://search.cpan.org/~mlehmann/common-sense-3.74/sense.pod)
  
  This one makes the list because (a) it is just so satisfying to see
  ```perl
    use common::sense;
  ```
  
  atop a Perl program, and (b) a citation of this on our company IRC chat is what planted the seed for this article.
  
  Another is [sanity.pm](https://metacpan.org/pod/sanity), as in “use sanity;”. Seems like a good approach.
  
### 4. [Silly::Werder](https://metacpan.org/pod/Silly::Werder)

Not a terribly interesting name, but it produces some head-scratching output. For instance,

> 
> *
> Broringers isess ailerwreakers paciouspiris dests bursonsinvading buggers companislandet despa ascen?
> *
> 

I suppose you might use this to generate some *[Lorem ipsum](https://en.wikipedia.org/wiki/Lorem_ipsum)*-type text, or maybe temporary passwords? Dialog for your science fiction novel?

### 5.

Any module with the word “Moose” in it. “Moose” is a funny word.

### 6. [D::oh](https://metacpan.org/pod/D::oh)

The humor here is a bit obscure: you have to have been around for Perl4-style namespace addressing, when you would have had to load this via:
```perl
use D'oh;
```

### 7. [your](https://metacpan.org/pod/your)

As in:
```perl
use your qw($wits %head @tools);
```

Here the name is the funny bit; the module itself is all business.

Well, that seems like enough to get you started. If you find others, post them here in the comments!


