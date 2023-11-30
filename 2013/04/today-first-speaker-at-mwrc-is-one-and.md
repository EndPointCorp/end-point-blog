---
author: Mike Farmer
title: MWRC Ruby 2.0 with Matz
github_issue_number: 777
tags:
- conference
- ruby
- rails
date: 2013-04-04
---

Today’s first speaker at [MWRC](https://web.archive.org/web/20130417043214/http://mtnwestrubyconf.org/) is the one and only Yukihiro Matsumoto, better known as Matz. Matz is the founder and chief architect of Ruby. Matz has a wonderfully friendly personality. His talks are always filled with humor.

Probably not unexpectedly Matz is talking about Ruby 2.0. Ruby 2.0 is the happiest ruby release ever. He outlined some of the new features in Ruby 2.0 as follows:

### Features of 2.0

- It’s faster than 1.9

- 100% compatible with 1.9

- Keyword Arguments: Keywork arguments provide support for literals at the end of the arguments: log("hello", level: "DEBUG") You can implement keyword arguments in 1.9, but 2.0 makes it simpler to read and write and implement

- Module#prepend: Module#prepend is kind of like alias_method_chain from Rails but it doesn’t use aliases.

    The prepend method evaluation comes before the existing methods but after the includes so that you can more easily extend existing methods. And you can package changes into a single module.

- Refinements: Currently, monkey patching is a common practice in ruby. But, monkey patching is difficult to scope because it is global. This often leads to name spacing problems and difficult debugging. Refinements offers a kind of scope to your modifications.

    ```ruby
    module R
      refine String do
        def foo
        end
      end
    end

    "".foo => error

    using R do
      "".foo => ok
    end
    ```

    It’s only partially implemented in Ruby 2.0 due to sharp criticism from the developers on the implementation.

- Enumerable#lazy: As the name suggests it allows lazy evaluation of Enumerables such as Array. This is helpful for method chains such as map().select().first(5). Now you can call lazy.map.select.first and every subsequent call will be lazily.

- UTF8 by default.

- Dtrace / TracePoint have been improved to support better debugging.

- Performance Improvements: Improved VM, Improved GC, require(improved invocation time)

### Future of ruby

Matz was clear to state that he doesn’t know what’s coming in the future. He has some ideas, but they are still working on them. It sounded to me like the core group is moving to a more iterative approach. Matz stated that there will be more frequent releases in the future to try to decrease the number of patch levels (1.9.3 has over 300 patch levels).
