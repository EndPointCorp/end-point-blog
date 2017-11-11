---
author: Brian Gadoury
gh_issue_number: 678
tags: ruby, rails, tips
title: Rails 3 ActiveRecord caching bug ahoy!
---



Sometimes bugs in other people's code makes me think I might be crazy. I’m not talking Walter Sobchak gun-in-the-air-and-a-Pomeranian-in-a-cat-carrier crazy, but “I must be doing something incredibly wrong here” crazy. I recently ran into a Rails 3 ActiveRecord caching bug that made me feel this kind of crazy. Check out this pretty simple caching setup and the bug I encountered and tell me; Am I wrong?

I have two models with a simple parent/child relationship defined with has_many and belongs_to ActiveRecord associations, respectively. Here are the pertinent bits of each:

```ruby
class MimeTypeCategory < ActiveRecord::Base
  # parent class
  has_many :mime_types

  def self.all
    Rails.cache.fetch("mime_type_categories") do
    MimeTypeCategory.find(:all, :include => :mime_types)
  end
end

class MimeType < ActiveRecord::Base
  # child class
  belongs_to :mime_type_category
end
```

Notice how in MimeTypeCategory.all, we are eager loading each MimeTypeCategory’s children MimeTypes because our app tends to use those MimeTypes any time we need a MimeTypeCategory. Then, we cache that entire data structure because it’s a good candidate for caching and we like our app to be fast.

Now, to reproduce this Rails caching bug, I clear my app’s cache using 'Rails.cache.clear' in the rails console, then load any page in my app that calls MimeTypeCategory.all. The page loads successfully and shows no errors. Doesn’t sound like a bug so far, right? If I load that same page a second time, I will get the standard Rails error page with:

```nohighlight
undefined class/module MimeType
...
(app/models/mime_type_category.rb:17:in 'all')
```

Crazy, right? Why does it *appear* that one cannot cache model instances in Rails, and why did it work for exactly one page request after the Rails cache was cleared? Well, the former obviously cannot be true, and the latter is due to how Rails.cache.fetch handles cache misses and cache hits. For a cache miss, Rails.cache.fetch executes its block, serializes the return value, saves it to your cache store, then returns the block’s return value directly. For a cache hit, it reads the cached block from your cache store, deserializes it into whatever objects it identifies itself as, and returns that.

This is all well and good until you’re going along, innocently working on your app in the development Rails environment with config.cache_classes = false (which forces your app to lazy-load requested classes for each page request.) In that situation, Rails will try to deserialize the cached data structure that had references to the MimeType class. But, Rails may not have loaded the MimeType class at that point, so deserialization will fail and produce the error we see there. If you have other code paths in your app that do happen to load the child class before this type of cached parent/child class data structure, you might not hit the bug. Now you’ve entered a world of debugging pain.

I’m not about to give up on automatic class reloading in my development environment, and I don’t want to remove the cached eager loading of my child MimeTypes class because it’s sweet. So, after some digging, I discovered a solution: require_association. Adding “require_association ‘mime_type’ to my parent MimeTypeCategory class forces Rails to load the MimeType model when it loads the MimeTypeCategory model such that it can always deserialize the cached data structure successfully. I’ve used require_association in the same way for other instances of the same caching bug in our app as well.

Hopefully this explanation helps people avoid some of the pain I experienced while trying to determine if it was a Rails bug/feature or if I had finally gone insane. I should point out that some of the reading I’ve done suggests “require_dependency” is the more appropriate solution for this problem. I’ve verified that require_association works in all my cases, but to avoid “programming by coincidence,” I am going to snoop around the Rails core to understand the difference between the two.

Lastly, please remember: You can’t board a Pomeranian - they get upset and their hair falls out.


