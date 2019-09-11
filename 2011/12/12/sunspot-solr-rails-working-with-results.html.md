---
author: Steph Skardal
gh_issue_number: 523
tags: rails, search, solr, sunspot
title: 'Sunspot, Solr, Rails: Working with Results'
---



Having worked with [Sunspot](http://sunspot.github.io/) and [Solr](https://lucene.apache.org/solr/) in several large Rails projects now, I’ve gained some knowledge about working with result sets optimally. Here’s a brief explanation on working with results or hits from a search object.

### MVC Setup

When working with Sunspot, searchable fields are defined in the model:

```ruby
class Thing < ActiveRecord::Base
  searchable do
    text :field1, :stored => true
    text :field2
    string :field3, :stored => true
    integer :field4, :multiple => true
  end
end
```

The code block above will include field1, field2, field3, and field4 in the search index of **things** . A keyword or text search on things will search field1 and field2 for matches. field3 and field4 may be used for scoping, or limiting the search result set based to specific values of field3 or field4.

In your controller, a new search object is created with the appropriate scoping and keyword values, shown below. Pagination is also added inside the search block.

```ruby
class ThingsController < ApplicationController
  def index
    @search = Sunspot.search(Thing) do
      #fulltext search
      fulltext params[:keyword]

      #scoping
      if params.has_key?(:field3)
        with :field3, params[:field3]
      end 
      if params.has_key?(:field4)
        with :field3, params[:field4]
      end

      paginate :page => params[:page], :per_page => 25
    end
    @search.execute!
  end
end
```

In the view, one can iterate through the result set, where results is an array of Thing instances.

```nohighlight
<% @search.results.each do |result| -%>
<h2><%= result.field3 %></h2>
<%= result.field1 %>
<% end -%>
```

### Working with Hits

The above code works. It works nicely until you display many results on one page where instantiation of things is not expensive. But the above code will call the query below for every search, and subsequently instantiate Ruby objects for each of the things found. This can become sluggish when the result set is large or the items themselves are expensive to instantiate.

```nohighlight
# development.log
Thing Load (0.9ms)  SELECT "things".* FROM "things" WHERE "things"."id" IN (6, 12, 7, 13, 8, ...)
```

An optimized way to work with search results sets is working directly with hits. @search.hits is an array of Sunspot::Search::Hits, which represent the raw information returned by Solr for a single returned item. Hit objects provide access to stored field values, identified by the :stored option in the model’s searchable definition. The model definition looks the same. The controller may now look like this:

```ruby
class ThingsController < ApplicationController
  def index
    search = Sunspot.search(Thing) do
      #fulltext search
      fulltext params[:keyword]

      #scoping
      if params.has_key?(:field3)
        with :field3, params[:field3]
      end 
      if params.has_key?(:field4)
        with :field3, params[:field4]
      end
    end
    search.execute!

    @hits = search.hits.paginate :page => params[:page], :per_page => 25
  end
end
```

And working with the data in the view may look like this:

```nohighlight
<% @hits.each do |result| -%>
<h2><%= hit.stored(:field3) %></h2>
<%= hit.stored(:field1) %>
<% end -%>
```

In some cases, you may want to introduce an additional piece of logic prior pagination, which is the case with the most recent Rails application I’ve been working on:

```ruby
    ...
    search.execute!

    filtered_results = []

    search.hits.each do |hit|
      if hit.stored(:field3) == "some arbitrary value"
        filtered_results << hit
      elsif hit.stored(:field1) == "some other arbitrary value"
        filtered_results << hit
      end
    end
   
    @hits = filtered_results.paginate :page => params[:page], :per_page => 25
```

Sunspot and Solr are rich with functionality and features that can add value to a Rails application, but it’s important to identify areas of the application where database calls can be minimized and lazy loading can be optimized for better performance. The standard log file and database log file are good places to start looking.


