---
author: Miguel Alatorre
gh_issue_number: 1035
tags: ruby, testing
title: Some metaprogramming examples from RSpec
---

I'm quite the curious cat and one thing that has interested me for a while has been how [RSpec](http://rspec.info/) and its **describe** and **it** methods work. In digging through  the [rspec-core gem source code (v3.1.4)](https://github.com/rspec/rspec-core/tree/v3.1.4), specifically the [example_group.rb](https://github.com/rspec/rspec-core/blob/v3.1.3/lib/rspec/core/example_group.rb) file, I came across some syntax that I had not been exposed to:

```ruby
# https://github.com/rspec/rspec-core/blob/v3.1.3/lib/rspec/core/example_group.rb

module RSpec
  module Core
    class ExampleGroup
      # ...

      def self.define_singleton_method(*a, &amp;b)
        (class &lt;&lt; self; self; end).__send__(:define_method, *a, &amp;b)
      end

      # ...

      def self.define_example_method(name, extra_options={})
        define_singleton_method(name) do |*all_args, &amp;block|

          # ...

        end
      end

      # ...

      define_example_method :it

      # ...

    end
  end
end
```

"What's with all this passing around of blocks? And what's **:define_method** doing?" I asked. The [documentation for the define_method](http://apidock.com/ruby/Module/define_method) is straightforward enough, yet I still wondered what was being accomplished in the code above. In pursuit of answers, here's what I found out.

### Metaprogramming

[Metaprogramming](http://en.wikipedia.org/wiki/Metaprogramming) is the writing of code that acts on other code instead of data, also commonly described as "code that writes code". As an example, let's reopen a class at runtime and add a method:

```ruby
class Dog
  # empty class
end

dog = Dog.new
=&gt; #&lt;Dog:0x00000006add440&gt;
dog.methods.include? :speak
=&gt; false
Dog.__send__(:define_method, :speak, Proc.new { "Woof!" })
=&gt; :speak
dog.speak
=&gt; "Woof!"
```

The block passed to the **define_method** method is used as the body of the method being defined, which in our case is the **speak** method. Note the use of **__send__** over **send**. Because some classes define their own **send** method, it's safer to use **__send__**. As another example, let's define a method that we can use to create more class methods:

```ruby
class Cat
  def create_method(method_name, &amp;method_body)
    self.class.__send__(:define_method, method_name, &amp;method_body)
  end
end

cat = Cat.new
 =&gt; #&lt;Cat:0x00000005973c68&gt;
cat.methods.include? :speak
 =&gt; false
cat.create_method(:speak) { "Meow!" }
=&gt; :speak
cat.speak
=&gt; "Meow!"
cat2 = Cat.new
=&gt; #&lt;Cat:0x00000005962da0&gt;
cat.2.speak
=&gt; "Meow!"
```

### Metaclasses

A [metaclass](http://en.wikipedia.org/wiki/Metaclass) is the class of an object that holds [singleton methods](http://en.wikipedia.org/wiki/Singleton_pattern), and a singleton method is a method which belongs to just one object. If we have an instance, dog, of a Dog class we can define a singleton method as follows:

```ruby
class Dog
end

dog = Dog.new
=&gt; #&lt;Dog:0x00000006990e70&gt;
def dog.sit
  "I'm sitting, now gimme a treat!"
end
=&gt; :sit
dog.sit
=&gt; "I'm sitting, now gimme a treat!"
dog2 = Dog.new
=&gt; #&lt;Dog:0x00000006977998&gt;
dog2.methods.include? :sit
=&gt; false
```

When Ruby looks for a method, it first looks in the object's metaclass. If it doesn't find it there, then it looks in the object's class and upwards through the inheritance chain. To access an object's metaclass we can use the following syntax:

```ruby
class Dog
end

dog = Dog.new
=&gt; #&lt;Dog:0x00000006990e70&gt;
def dog.sit
  "I'm sitting, now gimme a treat!"
end
=&gt; :sit
metaclass = class &lt;&lt; dog; self; end
=&gt; #&lt;Class:#&lt;Dog:0x00000006990e70&gt;&gt;
metaclass.instance_methods.include? :sit
=&gt; true
```

OK, with all this in mind let's define a class method that can be used to create singleton methods for that class. "Wait, wait, singleton methods for a class? But aren't singleton methods for objects?" I hear you.
In Ruby, classes are objects. If they are objects, then they can have metaclasses. Let's see it in action:

```ruby
class Cat
  def self.define_singleton_method(method_name, &amp;method_body)
    (class &lt;&lt; self; self; end).__send__(:define_method, method_name, &amp;method_body)
  end

  define_singleton_method(:speak) {  "Meow!" }
  define_singleton_method(:purr) { "Purr!" }
  define_singleton_method(:hiss) { "Hiss!" }
end

Cat.speak
=&gt; "Meow!"
Cat.methods.grep(/speak|purr|hiss/)
=&gt; [:speak, :purr, :hiss]
cat = Cat.new
=&gt; #&lt;Cat:0x000000067e8d20&gt;
cat.methods.grep(/speak|purr|hiss/)
[]
```

Hmm, the methods **speak**, **purr**, and **hiss** look like class methods, don't they? Aha! I've learned that class methods are actually singleton methods of the class object, or, instance methods of the class object's metaclass!

```ruby
class Person
  def self.greet
    "Hello there!"
  end
end

metaclass = class &lt;&lt; Person; self; end
=&gt; #&lt;Class: Person&gt;
metaclass.instance_methods.include? :greet
=&gt; true
```

If we go back and look at the code block where we defined class method **define_singleton_method** for the Cat class,
we can see now that this method, by opening up the class' metaclass and sending it **define_method**, is basically just creating
more class methods. And this is exactly what's going on in the example_group.rb file; the class methods :describe, :it, etc., are created via metaprogramming. Neat!

There's still lots more for me to learn when it comes to metaprogramming. Here's one [blog article](http://yehudakatz.com/2009/11/15/metaprogramming-in-ruby-its-all-about-the-self/) by Yehuda Katz that I found really helpful in understanding metaprogramming, especially the role of **self**.
