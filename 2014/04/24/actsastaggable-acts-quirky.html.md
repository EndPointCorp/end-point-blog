---
author: Marina Lohova
gh_issue_number: 971
tags: rails
title: ActsAsTaggable acts quirky
---

I've been recently working on a project with the extensive use of ActsAsTaggable gem (version 2.4.1). I would like to share a couple of things that were not immediately evident and caused some confusion.

Issue #1 

You should be consistent with how you assign tags. ActsAsTaggable is very versatile as it provides such features as tagging contexts and tagging ownership. Contexts allow to create named subsets of tags for the item. Ownerships allow for the item to have different tags for different owners. It is very easy to assign tag in the default "tags" context and later be wondering why the tag is not showing up in the custom context, or vice versa. The following method always assigns the tag within the "tags" context: 

```ruby
@photo.tag_list = "New York, USA"
```
So if you update the tag list in the custom context later:

```ruby
@photo.set_tag_list_on("album_3", "New York, USA")
```
you will basically be creating the second tagging for the "New York" tag with the "album_3" context.

The third tagging is generated if the same photo is tagged by the "owner" @user.

```ruby
@user.tag(@photo, :with => "New York", :on => "album_3")
```

Issue #2

Tag count methods include the common "tags" context no matter which "tagging_key" you specify.

```ruby
tags = Photo.tag_counts_on("album_3") 
tags.select {|t| t.name == "New York" }.first.count
=> 28470 
```
The above will return tags with the "album_3" and "tags" contexts.

Issue #3

"Tagged_with" method may return duplicates. It happens as a result of the query including the "tags" context by default. If multiple contexts were present you will have to manually exclude the duplicates from the list to get the correct counts.

```ruby
f = Photo.tagged_with("New York", :on => "album_3").size
=> 28470 
```
```ruby
f = Photo.tagged_with("New York", :on => "album_3").uniq.size
=> 27351 
```

