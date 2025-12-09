---
title: "Using ActiveSupport::ExecutionContext to improve Rails logging"
author: Couragyn Chretien
date: 2025-12-01
description: How to use ActiveSupport::ExecutionContext to improve rails log files. Learn how to automatically share user context across requests, background jobs, and database queries. Help transform your debugging experience from a slog to straightforward troubleshooting.
tags: 
- rails
- ActiveSupport
- ExecutionContext
- logs
---

## Using ActiveSupport::ExecutionContext to improve Rails logging

If you’ve ever tried to debug a complex user workflow in a modern Rails application, you know how difficult it can be. A single web request can spawn multiple background jobs, Turbo Stream updates, and a flurry of database queries. Answering the  question "What was this User doing?" should be simple, but tracing the flow of events through a web of a log file can be difficult and time consuming.

You can add custom log tags but that gets tedious and messy fast. Fortunately, Rails has a powerful, under-documented feature designed specifically for this problem: ActiveSupport::ExecutionContext.

In this post, we'll walk through what ExecutionContext is and how you can use it to add meaningful structure to your logs, making debugging a much more straightforward task.

### The Problem: A Tangled Web of Logs
Imagine a user places an order on your site. The OrdersController#create action fires, which then enqueues a ReceiptJob and a InventoryUpdateJob. The controller also renders a Turbo Stream to update the UI. You have at least four separate units of work: the HTTP request and three background tasks.

Now, if the InventoryUpdateJob fails, your log might show an exception, but it won't immediately tell you which user's order triggered it. You're left grepping for job IDs or tracing timestamps. ExecutionContext solves this by providing a shared context that is automatically shared across these different units of work.

### How ExecutionContext Works
Think of ActiveSupport::ExecutionContext as a container for data that automatically gets passed along. When you store something in it during a web request, that data is bundled up and made available in any background jobs you start from that request without you having to manually send it.

It's important to note that while ActiveSupport::ExecutionContext values are available within the same process (e.g., during the web request), they don't automatically serialize and propagate to background jobs. For the context to be available in jobs, you'll need to explicitly pass relevant values as job arguments. In our example, since we're already passing the order object to both jobs, we can access order.user_id and order.id directly in the job. For contexts without such natural carriers consider extracting the relevant values and passing them explicitly as additional job arguments.

This is the magic that allows you to trace a chain of events.

### A Practical Example: Tracing an Order
Let's implement a solution for the ordering scenario. Our goal is to tag every log line related to this specific order with the user's ID and the order ID.

First, we'll set the context in a `around_action` in our ApplicationController:

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  around_action :set_execution_context

  private

  def set_execution_context
    # We only set the context if a user is logged in.
    if current_user
      ActiveSupport::ExecutionContext[:user_id] = current_user.id
      # We can also trace requests
      ActiveSupport::ExecutionContext[:request_id] = request.request_id
    end

    yield
  ensure
    # Ensure the context is cleared after the request is done.
    ActiveSupport::ExecutionContext.clear
  end
end
```

```ruby
# app/controllers/orders_controller.rb
class OrdersController < ApplicationController
  def create
    @order = current_user.orders.create!(order_params)

    # Update the context with the real order_id
    ActiveSupport::ExecutionContext[:order_id] = @order.id

    ReceiptJob.perform_later(@order)
    InventoryUpdateJob.perform_later(@order)

    respond_to do |format|
      format.turbo_stream
    end
  end
end
```
Because we used `perform_later`, Active Job will automatically serialize our ExecutionContext (containing user_id and order_id) and make it available when the job runs.

Let's look at the InventoryUpdateJob:

```ruby
# app/jobs/inventory_update_job.rb
class InventoryUpdateJob < ApplicationJob
  def perform(order)
    logger.info "Updating inventory for order"

    # ... your business logic ...
  end
end
```

### Making the Context Visible in Logs
Setting the context is only half the battle; we need to see it in our logs. We can do this by customizing Rails' log formatter.

Here’s a simple formatter that appends the execution context to every log line:

```ruby
# config/initializers/log_formatting.rb
class ContextAwareFormatter < Logger::Formatter
  def call(severity, time, progname, msg)
    context = ActiveSupport::ExecutionContext.to_h

    tags = context.map { |key, value| "#{key}=#{value}" }.join(" ")
    tags = "[#{tags}] " unless tags.empty?

    "#{time.utc.iso8601(3)} #{severity} ##{Process.pid} #{tags}#{msg2str(msg)}\n"
  end
end

# Apply it to the Rails logger
Rails.logger.formatter = ContextAwareFormatter.new
```
With this in place, a log line from our InventoryUpdateJob might now look like this:

```text
2025-12-01T15:33:01.123 INFO #123 [user_id=1001 order_id=998842] Updating inventory for order
```
If that job fails, the stack trace will be prefixed with the same `[user_id=1001 order_id=998842]` context. You can instantly see which user and order were affected.

### Going Beyond: Tagging Database Queries
One of the most powerful applications is tagging database queries. This is incredibly useful for identifying expensive queries related to a specific user in a production environment.

You can subscribe to the SQL event and include the context in the log:

```ruby
# config/initializers/log_formatting.rb
ActiveSupport::Notifications.subscribe("sql.active_record") do |event|
  context = ActiveSupport::ExecutionContext.to_h
  next if context.empty?

  payload = event.payload
  sql_with_context = "/* #{context.map { |k, v| "#{k}:#{v}" }.join(', ')} */ #{payload[:sql]}"

  Rails.logger.debug("SQL: #{sql_with_context}")
end
```

Here is what that log line would look like:
```text
DEBUG -- : SQL: /* user_id:1001, order_id:998842 */ SELECT "orders".* FROM "orders" WHERE "orders"."user_id" = $1 LIMIT $2  [["user_id", 1001], ["LIMIT", 1]]
```

The SQL notification subscriber will fire on every database query which in production could introduce noticeable overhead. Consider wrapping this functionality in a `Rails.env.development?` check or using feature flags to control its activation. Be mindful of this trade-off when adding context to high-volume SQL logging.

### A Stitch in Time Saves Nine
ActiveSupport::ExecutionContext is a robust solution to a common problem in modern, event-driven Rails applications. It provides a clean, built-in mechanism for propagating context, which leads to more debuggable and observable systems.

The next time you find yourself lost in a sea of log files, remember this tool. By adding a few lines of code to set the context and customizing your log formatter, you can transform a chaotic log file into a well-organized story of what your application is doing for each and every user.