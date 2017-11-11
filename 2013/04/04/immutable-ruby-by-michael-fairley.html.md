---
author: Mike Farmer
gh_issue_number: 778
tags: conference, ruby
title: Immutable Ruby by Michael Fairley
---

[Michael Fairley](https://twitter.com/michaelfairley) is presenting on Immutable objects in ruby.

Immutability is a term used to describe data or objects that can’t be changed. This is a lesser known concept for ruby developers because almost everything in ruby is mutable. Despite this, much of ruby is full of immutable code. Make it explicit. Even in your databases there are some records you don’t want to modify.

One technique to making your database records immutable is to use the readonly? method in ActiveRecord or to revoke the permission to modify at the database level.

Many objects can utilize the freeze method which ensures that objects aren’t being modified. For example, use freeze for configurations. Be aware though that freeze doesn’t freeze objects in an array or hash so you’ll need a gem that provides the ability to deep freeze.

The gem values, provides a set of data structures that are frozen by default. These can be useful in cases where you might use Struct. You can create the object but it doesn’t allow you to change the attributes.

Use value objects in your ActiveRecord object by using composed_of which lets you use an object to combine attributes of the record into a value object. This gives you greater flexibility. The Address part of a user object is a good example.

Another use case for immutable data is in the logging of events. Many events such as a ledger or a database log are helpful because they can be replayed to create an accurate derived state such as current_status or an account balance.

If you use immutable objects for cache keys you can solve many issues around cache invalidation. Since the keys are immutable, you can rely on them being there. The exception to this would be deletion which could be solved by having a callback or something similar that invalidates the cache manually when the object is deleted.

There are some downsides to using immutable objects the key one being performance. Immutable objects tend to be copied a lot using a lot of memory and processing to recreate them.

More information can be found on this topic by visiting [Michael’s site](http://goo.gl/Esa7r).
