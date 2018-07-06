---
author: Steven Jenkins
gh_issue_number: 195
tags: rails, testing
title: Tests are not Specs
---

We’re big fans of Test Driven Development (TDD). However, a
co-worker and I encountered some obstacles
because we focused too intently on writing tests and didn’t spend
enough up-front time on good, old-fashioned specifications.

We initially discussed the new system (which is a publish/subscribe
interface used to do event
management for a reasonably large system, which totals around 70K lines
of Ruby). My co-worker did most of the design and put a high-level
one-pager together to outline how things should work, wrote unit tests
and a skeleton set of classes and modules, then handed the project to
me to implement.

So far, so good. All I had to do was make
all of the tests pass, and we were finished.

We only had unit tests, no integration tests, so there was no
guarantee that once I was done coding, that the integration work would
actually solve the problem at hand. In Testing (i.e., the academic
discipline that studies testing), this is referred to as a
*validation* problem: we may have
a repeatable, accurate measure, but it’s measuring the wrong thing.

We knew that was a weakness, but we pressed ahead anyway,
expecting to tackle that later. As an example, we identified 3
different uses of this publish/subscribe event management mechanism
that had wildly different use cases. When we discussed these
with the customer,
he clarified that one of the use cases is needed in the immediate term,
one is useful in the short term, and that the third is out of scope.
Getting that information was helpful in keeping us on track, and not
having the scope grow unmanageably.

Tests are code and no code (of sufficient size and complexity) is bug-free;
thus, tests have bugs.

When tests are the only spec, what is the best way to proceed?

The developer can assume tests are correct and Make The Tests Pass; clearly
that is not always the best approach. It’s better for the developer
to exercise judgement and fix obvious errors. However, the developer’s
judgement can be wrong, so the test writer needs
to pay special attention to any changes to the tests (and the need
to catch problems implies that the test designer and developer need
to be in tight communication—​don’t just hand your co-worker your tests
and then go on a long vacation).

Sometimes tests aren’t buggy, *per se*, but they may be ambiguous.
Variable names may not communicate clearly. They may be too large and not clearly test one thing. They may be too broad and leave unspecified the intent or design
parameters in mind.

In our recent experience, one test had the following code (slightly
altered):

```ruby
 it 'should pass event to each callback in sequence' do
  listener = mock 'listener' callback_seq = sequence 'callbacks'

  listener.expects(:one).with(@event).in_sequence(callback_seq)
  listener.expects(:two).with(@event).in_sequence(callback_seq)
  listener.expects(:three).with(@event).in_sequence(callback_seq)
  ...
```

What’s wrong with this? On the surface, nothing is wrong, until the
bigger picture is viewed: there is no other
mention of a listener anywhere else in the tests, high-level
design document, or code. Is a listener a subscriber? Should there be
a separate listener class somewhere? After all, mock ‘foo’
often means that there should be a foo object. Perhaps the
test developer forgot to include a file (or the developer overlooked it).

What actually transpired is not so mundane, but it identified a
very different approach in testing. My colleague made the observation
that it doesn’t matter if a listener is a subscriber or not for this
particular test, as it’s really only a syntactic placeholder: we could
do a variable renaming for listener and that should not
change the meaning of the code.

While his observation is true and correct, it ignores Abelson
and Sussman’s viewpoint that “programs must be written for other humans
to read, and only incidentally for machines to execute.” As the
implementer behind the pseudo-Chinese-wall of his tests, I expected the
tests to tell me how the universe of this system should be constructed,
and the mention of a listener communicated something other than
the intended message.

Sometimes, even unit tests require extensive setup, and it can be
tempting to add in extra tests and checks which don’t add a lot of
value but instead make the intent unclear, make the tests themselves
less DRY, and give yet another opportunity to introduce bugs. One
example looked something like:

```ruby
describe 'creating subscriber entry' do
  before do
    @subscriber = stub 'subscriber'
  end
  describe 'with a method name' do
    it 'should create a block that invokes the method name' do
      class << @subscriber                     
        attr_accessor :weakref, :last_received                      

        def callback(e)                         
          self.last_received = e
          self.weakref = self.respond_to?(:weakref_alive?)
        end
      end
      ...              
      entry = @publisher.class.create_subscriber_entry(@subscriber, :callback)
      entry.size.should == 2
      event = stub 'event'
      entry[:block].call(event)
      @subscriber.last_received.should == event
      @subscriber.weakref.should be_true
    end 
```

Note that the purpose of the test is *Creating a subscriber entry
with a method name should create a block that invokes the method name*,
yet the test checks the size of the subscriber entry, verifies that
the event is received, and that the callback itself is stored
via a weak reference so that it can be garbage collected. Each
of those should be in separate tests. In fact, the stated goal of
the test is only implicitly checked. Better is
something like

```ruby
  ...
  class << @subscriber
    attr_accessor :sentinel
    def callback(e)
      self.sentinel = true
    end
  end
  entry = @publisher.class.create_subscriber_entry(@subscriber, :callback)
  event = stub 'event'
  @subscriber.sentinel.should be_nil
  entry[:block].call(event)
  @subscriber.sentinel.should be_true
end
```

which only tests that the named callback is invoked, properly setting a
sentinel value.

If tests are being used as specification, then they will hide important details. A simple example if the type of storage to use for a particular set of values (for us, it was callbacks). Should they be in an array? a hash? a hash of arrays? something else?

How to handle this is a little more tricky—​implementation details like this could arguably not be part of a set of tests, as the behavior is the driver, not implementation details. However, without a specification, or a design document that outlines what kinds of performance characteristics we should aim for here, the implementer has to make choices, and those choices are not necessarily what the test writer would have wanted.

There is no one right answer there: for those who want to only use tests, then the tests need to be complete and cover the implementation details. Of course, this means that if a future scaling problem requires a change in data structures, then the test will also need to be ported to the new architecture. If specifications or design documents are used, that can speed the implementer’s work, but leaves open some questions of correctness (e.g., did the implementer use the right architecture in the right way).

We solved these problems (and more) in true Agile fashion: through good communication among the customer,the test designer, and the developer, but this experience reinforced to us
that tests alone are insufficient, and good communication needs to be maintained in the development process.

Real specs can help, too.
