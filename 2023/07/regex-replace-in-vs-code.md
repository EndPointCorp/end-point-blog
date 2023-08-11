---
title: "Text manipulation using regex replace in VS Code"
author: Kevin Quaranta Jr.
github_issue_number: 1997
tags:
- regex
- vscode
date: 2023-07-31
---

![A blank white wall and ceiling, with regular rays of light casting striped shadows at an acute angle. As the light hits the ceiling, the angle changes and the strips of light appear vertical.](/blog/2023/07/regex-replace-in-vs-code/light-patterns.webp)

<!-- Photo by Seth Jensen -->

Regular expressions are incredibly powerful tools that can make life easier for any developer. Being able to quickly and precisely parse text with the syntax you specify has kept regexes relevant from the '80s through to today.

Visual Studio Code is an excellent modern editor and development environment. According to the Stack Overflow Developer Survey of 2022, it was far and away the most popular IDE for both professional developers and those learning to code—more than twice as popular as the second-place choice.

Like any great editor, VS Code supports using regexes to find and replace text. In this article, we’ll go over how to use this powerful regex mode.

To demonstrate, we’ll extract code values from a JavaScript object so that we can query a SQL database for content that contains one of the code values. We can use standard SQL query WHERE clause multiple matching:

```sql
WHERE code IN ('code1', 'code2', 'code3')
```

Or we can add the values to a regex alternation group separated by pipes (vertical bars) that we can use as a string match:

```sql
WHERE code ~ '^(?:code1|code2|code3)$'
```

Each has different query plans and performance impacts in SQL, but for this example we’ll choose the second for its extra regex goodness. Doing the first would just require a few changes to our replacement regexes; feel free to practice your regex skills by figuring out how to fit our data to the standard SQL format!

We have copied and pasted all 287 lines of the object into VS Code. For the sake of this article, we’ll just show a handful of lines to demonstrate the point. Here are some lines from the object:

```plain
{ 'code' : '33866-5','description' : 'HIV 1 Ab [Presence] in Capillary blood by Immunoassay'},
{ 'code' : '34591-8','description' : 'HIV 1 Ab [Presence] in Body fluid by Immunoassay'},
{ 'code' : '35437-3','description' : 'HIV 1 Ab [Presence] in Saliva (oral fluid) by Immunoassay'},
{ 'code' : '35438-1','description' : 'HIV 1 Ab [Units/volume] in Saliva (oral fluid) by Immunoassay'},
{ 'code' : '40437-6','description' : 'HIV 1 p24 Ab [Presence] in Serum by Immunoassay'},
{ 'code' : '40438-4','description' : 'HIV 1 gp41 Ab [Presence] in Serum by Immunoassay'},
{ 'code' : '40439-2','description' : 'HIV 1 gp120+gp160 Ab [Presence] in Serum by Immunoassay'},
{ 'code' : '49905-3','description' : 'HIV 1 Ab [Presence] in Unspecified specimen Qualitative by Rapid immunoassay'},
{ 'code' : '89374-3','description' : 'HIV 1 Ab [Presence] in Unspecified specimen by Immunoassay '},
{ 'code' : '51786-2','description' : 'HIV 2 Ab Signal/Cutoff in Serum by Immunoassay'},
{ 'code' : '12855-3','description' : 'HIV 1 p23 Ab [Presence] in Serum by Immunoblot (IB)'},
{ 'code' : '12856-1','description' : 'HIV 1 p65 Ab [Presence] in Serum by Immunoblot (IB) '},
{ 'code' : '12857-9','description' : 'HIV 1 p28 Ab [Presence] in Serum by Immunoblot (IB)'},
{ 'code' : '12858-7','description' : 'HIV 1 p32 Ab [Presence] in Serum by Immunoblot (IB)'},
{ 'code' : '12859-5','description' : 'HIV 1 p18 Ab [Presence] in Serum by Immunoblot (IB)'},
{ 'code' : '12870-2','description' : 'HIV 1 gp34 Ab [Presence] in Serum by Immunoblot (IB)'},
{ 'code' : '12871-0','description' : 'HIV 1 p26 Ab [Presence] in Serum by Immunoblot (IB)'},
{ 'code' : '12872-8','description' : 'HIV 1 p15 Ab [Presence] in Serum by Immunoblot (IB)'},
```

