---
author: Brian Buchalter
gh_issue_number: 658
tags: rails
title: Simple Example of Dependency Injection with Rails
---



Today I came across a great opportunity to illustrate dependency injection in a simple context. I had a Rails partial that was duplicated across two subclasses.  The partial was responsible for displaying options to create a new record from the data of the current record.  It also offered two types of copy, shallow and deep.  The shallow copy used a button to POST data, while the deep copy offered a form with some additional options.  The only difference between the partials was the path to post data to. Let's see this in code.

```ruby
#app/views/fun_event/_copy_options.html.erb
button_to(t("create_and_edit_shallow_copy"), fun_event_path(:from_event => @event.id, :return => true), :    id => "shallow_copy_btn")

form_tag(fun_event_path(:return => true)) do
  #form code
end

#app/views/boring_event/_copy_options.html.erb
button_to(t("create_and_edit_shallow_copy"), boring_event_path(:from_event => @event.id, :return => true), :    id => "shallow_copy_btn")

form_tag(boring_event_path(:return => true)) do
  #form code
end
```

### The first, failed iteration

To remove the duplication, I passed in a path option into the partial, replacing specific references with the generic.

```ruby
#app/views/fun_events/copy.html.erb
<%= render :partial => "events/copy_options", :event_path => fun_event_path %>

#app/views/boring_events/copy.html.erb
<%= render :partial => "events/copy_options, :event_path => boring_event_path %>

#app/views/events/_copy_options.html.erb
button_to(t("create_and_edit_shallow_copy"), event_path(:from_event => @event.id, :return => true), :    id => "shallow_copy_btn")

form_tag(event_path(:return => true)) do
  #form code
end
```

Can you guess where this led?

```
undefined method `event_path' for ActionView::Base:0xd6acf18
```

### Dude! Inject the dependency!

Obviously the event_path variable I was passing was a string, not a method.  I needed the method so I could pass in the appropriate arguments to construct the URL I needed.  Had there not been two different calls to the routes, I would likely have just passed in the string needed in each context.  But in this case, I was forced to think outside the box.  Here's what I ended up with.

```ruby
#app/views/fun_events/copy.html.erb
<%= render :partial => "events/copy_options", :event_path => method(:fun_event_path) %>

#app/views/boring_events/copy.html.erb
<%= render :partial => "events/copy_options, :event_path => method(:boring_event_path) %>

#app/views/events/_copy_options.html.erb
button_to(t("create_and_edit_shallow_copy"), event_path.call(:from_event => @event.id, :return => true), :    id => "shallow_copy_btn")

form_tag(event_path.call(:return => true)) do
  #form code
end
```

The changes are really quite subtle, but we use Object's [method](http://ruby-doc.org/core-1.9.3/Object.html#method-i-method) method to pass the reference to the method we want to call, and simply pass in the arguments when needed.  Mind == Blown


