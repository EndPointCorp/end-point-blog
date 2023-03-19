---
author: "Kevin Campusano"
title: "Implementing Basic HTTP Authentication in Rails"
date: 2023-01-26
github_issue_number: 1932
tags:
- ruby
- rails
- authentication
---

![Two deer stand on a steep mountain slope. The mountain is reddened by the sunset, and cuts the image in half diagonally, with the other half being dominated by a pale blue sky. In the bottom, behind the front slope, lies a tall, snow-covered peak.](/blog/2023/01/implementing-basic-http-authentication-in-rails/deer-on-hill.webp)

<!-- Photo by Seth Jensen, 2022 -->

Nowadays it's rather unusual to deploy [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) in a production web application. However, the need came up recently from a client. In a nutshell, due to integration requirements with a third party system, we had to provide a web app which expected credentials supplied via Basic HTTP Auth and validated against an external web service.

Luckily for us, like a great many other things, this is very easy to implement with [Ruby on Rails](https://rubyonrails.org/).

### Setting up a new Rails project

If you want to work along with me, and you like [Docker](https://www.docker.com/) and [VS Code](https://code.visualstudio.com/), take a look at [this blog post](/blog/2023/01/developing-rails-apps-in-a-dev-container-with-vs-code/) to learn about the easiest way to set up an environment for development with Ruby on Rails in a container.

If not, you can follow [the official docs](https://www.ruby-lang.org/en/documentation/installation/) for installing Ruby.

Once you have your environment with Ruby ready, we can go ahead and create a new Rails project to demonstrate how to set up Basic HTTP Auth.

#### Creating the new project

First, install the rails gem:

```sh
$ gem install rails
```

Then, make sure you are located in the directory where you want to create the new project and do:

```sh
$ rails new . --minimal -O
```

> `--minimal` is a new option to `rails new` added in version 6.1 that disables a lot of default features and gems. You can learn more about it [here](https://github.com/rails/rails/pull/39282). `-O` excludes ActiveRecord from the project. We will not be using databases for this quick app so we don't need it.

And finally, run the app:

```sh
$ bin/rails server
```

Open a browser and navigate to [http://127.0.0.1:3000/](http://127.0.0.1:3000/) to see the classic Rails hello world screen:

![Hello Rails. A browser navigated to http://127.0.0.1:3000/, with the webpage displaying the Rails logo, and underneath reading "Rails version: 7.0.4"; "Ruby version: ruby 3.1.3p185 (2022-11-24 revision 1a6b16756e)[x86_64-linux]](/blog/2023/01/implementing-basic-http-authentication-in-rails/hello-rails.png)

### Implementing Basic HTTP Auth

Now that we have a Rails app up and running, let's actually add Basic HTTP auth to it.

First of all we need a page that we will secure:

```sh
$ bin/rails generate controller Pages home --no-helper
```

That'll give us a "Pages" controller with a "home" action and its corresponding view.

Next, we replace the `get 'pages/home'` line in `routes.rb` with `root 'pages#home'`. That will make it so the root URL of our app points to the action created in the previous step.

Going back to the browser at [http://127.0.0.1:3000/](http://127.0.0.1:3000/) you should see this now:

![A browser navigated to http://127.0.0.1:3000/. On the page, a header reads "Pages#home", with a sentence below reading "Find me in app/views/pages/home.html.erb".](/blog/2023/01/implementing-basic-http-authentication-in-rails/homepage.png)

Now we can restrict access to this page with Basic HTTP Auth by adding this code to the "PagesController":

```diff
 class PagesController < ApplicationController
+  before_action :authenticate_http_basic

   def home
   end

+  def authenticate_http_basic
+    return if authenticate_with_http_basic { |un, pw| do_authentication(un, pw) }
+
+    request_http_basic_authentication
+  end

+  def do_authentication(username, password)
+    username == "username" && password == "password"
+  end
 end
```

And that's really all it takes. Try to navigate to [http://127.0.0.1:3000/](http://127.0.0.1:3000/) in the browser and you'll now encounter this:

![A popup is shown above the home page, showing the site which created it (http://127.0.0.1:3000), and reading "This site is asking you to sign in", followed by text inputs for Username and Password. At the bottom of the popup are buttons for Cancel and Sign in.](/blog/2023/01/implementing-basic-http-authentication-in-rails/basic-http-auth-popup.png)

Basic HTTP Auth in action! Hit cancel or input the wrong credentials and a "HTTP Basic: Access denied." message will be shown; type in "username" and "password" and our beautiful homepage shows up.

Let's now discuss the few lines of code that we added to the controller.

First is the `authenticate_http_basic` method which we've registered to the controller's `before_action` callback. That means that before processing any of the controller's actions (`home` being the only one), the method will be invoked and serve as a precondition for its execution.

In the method, the first thing we do is call `authenticate_with_http_basic`, which is how we tell Rails to authenticate the current request using Basic HTTP Auth. The block that we pass to the method is provided the username and password that the user typed in and is where we put any custom logic that we may have for validating the credentials.

`authenticate_with_http_basic` returns whatever the block returns. That's why we have that `return if ...` guard clause as the first line of our `authenticate_http_basic` method. If the block returns truthy, the auth is deemed successful and the user is allowed in the page; if it returns falsy, execution continues and reaches the `request_http_basic_authentication` line; which prompts the authentication popup form that we saw earlier.

In our case, the custom logic that validates the credentials is very simple. It just calls a `do_authentication` method that checks the inputs against hardcoded values. But in the real world, this can be anything. For the client that I discussed at the beginning to this article, the requirement was to invoke an external web service to validate the provided credentials. You could also check the credentials against some database or file, etc.

#### Encapsulating the Basic HTTP Auth logic in a module

I also thought it'd be nice to encapsulate this in a module for easier reuse. That's something that's easy to accomplish thanks to [Rails' Concerns](https://api.rubyonrails.org/v7.0.4/classes/ActiveSupport/Concern.html). For our little demo app, it'd look something like this:

Create a new `app/controllers/concerns/http_basic_auth.rb` file and add the following code:

```ruby
# Provides the `authenticate_http_basic` method which can be used to
# authenticate requests using credentials provided via Basic HTTP Auth.
module HttpBasicAuth
  extend ActiveSupport::Concern

  included do
    def authenticate_http_basic
      return if authenticate_with_http_basic { |un, pw| do_authentication(un, pw) }

      request_http_basic_authentication
    end

    private

    def do_authentication(username, password)
      # TODO: Implement custom credentials validation logic.
      username == "username" && password == "password"
    end
  end
end
```

And in the controller that we want to restrict access to, all we need is this:

```ruby
class PagesController < ApplicationController
  include HttpBasicAuth
  before_action :authenticate_http_basic

  def home
  end
end
```

If the entire app needs Basic HTTP Auth then adding this to the base `ApplicationController` might make more sense. If only some actions need to be behind the authentication, then the [`:only` and `:except` modifiers](https://guides.rubyonrails.org/action_controller_overview.html#filters) can be used for finer grained control.

And that's all for now! It may be surprising to some but sometimes even Basic HTTP Auth is necessary. For those cases, Rails has our backs.
