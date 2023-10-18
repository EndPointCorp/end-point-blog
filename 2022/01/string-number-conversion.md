---
author: "Jeff Laughlin"
title: "On the Importance of Explicitly Converting Strings to Numbers"
tags:
- programming
- javascript
- typescript
github_issue_number: 1822
date: 2022-01-11
---

![Wall with tiles of 4 colors in a pattern](/blog/2022/01/string-number-conversion/20220111-024957-sm.jpg)

<!-- Photo by Jon Jensen -->

Recently a valued colleague approached me with a JavaScript problem. This individual is new to programming and is working on a self-taught course.

The assignment was fairly simple: Take a list of space-delimited integers and find the maximum and minimum values. If you are an experienced developer you can probably already guess where this is going. His code:

```javascript
function highAndLow(numbers) {
  const myArr = numbers.split(" ");
  let lowNum = myArr[0];
  let highNum = myArr[0];
  for (let i = 0; i < myArr.length; i++) {
    if (myArr[i] > highNum) {
      highNum = myArr[i];
    } else if (myArr[i] < lowNum) {
      lowNum = myArr[i];
    }
  }
  return highNum + ' ' + lowNum;
}

console.log(highAndLow("8 3 -5 42 -1 0 0 -9 4 7 4 -4"));
```

This produced the output:

```javascript
"8 -1"
```

These are clearly not the maximum or minimum values.

After looking at it for a few moments I recognized a classic JavaScript pitfall: failure to explicitly convert stringy numbers to actual number types.

You see, JavaScript tries to be clever. JavaScript tries to get it right. JavaScript tries to say “the thing you are doing looks like something that you would do with numbers so I’m going to automatically convert these stringy numbers to number-numbers for you.”

The problem is that JavaScript is *not* clever; it is in fact very dumb about this. The further problem is when developers come to trust and rely on automatic conversion. Careers have been ruined that way.

In this case the naive programmer would say “Well, I’m comparing the things with a mathematical operator (`<` and `>`) so JavaScript should treat the values as numbers, right?” Wrong. JavaScript compares them alphabetically, **not** numerically. Except that even the “alphabetical” comparison kind of sucks but that’s another topic. JavaScript doesn't even attempt to convert to numbers in this case.

Repeat after me:

**Always explicitly convert stringy numbers to actual numbers even if the language claims to do it automatically.**

I don’t care if it’s JavaScript, Perl, some fancy Python package, it doesn’t matter.

**Do not trust automatic type conversion.**

You will get it wrong. It will get it wrong. There will be tears.

Fixing this program is as simple as changing one line to explicitly convert the numbers from strings.

```javascript
const myArr = numbers.split(" ").map(n => Number.parseInt(n, 10));
```

`Number.parseInt(n, 10)` is the “one true way” to turn a string-number into a number-number in JavaScript. **Never** omit the `10`; it is technically optional but you will regret it if you omit it, trust me. If you are reading base 10 numbers, tell JavaScript so explicitly. Otherwise it will again try to be clever but be not-clever and probably screw up the conversion by guessing the wrong radix.

It’s good that the developer caught this error visually, also, because they did not include a unit test. Errors like this slip through the cracks all. the. time.

Even TypeScript would not catch this. This function is perfectly legal TypeScript. There’s nothing illegal about comparing strings with `<` or `>`. TypeScript could only catch this if the developer provided additional type information up front, for example:

![TypeScript example of mismatched string and number types](/blog/2022/01/string-number-conversion/string-number-conversion-1.png)

Now that we’ve *told* the compiler “This is a string” and “This is a number”, now it can helpfully tell us “Hey, you’re trying to mix strings and numbers in a not-good way”.

So it all comes back to the mantra of “Always explicitly convert strings to numbers. Always.” And if you're bothering to use TypeScript, go the extra step and actually tell it what the types are. Don't make it guess; it might guess wrong. Explicit is better than implicit.

Some things never change.
