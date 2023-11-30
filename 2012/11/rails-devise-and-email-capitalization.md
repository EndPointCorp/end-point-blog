---
author: Steph Skardal
title: 'Rails: Devise and Email Capitalization'
github_issue_number: 727
tags:
- rails
date: 2012-11-30
---

This week, I found a bug for one of our Rails clients that was worth a quick blog post. The client website runs on Rails 3.2.8 with ActiveRecord and PostgreSQL, uses [RailsAdmin](https://github.com/sferik/rails_admin) for an admin interface, [Devise](https://github.com/plataformatec/devise) for user authentication, and [CanCan](https://github.com/ryanb/cancan) for user authorization. Before we found the bug, our code looked something like this:

```ruby
class SomeController < ApplicationController
  def some_method
    user = User.find_or_create_by_email(params[:email])
    # do some stuff with the user provided parameters
    if user.save
      render :json => {}
    else
      render :json => {}, :status => 500
    end
  end
end
```

It's important to note that the 500 error wasn't reported to the website visitor — there were no visible UI notes to indicate the process had failed. But besides that, this code looks sane, right? We are looking up or creating a user from the provided email, updating the user parameters, and then attempting to save. For the most part, this worked fine, until we came across a situation where the user data was not getting updated properly.

Looking through the logs, I found that the user experiencing the bug was entering mixed caps emails, for example, Steph&#x40;endpoint.com. Let's walk through the code in this scenario:

First, a new user is created because there is no user in the system with the exact email Steph&#x40;endpoint.com. However, a user does exist in the system tied to steph&#x40;endpoint.com.

```ruby
user = User.find_or_create_by_email(params[:email]) # with "Steph@endpoint.com" 
```

No problems here:

```ruby
# do some stuff with the user provided parameters
```

Below is where the issue is coming up. Devise, our user authentication gem, automatically downcases (lowercases) all emails when they are stored in the database. There is already a user tied to steph&#x40;endpoint.com, so user.save fails, a 500 error is thrown, but as an end-user, I don't see anything to indicate that my AJAX call failed.

```ruby
if user.save
```

The moral of this story is that it's important to (a) understand how plugins manipulate user data automatically (in this case Devise automatically filters the email) and (b) test a variety of use cases (in this case, we hadn't considered testing mixed caps emails). Our updated code looks something like this, which downcases emails and upon failure, adds more to the logs for additional unexpected user update failures:

```ruby
class SomeController < ApplicationController
  def some_method
    user = User.find_or_create_by_email(params[:email].downcase)
    # do some stuff with the user provided parameters
    if user.save
      render :json => {}
    else
      render :json => {}, :status => 500
      Rails.logger.warn "USER ERROR: #{user.errors.full_messages} #{user.attributes.inspect}"
    end
  end
end
```
