---
author: Steph Skardal
gh_issue_number: 492
tags: performance, ruby, rails
title: Ruby on Rails Performance Overview
---



Over the last few months, I've been involved in a Ruby on Rails (version 2.3) project that had a strong need to implement performance improvements using various methods. Here, I'll summarize some the methods and tools used for performance optimization on this application.

### Fragment Caching

Before I started on the project, there was already a significant amount of [fragment caching](http://guides.rubyonrails.org/caching_with_rails.html#fragment-caching) in use throughout the site. In it's most basic form, fragment caching wraps a cache method around existing view code:

```nohighlight
<%= cache "product-meta-#{product.id}" %>
#insert view code
<% end %>
```

And [Rails Sweepers](http://guides.rubyonrails.org/caching_with_rails.html#sweepers) are used to clear the cached fragments, which looks something like the code shown below. In our application, the Sweeper attaches cache clearing methods to object callbacks, such as after_save, after_create, before_update.

```ruby
class ProductSweeper < ActionController::Caching::Sweeper
  observe Product

  def after_save(record)
    expire_fragment "product-meta-#{product.id}"
  end
end
```

Fragment caching is a good way to reuse small modular view components throughout the site. In this application, fragment caches tended to contain object meta data that was shown on various index list pages and single item show pages.

### Page Caching

I did not initially add page caching to the application because the system has complex role management where users can have edit access at an object, class, or super level. However, later I investigated  advanced techniques to leverage full page caching, described in depth [here](http://blog.endpoint.com/2011/08/rails-optimization-digging-deeper.html). The benefit gained here was that the application server was not hit during full page requests, and a quick AJAX request was made after the page loaded to determine user access level.

### Raw SQL methods

Another performance technique I employed on this application was using raw SQL rather than use standard ActiveRecord methods to lookup association data. The application uses [ActsAsTaggable](http://rubyforge.org/projects/taggable/), a gem that enables you to tag objects. The simplified data model looks like this, which includes a polymorphic relationship in the taggings table to the items tagged (products, categories):

<a href="/blog/2011/09/06/ruby-on-rails-performance-overview/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5649308360992095682" src="/blog/2011/09/06/ruby-on-rails-performance-overview/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 219px;"/></a>

In the application, the front-end required that we pull the most popular 25 tags for a specific class. Working with the objects and their associations, one might use the following code:

```ruby
def self.tag_list
  b = Product.all.collect { |p| p.tag_list }.flatten
  c = b.inject({}) { |h, a| h[a] ||= 0; h[a]+=1; h } 
  c.sort_by { |k, v| v }.reverse[0..25]
end
```

However, this request is quite sluggish because it has to iterate through each object and it's tags. I wrote raw SQL to generate the Tag objects, which runs at least 10 times faster than using standard ActiveRecord association lookup:

```ruby
def self.tag_list
  Tag.find_by_sql("SELECT ts.tag_id AS id, t.name FROM taggings ts
    JOIN tags t ON ts.tag_id = t.id
    WHERE taggable_type = 'Product'
    GROUP BY ts.tag_id, t.name
    ORDER BY COUNT(*) DESC LIMIT 25")
end
```

Typically, using ActiveRecord find methods and the item associations may yield more readable code and require minimal knowledge of the underlying database structure. But in this example, having an understanding of the database model and how to work with it gave a significant performance bump. This technique was also combined with fragment caching.

 

### Rails Low Level Caching

Next up, there were several opportunities through the site to use Rails low level caching. Here's one example of a simple use of Rails low level caching, which pulls a list of products that the user has owner or creator rights to:

```ruby
class User < ActiveRecord::Base 
  def products
    Rails.cache.fetch("user-products-#{self.id}") do
      self.roles
        .find(:all, :conditions => {:authorizable_type => 'Product', :name => ['owner','creator']})
        .collect(&:authorizable)
        .uniq
        .compact
        .sort_by{|a| a.updated_at}
    end
  end
end

```

Rails low level caching makes sense for data that's pulled throughout various actions but additional computations are applied to this data. We are unable to cache this at the page request or action level, but we can cache the data retrieved with low level caching. I also used Rails low level caching on the search index pages, which is described more in depth [here](http://blog.endpoint.com/2011/07/rails-optimization-advanced-techniques.html).

### HTML Asset related Performance

In addition to server-side optimization, I investigated several avenues of HTML asset related performance optimization:

- Extensive use of CSS Sprites
- Consolidation and minification of JS, CSS. Note that Rails 3.1 introduces new functionality to improve the process of serving minified and consolidated JS and CSS.
- HTML caching, gzipping, and Expires headers

### Tools Used

Throughout performance tweaking, I used the following tools:

- Rails' [standard logger](http://guides.rubyonrails.org/debugging_rails_applications.html#the-logger)
- PostgreSQL's [ANALYZE](http://www.postgresql.org/docs/8.1/static/sql-analyze.html)
- Ruby's [Benchmark Module](http://ruby-doc.org/stdlib/libdoc/benchmark/rdoc/index.html)
- [WebPageTest.org](http://www.webpagetest.org/)

### Conclusion

There are a few Rails caching techniques that I did not use in the application, such as [action caching](http://guides.rubyonrails.org/caching_with_rails.html#action-caching) and [SQL Caching](http://guides.rubyonrails.org/caching_with_rails.html#sql-caching). The [Rails caching overview](http://guides.rubyonrails.org/caching_with_rails.html) provides a great summary of caching techniques, but does not cover Rails low level caching. Another great resources for performance optimization is [Yahoo's Best Practices for Speeding Up Your Web Site](http://developer.yahoo.com/performance/rules.html), but it focuses on asset related optimization opportunities. I typically recommend pursuing optimization on both the server-side and asset related fronts.


