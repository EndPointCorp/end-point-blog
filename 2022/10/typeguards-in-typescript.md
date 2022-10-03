---
author: Nicholas Piano
title: Typeguards in TypeScript
date: 2022-10-03
github_issue_number: 1900
featured:
  image_url: /blog/2022/10/typeguards-in-typescript/relief_map.png
tags:
- types
- typescript
description: A little known, but useful, feature of typescript
---

![A relief map of Liverpool Street in London, UK](/blog/2022/10/typeguards-in-typescript/relief_map.png)

<!-- Photo by Seth Jensen, 2022 -->

### Type guards in TypeScript

Typescript has a very rich type system. Sometimes too rich. For example, interfaces and types perform the same function with slightly different syntax.

This is a short intro to a powerful feature in TypeScript: Typeguards. This feature also exists in many strongly typed languages. While TypeScript is not strongly typed, it replicates this excellent feature.

### The feature

Normally, a function can be annotated with `boolean` to indicate its return type. However, when the intention is to narrow the type of object being tested from a supertype to one of its subtypes, the annotation `argument is Type` can be used instead. This can allow the compiler to infer the type of the argument at other points in the code after the test has been passed.

The following code demonstrates a use of this feature:

```typescript
type Animal = {
  canWoof: boolean;
};

type Dog = {
  canWoof: true;
  woof: () => void;
};

const isDog = (animal: Animal): animal is Dog => {
  if (animal.canWoof) {
    return true;
  }

  return false;
};
```

In this example, `Animal` is a supertype of `Dog`. The function `isDog()` takes an `Animal` object and uses a simple test to determine whether the object satisfies the type `Dog`. If the test passes, the annotation kicks in, allowing more powerful inference by the compiler as can be seen in the following example.

### An example

Since `isDog()` has been annotated with `animal is Dog`, all following statements in the scope can be typed accordingly.

```typescript
const dogFunction = (animal: Animal) => {
  if (!isDog(animal)) {
    return;
  }

  animal.woof(); // <- this is valid since the type has been inferred above
};
```

This would not be possible if the return type of `isDog()` were `boolean`, but after a statement returning from the function after **failing** the `isDog()` test, `animal.woof()` can be called safely.

This is also true of union types such as:

```typescript
type Cat = {
  canWoof: false;
  meow: () => void;
};

type Dog = {
  canWoof: true;
  woof: () => void;
};

type Animal = Cat | Dog;
```

Again:

```typescript
const dogFunction = (animal: Animal) => {
  // animal could still be Cat | Dog
  animal.meow(); // <- uh oh, 'meow' does not exist on type 'Animal'

  if (!isDog(animal)) {
    animal.meow(); // <- definitely Cat

    return;
  }

  animal.woof(); // <- definitely Dog because of return above
};
```

In these examples, if the annotation `animal is Dog` were replaced with `boolean` these type inferences would not be possible, greatly reducing the power of TypeScript to provide suggestions and type checking.

### Filtering a list

A list of ambiguous objects can be filtered to be of a single type as follows:

```typescript
const ambiguousList: Animal[] = [new Cat(), new Dog()];
const dogList: Dog[] = ambiguousList.filter(isDog);
```

This is now valid as far as the compiler is concerned. The array is now of type `Dog`.

### Limitations from an example in the wild: lodash.isEmpty

The `isUndefined` function from the Lodash has the following signature:

```typescript
isUndefined(value: any): value is undefined;
```

This employs the typeguard correctly, allowing the value to be disambiguated. On the other hand, the `isEmpty` function has the following signature:

```typescript
isEmpty(value?: any): boolean;
```

Despite the fact that an `undefined` value should be captured by the `isEmpty` function, it means that the following code will not compile:

```typescript
type Container = {
  escape: () => void;
};

const runEscapeIfNotEmpty = (container?: Container) => {
  if (isEmpty(container)) {
    return;
  }

  container.escape(); // <-- this will complain that `container` could be `undefined`
};
```

To correct this, the compiler would need to be able to rule out `undefined` and `null` as values. Sadly, there is no `is not` operator in TypeScript, otherwise the following might be possible:

```typescript
isEmpty(value?: any): value is not undefined | null;
```

It's value to keep the limitations of this feature in mind when designing guard functions.

### Conclusion

In conclusion, this feature should be taken advantage of whenever possible. It can greatly simplify code, making it clearer and easier to read.

However, there are limitations, such as the inability to detect when a variable does NOT satisfy a type.

Refer to the [official TypeScript documentation](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates) for more.
