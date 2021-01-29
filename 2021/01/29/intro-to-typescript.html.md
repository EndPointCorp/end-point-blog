---
author: "Jeff Laughlin"
title: "An Introduction to TypeScript"
tags: TypeScript, JavaScript, Node, Web
gh_issue_number: 1715
---

# Introduction to Typescript

TypeScript is a programming language defined as a superset of JavaScript.
TypeScript adds static type information to JavaScript code using type
annotations. These annotations permit strong type-checking at compile-time;
kind of like a very strict linter. They are only used for static analysis.
TypeScript is transpiled to JavaScript for execution in the browser or Node
and the type annotations are stripped out. It is still possible to use
standard JavaScript type information at run-time, such as that obtained using
the `typeof` and `instanceof` operators.

Adding type annotations brings many benefits. Most importantly, TypeScript
can tell us when we're doing something dumb that's likely to cause a
type-related bug. But more than that, it powers editors/IDE's context
sensitive tool tips so when you hover or start typing the editor can supply
helpful information so you can get your job done quicker. This is
particularly useful to new developers as it saves them the trouble of reading
all the sources to figure out the variable types from context, especially
when troubleshooting bugs.

JavaScript is a fairly dynamic language but types still exist in JavaScript,
whether we like it or not. Because it's so dynamic it assumes that you the
programmer know the type of every object you are using on every line of code
and will do nothing to help you get it right. The type is specified by the
context. The trouble is that in any non-trivial code base it becomes
impossible to be absolutely 100% certain about the type of some particular
object that's being passed around without reading the context, which if often
a ton of code.

By eagerly annotating our JavaScript code with types we can eliminate entire
classes of bugs from our code base with no additional effort. TypeScript will
never let you play loosey-goosey with integers and strings, for example. If
you want a variable to be able to hold an int or a string you must explicitly
declare it as type "integer or string". 

TypeScript lowers the total-cost-of-ownership of a code base by saving time.
Programmers no longer have to guess or infer types and spend less time
reading documentation and fixing bugs. Because fewer classes of errors are
possible less testing is required. Serious problems never make it to the
customer because developers never commit them to git. New developers on-board
faster and make fewer mistakes. When multiple developers collaborate their
intent WRT types is immediately known to all, including the TS compiler,
without reading any docs.

TypeScript is a proprietary language maintained by Microsoft. However it is
"open" in the sense that it is free to use, the specification is publicly
available, the sources are open, and Microsoft has cultivated a strong
developer community with high levels of engagement.

## Declaring Variables and Functions

```typescript
let someBool: boolean;
```

TypeScript will complain if you try to do this:

```typescript
someBool = "hello world!" // this is a TypeScript error; someBool cannot hold
                          // a string.
```

Another way to declare types is to assign directly to constants:

```typescript
const someBool = true
```

Typescript knows through inference that someBool is of type `boolean` because
it's a const assigned from a boolean type expression. Again TypeScript will
complain if you try to assign a non-boolean typed value to someBool.

## Functions

Function declaration is similar to variable declaration:

```typescript
function someFunc(someBool: boolean): string {
    return "Hello, world!"
}
```

This useless function takes one boolean type argument and returns a string
type value:

```typescript
const someFunc = (someBool: boolean): string => "Hello, world!"
```

TypeScript requires parentheses around annotated lambda arguments. This applies even in
the case of a single argument.

## Assertions

TypeScript supports "type assertions", which is a way of telling the compiler
that you are very certain a particular value is of a particular type and that
it should assume you are right. These are sometimes called "casts" in other
languages.

Generally speaking, type assertions are a red flag. There's usually a better,
more strongly-type way to write the code that avoids their usage. But
sometimes they are convenient, particularly when interfacing with un-typed
JavaScript APIs. Of course it would be better to declare types for those
APIs, but this is beyond the scope of some projects.

Type assertions use the `as` keyword:

```typescript
let someBool: boolean;
someBool as unknown as string = "hello world" // Not an error (but probably a mistake)
```

Because this is case is so egregious, and likely to be a programmer error, TS
forces you to double cast it. A single `as` is usually sufficient.

## Interfaces

Ok, now the real fun begins. So far we've only looked at primitive types like
string and boolean. What about objects, arrays, and all that?

TypeScript "interfaces" allow us to declare the properties and behaviors that
objects should have. There are required properties, optional properties, etc.

