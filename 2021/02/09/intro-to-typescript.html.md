---
author: "Jeff Laughlin"
title: "An Introduction to TypeScript"
tags: typescript, javascript, nodejs
gh_issue_number: 1715
---

![TypeScript logo](/blog/2021/02/09/intro-to-typescript/ts-lettermark-white.svg)

TypeScript is a programming language defined as a superset of JavaScript. It adds static type information to JavaScript code using type annotations. These annotations permit strong type-checking at compile-time, kind of like a very strict linter. They are only used for static analysis. TypeScript is transpiled to JavaScript for execution in the browser or Node.js and the type annotations are stripped out. It is still possible to use standard JavaScript type information at run-time, such as that obtained using the `typeof` and `instanceof` operators.

Adding type annotations brings many benefits. Most importantly, TypeScript can tell us when we’re doing something dumb that’s likely to cause a type-related bug. But more than that, it powers editors’/​IDEs’ context sensitive tool tips so when you hover or start typing the editor can supply helpful information so you can get your job done quicker. This is particularly useful to new developers as it saves them the trouble of reading all the sources to figure out the variable types from context, especially when debugging.

JavaScript is a fairly dynamic language but types still exist in JavaScript, whether we like it or not. Because it’s so dynamic it assumes that you the programmer know the type of every object you are using on every line of code and will do nothing to help you get it right. The type is specified by the context. The trouble is that in any non-trivial codebase it becomes impossible to be absolutely 100% certain about the type of some particular object that’s being passed around without reading the context, which is often a ton of code.

By eagerly annotating our JavaScript code with types we can eliminate entire classes of bugs from our codebase. TypeScript will never let you play loosey-goosey with integers and strings, for example. If you want a variable to be able to hold an int or a string you must explicitly declare it as type “integer” or “string”.

TypeScript lowers the total cost of ownership of a codebase by saving time. Programmers no longer have to guess or infer types and spend less time reading documentation and fixing bugs. Because fewer classes of errors are possible, less testing is required. Entire classes of serious problems never make it to the users because developers never commit them to the codebase. New developers on-board faster and make fewer mistakes. When multiple developers collaborate, their intentions with respect to types are immediately known to all, including the TS compiler, without reading any docs.

TypeScript is open source software maintained by Microsoft: It is free to use, and the specification and tools are provided under the Apache open source license. Microsoft has cultivated a strong developer community with high levels of engagement.

### Strictness

