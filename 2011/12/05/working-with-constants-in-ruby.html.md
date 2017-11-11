---
author: Brian Buchalter
gh_issue_number: 519
tags: ruby
title: Working with constants in Ruby
---



Ruby is designed to put complete power into the programmer's hands and with great power comes great responsibility!  This includes the responsibility for freezing constants.  Here's an example of what someone might THINK is happening by default with a constant.

```ruby
class Foo
  DEFAULTS = [:a, :b]
end

#irb
default = Foo::DEFAULTS
default << :c
Foo::DEFAULTS #=> [:a, :b, :c]  WHOOPS!
```

As you can see, assigning a new variable from a constant lets you modify what you thought was a constant!  Needless to say, such an assumption would be very difficult to track down in a real application.  Let's see how we might improve on this design.  First, let's [freeze](http://ruby-doc.org/core-1.9.3/Object.html#method-i-freeze) our constant.

```ruby
class Foo
  DEFAULTS = [:a, :b].freeze
end

#irb
default = Foo::DEFAULTS
default << :c #=>  ERROR can't modify frozen array
```

Now we'll get very specific feedback about offending code.  The question is how can we use our constant now as a starting point for array, and still be able to modify it later?  Let's look at some more code.

```ruby
Foo::DEFAULTS.frozen? #=> true
Foo::DEFAULTS.clone.frozen? #=> true, this was my first guess, but it turns out we need...
Foo::DEFAULTS.dup.frozen? #=> false
```

It's worth reading the docs on [clone](http://ruby-doc.org/core-1.9.3/Object.html#method-i-clone) and [dup](http://ruby-doc.org/core-1.9.3/Object.html#method-i-dup) to understand there difference, but in short, clone replicates the internal state of the object while dup creates a new instance of the object.  There was one more question I needed to answer; what would happen when I wanted to append another frozen array to a non-frozen array?  Let's look to the code again!

```ruby
default = Foo::DEFAULTS.dup  #not frozen
new_default = default + [:c].frozen
new_default.frozen? # false
```

So it seems that the initial state of the object carries the frozen state, allowing you to append frozen arrays without having to dup them.  The moral of the story here is don't make assumptions about Ruby!  One of the best ways to challenge your assumptions is with unit tests.