First, use the shortcut Control+f (Command+f on macOS) to bring up the Search bar.

![The find bar of VS Code. A text field reads "Find", with three buttons on the right side of the field reading "Aa", "ab" underlined, and ".\*". To the left of the text field is a right-facing arrow. To the right text reads "No results".](/blog/2023/07/regex-replace-in-vs-code/find.webp)

The more advanced options for Find are the icons on the right hand side of the Find input field. Choose the Use Regular Expression option, indicated by `.*`

With regex mode enabled, the "Find" field allows you to use a regex when searching. Ultimately, we want to replace any matches we get with text, or with nothing at all in order to delete our matches. To reveal the "Replace" field, hit the right-facing arrow on the left side of the Find bar.

![The same find bar, now with a second text field below reading "Replace".](/blog/2023/07/regex-replace-in-vs-code/find-and-replace.webp)

It can be easiest to find and replace in two phases: first, to do so on everything before the values we want to keep, and second, on everything after the values.

In this example, to match everything leading up to our values, we’ll use this regex:

```plain
\{ 'code' : '
```

Because braces are special characters in regex, we have to escape the opening brace with a backslash to tell the regex engine that we want to match a literal `{`. Other than that, our input is a bunch of literal characters. With more varied inputs, you can of course turn to more complex regexes.

Once we enter that regex, we see that all characters leading up to our values are highlighted.

![A few lines from the earlier codes objects, with the characters "{ 'code' : '" highlighted in yellow. In the top right the Find/replace bar is visible with the prior regex in the Find field.](/blog/2023/07/regex-replace-in-vs-code/before-code-highlighted.webp)

To replace these with nothing, simply place the cursor in the Replace input field and hit the Replace All icon to the right of the Replace input field, or hit Control+Enter (Command+Enter on macOS).

![The Find/Replace bar, this time with our regex. The Replace field is highlighted, with a popup reading "Replace All (⌘Enter)"](/blog/2023/07/regex-replace-in-vs-code/before-code-replace.webp)

It should now look like this:

![A few lines from the codes object, but the part which was highlighted has been deleted, so each line starts with the code directly. The find/replace bar now reads "no results" with the first regex in the Find field.](/blog/2023/07/regex-replace-in-vs-code/before-code-no-results.webp)

All of our lines now begin with the value we want to keep. Now, we’ll enter a regex that will match with everything after the last digits of the values. We can match an apostrophe and everything after that with the regex

```plain
'.*
```

Once we enter that regex, we’ll see that all characters following our values are highlighted 

![The altered object with our new regex in the Find field. Everything after the codes is highlighted.](/blog/2023/07/regex-replace-in-vs-code/after-code-highlighted.webp)

Once again, to replace all of these characters with nothing, we can place the cursor in the Replace input field and replace all again.

It should now look like this:

![The new altered object. Every line has one code, and nothing else.](/blog/2023/07/regex-replace-in-vs-code/after-code-no-results.webp)

So we’ve isolated each individual segment on each line. Our final step is to get all of these segments onto the same line and separate with a pipe.

Let’s match the newline character, represented by `\n`.

![The codes, the same as the previous image. The space partially overlapping the end of each line is highlighted.](/blog/2023/07/regex-replace-in-vs-code/newline-highlighted.webp)

Let’s replace these newlines with a pipe character. We enter the pipe character in the Replace field and replace all. It will result in this:

![The codes are now all on the same line, separated by a "|" pipe character with no whitespace in between, like "33866-5|34591-8|35437-3|" et cetera.](/blog/2023/07/regex-replace-in-vs-code/pipe-separated.webp)

Once we have this, we can place parentheses around the whole thing and put it into the WHERE clause of our SQL statement.

There you have it! You can imagine the possibilities with this. With decent knowledge of regex, you can use this as a power tool to manipulate text, isolate values that you want, and so on.
