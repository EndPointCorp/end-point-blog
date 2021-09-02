---
author: Tim Case
title: Developer Specific Configuration in Ruby on Rails
github_issue_number: 907
tags:
- rails
date: 2013-12-27
---

Here’s a quick tip on how to set Rails configurations that you might want for yourself but not for the rest of the team.

I find the default Rails log too noisy when I’m developing because it gives me more information than what I generally need. 90% of the time I only want to see what route is being hit for a request, what controller action responded to the route, and what parameters are being passed to the action. Finding this info with the default Rails log means wading through a jungle of SQL statements, and other things that I’m not interested in. Fortunately, Rails makes it easy to change log levels and the one I prefer is log level “info”.

Setting this up however presents a new problem in that I recognize I’m deviating from what’s conventional in the Rails world and I only want this configuration for myself and not anyone else working on the project. The typical way to change the log level would be to add a line to the environments/development.rb:

```ruby
config.log_level = :info

```

If I do this and then commit the change I’ve now forced my own eccentricities on everyone else. What I could do instead is simply not commit it but then I create noise in my git workflow by having this unstaged change always sitting in my workspace and if I don’t like noisy logs, I don’t like dirty git workspaces even more. The solution I’ve come up with is to create a special directory to hold all my custom configurations and then have git ignore that directory.

1. Create a directory with a specific name and purpose, I use config/initializers/locals.

1. Add an entry to .gitignore:

    ```
    locals/
    ```

1. Add any configurations you want. In my case I created config/initializers/locals/log_level.rb which has the code that will change the log level at start up:

```ruby
Rails.logger.level = LOGGER::INFO
```

As a bonus you can add a “locals” directory anywhere in the application tree where it might be useful, and it will always be ignored. Perhaps you might stick one in app/models/locals where you can add decorators and objects that serve no other purpose than to aid in your local development.


