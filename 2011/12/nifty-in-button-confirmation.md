---
author: Evan Tann
title: Nifty In-Button Confirmation
github_issue_number: 529
tags:
- javascript
- jquery
- rails
date: 2011-12-19
---



I’ve been working on a personal email client after work, called [Warm Sunrise](https://web.archive.org/web/20120318064212/http://warmsunrise.com/), that forces myself to keep a manageable inbox. One of the goals of the project was to get to a zero-inbox everyday, so I needed a ‘Delete All’ button that was easy-to-use without running the risk of *accidentally* deleting emails. I took a look at JavaScript’s confirm, which is jarring, and jQuery’s dblClick, which doesn’t provide any feedback to the user after the first click, leaving the user to wonder why their emails weren’t deleted.

Given these options, I built my own button using Rails 3.1, jQuery, and CoffeeScript, that better fit the goals I set out with. It requires a double click, but gives the user a confirmation in the button itself, without any sort of timeout.

Starting with **app/views/letters/index.html.erb**, I generated the buttons using Rails helpers and Twitter’s Bootstrap classes:

```ruby
<%= link_to 'Write letter', new_letter_path, :class => "btn primary pull-right far-right" %>
<%= link_to 'Delete all', '#', :class => "btn pull-right no_danger", :id => "delete_all" %>
<%= link_to 'Are you sure?', delete_all_letters_path, :method => :destroy, :class =>"btn pull-right danger confirm", :id => "delete_all", :style => "display:none;" %>
```

Notice that the ‘Delete all’ button doesn’t actually specify a url and the ‘Are you sure?’ link’s style is set to "display:none"

Here’s the relationship I set up in my models:

**app/models/letter.rb**

```ruby
belongs to :user
```

**app/models/user.rb**

```ruby
has_many :letters, :dependent => :destroy
```

I set up **config/routes.rb** to work with the explicit path I set in:

```ruby
post 'delete_all_letters' => 'letters#delete_all'
```

Finally, I finished this lot by adding the delete_all action to my **app/controllers/letters_controller.rb**:

```ruby
def delete_all 
    current_user.letters.delete_all

    respond_to do |format|
        format.html { redirect_to letters_url, notice: 'Successfully deleted all letters.' }
        format.json { head :ok }
    end 
end 
```

CoffeeScript is a beautiful language that compiles to JavaScript, which I prefer to JavaScript itself. You can read more about it [here](https://coffeescript.org/). Let’s take a look at the **CoffeeScript** that makes this button work:

```js
$('a#delete_all.no_danger').hover( ->
    $(this).addClass('danger')
    $(this).click( ->
        $('a#delete_all.no_danger').hide()
        $('a#delete_all.confirm').show()
    )   
)
$('a#delete_all.no_danger').mouseleave( ->
    $(this).removeClass('danger')
)
$('a#delete_all.danger').mouseleave( ->
    $(this).hide()
    $('a#delete_all.no_danger').show()
)
```

Since the button’s text changes to a confirmation on the first click, makes it better for my purposes than Javascript’s dblClick method. Check the video to see what it looks like in action.

Let’s take a look at what this compiles to in plain **JavaScript**, too, since this is the only thing the browser sees:

```js
$('a#delete_all.no_danger').hover(function() {
    $(this).addClass('danger');
    return $(this).click(function() {
        $('a#delete_all.no_danger').hide();
        return $('a#delete_all.confirm').show();
    });
});
$('a#delete_all.no_danger').mouseleave(function() {
    return $(this).removeClass('danger');
});
$('a#delete_all.danger').mouseleave(function() {
    $(this).hide();
    return $('a#delete_all.no_danger').show();
});
```

Not shown in the video, but I modified index.html.erb to only show the ‘Delete all’ button when the user has a zero-inbox.

```ruby
<%= link_to 'Write letter', new_letter_path, :class => "btn primary pull-right far-right" %>
<% if !@letters.empty? %>
    <%= link_to 'Delete all', '#', :class => "btn pull-right no_danger", :id => "delete_all" %>
    <%= link_to 'Are you sure?', delete_all_letters_path, :method => :destroy, :class =>"btn pull-right danger confirm", :id => "delete_all", :style => "display:none;" %>
<% end %>
```

