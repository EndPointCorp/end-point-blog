---
author: Brian Gadoury
title: Instance Variable Collision with ActsAsTaggableOn
github_issue_number: 606
tags:
- ruby
- rails
date: 2012-05-03
---



As developers, a lot of what we do is essentially problem solving. Sometimes it’s a problem of how to implement a specific feature. Sometimes it’s a problem *with* a specific feature. Last week, I ran into a case of the latter in some relatively mature code in the Rails app I was working on.

I was getting a sporadic exception while trying to save an instance of my StoredFile model. I encountered the problem while implementing a pretty trivial boolean field in my model, while I was playing around with it in the rails console. This is where it gets a little weird.

The exception message:

```plain
#<NoMethodError: undefined method 'uniq' for "":String>
#Backtrace:
... acts-as-taggable-on-2.2.2/lib/acts_as_taggable_on/acts_as_taggable_on/<b>core.rb</b>:264:in 'block in save_tags'
...rest of backtrace...
```

Note that none of my work was related to my model’s use of [acts_as_taggable_on](https://rubygems.org/gems/acts-as-taggable-on). I looked briefly at line 264 and its cohorts in core.rb, but nothing jumped out as “a giant, obvious bug in acts-as-taggable-on” (which I wouldn’t expect.) Also, the actual error is a bit suspicious. I love duck typing (and ducks) as much as anyone, but it’s pretty rare to see well traveled code try to call uniq() on a String. An empty array, sure, no problem. I’ll call uniq() on an empty array all day—​but a String? *Madness*.

In the absence of any obvious answers, I switched to serious debug mode. I remembered that I ran into this same issue briefly about two weeks ago, but it had fixed itself. Then I remembered that this app is not Skynet and is therefore incapable of “fixing itself.” OK, so there’s been a bug lurking for a while. I was going to need a code debugging montage to get to the bottom of this. I fired up some techno music and the blue mood lighting in my office, and got down to debugging.

By the end of the debugging montage, I had determined that my StoredFile model was overriding the “tag_list” method supplied by ActsAsTaggableOn, in order to return the tags for this StoredFile instance regardless of which User owned the tags. Here’s our entire method:

```ruby
def tag_list
    @tag_list ||= self.anonymous_tag_list(:tags)
end
```

Can you guess where the issue might be with this code? Hint: It’s the @tag_list instance variable. We’re actually only using it here as a lazy way to cache the return value of self.anonymous_tag_list(:tags) during the lifespan of this single instance. I came to discover that ActsAsTaggableOn defines and uses an instance variable of the same exact name within the scope of my model. So, my tag_list method was assigning "" to the @tag_list instance variable for a StoredFile instance with zero tags, and that was trampling the [] that ActsAsTaggableOn would expect in that scenario. Hence, the ill-fated attempt to call "".uniq(). 

As a bonus, because it’s an instance variable assigned inside a method, it would only get populated/trampled by my StoredFile model if an instance’s tag_list was examined in any way. A sort of reverse Heisenbug, if you will. Renaming @tag_list to something else fixed the bug.

It was a problem and I solved it, which is cool. But, is this injection of instance variables considered poor behavior on ActsAsTaggableOn’s part? What do you think? I’m still not sure how I feel about it, but I do know how I felt when I figured it out and fixed it:

<div class="separator" style="clear: both; text-align: center; padding-bottom: 15px;"><img border="0" height="206" src="/blog/2012/05/instance-variable-collision-with/image-0.gif" width="320"/></div>


