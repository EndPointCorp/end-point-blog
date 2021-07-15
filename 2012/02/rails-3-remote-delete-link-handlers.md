---
author: Brian Gadoury
title: Rails 3 remote delete link handlers with Unobtrusive Javascript
github_issue_number: 560
tags:
- javascript
- jquery
- rails
- tips
date: 2012-02-28
---

I recently encountered a bug in a Rails 3 application that used a remote link_to tag to create a Facebook-style “delete comment” link using unobtrusive javascript. I had never worked with remote delete links like this before, so I figured I’d run through how I debugged the issue.

Here are the relevant parts of the models we’re dealing with:

```ruby
class StoredFile < ActiveRecord::Base
  has_many :comments, :dependent => :destroy
end
class Comment < ActiveRecord::Base
  belongs_to :user
  belongs_to :stored_file
end
```

Here’s the partial that renders a single Comment (from the show.html.erb view for a StoredFile) along with a delete link if the current_user owns that single Comment:

```ruby
<%= comment.content %> -<%= comment.user.first_name %>
<% if comment.user == current_user >
  <%= link_to 'X', stored_file_comment_path(@stored_file, comment), :remote => true, :method => :delete, :class => 'delete-comment' >
<% end ->
```

Here’s a mockup of the view with 3 comments:

<a href="/blog/2012/02/rails-3-remote-delete-link-handlers/image-0.png" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2012/02/rails-3-remote-delete-link-handlers/image-0.png"/></a>

At first, the bug seemed to be that the “X” wasn’t actually a link, and therefore, didn’t do anything. Clicking the “X” with Firebug enabled told a different story. There was a link there (hidden by sneaky CSS,) and the Firebug console showed that it was sending the appropriate request to the correct url: /stored_files/78/comments/25

The development.log file on the server corraborated the story and showed a successful delete:

```nohighlight
Started DELETE "/stored_files/78/comments/25"
  Processing by CommentsController#destroy as JS
  Parameters: {"stored_file_id"=>"78", "id"=>"25"}
  SQL (0.6ms)  DELETE FROM "comments" WHERE "comments"."id" = 25
  Completed 200 OK in 156ms
```

So far, so good. I know that our client code is making the correct request and the Rails app is handling it appropriately. I knew that the existing code “worked,” but still didn’t provide UI feedback to inform the user. I needed to write some jQuery to handle the successful (HTTP 
200) server response to our unobtrusive javascript call. 

Normally, when writing my own handler (e.g. to handle a button click) to initiate an Ajax call with jQuery, I’d use $.ajax or $.post and use its built-in success handler. Something like this:

```javascript
$.ajax({
    type: 'POST',
    url: 'my_url',
    data: { param_name1: 'param_value1'},
    success: function(data){ 
        alert('Successfully did the needful!');
    }
});
```

It turns out that you still define a event handler when handling server responses to unobtrusive javascript, it’s just that the syntax is very different. I needed to bind the ‘ajax:success’ event when it’s fired by any of my comment delete links (where class=”delete-comment”, as specified in my link_to call).

```javascript
$(document).on('ajax:success', '.delete-comment', function() {
    // .parent() is the div containing this "X" delete link
    $(this).parent().slideUp();
    }
);
```

(Note that I happen to be using the newer jQuery 1.7+ .on() method and 
argument list instead of the older, more common .live() style. In this case, they are 
functionally equivalent, but [the methods that .on() replaces are deprecated in jQuery 1.7](http://api.jquery.com/on/).)

Now, when the user clicks the “X” to delete one of their own comments, the successful unobtrusive javascript call is detected and the div containing that single comment is neatly hidden with the help of jQuery’s slideUp() method. 

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/02/rails-3-remote-delete-link-handlers/image-1.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2012/02/rails-3-remote-delete-link-handlers/image-1.png"/></a></div>

Much better!
