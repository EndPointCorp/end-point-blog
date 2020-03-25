---
author: "Árpád Lajos"
title: "A tribute to Kyle Simpson’s JavaScript book series"
tags: javascript, books, development
gh_issue_number: 1524
---

<img src="/blog/2019/07/24/tribute-to-kyle-simpsons-book-series/you-dont-know-js.jpg" alt="You Don’t Know JS" /> [Photo](https://flic.kr/p/rdi2Qg) by [othree](https://www.flickr.com/photos/othree/), used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

Inspired by [the Ruby Fight Club](/blog/2016/08/31/ruby-fight-club), a group of us have been reading [Kyle Simpson](https://me.getify.com/)’s [You Don’t Know JS](https://github.com/getify/You-Dont-Know-JS) series. These books are a great source of inspiration and available for free. I meet weekly with our small group to discuss chapters from these books. Each time we have a presenter who walks us through the chapter that we all read beforehand.

During these sessions we have learned a lot about JavaScript, but also about preparing presentations. The increasing quality level of the meetings was noticable each week. I think we all owe a large **thanks** to Kyle Simpson. In this article I will focus on the book “You Don’t Know JS: ES6 and Beyond”.

### Past, present and future

ECMAScript (ES for short) was versioned with a small number up until now, like 5. ES1 and ES2 were not widely known or implemented. ES3 was used by Internet Exporer 6–8 and Android 2.x. ES4 never came out. ES5 came out in 2009. ES5.1 came out in 2011 and was widely used by Firefox, Chrome, Opera, Safari, etc.

Now, version names will be in the format ES<year>, but it might change to a per-feature basis.

In the past JavaScript versions were based on major releases of ES. However, due to the importance of the language, it is too much of a hassle to wait till 20 features are ready and release them together. It is much better to make finished features available as soon as they are ready. As a result, we know what functionalities we’re gaining.

It’s good to reflect on just how important the language is. JavaScript is the lingua franca for web browsers. Web developers need to be aware of JavaScript to its slightest details. While the markup of a webpage is HTML and its design is CSS, the client-side programming is done via JavaScript, more or less in a standard manner.

Since JavaScript is almost completely standard for browsers, programmers would have a much easier life if they were writing JavaScript when coding on server-side as well. There is a mental leap when one works both on the client-side and server-side of a feature and has to write Java/​C++/​PHP/​Ruby or whatever server-side code and then, in the next moment, they have to change their way of thinking and switch to the client-side and write JavaScript code. This is not difficult for a seasoned programmer who’s used to doing this. But when such a switch happens 50–60 times a day, it gets tiresome, and the programmer might not even realize why the day was tiring, since all they did was implement some simple features or fix some simple bugs.

It is perfectly logical that JavaScript found its way into server-side programming. Node.js is a standalone JavaScript runtime and whoever uses it for server-side web programming automatically gains the benefit of being able to work with the same language both on server side and client side. Of course, one still has to work with HTML, CSS, and a database as a web programmer, so multiple languages will be needed at some point, but there is a level of comfort given to web programmers using Node.js. Of course, the event loop used by JavaScript along with its single-threaded approach makes it less effective in doing some CPU-intensive stuff.

However, for server-side calculations, I would not be surprised at all if sooner or later full support is added to Node.js for multithreaded work. A great possible benefit of using JavaScript both on server-side and client-side, especially if there is a WebSocket connection involved, is that the server and the client could use the very same object, which opens the possibility to create a new paradigm. I know it’s science fiction, but imagine how cool it would be to implement a JavaScript class/​prototype and while doing so being able to define what should be available for the client-side as well. Object state change could happen on both server-side and client-side and synchronization could be triggered in such a duplex channel. Internet connection problems could be handled as well. Let’s imagine the case when there is a grid to be shown for the user. The user wants to define filters, sort, maybe layout, the server has to find the data, possibly store the settings, also, generate the structure upon object creation. Of course, before this can be realized a lot of open questions need to be answered. However, as a utopian view, it looks great.

### Compiling and Transpiling

JavaScript is a hybrid interpreted and compiled language, since most modern runtimes compile the code, but it can be interpreted as well at runtime. Let’s see this code:

```javascript
var foo = [1,2,3];
var obj = {
 foo  // means `foo: foo`
};
obj.foo; // [1,2,3]
```

The code above natively assumes that the value of the foo attribute of obj is foo, because when an attribute is not defined, a value of the same name is the default, in this case, the value will be our foo variable. However, in old versions of JavaScript, this was not yet supported, so if we really need to use this code in older browsers, then we will need to convert our source-code into its oldschool equivalent, using a Transpiler (the action of transpiling is to convert a source-code to another source-code, possibly of different language, not modifying its essence).

JavaScript transpilers are a big topic, but for the sake of readability, we won’t delve too much into the details. I have the habit of using [Babel](https://babeljs.io/) whenever I’m in doubt that the result of compiling is the one that I expect, or I suspect an error in the result, or I am interested for any other reason about the actual result.

### Polyfilling

*“A polyfill, or polyfiller, is a piece of code (or plugin) that provides the technology that you, the developer, expect the browser to provide natively. Flattening the API landscape if you will.”* —Remy Sharp

If we expect a functionality or value to be in the web browser or, more widely, in JavaScript, but it is not existing yet, or is not sure to exist everywhere we intend to use it, then we define it. In general, if we expect something defined by the name of `myCoolStuff`, then we can do polyfilling like this:

```javascript
if (!myCoolStuff) { //Here we assume that some variable called myCoolStuff exists and we check whether it's falsy
    //Define myCoolStuff
}
```

The code above is unsafe though, because if `myCoolStuff` is not defined at all, then an error will be thrown. A better, more reliable approach is to compare its type against `undefined`.

```javascript
if (typeof myCoolStuff === "undefined") {
    //Define myCoolStuff
}
```

So far, so good. However, we might be tired of writing that kind of condition over and over again. An alternative is to abstract the approach, like:

```javascript
var toPolyfill = [
    {
        context: window,
        myCoolStuff: function () {/*...*/},
        someOtherStuff: 42,
        yetAnother: function (someParameter) {/*...*/},
        //...
    },
    {
        context: Object,
        foo: "bar"
    }
];
```

and then do something like this:

```
for (var obj of toPolyfill) {
    for (var key in obj) {
        if ((key !== "context") && (typeof obj.context[key] === "undefined")) {
            obj.context[key] = obj[key];
        }
    }
}
```

As we can see, we have an array called ```toPolyfill``` whose items are all objects. Each object has a ```context``` attribute, which specifies where should we check the other attributes for existence and use the default if not found.

Let’s take a look at the polyfilling of `Object.is`, which is a function to determine whether two variables hold the same values:

```javascript
if (Object.is === undefined) {
    Object.is = function(v1, v2) {
        // test for `-0`
        if (v1 === 0 && v2 === 0) {
            return 1 / v1 === 1 / v2;
        }
        // test for `NaN`
        if (v1 !== v1) {
            return v2 !== v2;
        }
        // everything else
        return v1 === v2;
    };
}

Object.is("abc", "abc") && Object.is(1/0, Infinity) && Object.is(NaN, NaN); //true
```

Well, that was nice, wasn’t it? But this is always called as `Object.is()`. Why not make it instance level?

```javascript
Object.prototype.is = function(value) {
    return Object.is(this, value);
};
```

It’s looking great and it should work, right? Let’s test it:

```javascript
"abc".is("abc"); //false
```

What? Don’t worry, we just missed using strict, which ensures that we are in strict mode, introduced in ES5:

```javascript
"use strict";
if (!Object.is) {
    Object.is = function(v1, v2) {
        // test for `-0`
        if (v1 === 0 && v2 === 0) {
            return 1 / v1 === 1 / v2;
        }
        // test for `NaN`
        if (v1 !== v1) {
            return v2 !== v2;
        }
        // everything else
        return v1 === v2;
    };
}

Object.prototype.is = function(value) {
    return Object.is(this, value);
}

"abc".is("abc"); //true
```

### Block scope

Virtually anyone with some experience in JavaScript has met a situation when variables did not behave as expected, especially when asynchronous stuff was involved. One reason is that variables created using the `var` keyword are function-scoped, not block-scoped. Proof:

```javascript
function foo() {
    if (1) {
        var something = 5;
    }
    something; //5
}

foo();
something; //error
```

The example above illustrates that the variable created in the inner scope of the function can be used without a problem outside the inner scope of the function, as long as it’s inside the function and that it cannot be reached outside the function; in short, we can see that our variable is function-scoped.

So let’s see an example where this is a problem. Let’s calculate the sum of natural numbers from 1 to 100, we expect, of course, 5050 as a result:

```javascript
var sum = 0;
for (var index = 1; index <= 100; index++) setTimeout(function() {sum += index}, 100);
setTimeout(function() {
    alert(sum); //10100
}, 200);
```

Wait, what? We expected 5050 as a result, yet, it was 10100, exactly twice as much. What happened? Let’s study this carefully:

- we initialize `sum` with 0
- we iterate a variable called `index` from 1 to 100 and add functions to the event loop to be executed 100 milliseconds later than the moment we reached to them at the iteration
- when `index` reaches 100, the last iteration is executed and `index` is incremented
- `index` is 101 at the end of the cycle
- we add a new `function` to the event loop to be executed 200 milliseconds later, alerting the result
- 100 milliseconds later the `function` which increases `sum` by `index` (101) will be executed 100 times
- as a result, `sum` will be 100 * 101 = 10100
- 100 more milliseconds later, the `function` which alerts `sum` (10100) is executed

Okay, we understand this. But why was `index` 101 and why not its current value of the iteration? Well, the answer is simple: the cycle ran before the functions which it added to the event loop. So we clearly have a problem with the function-scoped variable in this case. Luckily, we are able to use block scope as well, using the `let` keyword:

```javascript
var sum = 0;
for (let index = 1; index <= 100; index++) setTimeout(function() {sum += index}, 100);
setTimeout(function() {
    alert(sum); //5050
}, 200);
```

Wow, that was neat. Our cycle creates a block-scoped variable on each iteration and as a result the `function` given to `setTimeout` inside the same block will use the correct variable each time.

### Defaults

JavaScript has a neat way of setting defaults for parameters, like:

```javascript
function theMeaningOfLife(result = 42) {
    setTimeout(function() {
        console.log("The meaning of life is " + result);
    }, 10000000*365.25*24*60*60*1000);
}
```

This is nice, but there might be cases when the parameters are actually attributes of an object and that’s passed as parameter:

```javascript
function defaultize(params, expectedParams) {
    if (typeof params !== "object") {
        //params is not an object, do something
    }
    for (var key in expectedParams) {
        if (!(key in params)) params[key] = expectedParams[key];
    }
}

function bar(params) {
    defaultize(params, {
        foo: "fooDefault",
        bar: "barDefault",
        lorem: "loremDefault",
        ipsum: "ipsumDefault"
    });
    console.log(params);
}

bar({
    bar: "beer bar",
    ipsum: "dolor"
});
```

We can even use a function call as default:

```javascript
function defaultize(params, expectedParams) {
    if (typeof params !== "object") {
        //params is not an object, do something
    }
    for (var key in expectedParams) {
        if (!(key in params)) params[key] = expectedParams[key];
    }
}

function bar(params, defaults =
    defaultize(params, {
        foo: "fooDefault",
        bar: "barDefault",
        lorem: "loremDefault",
        ipsum: "ipsumDefault"
    })) {
    console.log(params);
}

bar({
    bar: "beer bar",
    ipsum: "dolor"
});
```

In the example above, if `defaults` is not passed to `bar`, then `defaultize` will be called, passing `params` and the `defaults`. Since `params` is an object, `defaultize` changes its attributes when needed. A neat example of default parameters can be seen in the next chunk of code, where a variable actually changes when a value is not passed to the `function`:

```javascript
var value = 0;

function something(x = value++) {
    console.log(x);
}

something(); //x has a value of 0, value is incremented to 1
something(); //x has a value of 1, value is incremented to 2
something(); //x has a value of 2, value is incremented to 3
something(1); //x has a value of 1, value remains 3
something(); //x has a value of 3, value is incremented to 4
```

### Applying defaults

The book (ES6 and beyond) gives us an example of applying defaults:

```javascript
var defaults = {
    options: {
        remove: true,
        enable: false,
        instance: {}
    },
    log: {
        warn: true,
        error: true
    }
};

var config = {
    options: {
        remove: false,
        instance: null
    }
};

config = Object.assign( {}, defaults, config );
```

With the code above we see that nested values in the default are not transferred. Losing data is not a desired situation. The problem is that `Object.assign` is shallow. The book gives this solution:

```javascript
var defaults = {
    options: {
        remove: true,
        enable: false,
        instance: {}
    },
    log: {
        warn: true,
        error: true
    }
};

var config = {
    options: {
        remove: false,
        instance: null
    }
};

config.options = config.options || {};
config.log = config.log || {};

({
    options: {
        remove: config.options.remove = defaults.options.remove,
        enable: config.options.enable = defaults.options.enable,
        instance: config.options.instance = defaults.options.instance
    } = {},
    log: {
        warn: config.log.warn = defaults.log.warn,
        error: config.log.error = defaults.log.error
    } = {}
} = config);
```

This solves our problem. `enable` is successfully set to `false`, but I did not like this solution very much, because it is a very particular solution for this data and is not reusable for other cases, where `config` and `options` have different attributes, so I came up with this reusable code:

```javascript
var defaults = {
    options: {
        remove: true,
        enable: false,
        instance: {}
    },
    log: {
        warn: true,
        error: true
    }
};

var config = {
    options: {
        remove: false,
        instance: null
    }
};

function applyDefaults(d, t) {
    if ((typeof d !== "object") && (typeof d !== "array")) {
        return d;
    }
    if (t === undefined) {
        if (typeof d === "object") {
            t = {};
        } else if (typeof d === "array") {
            t = [];
        }
    }
    for (var key in d) {
        if (t[key] === undefined) {
            t[key] = d[key];
        } else {
            applyDefaults(d[key], t[key]);
        }
    }
    return t;
}

applyDefaults(defaults, config);
console.log(config);
```

We can see that the recursive `applyDefaults` function does not rely on the attribute names and due to its agnosticity, we can reuse it for any defaulting.

### ES5 Getter/Setter

A very nice example in the book about ES5 getters and setters is this one:

```javascript
var o = {
    __id: 10,
    get id() { return this.__id++; },
    set id(v) {this.__id = v;}
}

console.log(o.id);                        // 10
console.log(o.id);                        // 11
console.log(o.id = 20);
console.log(o.id);                        // 20
// and:
console.log(o.__id);                        // 21
console.log(o.__id);                        // 21 – still!
```

The getter always returns the current value of `id` and increments it.

### Computed property names

```javascript
var myObject = {
    a: 1,
    b: 2,
    c: 3
};
```

What if we want to define some operations for it:

```javascript
var myObject = {
    a: 1,
    b: 2,
    c: 3,
    &&: function() {/*...*/},
    ||: function() {/*...*/},
    ===: function() {/*...*/},
    !==: function() {/*...*/},
    ==: function() {/*...*/},
    !=: function() {/*...*/},
};
```

The code will of course break, because data members of an object have the same syntax constraint in their naming as variables, see more [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_types). You can also try out a [name validator](https://mothereff.in/js-variables). We can solve the problem like this:

```javascript
var myObject = {
    a: 1,
    b: 2,
    c: 3
};
myObject["&&"] = function(){/*...*/};
myObject["||"] = function(){/*...*/};
myObject["==="] = function(){/*...*/};
myObject["!=="] = function(){/*...*/};
myObject["=="] = function(){/*...*/};
myObject["!="] = function(){/*...*/};
```

However, this doesn’t look as neat as the code which failed. After some research and experimenting I came up with this solution:

```javascript
var myObject = {
    a: 1,
    b: 2,
    c: 3,
    ["&&"]: function() {/*...*/},
    ["||"]: function() {/*...*/},
    ["==="]: function() {/*...*/},
    ["!=="]: function() {/*...*/},
    ["=="]: function() {/*...*/},
    ["!="]: function() {/*...*/},
};
```

Kyle Simpson makes sure that in the future none of the JavaScript programmers who had the blessing of reading his books will not have to suffer like me. He comes up with some very illustrative examples:

We can add computed properties to an object with the assignment of `foo["b" + "ar"] = "baz"`, like:

```javascript
var prefix = "user_";

var o = {
    baz: function(){  }
};

o[ prefix + "foo" ] = function(){ console.log("foo"); };
o[ prefix + "bar" ] = function(){ console.log("bar"); };

o[prefix + "foo"]();
o[prefix + "bar"]();
```

However, we can define these properties at initialization with the syntax of:

```javascript
var prefix = "user_";

var o = {
    baz: function(){  },
    [ prefix + "foo" ] : function(){ console.log("foo"); },
    [ prefix + "bar" ] : function(){ console.log("bar"); }
};

o[prefix + "foo"]();
o[prefix + "bar"]();
```

Symbol properties:

```javascript
var o = {
    [Symbol.toStringTag]: "really cool thing",
};

console.log(o.toString());

var o2 = {};

console.log(o2.toString());

o2[Symbol.toStringTag] = "really cool thing";

console.log(o2.toString());
```

Computed properties can be names of concise methods or concise generators:

```javascript
var o = {
    ["f" + "oo"]() {/*...*/},        // computed concise method
    *["b" + "ar"]() {/*...*/}        // computed concise generator
};
```

We can even set the prototype:

```javascript
var foo = 5;

var o1 = {
    foo
};

console.log(o1.foo); //5
foo++;

var o2 = {
    __proto__: o1,
};

console.log(o2.foo++); //5

var o3 = {
    __proto__: o2
}

console.log(o3.foo); //6
```

### Object super

We can set the prototype of an object and then calling `super` inside a function can make sense. Consider this example:

```javascript
var o1 = {
    foo() {
        console.log( "o1:foo" );
    }
};

var o2 = {
    foo() {
        super.foo();
        console.log( "o2:foo" );
    }
};

Object.setPrototypeOf( o2, o1 );

o2.foo();  // o1:foo
           // o2:foo
```

### Template literals

JavaScript provides us with a neat way to manage long texts in the form of template literals. Let’s see some examples from the book:

```javascript
var name = "Kyle";
var greeting = `Hello ${name}!`;

console.log( greeting );          // "Hello Kyle!"
console.log( typeof greeting );   // "string"
```

Notice that we have a template literal assigned to `greeting` and how neatly we can put into it dynamic values. In this case, the value of the name variable.

Another example is:

```javascript
var text =
`Now is the time for all good men
to come to the aid of their
country!`;

console.log( text );
// Now is the time for all good men
// to come to the aid of their
// country!
```

We can conveniently put HTML into template literals like this:

```javascript
var myHTML = `
<!DOCTYPE html>
<html>
<body>

<h2>An Unordered HTML List</h2>

<ul>
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ul>  

<h2>An Ordered HTML List</h2>

<ol>
  <li>Coffee</li>
  <li>Tea</li>
  <li>Milk</li>
</ol> 

</body>
</html>
`;
```

It is as if we were looking at only HTML code. Imagine how great it is to read code like this instead of concatenated strings with lots of addition signs and quotes. Let’s implement a function which generates the options of a select tag:

```javascript
function generateOptions(input) { //format of [{key, value}, …] is expected
    var output = "";
    for (let item of input) output += `<option value="${item.key}">${item.value}</option>`;
    return output;
}

var options = generateOptions([
    {key: 1, value: "Coffee"},
    {key: 2, value: "Tea"},
    {key: 3, value: "Milk"},
]);
```

I think this is very elegant. Let’s make a `select`:

```javascript
var select = `<select class="my-class">${options}</select>`;
//<select class="my-class"><option value="1">Coffee</option><option value="2">Tea</option><option value="3">Milk</option></select>
```

That’s not very pretty to read, is it? Let’s make it nicer:

```javascript
function generateOptions(input) { //format of [{key, value}, …] is expected
    var output = "";
    for (let item of input) output += `\n    <option value="${item.key}">${item.value}</option>`;
    return output;
}

var options = generateOptions([
    {key: 1, value: "Coffee"},
    {key: 2, value: "Tea"},
    {key: 3, value: "Milk"},
]);

var select = `<select class="my-class">${options}\n</select>`;
/*
<select class="my-class">
    <option value="1">Coffee</option>
    <option value="2">Tea</option>
    <option value="3">Milk</option>
</select>
*/
```

But wait, we do not even need the `\n` (we can keep it though if we want, it’s a matter of preference):

```javascript
function generateOptions(input) { //format of [{key, value}, …] is expected
    var output = "";
    for (let item of input) output += 
`
    <option value="${item.key}">${item.value}</option>`;
    return output;
}

var select = 
`<select class="my-class">${options}
</select>`;
```

Let’s add a `button`:

```javascript
function generateOptions(input) { //format of [{key, value}, …] is expected
    var output = "";
    for (let item of input) output += `
    <option value="${item.key}">${item.value}</option>`;
    return output;
}

var myChunk = `<select class="my-class">${options}
</select>
<input type="button" value="GO">`;
```

I’m literally (no pun intended) in awe to see that in JavaScript we can template HTML so nicely.

Even some more complex problems are not problems when one uses template literals:

```javascript
function upper(s) {
    return s.toUpperCase();
}

var who = "reader";

var text =
`A very ${upper( "warm" )} welcome
to all of you ${upper( `${who}s` )}!`;

console.log( text );
// A very WARM welcome
// to all of you READERS!
```

### for...of loops

The syntax looks like this:

```javascript
for (var item of collection) {
    //Do something with item
}
```

`for`...`of` loops can only be executed for iterables. It is as if we were doing:

```javascript
for (var key in collection) {
   //Do something with collection[key]
}
```

However, there are technical differences for the loop of:

```javascript
for (var item of collection) {
    //Do something with item
}
```

Babel generates:

```javascript
"use strict";

for (var _iterator = collection, _isArray = Array.isArray(_iterator), _i = 0, _iterator = _isArray ? _iterator : _iterator[Symbol.iterator]();;) {//Do something with item

  var _ref;

  if (_isArray) {
    if (_i >= _iterator.length) break;
    _ref = _iterator[_i++];
  } else {
    _i = _iterator.next();
    if (_i.done) break;
    _ref = _i.value;
  }

  var item = _ref;
}
```

Let’s see some examples:

```javascript
var a = ["a","b","c","d","e"];

for (var idx in a) {
    console.log( idx );
}
// 0 1 2 3 4

for (var valA of a) {
    console.log( valA );
}
// "a" "b" "c" "d" "e"

var b = {
    key1: "value1",
    key2: "value2",
    key3: "value3",
    key4: "value4",
    key5: "value5",
    key6: "value6",
}
//”key1” “key2” “key3” “key4” “key5” “key6”
for (var idy in b) console.log(idy);

for (var valB of b) console.log(valB);
//Uncaught TypeError: b is not iterable
```

A pre-ES6 alternative is to get the keys of the object and iterate the set of keys:

```javascript
var a = ["a","b","c","d","e"],
        k = Object.keys( a );

for (var val, i = 0; i < k.length; i++) {
    val = a[ k[i] ];
    console.log( val );
}
// "a" "b" "c" "d" "e"
```

An alternative using the iterator Symbol:

```javascript
var a = ["a","b","c","d","e"];

for (var val, ret, it = a[Symbol.iterator]();
    (ret = it.next()) && !ret.done;
) {
    val = ret.value;
    console.log( val );
}
// "a" "b" "c" "d" "e"
```

Supported built-in values in JavaScript that are by default iterable:

- Arrays
- Strings
- Generators
- Collections

An example with Strings:

```javascript
for (var c of "hello") {
        console.log( c );
}
// "h" "e" "l" "l" "o"

for (var c of new String("hello")) {
    console.log( c );
}
// "h" "e" "l" "l" "o"
```

And another one with arrays and destructuring:

```javascript
var o = {};

for (o.a of [1,2,3]);
console.log(o);

for ({x: o.a} of [ {x: 1}, {x: 2}, {x: 3} ]);
console.log(o);
```

And another one with generators:

```javascript
function *myGenerator() {
    var y = 1;
    while (y < 10) yield y++;
}

var values = myGenerator();

for (v of values) console.log(v);
```

We have an upper boundary for `y`. If there was no such boundary, the `for`...`of` would go on forever.

However, generators have a duplex channel of communication between the function and the caller. We can pass some values to a generator when we iterate it. I was thinking whether there is a way to pass values somehow to a generator while iterating it with a `for`...`of` loop. Consider this example:

```javascript
function *myGenerator(input) {
    console.log(input); //undefined
    while(input = yield) {
        console.log(input); //never gets here
    };
}

var gen = myGenerator(1);
for (var input of gen);
```

We do not have difficulties in doing that with a `while` cycle:

```javascript
function *myGenerator(input) {
    console.log(input);
    while(input = yield) {
        console.log(input);
    };
}

var gen = myGenerator(1);
//for (var input of gen);
var counter = 10;
while (!gen.next(--counter).done);
console.log("Finished");
```

If we intend to parameterize our generator using a for..of loop, then we are entering a rabbit hole and a lot of suffering awaits us. So, from our `for`...`of` loop that we would like to parameterize:

```javascript
function *myGenerator(input) {
    console.log(input); //undefined
    while(input = yield) {
        console.log(input); //never gets here
    };
}

var gen = myGenerator(1);
for (var input of gen);
```

Babel generates this hairy monster:

```javascript
"use strict";

var _marked = /*#__PURE__*/regeneratorRuntime.mark(myGenerator);

function myGenerator(input) {
    return regeneratorRuntime.wrap(function myGenerator$(_context) {
        while (1) {
            switch (_context.prev = _context.next) {
                case 0:
                    console.log(input);
                case 1:
                    _context.next = 3;
                    return;
                case 3:
                    if (!(input = _context.sent)) {
                        _context.next = 7;
                        break;
                    }
                    console.log(input);
                    _context.next = 1;
                    break;
                case 7:
                    ;
                case 8:
                case "end":
                    return _context.stop();
            }
        }
    }, _marked, this);
}

var gen = myGenerator();
for (var _iterator = gen, _isArray = Array.isArray(_iterator), _i = 0, _iterator = _isArray ? _iterator : _iterator[Symbol.iterator]();;) {
    var _ref;
    if (_isArray) {
        if (_i >= _iterator.length) break;
        _ref = _iterator[_i++];
    } else {
        _i = _iterator.next();
        if (_i.done) break;
        _ref = _i.value;
    }
    var input = _ref;
}
```

This is not enough, since this strangely throws an error because `regeneratorRuntime` does not exist, yet we try to call it. Let’s wrap a function around this code and download Babel’s polyfill:

```javascript
"use strict";
function mainFunction() {

var _marked = /*#__PURE__*/regeneratorRuntime.mark(myGenerator);

function myGenerator(input) {
    return regeneratorRuntime.wrap(function myGenerator$(_context) {
        while (1) {
            switch (_context.prev = _context.next) {
                case 0:
                    console.log(input);
                case 1:
                    _context.next = 3;
                    return;
                case 3:
                    if (!(input = _context.sent)) {
                        _context.next = 7;
                        break;
                    }

                    console.log(input);
                    _context.next = 1;
                    break;
                case 7:
                    ;
                case 8:
                case "end":
                    return _context.stop();
            }
        }
    }, _marked, this);
}


var gen = myGenerator(1);

for (var _iterator = gen, _isArray = Array.isArray(_iterator), _i = 0, _iterator = _isArray ? _iterator : _iterator[Symbol.iterator]();;) {
    var _ref;

    if (_isArray) {
        if (_i >= _iterator.length) break;
        _ref = _iterator[_i++];
    } else {
        _i = _iterator.next();
        if (_i.done) break;
            _ref = _i.value;
        }
        var input = _ref;
    }
}

var script = document.createElement('script');
script.onload = function () {
    mainFunction();
};
script.src = "https://cdnjs.cloudflare.com/ajax/libs/babel-polyfill/7.2.5/polyfill.min.js";

document.head.appendChild(script);
```

We can pass values to the iterator, like this:

```javascript
"use strict";

function mainFunction() {
    var _marked = /*#__PURE__*/regeneratorRuntime.mark(myGenerator);
    function myGenerator(input) {
        return regeneratorRuntime.wrap(function myGenerator$(_context) {
            while (1) {
                switch (_context.prev = _context.next) {
                    case 0:
                        console.log(input);
                    case 1:
                        _context.next = 3;
                        return;
                    case 3:
                        if (!(input = _context.sent)) {
                            _context.next = 7;
                            break;
                        }
                        console.log(input);
                        _context.next = 1;
                        break;
                    case 7:
                        ;
                    case 8:
                    case "end":
                        return _context.stop();
                }
            }
        }, _marked, this);
    }
    var gen = myGenerator(1);
    var index = 0;
    for (var _iterator = gen, _isArray = Array.isArray(_iterator), _i = 0, _iterator = _isArray ? _iterator : _iterator[Symbol.iterator]();;) {
        var _ref;
        if (_isArray) {
            if (_i >= _iterator.length) break;
            _ref = _iterator[_i++];
        } else {
            _i = _iterator.next(index = (index + 1) % 10); //passing parameters
            if (_i.done) break;
            _ref = _i.value;
        }
        var input = _ref;
    }
}


var script = document.createElement('script');
script.onload = function () {
    mainFunction();
};

script.src = "https://cdnjs.cloudflare.com/ajax/libs/babel-polyfill/7.2.5/polyfill.min.js";
document.head.appendChild(script);
//1 2 3 4 5 6 7 8 9
```

We can work with this, but we burden ourselves too much with:

- having to care about the Polyfills
- having to understand a bunch of unintuitive functions
- having to write and maintain unreadable code

If we are not that masochistic, we will reach the conclusion that we need an alternative, a plan B here:

```javascript
function *myGenerator(input) {
    console.log("start " + input);
    while((input = yield (input * 2)) < 10) {
        console.log("inner " + input);
    };
    return false;
}

var index = 1;
var gen = myGenerator(index = 1);
gen.next();
var tmp;
while(!(tmp = gen.next(++index)).done) console.log("tmp " + tmp.value);
```

### Final notes

I could write a lot more about Kyle’s books, notably promises, generators and their combinations are very interesting. But frankly, I think the book about asynchronous work does an excellent job explaining those. I recommend Kyle Simpson’s books to everyone. I think we owe a big **thank you** to him and his effort to educate us. You can find his website at [me.getify.com](https://me.getify.com/).
