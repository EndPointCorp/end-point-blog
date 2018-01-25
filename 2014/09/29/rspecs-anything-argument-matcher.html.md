---
author: Brian Gadoury
gh_issue_number: 1038
tags: ruby, rails, testing
title: RSpec’s Anything Argument Matcher Trickery
---

If you’re like me, and I know **I** am, then you’ve used RSpec’s “anything” argument matcher to test that a method is getting called with the expected arguments. If you haven’t, then I strongly recommend you [check it out](http://www.rubydoc.info/gems/rspec-mocks/RSpec/Mocks/ArgumentMatchers). Here’s a basic example:

```ruby
expect(object).to receive(:message).with(:foo, anything)
```

That test will pass if object.message() is called with :foo as its first argument, and any non-nil value as its second argument. The “anything” matcher can be used anywhere in the argument list, as well as multiple times. For example:

```ruby
expect(object).to receive(:message).with(anything, :bar, anything)
```

That test will pass if object.message() is called with a non-nil value for its first argument, :bar for its second argument, and any non-nil value for its third argument.

I recently made one of those discoveries where the happiness of making the discovery quickly turned into the sneaking suspicion that I was actually the last person on the planet to make this discovery. So, I told a co-worker about my discovery. She hadn’t heard of it before, which meant at worst I was the second to last person on the planet. “There could be others,” I thought. “I must set alight our grail shaped beacon!” And here we are.

I discovered that you can use the “anything” matcher as a kind of wildcard inside a data structure to test for the presence of a non-nil value there. Here’s the simplified version of what I came up with:

```ruby
expect(subject.targets).to eq [
  {:id => anything, :name => 'Franchise 1'},
  {:id => anything, :name => 'Franchise 2'},
  {:id => anything, :name => 'Franchise 3'},
  {:id => anything, :name => 'X-Men'},
]
```

My particular test doesn’t care about the values that the :id hash keys reference. They’re going to be standard ActiveRecord integer IDs. It really only cares about the overall structure (an array of hashes in this specific order,) that each hash has an :id tuple with a non-nil value, and that the :name tuples have the expected values.

So, that’s my discovery. It passes when it should pass. It fails when it should fail. However, it still looks a little suspect to me. It feels like I may be violating the spirit of the anything method, if not the syntax or functionality. I’ve trying consulting Uncle Google on the topic, but the “anything” search term makes it a tough to get relevant results.

To be honest, I’m half-hoping someone out there will shoot me down and describe why this is a terrible idea, how I’m a terrible person, and how they would test this differently. What say you, dear Internet?
