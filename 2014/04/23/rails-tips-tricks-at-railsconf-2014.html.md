---
author: Steph Skardal
gh_issue_number: 970
tags: conference, rails
title: Rails Tips &amp; Tricks at RailsConf 2014
---

<img border="0" src="/blog/2014/04/23/rails-tips-tricks-at-railsconf-2014/image-0.jpeg" style="margin-bottom:2px;" width="820"/>

Rails: They start so young!

One of the talks I attended on Day two of RailsConf 2014 was *Tricks that Rails didn't tell you about* by [Carlos Antonio](https://github.com/carlosantoniodasilva). As the title suggests, Carlos covered a number of Rails items that are either not widely used or not well documented. I've taken the lazy approach and listed out all the topics he covered, but provided documentation or relevent links to all of the tricks in case you'd like to learn more.

### Migrations

- Use [change_column_null](http://api.rubyonrails.org/classes/ActiveRecord/ConnectionAdapters/SchemaStatements.html#method-i-change_column_null) to change a column null, which is reversible in a migration.
- Use [change_column_default](http://api.rubyonrails.org/classes/ActiveRecord/ConnectionAdapters/SchemaStatements.html#method-i-change_column_default) to change a column default, but this doesn't work with change (isn't reversible).

### ActiveRecord

- [Relation.merge](http://apidock.com/rails/ActiveRecord/SpawnMethods/merge), e.g. Product.joins(:reviews).merge(Review.approved), allows you to utilize scope from another model rather than passing in exact SQL conditional, i.e. limiting knowledge of Review to Product.
- Utilize [group counting](http://api.rubyonrails.org/classes/ActiveRecord/Calculations.html#method-i-count) to group results by a column and get the count. This also accepts multiple fields to group.
- [relation.first!](http://api.rubyonrails.org/classes/ActiveRecord/FinderMethods.html#method-i-first-21) and [relation.last!](http://api.rubyonrails.org/classes/ActiveRecord/FinderMethods.html#method-i-last-21) are similar to first &amp; last but raise exception RecordNotFound if there are no records.
- [where.not](http://blog.remarkablelabs.com/2012/12/not-equal-support-for-active-record-queries-rails-4-countdown-to-2013) is a cool finder trick, e.g. scope :some_scope, -> { where.not status: 'draft' }
- You can control eager or lazy loading in Rails via [eager_load](http://blog.plataformatec.com.br/tag/eager-load/) and [preload](http://blog.bigbinary.com/2013/07/01/preload-vs-eager-load-vs-joins-vs-includes.html). These are a little tricky to sum up in a small example, so hopefully those links provide more.
- Instead of passing in SQL in finder methods or scopes, you can call with :desc, e.g. scope :some_scope, -> { order created_at: :desc }
- [pluck](http://apidock.com/rails/ActiveRecord/Calculations/pluck) is a wonderful tool. e.g. Product.pluck(:name), but also Product.pluck(:name, :price) will retrieve product name and pricing information.
- [to_param](http://apidock.com/rails/ActiveRecord/Base/to_param) allows you to override the default of using an object's id to a custom finder key.
- The difference between [exists?](http://apidock.com/rails/ActiveRecord/Base/exists%3F/class)/[any?](http://api.rubyonrails.org/classes/ActiveRecord/Relation.html#method-i-any-3F) and [present?](http://apidock.com/rails/Object/present%3F) is that the former two will first look at the database and then loop through, while the latter will look at the database once and does not require a second look.
- [ActiveRecord's "baked-in" benchmark](http://apidock.com/rails/ActiveRecord/Base/benchmark/class) allows you to benchmark blocks for runtime analysis

### Active Model

- [include ActiveModel::Model](http://api.rubyonrails.org/classes/ActiveModel/Model.html) in a class to allow Rails form helpers to be used on instances of that class, as well as leverage ActiveModel validation methods.

### Action Mailer

- Rails mailers come with some built in mapping between i18n defaults and the mailer language, class, method, value. This is a really hard thing to Google for, so I suggest to [read all the things](http://guides.rubyonrails.org/i18n.html).

### Action View

- [content_tag_for](http://api.rubyonrails.org/classes/ActionView/Helpers/RecordTagHelper.html#method-i-content_tag_for) builds HTML for a loop of objects.
- [render(collection)](http://robots.thoughtbot.com/rendering-collections-in-rails) returns false if a collection is empty, so rather than clouding your view with an if / else block, you can do something like: render(collection) || content_tag(:p, 'No Article Found')
- Learn more about [local_assigns](http://stackoverflow.com/questions/10819189/how-does-local-assigns-work-in-rails). I didn't quite understand this tip in the talk but I found a Stack Overflow qna on the subject.
- [truncate](http://api.rubyonrails.org/classes/ActionView/Helpers/TextHelper.html#method-i-truncate) does what you'd expect, truncate text after a number of characters.
- Rails locales have a *_html method automatically which allows you to pass HTML and does not require you specify raw(that content) when you use the content. See above about reading all the things in i18n.
- [benchmark](http://vesavanska.com/2011/benchmarking-rails-models-and-views/) in AV allows you to benchmark view rendering

### Action Controller

- You can redirect with params, e.g. redirect('/articles/%{id}').
- [config.exceptions_app](http://stackoverflow.com/questions/19103759/rails-4-custom-error-pages-for-404-500-and-where-is-the-default-500-error-mess) allows you to define your own custom routes for application exceptions.

### Console

- In the Rails console, [app](http://stackoverflow.com/questions/151030/how-do-i-call-controller-view-methods-from-the-console-in-rails) is an available variable which can make requests.
- In the Rails console, the [helper](http://stackoverflow.com/questions/151030/how-do-i-call-controller-view-methods-from-the-console-in-rails) variable can be used to access Rails helpers available in your views.
- Running [rails console --sandbox](http://stackoverflow.com/questions/3340680/rails-script-console-vs-script-console-sandbox) will rollback data changes after the console is exited

### Anotations

- [rake notes](http://guides.rubyonrails.org/command_line.html#notes) will list comments marked TODO, FIXME, OPTIMIZE, and has the ability to generate custom annotations

### Updating Rails

- When upgrading Rails, [rake rails:update](https://github.com/rails/rails_upgrade) reports on diffs in all configuration files and helps you work through conflicts
