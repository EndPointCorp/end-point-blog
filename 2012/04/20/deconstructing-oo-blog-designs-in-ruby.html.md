---
author: Brian Buchalter
gh_issue_number: 596
tags: ruby
title: Deconstructing an OO Blog Designs in Ruby 1.9
---



I've become interested in Avdi Grimm's new book [Object on Rails](http://objectsonrails.com), however I found the code to be terse.  Avdi is an expert Rubyist and he makes extensive use of Ruby 1.9 with minimal explanation.  In all fairness, he lobbies you to buy Peter Cooper's [Ruby 1.9 Walkthrough](http://www.rubyinside.com/19walkthrough/).  Instead of purchasing the videos, I wanted to try and deconstruct them myself.

In his first chapter featuring code, Mr. Grimm creates a Blog and Post class.  For those of you who remember the original [Rails blog demo](http://www.youtube.com/watch?v=Gzj723LkRJY), the two couldn't look more different. 

### Blog#post_source

In an effort to encourage Rails developers to think about relationships between classes beyond [ActiveRecord::Relation](http://api.rubyonrails.org/classes/ActiveRecord/Relation.html), he creates his own interface for defining how a Blog should interact with a "post source".

```ruby
# from http://objectsonrails.com/#sec-5-2
class Blog
  # ...
  attr_writer :post_source
  
  private
  def post_source
    @post_source ||= Post.public_method(:new)
  end
end
```

The code above defines the Blog class and makes available post_source= via the attr_writer method.  Additionally, it defines the attribute reader as a private method.  The idea being that a private method can be changed without breaking the class's API.  If we decide we want a new default Post source, we can do it safely.

The magic of this code is in defining the post source as a class's method, in this case, Post.public_method(:new).  The #public_method method is defined by Ruby's Object class and is similar to [#method](http://ruby-doc.org/core-1.9.3/Object.html#method-i-method) method.  In short, it gives us a way of not directly calling Post.new, but instead, referring to the method that's responsible for creating new posts.  This is logical if you remember that the name of this method is #post_source.

Now let's look how he puts post_source into action.

```ruby
class Blog
  # ...
  def new_post
    post_source.call.tap do |p|
      p.blog = self
    end
  end
  # ...
end
```

During my first reading, it wasn't clear at all what was going on here, but if we remember that post_source is responsible for returning the method need to "call", we know that post_source.call is equivalent to Post.new. For the sake of clarity-while-learning for those not familiar with post_source.call, let's substitute it with something more readable so we can understand how tap is being employed.

```ruby
class Blog
  # ...
  def new_post
    Post.new.tap do |p|
      p.blog = self
    end
  end
end
```

The [tap](http://ruby-doc.org/core-1.9.3/Object.html#method-i-tap) method is available to all Ruby objects and serves as a way to have a block "act on" the method's caller and return the object called.  Per the docs, "the primary purpose of this method is to 'tap into' a method chain, in order to perform operations on intermediate results within the chain".  For some examples on using tap see MenTaLguY's post on [Eavesdropping on Expressions](http://moonbase.rydia.net/mental/blog/programming/eavesdropping-on-expressions).  As he says in his post, "you can insert your [code] just about anywhere without disturbing the flow of data".  Neat.

In this case, it's being used to tap into the process of creating a new blog post and define the blog to which that post belongs.  Because tap returns the object it modifies, #new_post returns the post now assigned to the blog.

### Brining it All Together

Avdi's approach may seem cumbersome at first, and it is compared to "the Rails way."  But in general, that's the whole point of Object on Rails; to challenge you to see beyond a generic solution to a problem (in this case defining relationships between classes) so you can build more flexible solutions.  Let's see some interesting things we might be able to do with this more flexible Blog class.  We can imagine this same Blog class being able to handle posts from all sorts of different sources.  Let's see if we can get creative.

```ruby
class EmailPost &lt; ActionMailer::Base
  def receive(message)
    @blog = Blog.find_by_owner_email(message.from)
    @blog.post_source = EmailPost.public_method(:new)
    @email_post = @blog.new_post(params[:email_post])
    @email_post.publish
  end
end
```

With this little snippet, we're able to use the Blog class to process a different sort of post.  We simply let the blog know the method to call when we want a new post and pass along the arguments we'd expect.  Let's see if we can think of something else that's creative.

```ruby
require 'feedzirra'
# execute regularly with cronjob call like curl -d "blog_id=1&amp;url=http://somefeed.com" http://myblog.com/feed_poster"

class FeedPostersController
  def create
    @feed = Feedzirra::Feed.fetch_and_parse(params[:url])
    @blog = Blog.find(params[:blog_id])
    @post.post_source = FeedPost.public_method(:new)
    @feed.entries.each do |entry|
      @blog.new_post(entry)
    end
  end
end
```

We could imagine the FeedPost.new method being the equivalent of a retweet for your blog using an RSS feed!  Try having the blog class doing this with an ActiveRecord association!  Seems to me the Blog class might need to get a bit more complex to support all these Post sources which makes post_source.call.tap look pretty good!


