---
author: Kamil Ciemniewski
title: Strict typing fun example — Free Monads in Haskell
github_issue_number: 1210
tags:
- functional-programming
- haskell
- programming
date: 2016-03-11
---

From time to time I’ve got a chance to discuss different programming paradigms with colleagues. Very often I like steering the discussion into the programming languages realm as it’s something that interests me a lot.

Looking at the most popular languages list on GitHub, published last August, we can see that in the most popular five, we only have one that is “statically typed”. [https://github.com/blog/2047-language-trends-on-github](https://github.com/blog/2047-language-trends-on-github)

The most popular languages on GitHub as of August 2015:

- JavaScript
- Java
- Ruby
- PHP
- Python

The dynamic typing approach gives great flexibility. It very often empowers teams to be more productive. There are use cases for static type systems I feel that many people are not aware of though.
I view this post as an experiment. I’d like to present you with a pattern that’s being used in Haskell and Scala worlds (among others). The pattern is especially helpful in these contexts as both Haskell and Scala have extremely advanced type systems (comparing to e. g. Java or C++ and not to mention Ruby or Python).

My goal is not to explain in detail all the subtleties of the code I’m going to present. The learning curve for both languages can be pretty dramatic. The goal is to make you a bit curious about alternative development styles and how they could be very powerful.

### Short intro to the idea behind the pattern

The pattern I’m going to present is called the “Free Monad + Interpreter”. The idea behind it is that we can build [DSLs](https://en.wikipedia.org/wiki/Domain-specific_language) (domain specific languages) by making our functions not execute the code immediately, but to build the [AST](https://en.wikipedia.org/wiki/Abstract_syntax_tree) (abstract syntax tree) out of it and interpret it in different ways depending on the context.

A fun example I came up with is a DSL for system [provisioning](https://en.wikipedia.org/wiki/Provisioning#Server_provisioning) scripts that—​among many use cases one could come up with—​allows to:

- present the AST in bash or zsh code or whatever other language like Python, Ruby or Perl
- present the AST as a graph to visualize the execution
- execute it directly, natively in Haskell
- have an easy-to-comprehend set of provisioning instructions while lower level aspects like file handles etc.—​being handled in common Haskell code used for the execution of ASTs

There are potentially many more use cases but I just wanted to show you a couple—​enough to hopefully make you a bit curious. In this post we’ll focus on interpreting the AST as a bash script.

### The coding part

The first step is to define the set of instructions our interpreted Domain Specific Language will support:

```haskell
data Provision next =
  Begin next |
  Install String next |
  IfNotExists String (Free Provision ()) next |
  Touch String next |
  Cd String next |
  MkDir String Bool next |
  Echo String next |
  Continue |
  Done
  deriving(Functor)
```

This odd looking definition is what’s called an [Algebraic Data Type](https://en.wikipedia.org/wiki/Algebraic_data_type). For now it should suffice that the commands can take arguments of different types and almost all of them take a continuation command as the last parameter.

The continuation parameter is meant to store the next “provisioning command” so that we would have e.g:

```haskell
Begin (Install "postgresql-server" (Echo "installed!" (Done)))
```

Out of these blocks, our ASTs will be created. We need some way of composing these blocks into AST trees. I’m not going to explain here why the following code works—​it’s just a teaser post. Let’s just say that the following functions allow us to just build the tree instead of calling any system-affecting code. In other words, it allows these calls to look as if they’re doing something when in fact they are just constructing the data structure in memory:

```haskell
begin = liftF $ Begin id

install what = liftF $ Install what id

ifNotExists path what = liftF $ IfNotExists path what id

touch path = liftF $ Touch path id

cd path = liftF $ Cd path id

mkDir path wholeTree = liftF $ MkDir path wholeTree id

echo message = liftF $ Echo message id

continue = liftF $ Continue

done = liftF Done
```

Now that we have these building functions defined, we can create a function that uses them to construct a useful AST:

```haskell
app :: Free Provision a
app = do
  begin
  install "postgresql-server"
  mkDir "/var/run/the-app" True
  cd "/var/run/the-app"
  ifNotExists "the-app.log" $ touch "the-app.log" >> continue
  done
```

Running this function does nothing except for returning AST wrapped inside the “free monad”—​which you can think of as a special, useful kind of container. The above function looks like any other Haskell function. It’s also “type safe”—​which weeds out one class of errors that we’re only able to notice **after** we ran the code—​in languages like JavaScript or Python.

Later on we’ll see that to get different results out of the “provisioning workflow” we defined above, no change in this function will be needed.

Now, having an AST tree wrapped around some “useful” container almost screams for some kind of an interpreter for this to be useful too. That’s in fact part of the description of the pattern I gave you in the beginning of this post.

Let’s define a set of data types linked with the function that we’ll use as an interpreter:

```haskell
class InterpretingContext a where
  run :: Free Provision () -> a
```

The above just says that if we want to use the function **run** to turn the AST wrapped in a monad to some concrete value (by executing it)—​we need to implement this function for the type of the concrete value we’d like to get out of it.

For example, let’s say that for the portability sakes we want to turn the AST into the bash script. The natural (though naive) way to do this would be to implement this “class” along with its **run** function for the type of **String**:

```haskell
instance InterpretingContext String where
  run (Free (Begin next)) =
    "#!/usr/bin/env bash\n\n" ++ (run next)

  run (Free (Install what next)) =
    "apt-get install " ++ what ++ "\n" ++ nextStr
    where
      nextStr = run next

  run (Free (IfNotExists path what next)) =
    "if [ ! -f " ++ path ++ " ]; then\n\t" ++ whatStr
      ++ "\nfi\n" ++ nextStr
    where
      whatStr = run what
      nextStr = run next

  run (Free (Touch path next)) =
    "touch " ++ path ++ "\n" ++ (run next)

  run (Free (Cd path next)) =
    "cd " ++ path ++ "\n" ++ (run next)

  run (Free (MkDir path tree next)) =
    "mkdir " ++ treeOption ++ " " ++ path ++ "\n" ++ (run next)
    where
      treeOption =
        if tree then "-p" else ""

  run (Free (Echo message next)) =
    "echo " ++ message ++ "\n" ++ (run next)

  run (Free Continue) = ""

  run (Free Done) = "exit 0"
```

Each node kind is being **interpreted** as a data type we chose to be one of the **instances of this class**—​in our example a **String**.

What this allows us to do, is to use the **run** function, specifying that we want a **String** as a return value and automatically the instance we’ve just created will be used:

```haskell
run app :: String
```

This will return:

```haskell
"#!/usr/bin/env bash\n\napt-get install postgresql-server\nmkdir -p /var/run/the-app\ncd /var/run/the-app\nif [ ! -f the-app.log ]; then\n\ttouch the-app.log\n\nfi\nexit 0"
```

Pretty printed:

```bash
#!/usr/bin/env bash

apt-get install postgresql-server
mkdir -p /var/run/the-app
cd /var/run/the-app
if [ ! -f the-app.log ]; then
    touch the-app.log
fi
exit 0
```

If now we’d like to execute the AST in the context of an action that prints the script to stdout we could do so like this:

```haskell
instance InterpretingContext (IO ()) where
  run = print . run
```

From now on it would be perfectly valid to run the function with AST in both contexts:

```haskell
run app :: String
run app :: IO ()
```

We could add a context returning an ExitStatus by running the code against the system very easily too:

```haskell
data ExitStatus = ExitSuccess | ExitFailure Int

instance InterpretingContext (IO ExitStatus) where
  run = (…)
```

What this gives us is the ability to have the provisioning code that could be run in production while having a different interpreter in the testing suite to be able to ensure the structure of execution without inflicting any changes to the system itself.

If you’d like to play with the code yourself, you’ll need a couple of more lines for this to work:

```haskell
{-# LANGUAGE DeriveFunctor #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE TypeSynonymInstances #-}
{-# LANGUAGE OverloadedStrings #-}
```

And also:

```haskell
import Control.Monad.Free
```

Bear in mind though that the code I presented here is by no means optimal—​especially memory wise. I chose to present it this way for the clarity of what the code is doing for those of you not familiar with the language.

### What are other use cases for this pattern?

The pattern presented here has a huge number of uses. It could be used for providing a DSL for building SVG combined with an interpreter that could draw it visually for the ease of work. It could also be used for defining RPC data types describing structures and interpreting them differently based on the underlying [RPC](https://en.wikipedia.org/wiki/Remote_procedure_call) (remote procedure call) mechanics (Thrift, SOAP etc).

I doubt that the ability this gives thanks to the **very helpful** Haskell type system could be reproduced in languages like Ruby or Python easily. It is possible of course, but the amount of boilerplate code and complexity would require lots of testing code too. Here on the other hand the code holds many guarantees just because we’re coding in a language with an advanced strict type system.

Also, the similarity to the [Interpreter Pattern](https://en.wikipedia.org/wiki/Interpreter_pattern) known from the object oriented languages is only superficial. In that case there’s no way to use regular normal functions (or methods) to build AST—​as if it was a regular imperative code. It’s always about some weird mangling of data structures by hand.

### Curious?

If I managed to make you a bit curious about the aspects I presented here, here are some of the resources you might want to take a look at:

- [Learn You a Haskell — online book](http://learnyouahaskell.com/chapters)
- [Real World Haskell — online book](http://book.realworldhaskell.org/read/)
- [A pleasant visual tutorial about functors and monads](http://adit.io/posts/2013-04-17-functors,_applicatives,_and_monads_in_pictures.html)
- [Haskell Wiki article on monads](https://wiki.haskell.org/Monad)
- [A fantastic intro to the Free Monad pattern](http://programmers.stackexchange.com/questions/242795/what-is-the-free-monad-interpreter-pattern)