Note that TypeScript has several settings for controlling the strictness of its type checking. To obtain maximum benefit we recommend using the `--strict` option which turns on all strict-checking options. This blog post assumes that strict mode is enabled. For more information see the [TypeScript Compiler Options](https://www.typescriptlang.org/docs/handbook/compiler-options.html).

### Declaring Variables and Functions

```javascript
let someBool: boolean;
```

TypeScript will complain if you try to do this:

```javascript
someBool = "hello world!";  // this is a TypeScript error; someBool
                            // cannot hold a string.
```

Another way to declare types is to assign directly to constants:

```javascript
const someBool = true;
```

TypeScript knows through inference that someBool is of type `boolean` because it’s a const assigned from a boolean type expression. Later TypeScript will complain if you try to assign a non-boolean typed value to someBool.

### Functions

Function declaration is similar to variable declaration:

```javascript
function someFunc(someBool: boolean): string {
  return "Hello, world!";
}
```

This useless function takes one boolean type argument and returns a string type value:

```javascript
const someFunc = (someBool: boolean): string => "Hello, world!";
```

TypeScript requires parentheses around annotated lambda arguments, even for a single argument.

### Assertions

TypeScript supports “type assertions”, which is a way of telling the compiler that you are very certain a particular value is of a particular type and that it should assume you are right. These are sometimes called “casts” in other languages.

Generally speaking, type assertions are a red flag. There’s usually a better, more strongly-type way to write the code that avoids their usage. But sometimes they are convenient, particularly when interfacing with untyped JavaScript APIs. Of course it would be better to declare types for those APIs, but this is beyond the scope of some projects.

Type assertions use the `as` keyword:

```javascript
let someBool: boolean;
someBool as unknown as string = "hello world";  // Not an error (but probably a mistake)
```

Because this is case is so egregious, and likely to be a programmer error, TS forces you to double cast it. A single `as` is usually sufficient.

### Interfaces

Ok, now the real fun begins. So far we’ve only looked at primitive types like string and boolean. What about objects, arrays, and all that?

TypeScript “interfaces” allow us to declare the properties and behaviors that objects should have. There are required properties, optional properties, etc.

Interface declaration looks somewhat like object usage:

```javascript
interface myInterface {
  someBool: boolean;
  someString: string;
}
```

Now when we use it, both someBool and someString are required. Hence, the following attempt to assign an empty object to a const of type myInterface is a TypeScript error:

```javascript
const myObj: myInterface = {};  // TypeScript error!
```

The object we assign must have both required properties:

```javascript
const myObj: myInterface = {
  someBool: true,
  someString: "Hello"
};  // This works.
```

Optional fields are annotated using the ? character:

```javascript
interface myInterface {
  thisIsRequired: boolean;
  thisIsOptional?: string;
}

const myObj: myInterface = {
  thisIsRequired: true
};
```

### Union Types

Sometimes you want to say that “this thing is of this type... *or* that type.” Enter “union types”:

```javascript
type boolOrString = boolean | string;

let myVar: boolOrString;

myVar = true;
myVar = 'hello!';
```

This is 100% valid. myVar can hold either a boolean *or* a string value. However, TypeScript will force you to disambiguate which type it currently holds before you can do anything unsafe with it. For example, if we have a function that takes a union type:

```javascript
function upperBool(arg: boolean | string): string {
  if (typeof arg == 'string') {
    return arg.toUpperCase();
  }
  else if (typeof arg == 'boolean') {
    return arg.toString().toUpperCase();
  }
}
```

It looks like our function could fall through and return undefined, and theoretically in JavaScript it could, but any such usage would trigger an error in TypeScript (assuming you are using `--strictNullChecks`, part of the `--strict` group of checks we recommend). TypeScript “knows” that we’ve handled both possible types of arg and so the if/else definitely does not fall through.

### Intersection Types

An intersection type combines two or more interfaces into a single compound interface:

```javascript
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
};
```

### Classes

TS has classes. I won’t get deep into TS classes, but I want to mention them. They can transpile to ES6 classes or ES2015 prototypal code. They are very powerful. They are, however, optional, as classes are still somewhat “new” to many JavaScript developers.

### Enums

TypeScript supports enum declarations. An enum is a type that can only hold one of a specific set of possible values.

### Generics

Generics are a mechanism for declaring “complex” types like arrays and promises. Creating new generics is somewhat advanced, but a basic understanding is required to use TS effectively.

```javascript
const arrayOfStrings: string[];
const anotherArrayOfStrings: Array<string>;
```

Both of these syntaxes are equivalent. They both declare “an array of strings”.

TypeScript includes a significant number of built-in generic types and you will need them to use the language effectively.

```javascript
let promiseMeAString: Promise<string>;
```

This declares a promise that is expected to resolve to a string type value.

### Indexable Types

Indexable types allow the developer to specify the key and value types expected when using the square-bracket operator `[]` to access object or array properties. This is appropriate when the key set is large or arbitrary and not known in advance. In this case it’s not possible to define each possible key value.

This interface describes an object that holds a collection of string type keys with boolean values:

```javascript
interface stringKeysBoolVals {
  [key: string]: boolean
}
```

The syntax is a little funny in that it includes a “placeholder” field, which I’ve set to `key`. This field is essentially a comment. TS ignores it. You can set it to anything that makes sense, e.g. `index`.

This constructs an object acting as a collection of arbitrary key/​value pairs using the interface we just declared:

```javascript
const myCollection: stringKeysBoolVals = {
  "value1": true,
  "value2": false,
  "value3": true
};
```

This usage is invalid because neither the key type of int nor the value-type of string is compatible with the declared interface:

```javascript
const invalidCollection: stringKeysBoolVals = {
  0: "foobar"
};
```

### A Note about Tooling

To get the most out of TypeScript it’s critical that your editor integrates with it and supports real-time type checking and error highlighting. Yes, you can run the TS compiler and check for errors at the command line, but this is a much slower development process.

Also, most editors will be able to use TypeScript annotations to provide context-sensitive help and tell you about types and declarations, which is really helpful. Modern APIs are too complicated to memorize; don’t try.

### Conclusion

I hope this helps bring to light some of the wonderful features of TypeScript that help us write more reliable, more maintainable, and more readable code.

The [official TypeScript website](https://www.typescriptlang.org/docs) is a great place to learn more.
