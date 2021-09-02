---
author: Steph Skardal
title: Memcache Full HTML in Ruby on Rails with Nginx
github_issue_number: 1157
tags:
- performance
- rails
date: 2015-09-04
---



*Hi! Steph here, former long-time End Point employee now blogging from afar as a software developer for [Pinhole Press](https://pinholepress.com/). While I’m no longer an employee of End Point, I’m happy to blog and share here.*

I recently went down the rabbit hole of figuring out how to cache full HTML pages in [memcached](http://memcached.org/) and serve those pages via [nginx](http://nginx.org/) in a Ruby on Rails application, skipping Rails entirely. While troubleshooting this, I could not find much on Google or StackOverflow, except related articles for applying this technique in WordPress.

Here are the steps I went through to get this working:

### Replace Page Caching

First, I cloned the [page caching gem repository](https://github.com/rails/actionpack-page_caching) that was taken out of the Rails core on the move from Rails 3 to 4. It writes fully cached pages out to the file system. It can easily be added as a gem to any project, but the decision was made to remove it from the core.

Because of the complexities in cache invalidation across file systems on multiple instances (with load balancing), and the desire to skip a shared/mounted file server, and because the Rails application relies on memcached for standard Rails fragment and view caching throughout the site, the approach was to use memcached for these full HTML pages as well. A small portion of the page (my account and cart info) is modified via JavaScript with information it retrieves from another server.

The following [simplified] changes were made to the actionpack-page_caching gem, to modify where the full page content was stored:

```ruby
# Cache clearing update:
+ Rails.cache.delete(path)
- File.delete(path) if File.exist?(path)
- File.delete(path + '.gz') if File.exist?(path + '.gz')
```
```ruby
# Cache write update:
+ Rails.cache.write(path, content, raw: true)
- FileUtils.makedirs(File.dirname(path))
- File.open(path, 'wb+') { |f| f.write(content) }
- if gzip
-   Zlib::GzipWriter.open(path + '.gz', gzip) { |f| f.write(content) }
- end
```
```ruby
# Cache path change:
def page_cache_path(path, extension = nil)
+ path
- page_cache_directory.to_s + page_cache_file(path, extension)
end
```

See, it’s not that much! The rest of the gem was not modified much, and the interaction from the Rails app to this gem was maintained (via a controller class method :caches_page). The one thing to note above is the raw option passed in the call to write the cache, which forces the content to be served as a raw string.

### Step 2: Set up nginx to look for memcached files

Next, I had to set up nginx to serve the HTML from memcached. This was the tricky part (for me). After much experimentation and logging, I finally settled on the following simplified config:

```nohighlight
location / {
    set $memcached_key $uri;
    set $memcached_request 1;
    default_type "text/html";

    if $uri ~ "admin") {
      set $memcached_request 0;
    }

    if ($uri ~ "nocache") {
      set $memcached_request 0;
    }

    if ($memcached_request = 1) {
      memcached_pass localhost:11211;
      error_page 404 = /nocache/$uri;
    }
  }
```

The desired logic here is to look up the memcached pages for all requests. If there is no memcached page, nginx should fallback to serving the standard Rails page with a modified URL (“/nocache/” prepended). Without this URL modification, nginx would get stuck in an infinite loop of looking up all URLs in memcache repeatedly.

### Step 3: Setup a Rack::Rewrite rule to lookup /nocache/ pages.

Due to the infinite loop problem, Rails was receiving all requests with /nocache/ prepended to it. A simple solution to handle this was to add a Rack::Rewrite rule to internally rewrite the URL to ignore the /nocache/ fragment, shown below. The nice thing about this change is that if caching is disabled (e.g. on the development server), this rewrite rule won’t affect any requests.

```nohighlight
config.middleware.insert_before(Rack::Runtime, Rack::Rewrite) do
  rewrite %r{/nocache/(.*)}, '/$1'
end
```

### Step 4: Cache invalidation: the really hard part, right?

Finally, I had to add cache invalidation throughout the application where the memcache pages needed to expire. There are a few options for this, for example:

- Inside a Rails controller after a successful update/commit.
- Inside a Rails model, via ActiveRecord callbacks.
- Inside a module that decorates an ActiveRecord model via callbacks.

Choose your poison wisely here. A controller makes sense, but in the case where [RailsAdmin](https://github.com/sferik/rails_admin) is utilized for all admin CRUD methods, it’s not much different (IMHO) to extend the controllers as it is to extend the models. I’m a fan of ActiveRecord callbacks, so I went with option 2.

### Final Thoughts

Logs were invaluable here. Most importantly, the memcached log was invaluable here to confirm the infinite loop bug. Also, the Rails dev log was naturally helpful once I solved the nginx issue to handle the Rack::Rewrite rule.

One important note here is that this type of caching does not take advantage of [expiration via model timestamp cache keys](https://signalvnoise.com/posts/3113-how-key-based-cache-expiration-works) introduced in Rails 4. But, it wouldn’t be able to, because nginx needs a quick lookup on the URL in memcache to serve the file, and we ideally don’t want to hit the database to try to figure out what that key should be.


