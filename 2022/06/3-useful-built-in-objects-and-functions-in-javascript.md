---
author: Phineas Jensen
title: 3 useful built-in objects and functions in JavaScript
date: 2022-06-15
tags:
- javascript
---

I love learning (and learning about) programming languages. Right now I'm teaching myself Rust and trying to learn about 3D rendering. Every time I find a list of programming languages I have to look up every one that I haven't heard of, and when I see posts about Zig or Haskell or any other cool project on Hacker News, I can't help reading through the comments and seeing people discuss the unique features, quirks, and drawbacks of each language.

One thing I enjoy about learning about these languages (sometimes in an all-too-shallow way) is seeing all the different methods and syntaxes that exist for solving problems, and while it's always tempting to think the grass is greener on the other side, it's also important to do the same kind of exploration within the languages I'm using right now. Not only is it important, it actually makes using those languages a lot more enjoyable as I find new, more efficient ways to do things I've probably done dozens of times before.

With that spirit, here's a little list of cool objects and functions in JavaScript that have given me that feeling of excitement and made the language more fun and satisfying to use. Like any JavaScript feature, support will vary from browser to browser, runtime to runtime, and version to version, but with tools like Webpack becoming ubiquitous, that's becoming less and less of a problem.

## The Set object

The [`Set` object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) has a lot of use cases, but one I find myself using a lot is a set of selected items in a list like this:

![A table of items which can be selected with check boxes](/blog/2022/06/3-useful-built-in-objects-and-functions-in-javascript/selection.png)

