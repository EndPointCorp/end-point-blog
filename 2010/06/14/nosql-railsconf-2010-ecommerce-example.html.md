---
author: Steph Skardal
gh_issue_number: 319
tags: database, ecommerce, nosql, ruby, rails, spree, mongodb
title: 'NoSQL at RailsConf 2010: An Ecommerce Example'
---

Even more so than Rails 3, [NoSQL](https://en.wikipedia.org/wiki/NoSQL) was a popular technical topic at RailsConf this year. I haven’t had much exposure to NoSQL except for reading a few articles written by Ethan ([Quick Thoughts on NoSQL Live Boston Conference](/blog/2010/03/11/quick-thoughts-on-nosql-live-boston), [NoSQL Live: The Dynamo Derivatives (Cassandra, Voldemort, Riak)](/blog/2010/03/12/nosql-live-dynamo-derivatives-cassandra), and [Cassandra, Thrift, and Fibers in EventMachine](/blog/2010/05/08/cassandra-thrift-and-fibers-in)), so I attended a few sessions to learn more.

First, it was reinforced several times that if you can read JSON, you should have no problem comprehending NoSQL. So, it shouldn’t be too hard to jump into code examples! Next, I found it helpful when one of the speakers presented high-level categorization of NoSQL, whether or not the categories meant much to me at the time:

- **Key-Value Stores:** Advantages include that this is the simplest possible data model. Disadvantages include that range queries are not straightforward and modeling can get complicated. Examples include Redis, Riak, Voldemort, Tokyo Cabinet, MemcacheDB.
- **Document stores:** Advantages include that the value associated with a key is a document that exposes a structure that allows some database operations to be performed on it. Examples include CouchDB, MongoDB, Riak, FleetDB.
- **Column-based stores:** Examples include Cassandra, HBase.
- **Graph stores:** Advantages include that this allows for deep relationships. Examples include Neo4j, HypergraphDB, InfoGrid.

In one NoSQL talk, [Flip Sasser](https://web.archive.org/web/20100610062845/http://x451.com/) presented an example to demonstrate how an ecommerce application might be migrated to use NoSQL, which was the most efficient (and very familiar) way for me to gain an understanding of NoSQL use in a Rails application. Flip introduced the models and relationships shown here:

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5482744501534322754" src="/blog/2010/06/14/nosql-railsconf-2010-ecommerce-example/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 600px;"/>

In the transition to NoSQL, the transaction model stays as is. As a purchase is created, the Notification.create method is called.

```ruby
class Purchase < ActiveRecord::Base
  after_create :create_notification

  # model relationships
  # model validations

  def total
    quantity * product.price
  end

  protected
  def create_notification
    notifications.create({
      :action => "purchased #{quantity == 1 ? 'a' : quantity} #{quantity == 1 ? product.name : product.name.pluralize}",
      :description => "Spent a total of #{total}",
      :item => self,
      :user => user
    }
    )
  end
end
```

Flip moves the product class to Document store because it needs a lot of flexibility to handle the diverse product metadata. The structure of the product class is defined in the product class and nowhere else.

**Before**

```ruby
class Product < ActiveRecord::Base
  serialize :info, Hash
end
```

**After**

```ruby
class Product
  include MongoMapper::Document

  key :name, String
  key :image_path, String

  key :info, Hash

  timestamps!
end
```

The Notification class is moved to a Key-Value store. After a user completes a purchase, the create method is called to store a notification against the user that is to receive the notification.

**Before**

```ruby
class Notification < ActiveRecord::Base
  # model relationships
  # model validations
end
```

**After**

```ruby
require 'ostruct'

class Notification < OpenStruct
  class << self
    def create(attributes)
      message = "#{attributes[:user].name} #{attributes[:action]}"
      attributes[:user].follower_ids.each do |follower_id|
        Red.lpush("user:#{follower_id}:notifications", {:message => message, :description => attributes[:description], :timestamp => Time.now}.to_json)
      end
    end
  end
end
```

The user model remains an ActiveRecord model and uses the devise gem for user authentication, but is modified to retrieve the notifications, now an OpenStruct. The result is that whenever a user’s friend makes a purchase, the user is notified of the purchase. In this simple example, a purchase contains one product only.

**Before**

```ruby
class User < ActiveRecord::Base
  # user authentication here
  # model relationships

  def notifications
    Notification.where("friend_relationships.friend_id = notifications.user_id OR notifications.user_id = #{id}").
      joins("LEFT JOIN friend_relationships ON friend_relationships.user_id = #{id}")
  end
end
```

**After**

```ruby
class User < ActiveRecord::Base
  # user authentication here
  # model relationships

  def followers
    User.where('users.id IN (friend_relationships.user_id)').
      joins("JOIN friend_relationships ON friend_relationships.friend_id = #{id}")
  end

  def follower_ids
    followers.map(&:id)
  end

  def notifications
    (Red.lrange("user:#{id}:notifications", 0, -1) || []).map{|notification| Notification.new(ActiveSupport::JSON.decode(notification))}
  end
end
```

The disadvantages to the NoSQL and RDBMS hybrid is that data portability is limited and ActiveRecord plugins can no longer be used. But the general idea is that performance justifies the move to NoSQL for some data. In several sessions I attended, the speakers reiterated that you will likely never be in a situation where you’ll only use NoSQL, but that it’s another tool available to suit performance-related business needs. I later spoke with a few [Spree](https://spreecommerce.org/) developers and we concluded that the NoSQL approach may work well in **some** applications for product and variant data for improved performance with flexibility, but we didn’t come to an agreement on where else this approach may be applied.
