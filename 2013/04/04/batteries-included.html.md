---
author: Mike Farmer
gh_issue_number: 780
tags: conference, ruby
title: Batteries Included!
---

How many gems does it take to build an app? Many gems duplicate functionality that’s already in ruby core or in the standard library. [Daniel Huckstep](http://verboselogging.com) reviews some goodies that come with ruby that you could probably use to replace some of those gems.

### Basics

- [Set](http://www.ruby-doc.org/stdlib-2.0/libdoc/set/rdoc/Set.html): Like an array but only allows unique values. Set also optimizes for the include? method so if you are calling include? a lot on your arrays and you don’t require duplicates, Set will be a much better option for you.

- [Enumerable](http://ruby-doc.org/core-2.0/Enumerable.html): Gives you map, each_with_index, and all the other goodness that comes with the Enumerable class. All you need to implement is each and you get everything else in Enumerable for free.

- [Enumerator](http://ruby-doc.org/core-2.0/Enumerator.html): Allows you to build your new enomerators on the fly and implement lazy loading.

- [SimpleDelegator](http://www.ruby-doc.org/stdlib-1.9.3/libdoc/delegate/rdoc/SimpleDelegator.html): Inherit from SimpleDelegator and then set self and it will delegate any missing methods to the underlying class.

- [Forwardable](http://www.ruby-doc.org/stdlib-2.0/libdoc/forwardable/rdoc/Forwardable.html): Forward selected methods to another object

### Performance

- [Benchmark](http://www.ruby-doc.org/stdlib-1.9.3/libdoc/benchmark/rdoc/Benchmark.html): Allows you to measure the performance of blocks of code. It also has many different outputs and reporting formats.

- [RubyVM::InstructionSequence](http://ruby-doc.org/core-2.0/RubyVM/InstructionSequence.html): Set compile options to optimize things like tailcall in recursive methods.

- [Fiddle](http://www.ruby-doc.org/stdlib-1.9.3/libdoc/fiddle/rdoc/Fiddle.html): Allows you to call C functions in an external libraries.

- [WeakRef](http://www.ruby-doc.org/stdlib-2.0/libdoc/weakref/rdoc/WeakRef.html): (Ruby >= 2.0) Wrap whatever you pass to it to make it a candidate for garbage collection.

### Beyond

- [SecureRandom](http://www.ruby-doc.org/stdlib-1.9.3/libdoc/securerandom/rdoc/SecureRandom.html): Provides random numbers, uuid, base64, hex, etc.

- [GServer](http://www.ruby-doc.org/stdlib-2.0/libdoc/gserver/rdoc/GServer.html): Gives you a threaded TCP server.

- [Kernel#spawn](http://www.ruby-doc.org/core-2.0/Kernel.html#method-i-spawn): Provides a way to “spawn” an outside process.

- [Shellwords](http://www.ruby-doc.org/stdlib-1.9.3/libdoc/shellwords/rdoc/Shellwords.html): Easy argument parsing for command line.

- [PStore](http://ruby-doc.org/stdlib-1.9.2/libdoc/pstore/rdoc/PStore.html): PStore is a simple data store that uses marshal to store objects to disk. It’s thread safe and supports transactions.

- [MiniTest](http://www.ruby-doc.org/stdlib-1.9.3/libdoc/minitest/unit/rdoc/MiniTest.html): Full blown test framework built into ruby. Supports test unit and rspec like syntaxes and includes ability to mock.

Other nice libraries:
OptionParser, WEBrick, Rss, Drb, Find, Ripper, ThreadsWait, Queue / SizedQuue, MonitorMixin, Net::POP/FTP/HTTP/SMTP.

We have a great ecosystem of gems, but there’s already a lot of what we use gems for already in the Ruby core and standard library.
