---
author: Ethan Rowe
title: Cassandra, Thrift, and Fibers in EventMachine
github_issue_number: 300
tags:
- ruby
- scalability
- tips
date: 2010-05-08
---



I’ve been working with Cassandra and EventMachine lately, in an attempt to maximize write throughput for bulk loading situations (and I would prefer to not abandon the pretty Ruby classes I have fronting Cassandra, hence EventMachine rather than hopping over to Java or Scala).

The Thrift client transport for EventMachine requires the use of fibers. The documentation available for how fibers and EventMachine interact is not all that clear just yet, so perhaps documenting my adventures will be of use to somebody else.

### A single fiber is traditionally imperative

EventMachine puts the I/O on background threads, but your use of the I/O interface will interact with it as if it’s a traditional blocking operation.

```ruby
#!/usr/bin/env ruby

require 'eventmachine'
require 'thrift_client'
require 'thrift_client/event_machine'
require 'cassandra'

def get_client 
  Cassandra.new('Keyspace1',
                '127.0.0.1:9160',
                :transport_wrapper => nil,
                :transport         => Thrift::EventMachineTransport)
end

def write(client, key, hash)
  puts "Writing #{key}."
  client.insert('Standard1', key, hash)
  puts "Wrote #{key}."
end

EM.run do
  Fiber.new do
    client = get_client
    write(client, 'foo', {'aard' => 'vark'})
    write(client, 'bar', {'platy' => 'pus'})
    EM.stop
  end.resume
end
```

The Thrift::EventMachine transport performs the actual Thrift network operations (connecting, sending data, receiving data) on a fiber in one of EventMachine’s background threads. But it manages the callbacks and errbacks internally so the client behaves in usual blocking manner and does not expose the asyncronous delights going on behind the scenes.

Therefore, in the code snippet above, the “foo” row will be inserted first, and then the “bar” row. Every time. The output always is:

```nohighlight
Wrote foo.
Wrote bar.
```

The above snippet is contrived, but it makes an import point: given two or more Thrift operations (like Cassandra inserts) that are logically independent of each other such that their order does not matter, you’re not necessarily gaining a lot if those operations happen in the same fiber.

### For concurrency, use multiple fibers

Now let’s replace the above code sample’s EM.run block with this:

```ruby
EM.run do
  @done = 0 
  Fiber.new do
    write(get_client, 'foo', {'aard' => 'vark'})
    @done += 1
  end.resume
  Fiber.new do
    write(get_client, 'bar', {'platy' => 'pus'})
    @done += 1                 
  end.resume                   
  EM.add_periodic_timer(1) { EM.stop if @done == 2 } 
end
```

You don’t know how this is going to play out, but the typical output proves the concurrent operation of the two fibers involved:
```nohighlight
Writing foo.
Writing bar.
Wrote foo.
Wrote bar.
```

If we were writing a larger number of rows out to Cassandra, we could expect to see a greater variety of interleaving between the respective fibers.

Note a critical difference between the two examples. In the single-fiber example, we issue the EM.stop as the final step of the fiber. Because the single fiber proceeds serially, this makes sense. In the multi-fiber example, things run asyncronously, so we have no way of knowing for sure which fiber will complete first. Consequently, it’s necessary have some means of signifying that work is done and the EM can stop; in this lame example, the @done instance variable acts as this flag. In a more rigorous example, you might use a queue and a queue’s size to organize such things.


