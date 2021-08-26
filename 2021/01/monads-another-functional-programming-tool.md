---
author: Kevin Campusano
title: 'Monads: Another tool from the functional programming toolbox'
github_issue_number: 1717
tags:
- functional-programming
- javascript
date: 2021-01-27
---

![banner](/blog/2021/01/monads-another-functional-programming-tool/banner.png)

I was first exposed to the world of [functional programming](https://en.wikipedia.org/wiki/Functional_programming) back in 2007 with the release of [.NET Framework 3.5](https://dotnet.microsoft.com/download/dotnet-framework/net35-sp1) and the introduction of [LINQ](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/) into the C# language. At the time, I was just beginning to learn how to code and LINQ seemed to be little more than an extension of the C# language that allowed programmers to use SQL-like syntax to interact with collections of data. This was mostly useful for interacting with databases, via [LINQ to SQL](https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/sql/linq/). The concept of “functional programming” never even crossed my mind back then.

Once you had created a [LINQ to SQL Object Model](https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/sql/linq/creating-the-object-model) using the tools provided in [Visual Studio](https://visualstudio.microsoft.com/), you could write code like this directly in C#:

```csharp
var customersWithRecentExpensiveOrders =
  // Think of db.Orders as your hypothetical "orders" table.
  from o in db.Orders
  where o.Total >= 100.00 && o.Date == DateTime.Now
  // All orders have a customer
  select o.Customer;
```

Alternatively, you could also use the so-called method syntax:

```csharp
var customersWithRecentExpensiveOrders =
  db.Orders
    .Where(o => o.Total >= 100.00 && o.Date == DateTime.Now)
    .Select(o => o.Customer);
```

LINQ would take that and turn it into native SQL that got executed against your database. Pretty neat.

So I ran with it and little by little I discovered that the set of tools provided by LINQ offered much more than syntactic sugar over database interactions. I discovered the power of LINQ when it came to interacting with lists of objects, database or no. That’s when the breakthrough came. LINQ was indeed a set of tools for working with collections, but more profound than that, it proposed a paradigm shift when it came to reasoning about problems whose solutions involved any sort of iterative logic.

It was weird to write and think about at first, but eventually, I adopted a programming style where I seldom wanted to write “vanilla” `foreach` loops. Looping manually using accumulators, iterators, and other types of temporary values began to feel clunky, inefficient, and verbose. LINQ offered a much more succinct and declarative way of expressing such logic. It was transformative.

So, given a variable called “orders” which contains a collection of all orders in our system, if we wanted all customers who had made orders that were more expensive than $100.00, for example, we could certainly do something like:

```csharp
// a List<Order> orders variable is defined somewhere
var valuableCustomers = new List<Customer>();

foreach (var order in orders) {
  if (order.Total >= 100.00) {
    valuableCustomers.Add(order.Customer);
  }
}

return valuableCustomers;
```

But I would often try to do something like this instead:

```csharp
// a List<Order> orders variable is defined somewhere
return orders
  .Where(o => o.Total >= 100.00)
  .Select(o => o.Customer);
```

Or maybe even:

```csharp
var isExpensive = o => o.Total >= 100.00;
var theCustomer = o => o.Customer;

// a List<Order> orders variable is defined somewhere
return orders.Where(isExpensive).Select(theCustomer);
```

Reads almost like English.

My learning process was such that whenever I had to write some code, I began with a fully imperative approach, since that’s what I was wired up to do. I wrote loops and conditionals manually. Then, I would take a step back and refactor into the more functional and declarative approach unlocked by LINQ, whenever it made sense for readability.

I’m now at the point where the more functional style comes naturally, usually as a first instinct. I feel like I’ve gained proficiency with the tool. I haven’t “rewired” myself, so to speak, to use iteration functions instead of loop primitives all the time, but rather, I’ve added “new wires” that allow me to use and apply the correct tool for the job.

A great advantage is that most of the other languages that I use today (like [JavaScript](https://www.javascript.com/) or [Ruby](https://www.ruby-lang.org/en/)) include similar functional-style APIs for working with collections. Learning and getting used to those tools has proved to be a very good investment.

Now, when it comes to monads, I’ve been hearing about them for a while now and decided to take some time to learn more about them, what sort of problems they can help solve, and whether they would be a worthwhile addition to the tool set that I use on a daily basis when writing code. If they give me the same thing that LINQ gave me all those years ago, then I’d say they are undoubtedly worth the time.

In this article I’m going to share the very first steps in my learning about monads, how to take advantage of the concepts and what sort of problems could benefit from being approached with monads in mind. Bear in mind that I’m no functional programming expert, nor am I proficient when it comes to the formal mathematics behind it.

So this will be an exploration from the perspective of a software engineer mostly experienced in object-oriented analysis and design. I use my limited knowledge of functional programming concepts as tools for expressing lower-level implementation details like algorithms within the context of primarily object-oriented languages with functional capabilities sprinkled in, like JavaScript or C#.

So think OOP for the big chunks and FP for the smaller details, when it fits.

### What is a monad?

This is the first question that I had and, in hindsight, as a total beginner, it is probably not the correct one to ask. Counter-intuitive, I know. A better question to ask would maybe be “what can I do with monads?” and we’ll get there soon. For now, let’s look at a few sentences of what [Wikipedia says about monads](https://en.wikipedia.org/wiki/Monad_(functional_programming)):

> In functional programming, a monad is an abstraction that allows structuring programs generically. Supporting languages may use monads to abstract away boilerplate code needed by the program logic. Monads achieve this by providing their own data type (a particular type for each type of monad), which represents a specific form of computation, along with one procedure to wrap values of any basic type within the monad (yielding a monadic value) and another to compose functions that output monadic values (called monadic functions).

Ok, so right off the bat Wikipedia is telling us about a few key aspects of monads:

- “They can abstract away boilerplate.” What kind of boilerplate are we talking about here?
- “They allow us to structure programs generically.” Sounds good. Generic things are often easy to reuse.
- “They are their own data types.” By data types, do you mean classes? 
- “They represent computations.” Computations, huh? That is a very generic term. Can monads just do whatever you want?
- “They wrap around the values of any basic type.” Wrapping around values like a [decorator design pattern](https://en.wikipedia.org/wiki/Decorator_pattern)?
- “They allow for function composition.” Ok, I like function composition. I do it all the time with LINQ.

That’s quite a bit. My intuition and object oriented bias make me conclude a few things about this. This tells me that monads must be some sort of pattern where you have a class that augments other objects (like a decorator or wrapper). This class can implement some behavior, some computations (which can be considered boilerplate) which wrapped objects can take advantage of.

The encapsulated behavior/​computation/​boilerplate is generic though, so there should be great flexibility as to which types of objects can be wrapped in a monad. They also allow the decorated object to be operated on via method composition, that is, chaining together method calls, where the result of one method is the parameter for the next one. Maybe with a fluent API.

Wikipedia also touches on how they can be useful:

> This allows monads to simplify a wide range of problems, like handling potential undefined values (with the Maybe monad), or keeping values within a flexible, well-formed list (using the List monad). With a monad, a programmer can turn a complicated sequence of functions into a succinct pipeline that abstracts away auxiliary data management, control flow, or side-effects.

This is where the prospect of monads becomes exciting. “Turn a complicated sequence of functions into a succinct pipeline that abstracts away auxiliary data management, control flow, or side-effects,” you say? I’m in.

### How can we use monads?

So now I’m convinced that I need to learn more about these monads. But how to even use these things? What does code that uses monads look like?

Wikipedia does a good job in explaining the concepts in those introductory paragraphs. The code examples however, mostly fly over my head. This is when I looked at [Kyle Simpson](https://twitter.com/getify)’s excellent talk on monads, “[Mo’ Problems, Mo’ Nads](https://www.youtube.com/watch?v=PXwtCYymzjE)” which was great for seeing code examples and a general introductory explanation of the concept. There’s also [Mikhail Shilkov](https://mikhail.io/)’s blog post [Monads explained in C# (again)](https://mikhail.io/2018/07/monads-explained-in-csharp-again/), which was great for me personally given my C# background, but also because of its approach of arriving at the use of monads organically by discovering the need after writing some regular non-monadic code. Mikhail also points out some .NET Base Class Library elements which are actually monads. In my opinion, identifying when new concepts are used out in the wild is always useful when trying to understand them.

Se let’s get into a few examples.

### Handling null checks

This seems to be the quintessential example of code using monads. This example is about how we can use monads to rewrite some typical code that we battle with every day: a series of null reference checks down a reference chain.

Consider this JavaScript code:

```js
// Imagine we have a order object that looks like this and comes from some
// external source like a database or a web API.
const order = {
  orderNumber: '123456',
  total: 100.00,
  customer: {
    id: 10,
    name: 'test_customer_name',
    address: {
      street: '123 main st',
      state: 'New York',
      city: 'New York',
      zip: '10001',
    }
  }
};

function getZipCode() {
  return order.customer.address.zip;
}
```

The `getZipCode` function is very simple, clear, and succinct. Its implementation communicates its intention very well: getting the zip code of where the customer that placed the order is located.

Now, in the real world things are not usually as simple. For example, it’s common for some of the elements in data structures such as this to be missing. In order to prevent null reference exceptions, we usually check for them manually, before accessing fields. To do such checks, our code would have to change. Our `getZipCode` function may end up looking like this:

```js
function getZipCode() {
  if (order !== null) {
    const customer = order.customer;

    if (customer !== null) {
      const address = customer.address;

      if (address !== null) {
        return address.zip;
      }
    }
  }

  return null;
}
```

This works well and we still can understand it just fine. We’re used to writing code like this. However, there’s no denying that we’ve polluted our main algorithm somewhat with tedious validation. The code is not as succinct nor its intent as obvious anymore. It would be great if we could move all that null checking logic elsewhere, and reuse it easily. That would clean up this code. Let’s see how monads can enter the picture and help us out here.

Let’s define a new monad type to help us with this. In modern JavaScript, we can use a class to model our monad:

```js
// Encapsulates logic to conditionally operate on values depending on whether
// they are present or not.
class NullHandlerMonad {
  // Creates a new instance of NullHandlerMonad that wraps around the given
  // value.
  constructor(value) {
    this.value = value;
  }

  // Safely executes the given operation over the value wrapped inside this
  // instance.
  // Returns a new instance of NullHandlerMonad which wraps around the result of
  // the executed operation. Returning an instance of NullHandlerMonad is
  // important so that a method chain can be written in fluent syntax.
  chain(operation) {
    // If the value is not null, execute the operation...
    if (this.value !== null) {
      return new NullHandlerMonad(operation(this.value));
    // ...if it is, then just return null wrapped in the monad
    } else {
      return new NullHandlerMonad(null);
    }
  }

  // Returns the value wrapped inside this instance.
  getValue() {
    return this.value;
  }
}
```

Now what’s happening here? This is a class that defines a monad whose purpose is to abstract away null checks. In terms of good old object-oriented principles, this is just a wrapper. It takes an object and augments it with certain logic. In this case, it allows calling code to use said object in a safe manner with regard to null checks. In other words, the calling code does not need to worry about null checks, it can delegate that into this class. Into the monad.

This new class allows us to rewrite our `getZipCode` function like so:

```js
function getZipCode() {
  return new NullHandlerMonad(order)
    .chain(o => o.customer)
    .chain(c => c.address)
    .chain(a => a.zip)
    .getValue();
}
```

Pretty neat, huh? We’ve managed to get our `getZipCode` function back to a more succinct style while still keeping the safety provided by the null checks on the values that we’re working with: `order`, `customer`, `address` and `zip`. The repeated boilerplate of the conditionals with null checks is gone, abstracted away inside the monad class.

> This repeated null check pattern is so common in fact, that the designers of JavaScript decided to add a solution to this problem at the language level. This solution comes in the form of the [optional chaining operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining). Using it, the implementation of our `getZipCode` function would look like this:
>
> ```js
> function getZipCode() {
>  return order?.customer?.address?.zip;
> }
> ```
>
> It would have the same effect of returning `zip` if it is able to reach it, while short circuiting and returning `null` if any element in the chain is missing.

If we go back to what Wikipedia promised us about monads, we can see the promise fulfilled even in this small, trivial example. Wikipedia said that monads…

- “…can abstract away boilerplate”. Yes, we abstracted away the boilerplate null checks.
- “…allow us to structure programs generically”. Yes, our monad can work with any type of object.
- “…are their own data types”. Yes, we did define a new data type, via a class. 
- “…represent computations”. Yes, our monad represents the computation of “checking for null before working on a value”.
- “…wrap around the values of any basic type”. Yes, our monad is a wrapper. A decorator.
- “…allow for function composition”. Yes, we were able to use a function composition style syntax to get to our solution.

> Note on the generic nature of monads: Claiming that some code is “generic” is easier in JavaScript, due to its dynamic typing and lack of compile-time type checks. This advantage manifests in how our monad class is constructed. The constructor can accept any type: a number, a string, an array, an object. In statically-typed languages like C# or Java, the implementation would be a bit more involved and would require the use of language features like [generics](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/generics/). [Mikhail Shilkov](https://mikhail.io/) explains this perfectly in his blog post about [Monads explained in C# (again)](https://mikhail.io/2018/07/monads-explained-in-csharp-again/). Bottom line is, JavaScript’s dynamic nature does make it easier to write generic code, but it is perfectly possible to do so in statically-typed languages as well.

> By the way, this “NullHandlerMonad” type of monad is so common within functional programming circles that it’s got its own name. It is called the “Maybe” or “Option” monad. Same pattern, different name.

### Handling exceptions

When there’s a series of unsafe operations executed in sequence, exception handling code can also get unwieldy if left unchecked due to nesting and such.

Consider an `order` object that looks like this:

```js
// Imagine we have a order object that looks like this and comes from some
// external source like a database or a web API.
const order = {
  orderNumber: '123456',
  total: 100.00,

  // It has a getCustomer method that fetches customer data from the network.
  // It could throw an exception.
  getCustomer() {
    // throw new Error("could not find customer");

    return {
      id: 10,
      name: 'test_customer_name',

      // It also has a getAddress method that fetches customer data from the
      // network. It could throw an exception.
      getAddress() {
        // throw new Error("could not find address");

        return {
          street: '123 main st',
          state: 'New York',
          city: 'New York',
          getZip() { return '10001'; },
        }
      }
    };
  }
};
```

In order to work with an object like that, we could end up with code like this:

```js
function getZipCode() {
  try {
    customer = order.getCustomer();

    try {
      address = customer.getAddress();

      try {
        return address.getZip();
      } catch (error) {
        console.log(error.message);
      }
    } catch (error) {
      console.log(error.message);
    }
  } catch (error) {
    console.log(error.message);
  }

  return null;
}
```

> In a simple example such as this, we could gain some readability back by collapsing all the try/catch combos into a single catch all at the end. Code like this however can and does get complicated in the real world. The `try` blocks could get more complex and the handling blocks could differ slightly from each other. This is, however, a good example to see monads in action.

Here, we can see that the pattern of boilerplate that repeats itself many times is the try/catch. We could define a new type of monad which would help us rewrite this code in a more succinct manner. We could call it `ExceptionHandlerMonad` and it could look like this:

```js
// Encapsulates logic to handle operations that could throw exceptions.
class ExceptionHandlerMonad {
  // Creates a new instance of ExceptionHandlerMonad that wraps around the given
  // value.
  constructor(value) {
    this.value = value;
  }

  // Safely executes the given operation over the value wrapped inside this
  // instance by using proper exception handling logic.
  //
  // Meant to be used to chain together multiple subsequent such operations.
  // If a previous operation in the chain has thrown an exception, the next
  // operation in the chain is skipped until a catch is called.
  //
  // Returns this instance if the wrapped value is an error, that is, if a
  // previous operation has resulted in an error.
  // Returns a new ExceptionHandlerMonad containing the result of the given
  // operation when run on the wrapped value.
  // Returns a new ExceptionHandlerMonad containing the error if the given
  // operation results in an error when run on the wrapped value.
  chain(operation) {
    if (this.isError()) { return this; }

    try {
      return new ExceptionHandlerMonad(operation(this.value));
    } catch (error) {
      return new ExceptionHandlerMonad(error);
    }
  }

  // Catches any exception that happens before in the chain.
  // Executes the given handler passing it the wrapped error.
  //
  // Returns this instance if the wrapped value is not an error, that is, if
  // there hasn't been an exception previously in the chain.
  // Returns a new empty ExceptionHandlerMonad if the value wrapped is an error,
  // that is, if there has been an exception previously in the chain.
  catch(handler) {
    if (!this.isError()) { return this; }

    handler(this.value);

    return new ExceptionHandlerMonad(null);
  }

  // Returns the value wrapped inside this instance.
  getValue() {
    return this.value;
  }

  // Whether the wrapped value is an error.
  isError() {
    return this.value instanceof Error;
  }
}
```

This class is similar in purpose and structure to `NullHandlerMonad`. It encapsulates exception handling logic. It also adds a new `catch` method to its interface which can be used by client code to specify what to do when exceptions are thrown anywhere in the chain.

This class would allow us to rewrite our `getZipCode` method like this:

```js
function getZipCode() {
  return new ExceptionHandlerMonad(order)
    .chain(o => o.getCustomer())
    .chain(c => c.getAddress())
    .chain(a => a.getZip())
    .catch(e => console.log(e.message))
    .getValue();
}
```

Once again we’ve arrived at code that’s more compact and easier to read. Now, the monad takes care of all the exception handling logic and our `getZipCode` function is only concered with the core algorithm. The core workflow that we need for our solution. Like before, `getZipCode` returns null and logs to console a message if there is any error; if not, then the zip code is returned.

> In functional programming, there’s a common type of monad called “[Either](https://blog.logrocket.com/elegant-error-handling-javascript-either-monad/)” which is generally used for exception handling. “Either” does not have a `catch` method, like `ExceptionHandlerMonad` does. Instead, it uses subtypes called “Right” and “Left” to express whether the result of a given operation has been a success or a failure (i.e. an error/​exception). It then executes code according to that. Here, I’ve defined this `catch` method purely for convenience, sort of collapsing “Right” and “Left” logic into one class. Keep in mind that this approach is rather unorthodox as far as monads go.

At this point we should be familiar with the mechanics of monads and the kinds of things we can do with them. Let’s see another example.

### Handling nested iterations

Another common task is iterating through various levels of nested arrays in order to produce a list of all the innermost elements across multiple parents.

Imagine we run a company that offers vehicle maintenance services to companies with fleets of vehicles. We may have a data structure like the following:

```js
const cities = [
  {
    name: 'Los Angeles',
    locations: [
      {
        name: 'Port of LA',
        vehicles: [
          {
            id: 1,
            licensePlate: '123456',
            wheels: [
              { position: 'Front-Right', dateCode: 2001 },
              { position: 'Front-Left', dateCode: 2001 },
              { position: 'Rear-Right', dateCode: 2002 },
              { position: 'Rear-Left', dateCode: 2002 },
            ]
          },
          // ...more vehicles
        ]
      },
      // ...more locations
    ]
  },
  // ...more cities
];
```

We may want to get a list of all the wheels for all the vehicles that we maintain, maybe to then determine which ones are due for a change. We could write a function like this to obtain that list:

```js
function getWheels() {
  const wheels = [];

  for (const city of cities) {
    for (const location of city.locations) {
      for (const vehicle of location.vehicles) {
        wheels.push(...vehicle.wheels);
      }
    }
  }

  return wheels;
}
```

We know monads now though, so as soon as we see that repeating pattern of nested loops iterating over nested arrays from our original data structure, we can come up with a new type of monad that could help make that code less imperative and easier to write and read. We could write a class like this:

```js
// Encapsulates logic to iterate over arrays inside elements of an outer array
// and return a new array containing the elements of the inner array.
class NestedIteratorMonad {
  // Creates a new instance of NullHandlerMonad that wraps around the given
  // value.
  constructor(values) {
    this.values = values;
  }

  // Returns a new instance of NestedIteratorMonad which wraps around a new
  // array containing the combined elements of the inner arrays specified in
  // selector from each of the elements in the array wrapped inside this
  // instance.
  // 
  // Selector must be a function that receives an element from this.values and
  // returns an array.
  chain(selector) {
    const subValues = [];

    for (const value of this.values) {
      for (const subValue of selector(value)) {
        subValues.push(subValue);
      }
    }

    return new NestedIteratorMonad(subValues);
  }

  // Returns the value wrapped inside this instance.
  getValue() {
    return this.values;
  }
}
```

As you can see, this class implements the nested iteration logic. With it, we can rewrite our `getWheels` function and make it more succinct:

```js
function getWheels() {
  return new NestedIteratorMonad(cities)
    .chain(c => c.locations)
    .chain(l => l.vehicles)
    .chain(v => v.wheels)
    .getValues()
}
```

In fact, modern JavaScript already supports this pattern thanks to the built-in `Array.flatMap` method. It works directly on arrays so, if we were to use it, our function would look like this instead:

```js
function getWheels() {
  return cities
    .flatMap(c => c.locations)
    .flatMap(l => l.vehicles)
    .flatMap(v => v.wheels);
}
```

Pretty nice, right? JavaScript itself already supports some of these monad-related concepts.

### Wrapping up

And that’s it for now! 

Admittedly, these are very simple examples. However, I do believe they serve very well the purpose of getting your feet wet with the concept of monads, what they can do for us, and the mechanics behind them.

While the monads that we discussed here can become useful on their own, they really come to life when we introduce other supporting types and behaviors into the picture. That’s where libraries can become useful. There’s Kyle Simpson’s [Monio](https://github.com/getify/monio), for example. Monio is a JavaScript library that provides a set of monads and other utilities (“monads and friends”, as he calls them) that can help with things like async code, managing side effects, conditional execution, error handling, etc. Some of these are things that we discussed and implemented by hand in this article; with the library, though, we don’t have to implement things by hand. The library, like I said, also includes other utilities that further unlock the power and flexibility of monads, so it’s worth checking out.

I think it’s also useful to be on the lookout for monads in frameworks and libraries that we use everyday. As Mikhail Shilkov pointed out in his blog post, LINQ’s `SelectMany` is pretty much a monad. And we implemented similar functionality in our `NestedIteratorMonad` example. The JavaScript language designers also implemented this same pattern via the `flatMap` method on arrays.

Now, to conclude, I’m still not ready to say that the discovery of monads has caused a breakthrough in my programming style similar to what I had when I fist discovered LINQ in C#. What I can say is that, from now on, much like I did with LINQ, I will try to take a step back after I’m done writing an algorithm, and consider whether using monads would make it more readable. The journey continues; let’s see where it takes us!
