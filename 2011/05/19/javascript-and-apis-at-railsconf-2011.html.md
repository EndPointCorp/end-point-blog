---
author: Steph Skardal
gh_issue_number: 454
tags: conference, javascript, rails
title: JavaScript and APIs at RailsConf 2011
---



A big trend of RailsConf 2011 has been the presence of JavaScript, whether it be talk of [CoffeeScript](http://coffeescript.org/), [node.js](http://nodejs.org/), [Sproutcore](http://www.sproutcore.com/), [backbone.js](http://backbonejs.org/), etc. I attended [Yehuda Katz's](http://yehudakatz.com/) talk on [Building Rails Apps for the Rich Client](http://en.oreilly.com/rails2011/public/schedule/detail/18047) on Day 4 of the conference.

### Part 1: Rails versus Sinatra Smackdown

Yehuda gave a two part talk about developing API-heavy applications. The first bit addressed why to develop in Rails rather than Sinatra if your application is API-heavy and doesn't appear to be utilizing valuable parts of Rails? This is fairly applicable to a couple of Sinatra projects that I've done at End Point — I like Sinatra a lot, but at some point you begin to replicate parts of Rails. Yehuda explained that because it's easy to develop web applications efficiently using Rails conventions, developers can become forgetful/ignorant of the underlying functionality of Rails that doesn't ship with something like Sinatra, much like how working with an ORM can breed developers who aren't familiar with the underlying database interactions. The checklist for things that Rails manages we might forget about includes:

- [ActionDispatch](http://rubyonrails.org/screencasts/rails3/getting-started-action-dispatch) internals
- Session deserialization
- Browser standards mode
- Cookie abstraction and management
- Deserialization of content types like JSON, XML
- Reloading (by comparison Sinatra doesn't reload automagically unless you use a tool like [shotgun](http://rtomayko.github.com/shotgun/))
- Handling IP Spoofing
- Routing / Complex Routing
- Browser Caching (ETags, Last-Modified)
- Content negotiation to automatically support different MIMEs
- ActionMailer

This list is is a nice checklist of items you might review when you are considering building in Sinatra to be reminded of things that won't necessarily be trivial to implement.

### Part 2: Consistent APIs

The second part of Yehuda's talk covered his experience with building client rich applications with APIs. His general observation is that while Rails follows universal conventions like the ActiveRecord convention that requires foreign keys to be named {table_name}_id, there isn't a convention for APIs. While there has been decent support for building APIs in Rails since 2006, there's been missing documentation on what to generate which has produced APIs with limited consistency. He gave the following **pro tips** for developing an API:

- Return a JSON object with one or more keys, that is iterable. Rather than returning
```javascript
{ product_title: "Some Awesome Product." }
```

return something that has one or more keys that is iterable, such as:
```javascript
{
    "products": [
        {
            id: 1,
            title: "Some Awesome Product."
        }
    ]
}
```

- Avoid nested resources like /users/1/orders. Instead, always make the request do a GET on /orders or a
PUT on /orders/1. This will help maintain consistency (and maintainability) with a simple asset requests.
- In general, create a convention and follow conventions. Essentially, apply the principles of Rails here to produce maintainable and consistent code.

Finally, Yehuda presented the [bulk_api gem](http://rubygems.org/gems/bulk_api) to address the use case where you need to get a set of items, but want to avoid making single requests for multiple items and avoid getting all items and parse through them on the client side. An ecommerce example of this might be applicable in inventory management: Let's say you have ~30 unrelated listed inventory units that need to be updated to an on_hand state. From the admin screen, you may click on checkboxes next to those 30 items and then "Update". Rather than sending a single request to update each item, the bulk_api gem will make a single request to update the inventory unit status for all of the objects. Similarly, you can make a GET request to the bulk api to retrieve a set of objects, such as looking at a set of products on page 2 of a product listing. Yehuda went into more details on authentication and authorization with this gem, so I'd recommend reading the documentation [here](http://rubydoc.info/gems/bulk_api/0.0.7/frames).

### Conclusion

Yehuda concludes that Rails is great for JSON APIs and that we should continue to be building abstractions similar to ActiveRecord abstractions that follow conventions in a sensible way. Hooray for convention over configuration.


