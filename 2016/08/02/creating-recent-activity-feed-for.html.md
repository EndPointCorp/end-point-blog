---
author: Piotr Hankiewicz
gh_issue_number: 1248
tags: rails, ruby
title: Creating a recent activity feed for Thredded
---

### Introduction

[Thredded](https://github.com/thredded/thredded) is open source forum/message board software for [Rails](http://rubyonrails.org/) 4.2+. The project is still alive and maintained by its author actively. For a new Rails project for a client in End Point we used Thredded as a part of an application stack. It works pretty well, but sometimes it lacks some important features. Fortunately, it's coded very nice and easy to extend its core functionality. This time we wanted to create a recent activity feed for a current user. I wanted to share this with you because I think that it's a popular widget in many social community sites.

### Plan

We decided to put two main data sources for the feed:

- user personal message notifications,
- user forum message notifications (you may want to put some extra features here to show posts only from topics where the user is directly involved in by writing a message, for our needs it was enough to show every new post that the user was able to see).

### Getting data

Let's say that we created a *WidgetController* controller. How to get data that we are interested in? It's not so difficult. First, this is how we are getting the latest 5 private messages for a user:

```ruby
private_messages = Thredded::PrivateTopic
  .distinct
  .for_user(current_user)
  .order_recently_updated_first
  .includes(:user)
  .limit(5)
```

We use a *PrivateTopic* model to get private message for a *current_user*, sorted by date in descending order, including a message author and limiting to 5 records.

Now, to get a regular topic posts we need to:

```ruby
posts = current_user
  .thredded_posts
  .where(messageboard_id: Pundit.policy_scope(current_user, Thredded::Messageboard.all).pluck(:id))
  .order_newest_first
  .limit(5)
```

We get the latest 5 posts from all the threads that a user has access to. Assuming that an action name is *show*, this is how it can looks all together (widget_controller.rb):

```ruby
class WidgetController &lt; ApplicationController
  def show
    @messages = []

    posts = current_user
      .thredded_posts
      .where(messageboard_id: Pundit.policy_scope(current_user, Thredded::Messageboard.all).pluck(:id))
      .order_newest_first
      .limit(5)
    posts.each do |post|
      topic = Thredded::Topic.find(post.postable_id)

      @messages &lt;&lt; {
        title: topic.title,
        path: Thredded::UrlsHelper::topic_url(topic, only_path: true),
        author: User.find(post.user_id),
        type: 'forum',
        created_at: post.created_at
      }
    end

    private_messages = Thredded::PrivateTopic
      .distinct
      .for_user(current_user)
      .order_recently_updated_first
      .includes(:last_user, :user)
      .limit(5)

    private_messages.each do |pm|
      @messages &lt;&lt; {
        title: pm.title,
        path: Thredded::UrlsHelper::topic_url(pm, only_path: true),
        author: User.find(pm.user_id),
        type: 'pm',
        created_at: pm.created_at
      }
    end

    @messages = @messages.sort_by{|e| e[:created_at]}.reverse.take(5)
  end
end
```

We merged two lists of items, sorted by date and limited to show only 5 items and created a view variable to access it from a view that we are going to create now.

### Showing data

The data is ready now, the only thing that we need to do now is to create a view. We are going to use *haml* as a templating language. Create a file called show.html.haml. Put this piece of code in there:

```ruby
%table
  %tbody
    - @messages.each do |message|
      %tr
        %td
          - if message[:type] == 'pm'
            %strong= link_to truncate('Private message', :length =&gt; 25), message[:path]
            from
            = ' '
            = link_to message[:author].username, user_path(message[:author])
            = ' '
            = time_ago_in_words(message[:created_at])
          - else
            %strong= link_to truncate(message[:title], :length =&gt; 25), message[:path]
            by
            = ' '
            = link_to message[:author].username, user_path(message[:author])
            = ' '
            = time_ago_in_words(message[:created_at])
```

We are looping through a list of messages. We need to distinguish between a private message and a regular post, just to make it nicer and user friendly. You may need to play a little bit with an author's property, it may be different for your project. If you have any problems, please comment! Good luck!

### The end

The only documentation I know about is here: [https://github.com/thredded/thredded](https://github.com/thredded/thredded)

Thanks for reading.


