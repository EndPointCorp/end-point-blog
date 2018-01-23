---
author: Phin Jensen
title: Regular Expression Inconsistencies With Unicode
tags: python, ruby, javascript, go, perl, dotnet, unicode
---

<p>
<img src="/blog/2018/01/23/regular-expression-inconsistencies-with-unicode/mud-run.jpg" alt="A mud run"><br/>
<small>A casual stroll through the world of Unicode and Regular Expressions—[Photo](https://www.flickr.com/photos/presidioofmonterey/7025086135) by Presidio of Monterey</small>

Character classes in Regular Expressions are an extremely useful and widespread feature, but there’s one often overlooked issue with them that you might not know of.

The issue stems from how different programming languages, locales, and character encodings treat predefined character classes. Take, for example, the expression `\w` which is often defined as a shorthand for a character class that matches “word characters”. The question is, what exactly are “word characters”? One common explanation is that `\w` is equivalent to `[a-zA-Z0-9_]`. When ASCII was the biggest player in the character encoding scene that may have been true, but with the standardization of Unicode, the truth has become a lot more foggy. Take this example in Python 3.6.2:

```python
>>> re.match(r'^\w+$', 'username')
<_sre.SRE_Match object; span=(0, 8), match='username'>
>>> re.match(r'^\w+$', 'userاسم')
<_sre.SRE_Match object; span=(0, 7), match='userاسم'>
```

Wait. The characters in “اسم” (“ism” is “name” in Arabic) definitely don’t fall within `[a-zA-Z0-9_]`. Let’s take a look at [the Python docs](https://docs.python.org/3/library/re.html#regular-expression-syntax):

> `\w`
>
>   For Unicode (str) patterns:
>
>     Matches Unicode word characters; this includes most characters that can be part of a word in any language, as well as numbers and the underscore. If the ASCII flag is used, only [a-zA-Z0-9_] is matched (but the flag affects the entire regular expression, so in such cases using an explicit [a-zA-Z0-9_] may be a better choice).
>
>   For 8-bit (bytes) patterns:
>
>     Matches characters considered alphanumeric in the ASCII character set; this is equivalent to [a-zA-Z0-9_]. If the LOCALE flag is used, matches characters considered alphanumeric in the current locale and the underscore.

So `\w` includes “most characters that can be part of a word in any language, as well as numbers and the underscore”. A list of the characters that includes is difficult to pin down, so it would be best to use the `re.ASCII` flag as suggested when you’re unsure if you want letters from other languages matched:

```python
>>> re.match(r'^\w+$', 'userاسم', flags=re.ASCII)
>>> re.match(r'^\w+$', 'username', flags=re.ASCII)
<_sre.SRE_Match object; span=(0, 8), match='username'>
```

That’s much better. Keep in mind that these same gotchas can apply to every predefined character class in whatever language you’re using, so don’t forget to check language-specific implementations for other character class shorthands, such as `\s` and `\d`, not just `\w`.

The biggest problem here is that every language seems to do regular expressions a little bit differently, so here’s a short, incomplete guide for several languages we use frequently.

#### Ruby

Ruby’s [Regexp class](https://ruby-doc.org/core-2.5.0/Regexp.html#class-Regexp-label-Character+Classes) documentation gives a simple and useful explanation: backslash character classes (e.g. `\w`, `\s`, `\d`) are ASCII-only, while POSIX-style bracket expressions (e.g. `[[:alnum:]]`) include other Unicode characters.

```ruby
irb(main):001:0> /^\w+$/ =~ "userاسم"
=> nil
irb(main):002:0> /^[[:word:]]+$/ =~ "userاسم"
=> 0
```

#### JavaScript

JavaScript doesn’t support POSIX-style bracket expressions, and its backslash character classes are simple, straightforward lists of ASCII characters. The [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions#Using_special_characters) has simple explanations for each one.

#### Go

Go follows the regular expression syntax used by [Google’s RE2 engine](https://github.com/google/re2/wiki/Syntax), which has easy syntax for specifying whether you want Unicode characters to be captured or not:

```go
package main

import (
	"fmt"
	"regexp"
)

func main() {
	// Perl-style
	fmt.Println(regexp.MatchString(`^\w+$`, "username")) // true
	fmt.Println(regexp.MatchString(`^\w+$`, "userاسم")) // false

	// POSIX-style
	fmt.Println(regexp.MatchString(`^[[:word:]]+$`, "username")) // true
	fmt.Println(regexp.MatchString(`^[[:word:]]+$`, "userاسم")) // false

	// Unicode character class
	fmt.Println(regexp.MatchString(`^\pL+$`, "username")) // true
	fmt.Println(regexp.MatchString(`^\pL+$`, "userاسم")) // true
}
```

You can see this code in action [here](https://play.golang.org/p/Y0HEhWXgXYa).

#### Perl

Documentation on how perl handles character classes is found in [perlrecharclass](https://perldoc.perl.org/perlrecharclass.html#Backslash-sequences). The rules aren’t as simple as with some languages, but can be generalized as such: `\w` will match Unicode characters with the “Word” property (equivalent to `\p{Word}`), unless the `/a` flag is enabled, in which case it will be equivalent to `[a-zA-Z0-9_]`.

```perl
use 5.012; # use 5.012 or higher includes Unicode support
use utf8; # necessary for Unicode string literals

print "username" =~ /^\w+$/; # 1
print "userاسم" =~ /^\w+$/; # 1

print "username" =~ /^\w+$/a; # 1
print "userاسم" =~ /^\w+$/a; # 0
```

However, you should know that for code points below 256, these rules can change depending on whether Unicode or locale rules are on, so if you’re unsure, consult the [perlre](https://perldoc.perl.org/perlre.html) and [perlrecharclass](https://perldoc.perl.org/perlrecharclass.html).

#### PHP

PHP’s documentation explains that `\w` matches letters, digits, and the underscore as defined by your locale. It’s not totally clear about how Unicode is treated, but it uses PCRE (Perl Compatible Regular Expressions) which supports a `/u` flag that can be used to enable Unicode matching in character classes:

```php
<?php

echo preg_match("/^\\w+$/", "username"), "\n";  # 1
echo preg_match("/^\\w+$/", "userاسم"), "\n";   # 0

echo preg_match("/^\\w+$/u", "username"), "\n"; # 1
echo preg_match("/^\\w+$/u", "userاسم"), "\n";  # 1
```

#### grep

Implementations of grep vary widely across platforms and versions. On my personal computer with GNU grep 3.1, `\w` doesn't work at all with default settings, matches only ASCII characters with the `-P` (PCRE) option, and matches Unicode characters with `-E`:

```bash
[phin@caballero ~]$ grep "^\w+$" <(echo "username")    # no match
[phin@caballero ~]$ grep -P "^\w+$" <(echo "username")
username
[phin@caballero ~]$ grep -P "^\w+$" <(echo "userاسم")  # no match
[phin@caballero ~]$ grep -E "^\w+$" <(echo "username")
username
[phin@caballero ~]$ grep -E "^\w+$" <(echo "userاسم")
userاسم
```

Again, implementations vary a lot. So double check on your system before doing anything important.

#### .NET

The [.NET Quick Reference](https://docs.microsoft.com/en-us/dotnet/standard/base-types/character-classes-in-regular-expressions) has a comprehensive guide to character classes. For word characters, it defines a specific group of Unicode categories including letters, modifiers, and connectors from many languages, but also points out that setting the [ECMAScript Matching Behavior](https://docs.microsoft.com/en-us/dotnet/standard/base-types/regular-expression-options#ECMAScript) option will limit `\w` to `[a-zA-Z_0-9]`, among other things. Microsoft’s documentation is clear and comprehensive with great examples, so I recommend referring to it frequently.

### Other links

As great as Unicode and Regular Expressions are, their implementations vary widely across various languages and tools, and that introduces far more unexpected behavior than I can write about in this post. Whenever you're going to use something with Unicode and regular expressions, make sure to check language specifications to make sure everything will work as expected. Of course, this topic has already been discussed and written about at great length, so here is a list of articles, tools, and blog posts that I’ve found interesting or useful.

- [The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/) - This is an oft-referenced article by Joel Spolsky. It was written in 2003 but the wealth of valuable information within is still very relevant and it helps greatly in going from Unicode noob to having a comfortable, useful knowledge of many common issues.
- ["💩".length === 2](http://blog.jonnew.com/posts/poo-dot-length-equals-two) - This blog post goes into some detail about the how and why JavaScript handles emoji as two characters and explores possible solutions. It also addresses some legacy inconsitencies, like how old HEAVY BLACK HEART character and other older Unicode symbols might be represented differently.
- [ftfy for Python](https://github.com/LuminosoInsight/python-ftfy) - ftfy is a Python library that takes corrupt Unicode text and attempts to fix it as best it can. Disclaimer: I haven’t had a chance to use it, but the examples are compelling and it’s definitely worth knowing about.
