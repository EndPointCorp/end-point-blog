---
author: Kamil Ciemniewski
title: Rapid Test-Driven Development in Julia
github_issue_number: 1685
tags:
- julia
- automation
- development
- testing
date: 2020-11-09
---

![Automation](/blog/2020/11/rapid-tdd-in-julia/automation.jpg)

[//]: # ( Kamil wrote: image I've obtained from www.freepik.com where I have a paid account. The license type says: Premium license (Unlimited use without attribution). https://www.freepik.com/free-vector/isometric-automated-production-line-concept-with-industrial-conveyor-belt-robotic-mechanical-arms-isolated_10055534.htm )

The Julia programming language has been rising in the ranks among the science-oriented programming languages lately. It has proven to be revolutionary in many ways. I’ve been watching its development for years now. It’s one of the most innovative of all the modern programming languages.

Julia’s design seems to be driven by two goals: to appeal to the scientific community and to achieve the best performance possible. This is an attempt to solve the “[two languages problem](https://thebottomline.as.ucsb.edu/2018/10/julia-a-solution-to-the-two-language-programming-problem)” where data analysis and model building is performed using a slower interpreted language (like R or Python) while performance-critical parts are written in a faster language like C or C++.

The type-system is what allows Julia to meet its goals. The mix of strong and dynamic typing enables Python-like productivity with C++ or Rust-like performance. Julia is not an interpreted language. It compiles its code to native binary just like C, C++, Go, or Rust. The compilation and execution, though, are what sets it 1000 feet apart from all those other languages.

Here’s a simplified, brief outline of the steps in [Julia’s code execution model](https://docs.julialang.org/en/v1/devdocs/eval/#Julia-Execution):

1. Julia process starts up.
2. Code is parsed.
3. For each code chunk:
    - If it hasn’t yet been compiled, decide whether to interpret or JIT compile it and then execute:
        - If compile then **infer the types** and **use LLVM to produce native code**.
        - Execute the newly-created native code.
    - If it has been compiled, execute it.
4. Repeat until the program ends or the user closes the REPL.

It’s quite apparent that the compilation and type inference happen at a very different time compared to other compiled languages. Using Rust, you compile your code just once. Execution isn’t taxed by consecutive recompilation.

The result is quite a big negative surprise to Julia’s newcomers. Each time you run your app, there’s a significant slowdown before you see anything. It’s called the “time to first plot” issue. This is because, for example, a data scientist may want to generate some plots during her “exploratory data analysis”. Doing it in languages that are slower on paper — like R — makes those plots appear way quicker than in Julia.

### There are more “time to first X” issues in Julia

Julia’s execution model makes more aspects trickier than just seeing the first plot. If you’re a software engineer who’s used to following the [test-driven development](https://en.wikipedia.org/wiki/Test-driven_development) (TDD) approach, you’re in for a big surprise.

In languages like Ruby or Rust, it’s easy to have a tool watch for any file changes and respond by running the project’s testing suite. I often use the [watchexec](https://github.com/watchexec/watchexec) tool which works with virtually any language, interpreter, or compiler. I run `watchexec -cw . "bundle exec rspec --fail-fast"` when working on a Ruby project, or `watchexec -cw . "cargo test"` with Rust.

With Julia this approach is not an option though — the “time to first test” is dramatically long. The wastefulness of continuous re-compilation steals my precious time, making me extremely unproductive.

### Making it work in Julia

The “time to first X” issue is only a problem if we’re closing the session in which our code has already been compiled. If we could move the file-watching and test-running steps all into the same session, the testing suite would run slowly only the first time. Julia’s standard library has built-in file watching functions that we could use to reproduce the `watchexec` in our code:

```plain
julia> using FileWatching

julia> watch_file
watch_file (generic function with 2 methods)

julia> watch_folder
watch_folder (generic function with 4 methods)
```

We can use those to get notified about the changes in our project’s files whenever they happen. Let’s imagine the following simple project’s structure:

```bash
$ tree
.
└── src
    ├── App.jl
    └── nested
        └── Other.jl

2 directories, 2 files
```

How do we watch for file changes in Julia? Let’s start up the REPL and see:

```plain
julia> using FileWatching

help?> watch_file
search: watch_file watch_folder unwatch_folder

  watch_file(path::AbstractString, timeout_s::Real=-1)


  Watch file or directory path for changes until a change occurs or timeout_s seconds have elapsed.

  The returned value is an object with boolean fields changed, renamed, and timedout, giving the result of watching the file.

  This behavior of this function varies slightly across platforms. See https://nodejs.org/api/fs.html#fs_caveats (https://nodejs.org/api/fs.html#fs_caveats) for more detailed information.

julia> watch_file("src")
```

The REPL didn’t return from the `watch_file` function.
We can now change the “src/App.jl” file and see what happens:

```plain
julia> watch_file("src")
FileWatching.FileEvent(true, true, false)

julia>
```

Good! The function returned a `FileEvent` struct. We can ask Julia for its definition:

```plain
help?> FileWatching.FileEvent
  No documentation found.

  Summary
  ≡≡≡≡≡≡≡≡≡

  struct FileWatching.FileEvent <: Any


  Fields
  ≡≡≡≡≡≡≡≡

  renamed  :: Bool
  changed  :: Bool
  timedout :: Bool
```

We can see it tells us whether the file’s been renamed, changed, or if the timeout happened.

So far so good, can we get it to notify us when the nested file changes too?

```plain
julia> watch_file("src")
```

Now changing the “src/nested/Other.jl”:

```plain
julia> watch_file("src")
```

Nothing happened. We’ll need to be specific about the nested directory to make it work:

```plain
julia> watch_file("src/nested")
FileWatching.FileEvent(true, true, false)
```

With those experiments we can now conclude that:

1. We’ll need to watch on all possible nested directories at the same time.
2. Watching blocks the current thread so for each folder to watch we need a separate thread.

We’ll need a list of folders. My first idea was to use the `Glob` package:

```plain
julia> using Glob

julia> glob("**/*")
2-element Array{String,1}:
 "src/App.jl"
 "src/nested"
```

This seems legit but let’s nest another folder. Here’s how the project’s structure would look now:

```bash
$ tree .
.
└── src
    ├── App.jl
    └── nested
        ├── Other.jl
        └── nested2
            └── YetAnother.jl

3 directories, 3 files
```

Trying the `Glob` package again:

```plain
julia> glob("**/*")
2-element Array{String,1}:
 "src/App.jl"
 "src/nested"

julia> glob("**/**/*")
2-element Array{String,1}:
 "src/nested/Other.jl"
 "src/nested/nested2"
```

Turns out that Julia’s `Glob` package doesn’t support extensions that allow “recursive” globbing. We’ll need to roll our own code to return all the possible nested folders:

```plain
julia> function subdirs(base="src")
         ret = [base]

         for (root, dirs, _) in walkdir(base)
           fulldirs = map(d -> joinpath(root, d), dirs)

           ret = vcat(vcat(vcat(map(subdirs, fulldirs)...), fulldirs), ret)
         end

         return ret |> unique
       end
subdirs (generic function with 2 methods)

julia> subdirs("src")
3-element Array{Any,1}:
 "src/nested/nested2"
 "src/nested"
 "src"
```

Being able to list all the nested directories, we can now work on the file-watching function. Here’s the plan of attack:

1. Create a “channel” to receive the file changes from other threads watching each of those directories.
2. Spin up a new thread for working through the stream from the channel specifically.
3. Spin up threads for every nested directory found and watch for changes at the same time.
4. When the file change is detected, queue it into the channel.

```plain
function onchange(f, basedirs=["src"])
  channel = Channel()

  function handle()
    should_continue = true

    for file in channel
      try
        f(file)
      catch err
        should_continue = typeof(err) != InterruptException

        @warn("Error in the hanlder:\n$err")
      end
    end
  end

  function schedule(file)
    put!(channel, file)
  end

  Threads.@spawn handle()

  subs = vcat(map(basedir -> subdirs(basedir), basedirs)...)

  @threads for dir in subs
    should_continue = true

    while true
      (file, event) = watch_folder(dir, 1)

      if event.changed
        try
          schedule(file)
        catch err
          should_continue = typeof(err) != InterruptException

          @warn("Error in the scheduler:\n$err")
        end
      end
    end
  end

  for dir in subs
    unwatch_folder(dir)
  end
end
```

Before we can run this code though, we need to mention one of other of Julia’s quirks. The `@threads` macro is cool and all, but it’s not going to work unless you start Julia with some predefined number of threads first:

```bash
$ JULIA_NUM_THREADS=4 julia
```

Let’s give it a go now:

```plain
julia> onchange(f -> println(f))
```

While the REPL is still “inside” the `onchange` function, let’s change some of those files in the dummy project and see what happens:

```plain
julia> onchange(f -> println(f))
4913
App.jl
App.jl
4913
Other.jl
Other.jl
```

It works! The output is weird but we do get something here. For each file change, we get three messages here. After being puzzled for hours with how Julia implements this file watching I decided to just not mind it and add the throttling to make it work for my testing needs. The idea is that the throttling will only run the suite once per each of those triples.

Fortunately, the `Flux` package comes with the `throttle` function that we can reuse:

```plain
function throttle(f, timeout; leading=true, trailing=false)
  cooldown = true
  later = nothing
  result = nothing

  function throttled(args...; kwargs...)
    yield()

    if cooldown
      if leading
        result = f(args...; kwargs...)
      else
        later = () -> f(args...; kwargs...)
      end

      cooldown = false
      @async try
      while (sleep(timeout); later != nothing)
          later()
          later = nothing
        end
      finally
        cooldown = true
      end
    elseif trailing
      later = () -> (result = f(args...; kwargs...))
    end

    return result
  end
end
```

And the final version of our function:

```plain
function onchange(f, basedirs=["src", "test"], timeout=1)
  channel = Channel()

  function handle()
    should_continue = true

    for file in channel
      try
        f(file)
      catch err
        should_continue = typeof(err) != InterruptException

        @warn("Error in the hanlder:\n$err")
      end
    end
  end

  function schedule(file)
    put!(channel, file)
  end

  throttled_schedule = throttle(schedule, timeout)

  Threads.@spawn handle()

  subs = vcat(map(basedir -> subdirs(basedir), basedirs)...)

  @threads for dir in subs
    should_continue = true

    while true
      (file, event) = watch_folder(dir, 1)

      if event.changed
        try
          throttled_schedule(file)
        catch err
          should_continue = typeof(err) != InterruptException

          @warn("Error in the scheduler:\n$err")
        end
      end
    end
  end

  for dir in subs
    unwatch_folder(dir)
  end
end
```

### Putting it all together

Armed with the helper `onchange` function we can now set up our nice auto-test runner. Let’s add the “test/runtests.jl” file:

```plain
using Test

function runtests()
  @testset "the project" begin
    include("test/test_one.jl")
    include("test/test_two.jl")
  end

  nothing
end

function watchtest()
  onchange(_ -> runtests())
end
```

Now, with the `watchtest` function running the whole testing suite re-runs whenever any of the project’s files changes.

### Final words

I found it easy to have a love-hate relationship with Julia. I have all the respect for its creators. They’re doing an amazing job and are very bold with bringing in innovation. Once the code is compiled, it’s amazingly fast. The language’s ecosystem, along with amazing packages is one of its strongest points.

However, it’s awfully slow when you run your functions for the first time **in the current session**. Also, developers often have to rethink the workflows they’re so used to. This article touches on one of those issues.

The way the file watching is implemented in the standard library leaves a lot of room for improvement. As an example, I’m getting the “renamed” flag instead of “changed” in the `FileWatching.FileEvent` when I’m changing the file. That’s why in code I’m just checking for the absence of the timeout. It feels like a dirty hack but what can you do? The watcher was also not working consistently when the timeout was not given.

The immaturity of the standard library isn’t a show-stopper for many. Julia is developing rapidly and we can expect it to get better and better over time. Other issues will need engineers themselves to rethink their paradigms. I think it’s good though — challenges are what’s making us evolve after all and radical innovation doesn’t happen that often.
