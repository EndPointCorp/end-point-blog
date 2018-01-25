---
author: Patrick Lewis
gh_issue_number: 1277
tags: database, rails
title: 'Seedbank: Structured Seed Files for Rails Projects'
---

Rails [seed files](http://guides.rubyonrails.org/active_record_migrations.html#migrations-and-seed-data) are a useful way of populating a database with the initial data needed for a Rails project. The Rails **db/seeds.rb** file contains plain Ruby code and can be run with the Rails-default **rails db:seed** task. Though convenient, this “one big seed file” approach can quickly become unwieldy once you start pre-populating data for multiple models or needing more advanced mechanisms for retrieving data from a CSV file or other data store.

The [Seedbank](https://github.com/james2m/seedbank) gem aims to solve this scalability problem by providing a drop-in replacement for Rails seed files that allows developers to distribute seed data across multiple files and provides support for environment-specific files.

Organizing seed files in a specific structure within a project’s **db/seeds/** directory enables Seedbank to either run all of the seed files for the current environment using the same **rails db:seed** task as vanilla Rails or to run a specific subset of tasks by specifying a seed file or environment name when running the task. It’s also possible to fall back to the original “single seeds.rb file” approach by running **rails db:seed:original**.

Given a file structure like:

```nohighlight
db/seeds/
  courses.seeds.rb
  development/
    users.seeds.rb
  students.seeds.rb
```

Seedbank will generate tasks including:

```nohighlight
rails db:seed                   # load data from db/seeds.rb, db/seeds/*.seeds.rb, and db/seeds/[ENVIRONMENT]/*.seeds.rb
rails db:seed:courses           # load data from db/seeds/courses.seeds.rb
rails db:seed:common            # load data from db/seeds.rb, db/seeds/*.seeds.rb
rails db:seed:development       # load data from db/seeds.rb, db/seeds/*.seeds.rb, and db/seeds/development/*.seeds.rb
rails db:seed:development:users # load data from db/seeds/development/users.seeds.rb
rails db:seed:original          # load data from db/seeds.rb
```

I’ve found the ability to define development-specific seed files helpful in recent projects for populating “test user” accounts for sites running in development mode. We’ve been able to maintain a consistent set of test user accounts across multiple development sites without having to worry about accidentally creating those same test accounts once the site is running in a publicly accessible production environment.

Splitting seed data from one file into multiple files does introduce a potential issue when the data created in one seed file is dependent on data from a different seed file. Seedbank addresses this problem by allowing for dependencies to be defined within the seed files, enabling the developer to control the order in which the seed files will be run.

Seedbank runs seed files in alphabetical order by default but simply wrapping the code in a block allows the developer to manually enforce the order in which tasks should be run. Given a case where Students are dependent on Course records having already been created, the file can be set up like this:

```ruby
# db/seeds/students.seeds.rb
after :courses do
  course = Course.find_by_name('Calculus')
  course.students.create(first_name: 'Patrick', last_name: 'Lewis')
end
```

The added dependency block will ensure that the **db/seeds/courses.seeds.rb** file is executed before the **db/seeds/students.seeds.rb** file, even when the students file is run via a specific **rails db:seed:students** task.

Seedbank provides additional support for adding shared methods that can be reused within multiple seed files and I encourage anyone interested in the gem to check out the [Seedbank README](https://github.com/james2m/seedbank) for more details. Though the current 0.4 version of Seedbank doesn’t officially have support for Rails 5, I’ve been using it without issue on Rails 5 projects for over six months now and consider it a great addition to any Rails project that needs to pre-populate a database with a non-trivial amount of data.