Interface declaration looks somewhat like object usage:

```typescript
interface myInterface {
    someBool: boolean;
    someString: string;
}
```

Now when we use it, both someBool and someString are required. Hence, the
following attempt to assign an empty object to a const of type myInterface is
a TypeScript error:

```typescript
const myObj: myInterface = {} // TypeScript error!
```

The object we assign must have both required properties:

```typescript
const myObj: myInterface = {
    someBool: true,
    someString: "Hello"
} // This works.
```

Optional fields are annotated using the ? character:

```typescript
interface myInterface {
    thisIsRequired: boolean;
    thisIsOptional?: string;
}

const myObj: myInterface = {
    thisIsRequired: true
}
```

## Union Types

Sometimes you want to say that "this thing is of this type... OR that type." Enter "union types":

```typescript
type boolOrString = boolean | string;

let myVar: boolOrString;

myVar = true;
myVar = 'hello!'
```

This is 100% valid. myVar can hold either a boolean OR a string value.
However, typescript will force you to disambiguate which type it currently
holds before you can do anything unsafe with it. For example, if we have a
function that takes a union type:

```typescript
function upperBool(arg: boolean | string): string {
    if (typeof arg == 'string') {
        return arg.toUpperCase()
    }
    else if (typeof arg == 'boolean') {
        return arg.toString().toUpperCase()
    }
}
```

It looks like our function could fall through and return undefined, and
theoretically in JavaScript it could, but any such usage would trigger an
error in TypeScript. TypeScript "knows" that we've handled both possible
types of arg and so the if/else definitely does not fall through.

## Intersection Types

An intersection type combines two or more interfaces into a single compound
interface:

```typescript
interface This {
    aProperty: string;
}

interface That {
    bProperty: boolean;
}

type Both = This & That;

const both: Both = {
    aProperty: 'funny',
    bProperty: true
}
```

## Classes

I won't get deep into TS classes, but I want to mention them. TS has classes.
They can transpile to ES6 classes or ES2015 prototypal code. They are very
powerful. They are, however, optional, as classes are still somewhat "new" to
many JS devs.

## Enums

TypeScript supports enum declarations. An enum is a type that can only hold
one of a specific set of possible values.

## Generics

Generics are a mechanism for declaring "complex" types like arrays and
promises. Creating new generics is somewhat advanced, but a basic
understanding is required to use TS effectively.

```typescript
const arrayOfStrings: string[];
const anotherArrayOfStrings: Array<string>;
```

Both of these syntaxes are equivalent. They both declare "an array of strings".

TypeScript includes a significant number of built-in generic types and you
will need them to use the language effectively.

```typescript
let promiseMeAString: Promise<string>
```

This declares a promise that is expected to resolve to a string type value.

## Indexible Types

Indexable types allow the developer to specify the key and value types
expected when using the square-bracket operator to access object or array
properties. This is appropriate when the key set is large or arbitrary and
not known in advance. In this case it's not possible to define each possible
key value.


This interface describes an object that holds a collection of string type
keys with boolean values:

```typescript
interface stringKeysBoolVals {
    [key: string]: boolean
}
```

The syntax is a little funny in that it includes a "placeholder" field, which
I've set to `key`. This field is essentially a comment. TS ignores it. You can
set it to anything that makes sense, e.g. `index`.

This constructs an object acting as a collection of arbitrary key/value
pairs using the interface we just declared:

```typescript
const myCollection: stringKeysBoolVals = {
    "value1": true,
    "value2": false,
    "value3": true
} 
```

This usage is invalid because neither the key type of int nor the value-type
of string is compatible with the declared interface:

```typescript
const invalidCollection: stringKeysBoolVals = {
    0: "foobar"
}
```

## A Note About Tooling

To get the most out of typescript it's critical that your editor integrates
with it and supports real time type checking and error highlighting. Yes, you
can run the TS compiler and check for errors at the command line, but this is
a much slower development process.

Also, most editors will be able to use TypeScript annotations to provide
context-sensitive help and tell you about types and declarations and things
which is really helpful. Modern APIs are too complicated to memorize; don't
try.

## Conclusion

I hope this helps bring to light some of the wonderful features of TypeScript
that help us write more reliable, more maintainable, and more readable code.

The official TypeScript web site is a great place to learn more information
about TypeScript.

https://www.typescriptlang.org/docs
