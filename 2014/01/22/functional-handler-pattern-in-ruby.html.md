---
author: Mike Farmer
gh_issue_number: 916
tags: functional-programming, ruby, rails
title: Functional Handler —​ A Pattern in Ruby
---



First, a disclaimer. Naming things in the world of programming is always a challenge. Naming this blog post was also difficult. There are all sorts of implications that come up when you claim something is “functional” or that something is a “pattern”. I don’t claim to be an expert on either of these topics, but what I want to describe is a pattern that I’ve seen develop in my code lately and it involves functions, or anonymous functions to be more precise. So please forgive me if I don’t hold to all the constraints of both of these loaded terms.

### A pattern

The pattern that I’ve seen lately is that I need to accomplish of myriad of steps, all in sequence, and I need to only proceed to the next step if my current step succeeds. This is common in the world of Rails controllers. For example:

```ruby
def update
  @order = Order.find params[:id]

  if @order.update_attributes(params[:order])
    @order.calculate_tax!
    @order.calculate_shipping!
    @order.send_invoice!  if @order.complete?
    flash[:notice] = "Order saved"
    redirect_to :index
  else
    render :edit
  end

end
```

What I’m really trying to accomplish here is that I want to perform the following steps:

- Find my order
- Update the attributes of my order
- Calculate the tax
- Calculate the shipping
- Send the invoice, but only if the order is complete
- Redirect back to the index page.

There are a number of ways to accomplish this set of steps. There’s the option above but now my controller is doing way more than it should and testing this is going to get ugly. In the past, I may have created a callback in my order model. Something like after_save :calculate_tax_and_shipping and after_save :send_invoice if: :complete?. The trouble with this approach is that now *anytime* my order is updated these steps also occur. There may be many instances where I want to update my order and what I’m updating has nothing to do with calculating totals. This is particularly problematic when these calculations take a lot of processing and have a lot of dependencies on other models.

Another approach may be to move some of my steps into the controller before and after filters (now before_action and after_action in Rails 4). This approach is even worse because I’ve spread my order specific steps to a layer of my application that should only be responsible for routing user interaction to the business logic of my application. This makes maintaining this application more difficult and debugging a nightmare.

The approach I prefer is to hand off the processing of the order to a class that has the responsibility of processing the user’s interaction with the model, in this case, the order. Let’s take a look at how my controller action may look with this approach.

```ruby
def update
  handler = OrderControllerHandler.new(params)
  handler.execute!

  if hander.order_saved?
    redirect_to :index
  else
    @order = handler.order
    render :edit
  end
end
```

OK, now that I have my controller setup so that it’s only handling routing, as it should, how do I implement this OrderControllerHandler class? Let’s walk through this:

```ruby
class OrderControllerHandler

  attr_reader :order

  def initialize(params)
    @params = params
    @order = nil # a null object would be better!
    @order_saved = false
  end

  def execute!
  end

  def order_saved?
    @order_saved
  end

end
```

We now have the skeleton of our class setup and all we need to do is proceed with the implementation. Here’s where we can bust out our TDD chops and get to work. In the interest of brevity, I’ll leave out the tests, but I want to make the point that this approach makes testing so much easier. We now have a specific object to test without messing with all the intricacies of the controller. We can test the controller to route correctly on the order_saved? condition which can be safely mocked. We can also test the processing of our order in a more safe and isolated context. Ok, enough about testing, let’s proceed with the implementation. First, the execute method:

```ruby
def execute!
  lookup_order
  update_order
  calculate_tax
  calculate_shipping
  send_invoice
end
```

Looks good right? Now we just need to create a method for each of these statements. Note, I’m not adding responsibility to my handler. For example, I’m not actually calculating the tax here. I’m just going to tell the order to calculate the tax, or even better, tell a TaxCalculator to calculate the tax for my order. The purpose of the handler class is to orchestrate the running of these different steps, not to actually perform the work. So, in the private section of my class, I may have some methods that look like this:

```ruby
private
def lookup_order
  @order = Order.find(@params[:id])
end

def update_order
  @saved_order = @order.update_attributes(@params[:order])
end

def calculate_tax
  TaxCalculator.calculate(@order)
end

... etc, you get the idea
```

### Getting function(al)

So far, so good. But we have a problem here. What do we do if the lookup up of the order fails? I wouldn’t want to proceed to update the order in that case. Here’s where a little bit of functional programming can help us out (previous disclaimers apply). Let’s take another shot at our execute! method again and this time, we’ll wrap each step in an anonymous function aka, stabby lambda:

```ruby
def execute!
  steps = [
    ->{ lookup_order },
    ->{ update_order },
    ->{ calculate_tax },
    ->{ calculate_shipping },
    ->{ send_invoice! },
  ]

  steps.each { |step| break unless step.call }
end
```

What does this little refactor do for us? Well, it makes each step conditional on the return status of the previous step. Now we will only proceed through the steps when they complete successfully. But now each of our steps needs to return either true or false. To pretty this up and add some more meaning, we can do something like this:

```ruby
private
def stop; false; end
def proceed; true; end

def lookup_order
  @order = Order.find(@params[:id])
  @order ? proceed : stop
end
```

Now each of my step methods has a nice clean way to show that I should either proceed or stop execution that reads well and is clear on its intent.

We can continue to improve this by catching some errors along the way so that we can report back what went wrong if there was a problem.

```ruby
attr_reader :order, :errors

def initialize(params)
  @params = params
  @order = nil # a null object would be better!
  @order_saved = false
  @errors = []
end

...

private

def proceed; true; end
def stop(message="")
  @errors << message if message.present?
  false
end

def invalid(message)
  @errors << message
  proceed
end

def lookup_order
  @order = Order.find(@params[:id])
  @order ? proceed : stop("Order could not be found.")
end

...
```

I’ve added these helpers to provide us with three different options for capturing errors and controlling the flow of our steps. We use the proceed method to just continue processing, invalid to record an error but continue processing anyway, and stop to optionally take a message and halt the processing of our step.

In summary, we’ve taken a controller with a lot of mixed responsibilities and conditional statements that determine the flow of the application and implemented a functional handler. This handler orchestrates the running of several steps and provides a way to control how those steps are run and even captures some error output if need be. This results in much cleaner code that is more testable and maintainable over time.

### Homework Assignment

- How could this pattern be pulled out into a module that could be easily included every time I wanted to use it?
- How could I decouple the OrderControllerHandler class from the controller and make it a more general class that can be easily reused throughout my application anytime I needed to perform this set of steps?
- How could this pattern be implemented as a functional pipeline that acts on a payload? How is this similar to Rack middleware?

Hint: 

```ruby
def steps
  [
    ->(payload){ step1(payload) },
    ->(payload){ step2(payload) },
    ->(payload){ step3(payload) },
  ]
end

def execute_pipeline!(payload)
  last_result = payload
  steps.each do |step|
    last_result = step.call(last_result)
  end

end
```


