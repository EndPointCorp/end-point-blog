---
author: Kent Krenrich
gh_issue_number: 1144
tags: ruby, rails
title: 'Ruby On Rails: Hash#slice With Default Values'
---

Recently, I needed to add some functionality to an older section of code. This code initialized and passed around a reasonably sized set of various hashes, all with similar keys. As those hashes were accessed and manipulated, there were quite a few lines of code devoted to addressing boundary conditions within those hashes. For example, an if/else statement setting a default value to a given key if it didn't already exist. With all the added safety checks, the main method dragged on for several screens worth of code. While puttering around amidst this section, I figured I'd be a [good little boyscout](http://programmer.97things.oreilly.com/wiki/index.php/The_Boy_Scout_Rule) and leave my campsite better than when I found it.

I figured a fairly easy way to do that would be to eliminate the need for all the extra if/else clauses laying around. All they were really doing was ensuring we ended up with a minimum set of hash keys. I decided to turn all the various hashes into instances of a very simple class inheriting from Ruby on Rails' [HashWithIndifferentAccess](http://api.rubyonrails.org/classes/ActiveSupport/HashWithIndifferentAccess.html) along with some basic key management functionality.

My first draft came out looking something like:

```ruby
class MyHash &lt; HashWithIndifferentAccess
  def initialize(constuctor = {}) do
    super
    self[:important_key_1] ||= "default 1"
    self[:important_key_2] ||= "default 2"
  end
end
```

This seemed to work fine. I didn't need to worry about ensuring "important keys" were present anymore. And it was perfectly viable to pass in one of the important keys as part of the initialization.

I soon discovered in my test suite that my code did not do exactly what I intended it to do. In the tests, I wanted to ensure several of my hash keys came out with the right values. I made use of MyHash#slice to ensure I ended up with the right subset of values for my given test. However, no matter what I did, I could not weed out the important keys:

```bash
1.9.3 :003 &gt; MyHash.new({foo: 'bar', bar: 'lemon'}).slice(:bar)
=&gt; {"important_key_1"=&gt;"default 1", "important_key_2"=&gt;"default 2", "bar"=&gt;"lemon"}
```

I admit I was quite perplexed by this. I tried several re-writes of the initialize method looking for some version that didn't exhibit this strange slice behavior. Finally, I took to the Ruby on Rails and Ruby docs.

Looking at [the source for slice](http://api.rubyonrails.org/classes/Hash.html#method-i-slice), I found the problem:

```ruby
keys.each_with_object(self.class.new)...
```

The method slice calls "new" (which includes the default values) to create another object to avoid clobbering the one the method is called on. Since I didn't feel like writing my own custom slice method, or trying to monkey patch Rails, I realized I was beaten. I needed to find a new solution.

After a little thought, I came up with this:

```ruby
class MyHash &lt; HashWithIndifferentAccess
  def self.build(constructor = {}) do
    h = new(constructor)
    h[:important_key_1] ||= "default 1"
    h[:important_key_2] ||= "default 2"
  end
end
```

This does not fix the problem, but manages to sidestep it. Most Ruby on Rails veterans will be familiar with methods called "build" so it shouldn't be too clumsy to work with. I replaced all the entries in my code that called MyHash.new(...) with MyHash.build(...) and went on my merry way.