Why is `Set` a good fit for this? Because a `Set` is a list of unique items (we shouldn't have one item in the `selected` list twice), we can add and remove items from it easily, and we can check membership with a single, obvious method that returns a boolean. Let's look at an example using an array first, which mimics code I've seen quite a bit.

```javascript
const selected = [];

function select(item) {
    if (selected.indexOf(item) == -1) {
        selected.push(item);
    }
}

function deselect(item) {
    const index = selected.indexOf(item);
    if (index != -1) {
        selected.splice(index, 1);
    }
}

function isSelected(item) {
    return selected.indexOf(item) != -1;
}
```

This isn't too complex, and it works well, but it's pretty verbose. Using the `indexOf` function three times is a little messy, and the `splice` function is uncommon enough that it's easy to forget exactly how it works. We can implement the same functions more simply using a `Set`:

```javascript
const selected = new Set();

function select(item) {
    selected.add(item);
}

function deselect(item) {
    selected.delete(item);
}

function isSelected(item) {
    return selected.has(item);
}
```

In fact, I'd say this functionality is so much simpler that we don't even need to define new functions. Selecting an item by calling `selected.add(...)` reads just as well as or better than `select(...)`, and the same goes for these other function names. `Set` handles it all for us.

Note that if you use a `Set` in React with `useState`, the component won't re-render unless you create a new `Set` object when you update the state, like so:

```javascript
function Example(props) {
    const [selected, setSelected] = useState();
    
    const addItem = (item) => {
        selected.add(item);
        setSelected(new Set(selected));
    }

    return items.map(item => (
        <button onClick={() => addItem(item)}>
    ));
}
```

This is because React will [bail out of the state update](https://reactjs.org/docs/hooks-reference.html#bailing-out-of-a-state-update) if the values are the same according to the [`Object.is`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) function.

## The URL API’s URLSearchParams object

Imagine you're writing a function that needs to parse and use a URL's search parameters. Pretty simple task, right? It wouldn't be too hard to do by hand, but there's probably a library out there somewhere, so you do a google search for "javascript parse url parameters" and click on the [first Stack Overflow answer](https://stackoverflow.com/questions/8486099/how-do-i-parse-a-url-query-parameters-in-javascript) in the results. You're greeted with an answer that defines a function using `.split()` a few times and then a much longer and more complex function that decodes the parameters in a non-standard way. Is this really necessary?

With the built-in [`URLSearchParams`](https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams) object, no. Supported in every major browser except Internet Explorer (which just reached its end of support life), this nice object handles parsing and formatting of string parameters with proper encoding and decoding:

```javascript
const params = new URLSearchParams('?foo=1');

params.append('bar', 'has weird & tricky characters'); // Add another parameter
console.log(params.toString()); // Prints 'foo=1&bar=has+weird+%26+tricky+characters'
```

It handles multiple parameters with the same key easily and supports iteration:

```javascript
const params = new URLSearchParams('?foo=1&foo=2&foo=3');
console.log(params.getAll('foo')) // Prints ["1", "2", "3"]

for (const [k, v] of params) {
    console.log(`${k}: ${v}`);
}
// Output: 
// foo: 1
// foo: 2
// foo: 3
```

Much nicer, and requires no copy-pasting of code from Stack Overflow or installing dependencies!

## The Array iterator functions

If you've used a lot of JavaScript or used languages like Perl, Python, Ruby, Rust, functional languages or languages with iterators, you've probably seen functions like `map` or `forEach`. I've used them pretty extensively but still find that a lot of people don't seem to know about them. For people coming from languages like C or C++, where they aren't available, or for people who are fresh out of a university program where neat things like that are often not taught in favor of theory, that's not much of a surprise.

`Array.prototype.forEach` is pretty straightforward. Compare the following equivalent code snippets:

```javascript
const names = ["bob", "roberta", "alice", "reza"];

// This...
for (let i = 0; i < names.length; i++) {
    console.log(names[i].substr(0,1).toUpperCase() + names[i].substr(1));
}

// ...is equivalent to this:
names.forEach(value => console.log(value.substr(0,1).toUpperCase() + value.substr(1)));
```

`forEach` takes as its argument a *callback function*, which it then calls once for each item in the array. The callback function can take more arguments than just the value as well, see its [MDN page](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach).

I personally find `map` more interesting and useful. Map is very similar to `forEach`, except that the values returned by the callback function are assembled to make a new array of the same length as the old one, essentially returning a transformed array.

```javascript
const names = ["bob", "roberta", "alice", "reza"];

// This...
const uppercaseNames = [];
for (let i = 0; i < names.length; i++) {
    const name = names[i];
    uppercaseNames.push(name.substr(0,1).toUpperCase() + name.substr(1));
}

// ...is equivalent to this:
const uppercaseNames = names.map(name => name.substr(0,1).toUpperCase() + name.substr(1));
```

There are similar cool functions that return `true` or `false` if the callback function returns `true` for *every* or *any* item in the list:

```javascript
const names = ["bob", "roberta", "alice", "reza", "spaces are good"];
// Both values will be false because of the "spaces are good" item
const allSpaceless = names.every(name => name.indexOf(" ") === -1);
// or...
const allSpaceless = !names.some(name => name.indexOf(" ") !== -1);
```

Or we can find individual or multiple items using a function, rather than just by value:

```javascript
const names = ["bob", "roberta", "alice", "Reza", "spaces are good"];
const namesStartingWithR = names.filter(name => name[0].toLowerCase() === "r") // returns ["roberta", "Reza"]
const firstNameWithC = names.find(name => name.toLowerCase().includes("c")) // returns "alice"
```

Then there's the complex but very cool `reduce` function, which starts with an initial value and replaces it with the result of the callback function on each iteration. `map` can be implemented using `reduce`:

```javascript
const names = ["bob", "roberta", "alice", "reza"];
// This...
const uppercaseNames = names.map(name => name.substr(0,1).toUpperCase() + name.substr(1));
// ...is equivalent to this:
const uppercaseNames = names.reduce(
    (previousValue, name) => {
        previousValue.push(name.substr(0,1).toUpperCase() + name.substr(1));
        return previousValue;
    },
    [] // Initial value
);
```

Obviously, it's not terribly useful in this case, but can be extremely useful for things like summing items in a list or transforming a list into an object somehow.

Consider keeping the [Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array) reference on hand to keep these functions close to your heart and start to learn some of their other features. As new versions of ECMAScript come out, new prototype functions will crop up too. Note that some of these functions will vary in performance compared to normal loop iterations. If you're using them in heavy workload or low-latency scenarios, make sure to compare and benchmark performance as needed.

## Conclusion

Okay, that was actually more than 3 things, but they fit into three categories, so I'm keeping the post's name. JavaScript's [built-in objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects) and the generally available [Web APIs](https://developer.mozilla.org/en-US/docs/Web/API) have a lot more cool APIs and functions and features that are very much worth checking out. MDN (which I linked several times throughout this article) is a fantastic resource to learn about them, so make sure to get familiar with it as you work with JavaScript. It'll pay off.
