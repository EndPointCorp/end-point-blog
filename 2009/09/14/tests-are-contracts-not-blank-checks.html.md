---
author: Steven Jenkins
gh_issue_number: 198
tags: rails
title: Tests are contracts, not blank checks
---



Recently, I wrote up a new class and some tests to go along with it, and I was
lazy and sloppy.  My class had a fairly simple implementation (mostly a set of accessors, plus a to_s method).   It looked something like this:

```ruby
class Soldier
  attr_accessor :name, :rank, :serial_number
  def initialize(name,rank,serial_number)
    @name = name
    @rank = rank
    @serial_number = serial_number
  end

  def to_s
    "#{name}, #{rank}, #{serial_number}"
  end
end
```

I had been trying to determine the essential attributes of the class (e.g., what are the minimal elements of this class?  should I have a base class, then sub-class it for the various differences, or should I have only a single class that contains everything I need?)

As a result of the speculative nature of the development, my tests only included a few of the attributes.

What's wrong with that?

On the surface, there is nothing technically wrong with skipping accessor tests: after all, testing each accessor individually is really testing Ruby, not the code I wrote.  Another excuse I made is that testing each individually is very non-DRY - the testing code itself has lots of duplication.

The problem is that the set of tests should be considered a contract between the class writer and the outside world.  By not including the correct and complete list of accessors, I left out important information;  it's a check, already signed by the class developer, but with the amount left blank.

I've seen some code solve the non-DRY-ness problem like the following:

```ruby
class Soldier
  Attributes = [:name, :rank, :serial_number]
  Attributes.each {|attr| attr_accessor attr}
  ...
```

then testing code of:

```ruby
  Attributes.each do |attr|
    it "should have an accessor for #{attr}" do
      ...
```

That let's the testing code be nice and compact; simply load in the class, then iterate over the Attributes to verify that the accessors are present.

From a tests are contracts standpoint, this approach is terrible, though, perhaps even worse than the original, incomplete set of tests I had written.  All the reader of the tests learns is that there is an array of attributes; the reader has to go look at the implementation itself to see what those attributes are.

Better is to use an anonymous array in the test, duplicating the attribute list; i.e.,

```ruby
  [:name,:rank,:serial_number].each do |attr|
    it "should have an accessor for #{attr}" do
      ...
    end
  end
```

That seems to be a good balance between keeping tests as contacts yet keeping them DRY.


