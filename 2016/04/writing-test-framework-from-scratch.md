---
author: Phin Jensen
title: Writing a Test Framework from Scratch
github_issue_number: 1218
tags:
- conference
- ruby
date: 2016-04-08
---

On March 21 and 22, I had the opportunity to attend the 10th and final [MountainWest RubyConf](http://mtnwestrubyconf.org) at the Rose Wagner Performing Arts Center in Salt Lake City.

One talk that I really enjoyed was *Writing a Test Framework from Scratch* by Ryan Davis, author of MiniTest. His goal was to teach the audience how MiniTest was created, by explaining the what, why and how of decisions made throughout the process. I learned a lot from the talk and took plenty of notes, so I’d like to share some of that.

The first thing a test framework needs is an *assert* function, which will simply check if some value or comparison is true. If it is, great, the test passed! If not, the test failed and an exception should be raised. Here is our first *assert* definition:

```ruby
def assert test
  raise "Failed test" unless test
end
```

This function is the bare minimum you need to test an application, however, it won’t be easy or enjoyable to use. The first step to improve this is to make error messages more clear. This is what the current *assert* function will return for an error:

```plain
path/to/microtest.rb:2:in `assert': Failed test (RuntimeError)
        from test.rb:5:in `<main>'
```

To make this more readable, we can change the raise statement a bit:

```ruby
def assert test
  raise RuntimeError, "Failed test", caller unless test
end
```

A failed *assert* will now throw this error, which does a better job of explaining where things went wrong:

```plain
test.rb:5:in `<main>': Failed test (RuntimeError)
```

Now we’re ready to create another assertion function, *assert_equals*. A test framework can have many different types of assertions, but when testing real applications, the vast majority will be tests for equality. Writing this assertion is easy:

```ruby
def assert_equal a, b
  assert a == b
end

assert_equal 4, 2+2 # this will pass
assert_equal 5, 2+2 # this will raise an error
```

Great, right? Wrong! Unfortunately, the error messages have gone right back to being unhelpful:

```plain
path/to/microtest.rb:6:in `assert_equal': Failed test (RuntimeError)
        from test.rb:9:in `<main>'
```

There are a couple of things we can do to improve these error messages. First, we can filter the backtrace to make it more clear where the error is coming from. Second, we can add a parameter to *assert* which will take a custom message.

```ruby
def assert test, msg = "Failed test"
  unless test then
    bt = caller.drop_while { |s| s =~ /#{__FILE__}/ }
    raise RuntimeError, msg, bt
  end
end

def assert_equal a, b
  assert a == b, "Failed assert_equal #{a} vs #{b}"
end

#=> test.rb:9:in `<main>': Failed assert_equal 5 vs 4 (RuntimeError)
```

This is much better! We’re ready to move on to another assert function, *assert_in_delta*. The way floating point numbers are represented, comparing them for equality won’t work. Instead, we will check to see that they are within a certain range of each other. We can do this with a simple calculation: (a-b).abs < ∂, where ∂ is a very small number, like 0.001 (in reality, you will probably want a smaller delta than that). Here’s the function in Ruby:

```ruby
def assert_in_delta a, b
  assert (a-b).abs <= 0.001, "Failed assert_in_delta #{a} vs #{b}"
end

assert_in_delta 0.0001, 0.0002 # pass
assert_in_delta 0.5000, 0.6000 # raise
```

We now have a solid base for our test framework. We have a few assertions and the ability to easily write more. Our next logical step would be to make a way to put our assertions into separate tests. Organizing these assertions allows us to refactor more easily, reuse code more effectively, avoid problems with conflicting tests, and run multiple tests at once.

To do this, we will wrap our assertions into functions and those function into classes, giving us two layers of compartmentalization.

```ruby
class XTest
  def first_test
    a = 1
    assert_equal 1, a # passes
  end

  def second_test
    a = 1
    a += 1
    assert_equal 2, a # passes
  end

  def third_test
    a = 1
    assert_equal 1, a # passes
  end
end
```

That adds some structure, but how do we run the tests now? It’s not pretty:

```ruby
XTest.new.first_test
XTest.new.second_test
XTest.new.third_test
```

Each test function needs to be called specifically, by name, which will become very tedious once there are 5, or 10, or 1000 tests. This is obviously not the best way to run tests. Ideally, the tests would run themselves, and to do that we’ll start by adding a method to run our tests to the class:

```ruby
class XTest
  def run name
    send name
  end

  # ...test methods…
end

XTest.new.run :first_test
XTest.new.run :second_test
XTest.new.run :third_test
```

This is still very cumbersome, but it puts us in a better position, closer to our goal of automation. Using *Class.public_instance_methods*, we can find which methods are tests:

```ruby
XTest.public_instance_methods
# => %w[some_method one_test two_test ...]

XTest.public_instance_methods.grep(/_test$/)
# => %w[one_test two_test red_test blue_test]
```

And run those automatically.

```ruby
class XTest
  def self.run
    public_instance_methods.grep(/_test$/).each do |name|
      self.new.run name
    end
  end
  # def run...
  # ...test methods...
end

XTest.run # => All tests run
```

This is much better now, but we can still improve our code. If we try to make a new set of tests, called *YTest* for example, we would have to copy these run methods over. It would be better to move the run methods into a new abstract class, *Test*, and inherit from that.

```ruby
class Test
  # ...run & assertions...
end

class XTest < Test
  # ...test methods...
end

XTest.run
```

This improves our code structure significantly. However, when we have multiple classes, we get that same tedious repetition:

```ruby
XTest.run
YTest.run
ZTest.run # ...ugh
```

To solve this, we can have the *Test* class create a list of classes which inherit it. Then we can write a method in *Test* which will run all of those classes.

```ruby
class Test
  TESTS = []

  def self.inherited x
    TESTS << x
  end

  def self.run_all_tests
    TESTS.each do |klass|
      klass.run
    end
  end
  # ...self.run, run, and assertions...
end

Test.run_all_tests # => We can use this instead of XTest.run; YTest.run; etc.
```

We’re really making progress now. The most important feature our framework is missing now is some way of reporting test success and failure. A common way to do this is to simply print a dot when a test successfully runs.

```ruby
def self.run_all_tests
  TESTS.each do |klass|
    Klass.run
  end
  puts
end

def self.run
  public_instance_methods.grep(/_test$/).each do |name|
    self.new.run name
    print "."
  end
end
```

Now, when we run the tests, it will look something like this:

```plain
% ruby test.rb
...
```

Indicating that we had three successful tests. But what happens if a test fails?

```plain
% ruby test.rb
.test.rb:20:in `test_assert_equal_bad': Failed assert_equal 5 vs 4 (RuntimeError)
  [...tons of blah blah...]
  from test.rb:30:in `<main>'
```

The very first error we come across will stop the entire test. Instead of the error being printed naturally, we can catch it and print the error message ourselves, letting other tests continue:

```ruby
def self.run
  public_instance_methods.grep(/_test$/).each do |name|
    begin
      self.new.run name
      print "."
    rescue => e
      puts
      puts "Failure: #{self}##{name}: #{e.message}"
      puts "  #{e.backtrace.first}"
    end
  end
end

# Output

% ruby test.rb
.
Failure: Class#test_assert_equal_bad: Failed assert_equal 5 vs 4
  test.rb:20:in `test_assert_equal'
.
```

That’s better, but it’s still ugly. We have failures interrupting the visual flow and getting in the way. We can improve on this. First, we should reexamine our code and try to organize it more sensibly.

```ruby
def self.run
  public_instance_methods.grep(/_test$/).each do |name|
    begin
      self.new.run name
      print "."
    rescue => e
      puts
      puts "Failure: #{self}##{name}: #{e.message}"
      puts "  #{e.backtrace.first}"
    end
  end
end
```

Currently, this one function is doing 4 things:

1. Line 2 is selecting and filtering tests.
1. The begin clause is handling errors.
1. `self.new.run name` runs the tests.
1. The various puts and print statements print results.

This is too many responsibilities for one function. *Test.run_all_tests* should simply run classes, *Test.run* should run multiple tests, *Test#run* should run a single test, and result reporting should be done by... Something else. We’ll get back to that. The first thing we can do to improve this organization is to push the exception handling into the individual test running method.

```ruby
class Test
  def run name
    send name
    false
  rescue => e
    e
  end

  def self.run
    public_instance_methods.grep(/_test$/).each do |name|
      e = self.new.run name

      unless e then
        print "."
      else
        puts
        puts "Failure: #{self}##{name}: #{e.message}"
        puts " #{e.backtrace.first}"
      end
    end
  end
end
```

This is a little better, but *Test.run* is still handling all the result reporting. To improve on that, we can move the reporting into another function, or better yet, its own class.

```ruby
class Reporter
  def report e, name
    unless e then
      print "."
    else
      puts
      puts "Failure: #{self}##{name}: #{e.message}"
      puts " #{e.backtrace.first}"
    end
  end

  def done
    puts
  end
end

class Test
  def self.run_all_tests
    reporter = Reporter.new

    TESTS.each do |klass|
      klass.run reporter
    end

    reporter.done
  end

  def self.run reporter
    public_instance_methods.grep(/_test$/).each do |name|
      e = self.new.run name
      reporter.report e, name
    end
  end

  # ...
end
```

By creating this *Reporter* class, we move all IO out of the *Test* class. This is a big improvement, but there’s a problem with this class. It takes too many arguments to get the information it needs, and it’s not even getting everything it should have! See what happens when we run tests with *Reporter*:

```plain
.
Failure: #<reporter:0x007fb64c0a6e78>#test_assert_bad:
Failed test
 test.rb:9:in `test_assert_bad'
.
Failure: #<reporter: 0x007fb64c0a6e78="">#test_assert_equal_bad: Failed
assert_equal 5 vs 4
 test.rb:17:in `test_assert_equal_bad'
.
Failure: #<reporter: 0x007fb64c0a6e78="">#test_assert_in_delta_bad: Failed
assert_in_delta 0.5 vs 0.6
 test.rb:25:in `test_assert_in_delta_bad'
</reporter:></reporter:></reporter:0x007fb64c0a6e78>
```

Instead of reporting what class has the failing test, it’s saying what reporter object is running it! The quickest way to fix this would be to simply add another argument to the report function, but that just creates a more tangled architecture. It would be better to make report take a single argument that contains all the information about the error. The first step to do this is to move the error object into a *Test* class attribute:

```ruby
class Test
  # ...
  attr_accessor :failure

  def initialize
    self.failure = false
  end

  def run name
    send name
    false
  rescue => e
    self.failure = e
    self
  end
end

```

After moving the failure, we’re ready to get rid of the name parameter. We can do this by adding a name attribute to the *Test* class, like we did with the failure class:

```ruby
class Test
  attr_accessor :name
  attr_accessor :failure
  def initialize name
    self.name = name
    self.failure = false
  end

  def self.run reporter
    public_instance_methods.grep(/_test$/).each do |name|
      e = self.new(name).run
      reporter.report e
    end
  end
  # ...
end
```

This new way of calling the *Test#run* method requires us to change that a little bit:

```ruby
class Test
  def run
    send name
    false
  rescue => e
    self.failure = e
    self
  end
end
```

We can now make our *Reporter* class work with a single argument:

```ruby
class Reporter
  def report e
    unless e then
      print "."
    else
      puts
      puts "Failure: #{e.class}##{e.name}: #{e.failure.message}"
      puts " #{e.failure.backtrace.first}"
    end
  end
end
```

We now have a much better *Reporter* class, and we can now turn our attention to a new problem in *Test#run*: it can return two completely different classes. false for a successful test and a *Test* object for a failure. Tests know if they fail, so we can know when they succeed without that false value.

```ruby
class Test
  # ...
  attr_accessor :failure
  alias failure? failure
  # ...

  def run
    send name
  rescue => e
    self.failure = e
  ensure
    return self
  end
end

class Reporter
  def report e
    unless e.failure? then
      print "."
    else
      # ...
    end
  end
end
```

It would now be more appropriate for the argument to *Reporter#report* to be named result instead of *e*.

```ruby
class Reporter
  def report result
    unless result.failure? then
      print "."
    else
      failure = result.failure
      puts
      puts "Failure: #{result.class}##{result.name}: #{failure.message}"
      puts " #{failure.backtrace.first}"
    end
  end
end
```

Now, we have one more step to improve reporting. As of right now, errors will be printed with the dots. This can make it difficult to get an overview of how many tests passed or failed. To fix this, we can move failure printing and progress reporting into two different sections. One will be an overview made up of dots and "F"s, and the other a detailed summary, for example:

```plain
...F..F..F

Failure: TestClass#test_method1: failure message 1
 test.rb:1:in `test_method1’

Failure: TestClass#test_method2: failure message 2
 test.rb:5:in `test_method2’

... and so on ...
```

To get this kind of output, we can store failures while running tests and modify the done function to print them at the end of the tests.

```ruby
class Reporter
  attr_accessor :failures
  def initialize
    self.failures = []
  end

  def report result
    unless result.failure? then
      print "."
    else
      print "F"
      failures << result
    end
  end

  def done
    puts

    failures.each do |result|
      failure = result.failure
      puts
      puts "Failure: #{result.class}##{result.name}: #{failure.message}"
      puts " #{failure.backtrace.first}"
    end
  end
end
```

One last bit of polishing on the reporter class. We’ll rename the *report* method to *<<* and the *done* method to *summary*.

```ruby
class Reporter
  # ...
  def << result
    # ...
  end

  def summary
    # ...
  end
end

class Test
  def self.run_all_tests
    # ...
    reporter.summary
  end

  def self.run reporter
    public_instance_methods.grep(/_test$/).each do |name|
    reporter << self.new(name).run
  end
end
```

We’re almost done now! We’ve got one more step. Tests should be able to run in any order, so we want to make them run in a random order every time. This is as simple as adding `.shuffle` to our *Test.run* function, but we’ll make it a little more readable by moving the *public_instance_methods.grep* statement into a new function:

```ruby
class Test
  def self.test_names
    public_instance_methods.grep(/_test$/)
  end

  def self.run reporter
    test_names.shuffle.each do |name|
      reporter << self.new(name).run
    end
  end
end
```

And we’re done! This may not be the most feature-rich test framework, but it’s very simple, small, well written, and gives us a base which is easy to extend and build on. The entire framework is only about 70 lines of code.

Thanks to Ryan Davis for an excellent talk! Also check out the [code](https://github.com/zenspider/microtest) and [slides](http://www.zenspider.com/pdf/2016_MWRC_Microtest.pdf) from the talk.
