---
author: Jeff Boes
gh_issue_number: 551
tags: json, perl
title: Lock up your keys
---



## Locking hash keys with Hash::Util

It’s a given that you shouldn’t write Perl without “use strict”; it prevents all kinds of silent bugs involving misspelled and uninitialized variables. A similar aid for misspelled and uninitialized hash keys exists in the module “[Hash::Util](http://search.cpan.org/perldoc?Hash::Util)”.

By way of background: I was working on a long chunk of code that prepares an e-commerce order for storage in a database. Many of the incoming fields map directly to the table, but others do not. The interface between this code and the page which submits a large JSON structure was in flux for a while, so from time to time I had to chase bugs involving “missing” or “extra” fields. I settled on a restricted hash to help me squash these and future bugs.

The idea of a restricted hash is to clamp down on Perl’s rather loose “record” structure (by which I mean the common practice of using a hash to represent a record with named fields), which is great in some circumstances. While in most programming languages you must pre-declare a structure and live with it, in Perl hashes you can add new keys on the fly, misspellings and all. A restricted hash can only have a particular set of keys, but is still a hash for all other purposes.

An example:

```perl
my %hash = (aaa =&gt; 1, bbb =&gt; 2);
```

Attempts to reference $hash{ccc} will not return an error, but only an undefined value. We can now lock the hash so that its current roster of keys will be constant:

```perl
    use Hash::Util qw(lock_keys);
    lock_keys(%hash);
```

and now $hash{ccc} is not only undefined, it’s a run-time error:

```perl
    $hash{ccc};
    Attempt to access disallowed key 'ccc' in a restricted hash
```

If we know the list of keys before the hash is initialized, we can set it up like this:

```perl
    my %hash;
    lock_keys(%hash, qw(aaa bbb ccc));
```

Keep in mind the values of $hash{aaa}, etc. are mutable (can be undefined, not exist, scalars, references, etc.), just like a normal hash.

What if our key roster needs to change over the course of the program? In my example, there were several kinds of transactions being sent via JSON, and I needed to validate and restrict fields based on the presence and values of other fields. E.g.,

```perl
    if ($hash{record_type} eq 'A') {
        # validate %hash for aaa, bbb, ccc
    }
    else {
        # validate %hash for aaa, bbb, ddd; ccc should not appear
    }
```

You can add to or modify the accepted keys as you go, but it’s a two-step process: not even Hash::Util can modify the keys of a locked hash, so you have to unlock and re-lock:

```perl
    my %hash;
    lock_keys(%hash, qw(record_type aaa bbb ccc));
    # …
    unlock_keys(%hash);
    if ($hash{record_type} eq 'A') {
        lock_keys(%hash, qw(record_type aaa bbb ccc));
    }
    else {
        lock_keys(%hash, qw(record_type aaa bbb ddd));
    }
```

Of course, that’s kind of wordy: we’d really rather just splice in a key here and there. Hash::Util has you covered, because you can retrieve the list of legal keys for a hash (even if it’s not currently locked):

```perl
    lock_keys_plus(%hash, qw(ddd));
```

adds ‘ddd’ to the list, keeping the previous keys as well. However, if any of the *legal* keys are not *current keys*, they won’t make it into the key roster. Instead, use:

```perl
    lock_keys_plus(%hash, (legal_keys(%hash), qw(more keys here)));
```

Everything shown here for hashes is also available for hashrefs: for instance, to lock up a hashref $hr:

```perl
    lock_ref_keys($hr);
    unlock_ref_keys($hr);
    lock_ref_keys_plus($hr, (legal_ref_keys($hr), qw(other keys)));
```

Of course, adding all this locking and unlocking adds complexity to your code, so you should consider carefully whether it’s justified. In my case I had 60+ keys, in a nested structure, spanning 1500 lines of code – I just could not keep all the correct spellings in my head any more, so now when I write

```perl
    if ($opt-&gt;{order_status})
```

when I mean “transaction_status”, I’ll get a helpful run-time error instead of a silent skip of that block of code.

Are there other approaches? Yes, depending on your needs: JSON::Schema, for instance, will let you validate a JSON structure against a “golden master”. However, it does not prevent subsequent assignments to the structure, creating new keys on the fly (possibly in error). Moose would support a restricted object like this, but may add more complexity than you need, so Hash::Util may be the appropriate, lighter-weight approach.


