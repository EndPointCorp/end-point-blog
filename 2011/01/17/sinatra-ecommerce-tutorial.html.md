---
author: Steph Skardal
gh_issue_number: 396
tags: ecommerce, ruby, sinatra
title: 'Ecommerce on Sinatra: In a Jiffy'
---



Several of us at End Point have been involved in a non-ecommerce project for one of our clients running on Ruby, Sinatra, Unicorn, using DataMapper, PostgreSQL, PostGIS, with heavy use of JavaScript (specifically YUI). [Sinatra](http://www.sinatrarb.com/) is a lightweight Ruby web framework – it's not in direct competition with Rails but it might be a better "tool" for lightweight applications. It's been a fun project to work with Sinatra, DataMapper, and YUI as I've been working traditionally focused on their respective related technologies (Rails, ActiveRecord, jQuery).

Out of curiosity, I wanted to see what it might take to implement a bare-bones ecommerce store using Sinatra. Here is a mini-tutorial to develop an ecommerce store using Sinatra.

<a href="/blog/2011/01/17/sinatra-ecommerce-tutorial/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5561508822115980674" src="/blog/2011/01/17/sinatra-ecommerce-tutorial/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 232px;"/></a>

A snapshot of our final working app.

### Getting Started

I create a new directory for the project with the following directories:

```nohighlight
sinatrashop/
  db/
    migrate/
  models/
  public/
    images/
     stylesheets/
  views/
```

### Data Model

Now, let's look at the data model. Since this is a bare-bones store, I have one order model which contains all the order information including contact information and addresses. We're not storing the credit card in the database. Also, since this is a bare-bones app, we're going to go with one product with a set price and force the limitation that users only buy one at a time. I've also chosen to use ActiveRecord here since I'm still not sold on DataMapper, but another ORM can be used as well. Here is our model:

```ruby
# sinatrashop/models/order.rb
class Order < ActiveRecord::Base
  validates_presence_of :email
  validates_presence_of :bill_firstname
  validates_presence_of :bill_lastname
  validates_presence_of :bill_address1
  validates_presence_of :bill_city
  validates_presence_of :bill_state
  validates_presence_of :bill_zipcode
  validates_presence_of :ship_firstname
  validates_presence_of :ship_lastname
  validates_presence_of :ship_address1
  validates_presence_of :ship_city
  validates_presence_of :ship_state
  validates_presence_of :ship_zipcode
  validates_presence_of :phone
  validates_format_of :email,
    :with => /\A([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})\Z/i,
    :on => :create
end
```

And here is our migration:

```ruby
# sinatrashop/db/migrate/001_create_orders.rb
class CreateOrders < ActiveRecord::Migration
  def self.up
    create_table :orders do |t|
      t.string   :email, :null => false
      t.string   :bill_firstname, :null => false
      t.string   :bill_lastname, :null => false
      t.string   :bill_address1, :null => false
      t.string   :bill_address2
      t.string   :bill_city, :null => false
      t.integer  :bill_state, :null => false
      t.string   :bill_zipcode, :null => false
      t.string   :ship_firstname, :null => false
      t.string   :ship_lastname, :null => false
      t.string   :ship_address1, :null => false
      t.string   :ship_address2
      t.string   :ship_city, :null => false
      t.integer  :ship_state, :null => false
      t.string   :ship_zipcode, :null => false
      t.string   :phone, :null => false
      t.timestamps
    end
  end

  def self.down
    drop_table :orders
  end
end
```

I did some research here and created the Rakefile shown below to run the migrations. The Rakefile establishes a connection to a sqlite3 database and runs migrations in the db/migrate directory.

```ruby
# sinatrashop/Rakefile
namespace :db do
  task :environment do
    require 'rubygems'
    require 'logger'
    require 'active_record'
    ActiveRecord::Base.establish_connection :adapter => 'sqlite3',
      :database => 'db/development.sqlite3.db'
  end

  desc "Migrate the database"
  task(:migrate => :environment) do
    ActiveRecord::Base.logger = Logger.new(STDOUT)
    ActiveRecord::Migration.verbose = true
    ActiveRecord::Migrator.migrate("db/migrate")
  end
end
```

### Views

Now, let's think about the views we'll present to users. There are many template rendering options in Sinatra, but we'll go with erb and create an index.erb file. By default, Sinatra looks for views in the ROOT/views directory. This will be our only view and layout and below is a breakdown of what it will include:

```nohighlight
# header information
<body>
# product information
# form for submission
# errors or success message
</body>
```

Obviously, there will be a lot more code here, but the view needs to show the basic product information, the form fields to collection information, and errors or a success message to handle the different use cases. See the code [here](https://github.com/stephskardal/sinatrashop/blob/master/views/index.erb) to examine the contents.

### Application Code

Next, let's take a look at the application code. This will be in sinatrashop/store.rb:

```ruby
require 'sinatra'
require 'erb'
require 'active_record'
require 'configuration'
require 'models/order'

get '/' do
  erb :index
end

post '/' do
  erb :index
end
```

The application code handles two requests, a get and post to '/'. The get is a standard home page request. The post to '/' is the order submission. The post '/' action needs to save the order, establish a connection to the payment gateway, and authorize and capture the payment. If any of these actions fail, the order must not be saved to the database and errors must be presented to the user. Consider the following code, which uses ActiveRecord::Base.transaction method and will rollback the saved order if any part of the authorization fails. We also use [ActiveMerchant](http://www.activemerchant.org/) here, which is an extraction from [Shopify](http://www.shopify.com/) for payment gateway integration that can be used as a gem.

```ruby
# sinatrashop/store.rb
post '/' do
  begin
    order = Order.new(params[:order])
    ActiveRecord::Base.transaction do
      if order.save
        params[:credit_card][:first_name] = params[:order][:bill_firstname]
        params[:credit_card][:last_name] = params[:order][:bill_lastname]
        credit_card = ActiveMerchant::Billing::CreditCard.new(params[:credit_card])
        if credit_card.valid?
           gateway = ActiveMerchant::Billing::AuthorizeNetGateway.new(settings.authorize_credentials)

           # Authorize for $10 dollars (1000 cents) 
           response = gateway.authorize(1000, credit_card)
           if response.success?
             order.update_attribute(:status, "complete")
             gateway.capture(1000, response.authorization)
             @success = true
           else
             raise Exception, response.message
           end
         else
           raise Exception, "Your credit card was not valid."
         end
       else
         raise Exception, '<b>Errors:</b> ' + order.errors.full_messages.join(', ')
       end
     end
  rescue Exception => e
    @message = e.message 
  end
end
```

### Configuration

You might notice above that there is a "settings" hash used in the payment gateway connection request. I create a configuration file which sets up some configuration variables in Sinatra's configure do block:

```ruby
# sinatrashop/configuration.rb
require 'active_merchant'

configure do
  set :authorize_credentials => {
    :login => "LOGIN"
    :password => "PASSWORD"
  }
  ActiveRecord::Base.establish_connection(
    :adapter => 'sqlite3',
    :database =>  'db/development.sqlite3.db'
  )
  ActiveMerchant::Billing::Base.mode = :test
end
```

### Testing

I wrote several tests to handle a few use cases. These can be examined [here](https://github.com/stephskardal/sinatrashop/blob/master/test_store.rb). The tests use Rack::Test and can be run with the command ruby -rubygems test_store.rb.

### Infrastructure Concerns

Additional changes are required for running the application on the HTTP server of your choice. Additionally, the entire site should probably run in SSL, which would need configuration. Finally, sqlite may be replaced with a different database here with updates to the configuration.rb and Rakefile files. During development, I ran my app with the command ruby -rubygems store.rb.

### Conclusion

Our bare-bones ecommerce app contains a single simple order model that contains all of our order information. There are only two actions defined our application code. There is one index view. Public assets are served from ROOT/public/. The Rakefile contains functionality for running migrations. There is no admin interface here. A site administrator needs to retrieve orders from the database for sending email notifications and fulfillment. In incremental development, this is the simplest setup to allow someone to collect money, but it requires quite a bit of manual management (emails, fulfillment, etc.). The code can be found [here](https://github.com/stephskardal/sinatrashop). Here are more screenshots of the working application:

<a href="/blog/2011/01/17/sinatra-ecommerce-tutorial/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5561508818277195026" src="/blog/2011/01/17/sinatra-ecommerce-tutorial/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 221px;"/></a>

Order errors!

<a href="/blog/2011/01/17/sinatra-ecommerce-tutorial/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5561508825714293378" src="/blog/2011/01/17/sinatra-ecommerce-tutorial/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 229px;"/></a>

Payment gateway errors.

<a href="/blog/2011/01/17/sinatra-ecommerce-tutorial/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5561508829983726098" src="/blog/2011/01/17/sinatra-ecommerce-tutorial/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 253px;"/></a>

A successful transaction.


