---
author: Mike Farmer
gh_issue_number: 804
tags: ruby, rails, testing
title: Isolation Test Helper for Rails Development
---



Lately I've been inspired to test drive my development as much as possible. One thing that is absolutely critical for test driven development is fast feedback from your tests. Because of this, I try to remove the "Rails" dependency as often as possible from my tests so I don't have to wait for Rails to load for my tests to run. Sure, I could use [spork](https://github.com/sporkrb/spork) or [zeus](https://github.com/burke/zeus) to pre-load Rails, but I find that those tools don't always reload the files I'm working on. Besides, I believe that much of your application should be plain old ruby objects that are well designed.

One of the things I continually bump against with isolated tests is that there are a few things that I always have to do to get my isolated tests to work. Since we are accustomed to requiring spec_helper.rb or test_helper.rb for tests dependent on Rails, I decided to build a helper for when I run isolated tests to just load some niceties that make running them a little easier.

So, here's the full code from my isolation helper (this one works with RSpec).

```ruby
# spec/isolation_helper.rb
DO_ISOLATION = ! defined?(Rails)

def isolate_from_rails(&amp;block)
  return unless DO_ISOLATION
  block.call
end

isolate_from_rails do
  require 'awesome_print'
  require 'active_support/all'
  require 'ostruct'
  ap "You are running isolated from Rails!"

  # swallow calls to Rails
  class ::Rails
    def self.root; File.expand_path("../", File.dirname(__FILE__)); end
    def self.method_missing(a,*b); self; end
  end

  # Some RSpec config
  RSpec.configure do |config|
    config.treat_symbols_as_metadata_keys_with_true_values = true
    config.filter_run :focus =&gt; true
    config.run_all_when_everything_filtered = true
  end
end
```

I'm going to walk through this a little as so that you can understand why I'm doing some of these things. First off, I don't want to run isolated if Rails is actually loaded. This ensures that my tests pass when run as a whole and by themselves. So the DO_ISOLATION constant just lets me know whether Rails is loaded or not.

The second part of the helper is where I setup a little method called isolate_from_rails. This is just a method that can be used to hide things from Rails during my isolated tests. For example:

```ruby
require 'isolation_helper'

isolate_from_rails do 
  class Product; end
end

describe MyProductValidator do

  it "ensures that invalid records return false" do
    Product.stub :find_by_name { OpenStruct.new(:product, :name =&gt; "invalid", :valid =&gt; false) }
    pv = MyProductValidator.validate Product.find_by_name("invalid")
    pv.valid.should be_false
  end

end
```

This is obviously a contrived example. But what I want here is to make sure when I run in isolation that I have the behavior of my models stubbed correctly. So I isolate the model from Rails and stub the behavior I want to test against. This test will pass whether Rails is loaded or not. (I know, this is just testing my stub, but I'm attempting to demonstrate an example, not real running code.)

The next thing is I do in the isolation_helper is use the isolate_from_rails method to setup some commonly used things I use in my isolated tests. First are the requires. [awesome_print](https://github.com/michaeldv/awesome_print) is a handy gem that makes it easy to spit stuff out to SDTOUT in a pretty way. Think pp on steroids. Then I load active_support. This one is optional, but I find that active_support really doesn't take all that long to load and it's worth it to be able to use all the niceties that Rails provides such as blank? and present? methods.

The ostruct library is very nice for stubbing or mocking object dependencies using the OpenStruct class. I've already given an example above of how nice it can be for quickly stubbing out a model, but it works great for just about any object.

Next I just put a friendly reminder out there using awesome_print that I'm running isolated.

One of the biggest annoyances with running isolated tests are logging statements. If I'm testing a class in isolation, I don't really want to see the output of all the Rails.logger.info statements in the code. I also want to make sure Rails dependencies aren't turning up in my code. The next lines in the helper simply swallow all method calls made to Rails. (BTW, this include Rails.cache which is why I always wrap my calls to the rails cache in a facade, so it's easy to switch out during testing to ensure caching is working. I'll have to explain further in another blog post.) The only method left behind is is Rails.root and I leave that there just in case I need to get at the root of the application easily.

The next block of code are some configuration settings for RSpec. These can be removed if you are using TestUnit or MiniTest.

Overall, I've really liked the freedom this little helper gives me during my test development. It's pretty straight-forward and doesn't do anything too magical. It can also easily be added upon, just like spec_helper.rb or test_helper.rb if needed. If you have anything you think should or shouldn't be added in there, please feel free to leave a comment. I'm always looking for a way to improve things.


