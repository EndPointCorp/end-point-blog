---
author: Marina Lohova
title: Respecting API Call Limit with Radian6
github_issue_number: 663
tags:
- rails
- social-networks
date: 2012-06-29
---



A common practice in the online API world is to enforce the call limit. Twitter allows 150 API calls per hour. Shopify has 500 API calls per 5 minutes limit. You may learn how to work with Shopify call limit from [this great article](https://web.archive.org/web/20120826132711/http://wiki.shopify.com/Learning_to_Respect_the_API_calls_limit).

One of our projects was built around interaction with [Radian6](http://www.radian6.com/) platform. Radian6 is a new and growing data mining service with the default limit of 100 calls per hour. I will describe our take on the call limit implementation.

### Introducing the call counter

First, we need to know how many calls have been executed in the current hour. Every external call increments the counter field on a special model until the counter reaches the limit. The counter is reset back to zero at the beginning of every hour.

```
script/rails g model RadianCallCount
```

In the migration:

```ruby
class CreateRadianCallCounts < ActiveRecord::Migration
  def change
    create_table :radian_call_counts do |t|
      t.integer :count
      t.timestamps
    end
  end
end
```

In db/seeds.rb file

```ruby
puts "Initializing Radian6 counter"
RadianCallCount.delete_all
RadianCallCount.create(:count => 0)
```

Let’s roll the counter!

```bash
rake db:migrate
rake db:seed
```

### Scheduling the counter reset

It is necessary to reset the counter back to zero in the beginning of each hour otherwise the subsequent calls will not be executed. The excellent ‘whenever’ gem will take care of this.

```bash
gem install whenever
cd your_webapp
wheneverize .
```

In the model:

```ruby
class RadianCallCount < ActiveRecord::Base
  def self.reset
    RadianCallCount.first.update_attribute(:count, 0)
  end
end
```

In config/schedule.rb:

```ruby
every :hour do 
   runner "RadianCallCount.reset"
end
```

### Tracking call count

We will now use the [rcapture](https://rubygems.org/gems/rcapture) gem to intercept a call to external API and increment the counter with it.

```bash
gem install rcapture
```

In the module containing all Radian-specific methods:

```ruby
require 'rcapture'
API_LIMIT = 100
def self.included(base)
  base.extend RCapture::Interceptable
  base.capture_pre :methods => [:authenticate,:tweet_stats] do |cs|
    RadianCallCount.transaction do 
      calls_per_hour = RadianCallCount.first.count 
      allowed = (calls_per_hour < Radian::API_LIMIT)
      cs.predicate = allowed
      cs.return = false 
      RadianCallCount.first.increment!(:count) if allowed
    end
  end
end
```

The code introduces a simple check before ‘authenticate’ and ‘tweets_stats’ methods. If call count exceeds the allowed limit the method is not executed and the method returns **false**. Otherwise, the counter increments after the successful method execution. We wrap the code in transaction because the actual count in the database may increase while we are making the API_LIMIT comparison.

### Making the limit-aware call

Everything is ready to make the non-blocking API call. I scheduled a twitter statistics update to run every 3 hours:

```ruby
every 3.hours do
   runner "Article.tweet_stats"
end
```

The non-blocking calls are suitable for most situations. Sometimes there is a need to just keep trying...

```ruby
def call_with_timeout(&block)
  timeout = 0.minutes 
  results = false 
  while !results do
    results = block.call
    if !results
      break if timeout >= Radian::API_MAX_TIMEOUT
      Rails.logger.info("Sleeping for 5 minutes")
      sleep(Radian::API_CALL_TIMEOUT)
      timeout += Radian::API_CALL_TIMEOUT
    end
  end
  results 
end
...
call_with_timeout { tweet_stats }
```

That is all for today. Thanks for your attention. Hope the post was useful.


