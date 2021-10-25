---
title: What is serialization?
author: Zed Jensen
github_issue_number: 1738
tags:
- data-processing
- json
date: 2021-05-06
---

![Mailbox](/blog/2021/05/what-is-serialization/banner.jpg)
Photo by [Brian Patrick Tagalog](https://unsplash.com/@briantagalog) on [Unsplash](https://unsplash.com/photos/axwRgfER-sA)

Serialization is a process used constantly by most applications today. However, there are some common misconceptions and misunderstandings about what it is and how it works; I hope to clear up a few of these in this post. I’ll be talking specifically about serialization and not marshalling, a related process.

### What is serialization?

Most developers know that complex objects need to be transformed into another format before they can be sent to a server, but many might not be aware that every time they print an object in the Python or JavaScript console, the same type of thing is happening. Variables and objects as they’re stored in memory—either in a headless program or one with developer tools attached—are not really usable to us humans.

Data serialization is the process of taking an object in memory and translating it to another format. This may entail encoding the information as a chunk of binary to store in a database, creating a string representation that a human can understand, or saving a config file from the options a user selected in an application. The reverse—deserialization—takes an object in one of these formats and converts it to an in-memory object the program can work with. This two-way process of translation is a very important part of the ability of various programs and computers to communicate with one another.

An example of serialization that we deal with every day can be found in the way we view numbers on a calculator. Computers use binary numbers, not decimal, so how do we ask one to add 230 and 4 and get back 234? Because the 230 and the 4 are deserialized to their machine representations, added in that format, and then serialized again in a form we understand: 234. To get 230 in a form the computer understands, it has to read each digit one at a time, figure out what that digit’s value is (i.e. the 2 is 200 and the 3 is 30), and then add them together. It’s easy to overlook how often this concept appears in everything we do with computers!

### Why it’s important to understand how it works

As a developer, there are many reasons you should be familiar with how serialization works as well as the various formats available, including:

- Different formats are best suited for different use cases.
- Standardization varies between formats. For example, INI files have no single specification, but TOML does. YAML 1.2 came out in 2009 but most YAML parsers still implement only parts of the earlier YAML 1.1 spec.
- Each application typically supports only one or a few formats.
- Formats have different goals, such as readability &amp; simplicity for humans, speed for computers, and conciseness for storage space and transfer efficiency.
- Applications use the various formats very differently from each other.

Before you start working on a project, it will certainly pay off to make sure you’re familiar with the options for serialization formats so you can pick the one most suited to your particular use case.

### Binary vs. human-readable serialization

There’s one more important distinction to be made before I show any examples, and that is human-readable vs. binary serialization. The advantage of human-readability is obvious: debugging in particular is much simpler, but other things like scanning data for keywords is much easier as well. Binary serialization, however, can be much faster to process for both the sender and recipient, it can sometimes include information that’s hard to represent in plain text, and it can be much more efficient with space without needing separate compression. I’ll stick to reviewing human-readable formats in this post.

### Common serialization formats with examples

#### CSV

For my examples, I’ll have a simple JavaScript object representing myself, with properties including my name, recent books I’ve read, and my favorite food. I’ll start with [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) (comma-separated values) because it’s intended for simpler data records than most of the other formats I’ll be showing; you’ll notice that there isn’t an easy way to do object hierarchies or lists. CSV files begin with a list of the column names followed by the rows of data:

```csv
name,favorite_food_name,favorite_food_prep_time,recent_book
Zed,Pizza,30,Leviathan Wakes
```

CSV files are most often used for storing or transferring tabular data, but there’s no single specification, so the implementation can be fairly different in different programs. The most common differences involve data with commas or line breaks, requiring quoting of some or all elements, and escaping some characters.

#### TSV

Files in tab-separated values (TSV) format are also fairly common, using tabs instead of commas to separate columns of data.

Because the tab character is rarely used in text put into table format, it is less of a problem as a separator than the very frequently-occurring comma. Typically no quoting or escaping of any kind is needed or possible in a TSV file.

```plain
name	favorite_food_name	favorite_food_prep_time	recent_book
Zed	Pizza	30	Leviathan Wakes
```

For the rest of my examples of each format, I’ll show the command (and library, if needed) that I used to get the serialized form of my object.

#### JSON

[JSON](https://www.json.org/json-en.html) stands for JavaScript Object Notation, and thus you might be fooled into thinking that it’s just an extension of JavaScript itself. However, this isn’t the case; it was originally derived from JavaScript syntax, but it has significant differences. For example, JSON has a stricter syntax for declaring objects. For my example, using the Google Chrome developer console I declared my object like this:

```javascript
const me = {
  name: 'Zed',
  recent_books: [
    'Leviathan Wakes',
    'Pride and Prejudice and Zombies'
  ],
  favorite_food: {
    name: 'Pizza',
    prep_time: 30
  }
};
```

You’ll notice that the property names aren’t quoted and the strings are single-quoted with `'`. This is perfectly valid JavaScript, but invalid JSON. Let’s see what an equivalent JSON file could look like:

```json
{
  "name": "Zed",
  "recent_books": [
    "Leviathan Wakes",
    "Pride and Prejudice and Zombies"
  ],
  "favorite_food": {
    "name": "Pizza",
    "prep_time": 30
  }
}
```

JSON requires property names to be quoted, and only double quotes `"` are allowed. It’s true that they look very similar, but the difference is important. Also notice that this JSON is formatted in an easy-to-read way, on multiple lines with indentation. This is called pretty-printing and is possible because JSON doesn’t care about whitespace.

Imagine my JavaScript application wants to send this object to some server that’s expecting JSON, using any other platform such as Java or .NET and not necessarily JavaScript. It would need to serialize the object from memory into a JSON string first, which can be done by JavaScript itself:

```javascript
> let meJSON = JSON.stringify(me);
> console.log(meJSON);
{"name":"Zed","recent_books":["Leviathan Wakes","Pride and Prejudice and Zombies"],"favorite_food":{"name":"Pizza","prep_time":30}}
```

Note that the result here has no extra line breaks or spaces. This is called minifying, and is the reverse of pretty-printing. The flexibility allowed by these two processes is one reason people like JSON.

Parsing our example back into a JavaScript object is also very easy:

```javascript
> console.log(JSON.parse(meJSON));
{
  name: 'Zed',
  recent_books: [ 'Leviathan Wakes', 'Pride and Prejudice and Zombies' ],
  favorite_food: { name: 'Pizza', prep_time: 30 }
}
```

The easy integration with JavaScript is a big reason JSON is so popular. I showed these examples to highlight how easy it is to use, but also to point out that sometimes we might use serialization without being aware of what’s going on under the hood; it’s important to remember that JSON texts aren’t JavaScript objects, and there may be instances where it makes more sense to use another format.

For instance, if you need a config file format that’s easy for humans to read, it is very helpful to allow comments that are not part of the data structure once it is read into memory. But CSV, TSV, and JSON do not allow for comments. The most obvious or popular choice isn’t always the only one, or the best one, so let’s keep looking at other formats.

#### XML

[XML](https://www.w3.org/XML/) is well known as the markup language of which HTML is a subset, or at least a close sibling. It can also be used for serialization of data, and allows us to add comments such as the one at the beginning:

```xml
<!-- My favorites as of May 2021 -->
<name>Zed</name>
<recent_books>Leviathan Wakes</recent_books>
<recent_books>Pride and Prejudice and Zombies</recent_books>
<favorite_food>
    <name>Pizza</name>
    <prep_time>30</prep_time>
</favorite_food>
```

XML has the benefit of being widely used, and it can represent more complex data structures since each element can also optionally have various attributes, and ordering of its child elements is significant.

But XML is unpleasant to type and for many use cases feels rather complex and bloated, so it suffers when compared to other formats we are looking at in this post.

#### YAML

[YAML](https://yaml.org/) is a serialization format for all kinds of data that’s designed to be human-readable. Simple files look fine, like our example:

```yaml
---
# My favorites as of May 2021
name: "Zed"
recent_books:
  - "Leviathan Wakes"
  - "Pride and Prejudice and Zombies"
favorite_food:
  name: "pizza"
  prep_time: 30
```

However, the YAML specification is far from simple, and quite a bit has been written on why it’s better to use other formats where possible:

- [YAML sucks.](https://github.com/cblp/yaml-sucks)
- [YAML: probably not so great after all](https://www.arp242.net/yaml-config.html)
- [The YAML-NOrway Law](https://allan.reyes.sh/programming/2018/06/20/The-YAML-NOrway-Law.html)

#### INI

[INI](https://en.wikipedia.org/wiki/INI_file), short for *initialization*, is well-known and has been around since the ’90s or earlier. It was most notably used for configuration files in Windows, especially in the era before Windows 95. INI files are still used in many places, including Windows and Linux programs’ system configuration files such as for the Git version control system.

Our example in INI format looks like this:

```ini
; My favorites as of May 2021

name=Zed
recent_books[]=Leviathan Wakes
recent_books[]=Pride and Prejudice and Zombies

[favorite_food]
name=Pizza
prep_time=30
```

INI has no single specification, so one project’s config files might use different syntax from another. This makes it hard to recommend over newer formats like TOML.

#### TOML

[TOML](https://toml.io/en/), which stands for Tom’s Obvious Minimal Language, is a more recent addition to serialization formats; its first version was released in 2013. TOML maps directly to dictionary objects and is intended especially for configuration files as an alternative to INI. It has similar syntax to INI as well:

```toml
# My favorites as of May 2021

name = "Zed"

recent_books = [
  "Leviathan Wakes",
  "Pride and Prejudice and Zombies"
]

[favorite_food]
name = "Pizza"
prep_time = 30
```

Unlike INI and YAML, TOML has a very clear and well-defined specification, and seems like a great option for new projects in the future. It is currently used most prominently by the Rust programming language tools. There is a list of TOML libraries per language and version on the [TOML wiki at GitHub](https://github.com/toml-lang/toml/wiki).

#### PHP’s serialize()

[PHP’s serialization output](https://www.php.net/manual/en/function.serialize.php) isn’t quite as readable, but the data is still recognizable for someone scanning visually for keywords or doing a more rigorous search. Converting from JSON is fairly simple:

```php
#!/usr/bin/env php

<?php

$json = '
{
  "name": "Zed",
  "recent_books": [
    "Leviathan Wakes",
    "Pride and Prejudice and Zombies"
  ],
  "favorite_food": {
    "name": "Pizza",
    "prep_time": 30
  }
}
';

$obj = json_decode($json, true);

echo serialize($obj);
```

And the result:

```plain
a:3:{s:4:"name";s:3:"Zed";s:12:"recent_books";a:2:{i:0;s:15:"Leviathan Wakes";i:1;s:27:"Pride and Prejudice and Zombies";}s:13:"favorite_food";a:2:{s:4:"name";s:5:"Pizza";s:9:"prep_time";i:30;}}
```

PHP serialize() does not allow for comments, but it does support full object marshalling, which it is more commonly used for.

#### Perl’s Data::Dumper

Perl’s [Data::Dumper](https://metacpan.org/pod/Data::Dumper) module serializes data in a format specifically for Perl to load back into memory:

```perl
#!/usr/bin/env perl

use strict;
use warnings;
use JSON;
use Data::Dumper 'Dumper';

my $json = <<'END';
{
  "name": "Zed",
  "recent_books": [
    "Leviathan Wakes",
    "Pride and Prejudice and Zombies"
  ],
  "favorite_food": {
    "name": "Pizza",
    "prep_time": 30
  }
}
END

my $hash = decode_json $json;

print Dumper($hash);
```

And the result, which is a valid Perl statement:

```perl
$VAR1 = {
          'recent_books' => [
                              'Leviathan Wakes',
                              'Pride and Prejudice and Zombies'
                            ],
          'name' => 'Zed',
          'favorite_food' => {
                               'name' => 'Pizza',
                               'prep_time' => 30
                             }
        }
```

### Conclusion

Serialization is an extremely common function that we as programmers should be familiar with. Knowing which is a good option for a new project can save time and money, as well as making things easier for developers and API users.

Please leave a comment if I have missed your favorite format!

#### Further reading

- [Serialization on Wikipedia](https://en.wikipedia.org/wiki/Serialization)
- [Marshaling on Wikipedia](https://en.wikipedia.org/wiki/Marshalling_(computer_science))
