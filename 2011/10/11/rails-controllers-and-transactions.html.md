---
author: Sonny Cook
gh_issue_number: 507
tags: ruby, rails
title: Rails Controllers and Transactions
---



Actions involving single objects in Rails are generally nicely and automatically handled. By handled, what I mean specifically, is that ActiveRecord will encapsulate saving and updating an object in a transaction and you can set up the various callbacks and validations to ensure that the object and its associations meet whatever requirements you have before you allow it to be committed to the database.

You are allowed some degree of latitude to say "Give it a shot, if it doesn't work, then it's no big deal." One of the upsides is that you can throw whatever random nonsense the UI passes you right on through, and, presumably, the model correctness validation code will do double duty as input validation as well.

Which is nice, as far as it goes, but it tends to be localized. Which is to say, that your objects generally only care about validating themselves. Sometimes, it turns out to be necessary to update the state of multiple (possibly unrelated) objects simultaneously and additionally to ensure that if any part of any of these updates fail, you roll the whole thing back.

The application in mind is in a controller, where we are getting input from the browser and we have access to a set of callbacks, but not the atomic-like transactional control we get around save/update actions in a model single.

I suspect the wording of the problem suggests the solution, but let's discuss the hard way to approach it for a bit first. You could enumerate all of the objects that you knew you were going to update, iterate through each of them, determine what state that you were going to attempt to transition them to, determine if that state is valid independently (easier), determine if that state is valid in concert with all of the other attempted transitions (harder), and then, if everything looked cool, make all of the transitions. You might notice that I left out secondary, tertiary, etc. cascading transitions caused by first order transitions that we were inspecting.

That approach starts looking likely to fail in pretty short order, even for small numbers of items. I believe the impetus for this blog post was about 3 items, and a complete lack of ability to track down all of the corner cases generated.

With that, the obvious solution is to wrap the entire operation in a transaction. It turns out the necessary parts have always been there, waiting. Here's one way to use them together.

### Set up your own transactions

First, we need to be able to create our own transaction. We can do so by simply enclosing our code like so:

```ruby
ActiveRecord::Base.transaction do
    ... code ...
end
```

We can use either a class object (as in this example), or an instance object. The documentation for ActiveRecord transactions is 
[here](http://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html). The advantage in this case for using the base class to set up the transaction is that the controller doesn't need to do any semi-mystical nonsense to try to guess the name of the object it might be related to.

### How can we get our action into the middle of that transaction block?

The second part is how to get the transaction wrapped around our controller methods. The obvious in retrospect solution is the [around_filter](http://guides.rubyonrails.org/action_controller_overview.html#after-filters-and-around-filters) provided by ActionController. If you have a controller, then you could implement such a filter like so:

```ruby
 
class MyObjectController < ApplicationController
    around_filter :transactions_filter

    def transactions_filter
        ActiveRecord::Base.transaction do
            yield
        end
    end
    ... the rest of the controller ...
    end
```

It probably only makes sense to add the around_filter to actions which are of the modification type. A definition like this might be more reasonable.

```ruby
    around_filter :transactions_filter, :only => [:create, :update, :destroy]
```

Its also simple enough to add this to your ApplicationController definition if you want to have all of your controller classes inherit this functionality universally.


