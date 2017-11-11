---
author: Steph Skardal
gh_issue_number: 1005
tags: performance, ruby, rails
title: Rails Performance with Skylight
---



Back at [RailsConf](http://railsconf.com/), I met a couple of the creators of [Skylight.io](https://www.skylight.io/), a recently launched Ruby on Rails profiler. I was anxious to try it out after having unconvincing experiences with New Relic, but first I had to get through a pretty big upgrade of Rails 2.3 to 4.1 on [H2O](http://cyber.law.harvard.edu/research/h2o). I survived the upgrade and moved on to profiling.

Installation of Skylight.io was super simple and the installation screen provided real-time feedback during gem installation and configuration. The web-app had data to share within a minute or so. At the moment, Skylight offers a free month trial to get started, and paid plans after that month. Skylight reports metrics requests (referenced by controller#action) per minute and time per request and allows you to sort results by those metrics combined (Response time x Requests Per Minute = Agony), individually or alphabetically. The Agony-sorted option highlights methods that are candidates for the most impactful changes. One interesting note here is because our application uses full page caching, the requests recorded by Skylight do not include those static cached requests, so the Skylight data is a representation of the work the Rails application is doing to generate non-cached content and apply various writes.

<img border="0" src="/blog/2014/06/26/rails-performance-with-skylight/image-0.png" style="margin-bottom:5px;" width="820"/>

Skylight app screenshot offering various ways to sort requests. Controller names blurred out.

Once you drill down to a specific controller#action method, Skylight provides a waterfall of the various processes, including view rendering and database hits. It highlights potential problem areas where the same query executes repeatedly in one request (n+1). There's a lot of data and interactivity available in the waterfall view.

<img border="0" src="/blog/2014/06/26/rails-performance-with-skylight/image-1.png" style="margin-bottom:5px;" width="820"/>

Skylight request waterfall screenshot. Table names blurred out

With my recent upgrade from Rails 2.3 to Rails 4.1, I initially chose the simple, happy, and wise path of minimal refactoring, which did not take advantage of improved cache management in Rails 4 or eager loading strategies. Armed with Skylight metrics, I was able to apply a number of changes to improve performance, described below.

### Data Model Challenges

Before I go into the performance details, I want to describe the inherent challenge associated with the application's data model, which combines nesting of listed items and polymorphism. In the diagram below, ItemA, ItemB, ItemC, and ItemD are all Rails models. A model of type ItemA has a list of items (of class ListItem). Each of those list items points to another item via a polymorphic relationship (of class ItemA, ItemB, ItemC, ItemD). The nested referenced item can include further nesting. Nesting is allowed at up to 4 levels and infinite nested loops are not allowed. When the top-level ItemA loads, there are some metrics pulled from the aggregate of all of its nested list items, which requires all nested items to be loaded from the database. Because of this nested data model, one must pay special attention to eager loading in Rails (via the includes() method, or default scope). In some cases, eager loading of all nested items is necessary and in other cases it only becomes a performance burden if the data is not needed. This nested polymorphic data model has created some challenges in terms of performance and cache invalidation.

```nohighlight
ItemA
  ListItem =&gt; ItemA
    ListItem =&gt; ItemA
      ListItem =&gt; ItemB
    ListItem =&gt; ItemA
      ListItem =&gt; ItemB
    ListItem =&gt; ItemB
  ListItem =&gt; ItemB
  ListItem =&gt; ItemC
  ListItem =&gt; ItemD
```

### Repeating Queries

Skylight reported a number of (n+1) scenarios. This was a relatively simple improvement with a couple of changes:

- updating the default_scope of various models to include associations often included
- updating specific queries to use the includes(:some_association) method to eagerly load these associations.

I also found an opportunity via [Sunspot](http://sunspot.github.io/), a Solr-based Rails search gem, for eager-loading associations on associations to search results objects. Here are some code examples:

```ruby
default_scope { includes(:some_association) } # example default scope in model
SomeModel.includes(:some_association).limit(5) # example eager loading associations on query
SomeModel.search(:include =&gt; :user) # example Sunspot search with eager loading
```

These updates proved extremely valuable in terms of minimizing database hits by reducing repeated queries.

### Cache Management

One of the problem areas that Skylight highlighted was that many of our writes were taking quite a while. In the Rails 2.3 app, [Rails Sweepers](http://apidock.com/rails/ActionController/Caching/Sweeping) were used extensively to perform manual cache expiration after specific actions (e.g. create or update). With the update to Rails 4.1, the code can take advantage of better Rails cache key management as well as [Russian Doll caching](http://blog.remarkablelabs.com/2012/12/russian-doll-caching-cache-digests-rails-4-countdown-to-2013), eliminating the need for manual cache management. The application still uses full page caching in some instances, so some cache management is required to clear the fully cached pages, but the fragment cache management has improved dramatically.

```ruby
# Example of cache key based on item only
&lt;% cache(item) do -%&gt;
# Stuff here
&lt;% end -%&gt;

# Example of cache key based on item and item.user
# Fragment cache will expire when item.user or item is updated
&lt;% cache([item.user, "listed-item", item]) do -%&gt;
# Stuff here
&lt;% end -%&gt;
```

### Remove unnecessary AJAX Requests

Although this wasn't a specific issue highlighted by Skylight, I did take the opportunity to investigate where AJAX requests could be reduced. In one case, this meant moving from an eager loading strategy via AJAX to a lazy loading strategy. In another scenario, it meant utilizing Rails [render_to_string](http://apidock.com/rails/ActionController/Base/render_to_string) method which allowed me to return both view content and object data from a JSON post, instead of making two requests that return different data types (JSON followed by HTML).

```ruby
# Example of render_to_string to return HTML and JSON data from single AJAX request
content = render_to_string("path/to/view.html.erb", :locals =&gt; { :item =&gt; item })
render :json =&gt; { :some_key =&gt; item,
                  :content =&gt; content,
                  :other_data =&gt; some_other_data
                }
```

### Database Management

Because Skylight highlighted a few areas where writes were taking excessively long, I revisited options for more efficient interaction with the database. This included updates such as using [update_column](http://apidock.com/rails/ActiveRecord/Persistence/update_column) instead of [update_attribute](http://apidock.com/rails/ActiveRecord/Base/update_attribute), which eliminated redundant cache expiration logic. This also included minor updates to minimize the number of updates applied to the database where applicable. Those are both ***duh!*** updates to a seasoned Rails developer, but having a profiler point out the most agonizing requests (including updates) forced me to dig in deep on specific actions.

### Conclusion

My experience with [Skylight](https://www.skylight.io/) has been positive. Skylight is opinionated about what data it provides but what it does present is actionable, compared to other profilers which may present a large and overwhelming amount of information and metrics. Because I've provided feedback on Skylight, I know they are continuously making updates and improvements in hopes of improving the service. I definitely suggest trying Skylight out to profile your application.


