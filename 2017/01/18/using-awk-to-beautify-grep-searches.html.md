---
author: Kamil Ciemniewski
gh_issue_number: 1282
tags: shell
title: Using Awk to beautify grep searches
---

Recently we’ve seen a sprout of re-implementations of many popular Unix tools. With the expansion of communities built around new languages or platforms, it seems that apart from the novelties in technologies — the ideas on how to use them stay the same. There are more and more solutions to the same kinds of problems:

- text editors
- CSS pre-processors
- find-in-files tools
- screen scraping tools
- ... many more ...

In this blog post I’d like to tackle the problem from yet another perspective. Instead of resolving to “new and cool” libraries and languages (grep implemented in X language) — I’d like to use what’s out there already in terms of tooling to build a nice search-in-files tool for myself.

### Search in files tools

It seems that for many people it’s very important to have a “search in files” tool that they really like. Some of the nice work we’ve seen so far include:

- [ack](https://github.com/petdance/ack2)
- [ripgrep](https://github.com/BurntSushi/ripgrep)
- [the_silver_searcher](https://github.com/ggreer/the_silver_searcher)

These are certainly very nice. As the goal of this post is to build something out of the tooling found in any minimal Unix-like installation — they won’t work though. They either need to be compiled or require Perl to be installed which isn’t everywhere (e. g. FreeBSD on default — though obviously available via the ports).

### What I really need from the tool

I do understand that for some developers, waiting 100 ms longer for the search results might be too long. I’m not like that though. Personally, all I care about when searching is how the results are being presented. I also like to have the consistency of using the same approach between many machines I work on. We’re often working on remote machines at End Point. The need to install e.g Rust compiler just to get the ripgrep tool is too time consuming and hence doesn’t contribute to getting things done faster. Same goes for e. g the_silver_searcher which needs to be compiled too. What options do I have then?

### Using good old Unix tools

The “find in files” functionality is covered fully by the Unix grep tool. It allows searching for a given substring but also “Regex” matches. The output can not only contain only the lines with matches, but also the lines before and after to give some context. The tool can provide line numbers and also search recursively within directories.

While I’m not into speeding it up, I’d certainly love to play with its output because I do care about my brain’s ability to parse text and hence: be more productive.

The usual output of grep:

```bash
$ # searching inside of the ripgrep repo sources:
$ egrep -nR Option src
(...)
src/search_stream.rs:46:    fn cause(&self) -> Option<&StdError> {
src/search_stream.rs:64:    opts: Options,
src/search_stream.rs:71:    line_count: Option<u64>,
src/search_stream.rs:78:/// Options for configuring search.
src/search_stream.rs:80:pub struct Options {
src/search_stream.rs:89:    pub max_count: Option<u64>,
src/search_stream.rs:94:impl Default for Options {
src/search_stream.rs:95:    fn default() -> Options {
src/search_stream.rs:96:        Options {
src/search_stream.rs:113:impl Options {
src/search_stream.rs:160:            opts: Options::default(),
src/search_stream.rs:236:    pub fn max_count(mut self, count: Option<u64>) -> Self {
src/search_stream.rs:674:    pub fn next(&mut self, buf: &[u8]) -> Option<(usize, usize)> {
src/worker.rs:24:    opts: Options,
src/worker.rs:28:struct Options {
src/worker.rs:38:    max_count: Option<u64>,
src/worker.rs:44:impl Default for Options {
src/worker.rs:45:    fn default() -> Options {
src/worker.rs:46:        Options {
src/worker.rs:72:            opts: Options::default(),
src/worker.rs:148:    pub fn max_count(mut self, count: Option<u64>) -> Self {
src/worker.rs:186:    opts: Options,
(...)
```

What my eyes would like to see is more like the following:

```bash
$ mygrep Option src
(...)
src/search_stream.rs:
 46        fn cause(&self) -> Option<&StdError> {
 ⁞
 64        opts: Options,
 ⁞
 71        line_count: Option<u64>,
 ⁞
 78    /// Options for configuring search.
 ⁞
 80    pub struct Options {
 ⁞
 89        pub max_count: Option<u64>,
 ⁞
 94    impl Default for Options {
 95        fn default() -> Options {
 96            Options {
 ⁞
 113   impl Options {
 ⁞
 160               opts: Options::default(),
 ⁞
 236       pub fn max_count(mut self, count: Option<u64>) -> Self {
 ⁞
 674       pub fn next(&mut self, buf: &[u8]) -> Option<(usize, usize)> {

src/worker.rs:
 24        opts: Options,
 ⁞
 28    struct Options {
 ⁞
 38        max_count: Option<u64>,
 ⁞
 44    impl Default for Options {
 45        fn default() -> Options {
 46            Options {
 ⁞
 72                opts: Options::default(),
 ⁞
 148       pub fn max_count(mut self, count: Option<u64>) -> Self {
 ⁞
 186       opts: Options,
(...)
```

Fortunately, even the tiniest of Unix like system installation already has all we need to make it happen without the need to install anything else. Let’s take a look at how we can modify the output of grep with awk to achieve what we need.

### Piping into awk

Awk has been in Unix systems for many years — it’s older than me! It is a programming language interpreter designed specifically to work with text. In Unix, we can use pipes to direct output of one program to be the standard input of another in the following way:

```bash
$ oneapp | secondapp
```

The idea with our searching tool is to use what we already have and pipe it between the programs to format the output as we’d like:

```bash
$ egrep -nR Option src | awk -f script.awk
```

Notice that we used egrep when in this simple case we didn’t need to. It was sufficient to use fgrep or just grep.

### Very quick introduction to coding with Awk

Awk is one of the forefathers of languages like Perl and Ruby. In fact some of the ideas I’ll show you here exist in them as well.

The structure of awk programs can be summarized as follows:

```perl
BEGIN {
  # init code goes here
}

# "body" of the script follows:

/pattern-1/ {
  # what to do with the line matching the pattern?
}

/pattern-n/ {
  # ...
}

END {
  # finalizing
}
```

The interpreter provides default versions for all three parts: a "no-op" for BEGIN and END and "print each line unmodified" for the "body" of the script.

Each line is being exploded into columns based on the "separator" which by default is any number of consecutive white characters. One can change it via the -F switch or by assigning the FS variable inside the BEGIN area. We’ll do just that in our example.

The "columns" that lines are being exploded into can be accessed via the special variables:

```perl
$0 # the whole line
$1 # first column
$2 # second column
# etc
```

The FS variable can contain a pattern too. So for example if we’d have a file with the following contents:

```
One | Two | Three | Four
Eins | Zwei | Drei | Vier
One | Zwei | Three | Vier
```

The following assignment would make Awk explode lines into proper columns:

```perl
BEGIN {
  FS="|"
}

# the ~ operator gives true if left side matches
# the regex denoted by the right side:
$1 ~ "One" {
  print $2
}
```

Running the following script would result with:

```bash
$ cat file.txt | awk -f script.awk
Two
Zwei
```

### Simple Awk coding to format the search results

Armed with this simple knowledge, we can tackle the problem we stated in the earlier part of this post:

```perl
BEGIN {
  # the output of grep in the simple case
  # contains:
  # <file-name>:<line-number>:<file-fragment>
  # let's capture these parts into columns:
  FS=":"

  # we are going to need to "remember" if the <file-name>
  # changes to print it's name and to do that only
  # once per file:
  file=""

  # we'll be printing line numbers too; the non-consecutive
  # ones will be marked with the special line with vertical
  # dots; let's have a variable to keep track of the last
  # line number:
  ln=0

  # we also need to know we've just encountered a new file
  # not to print these vertical dots in such case:
  filestarted=0
}

# let's process every line except the ones grep prints to
# say if some binary file matched the predicate:
!/(--|Binary)/ {

  # remember: $1 is the first column which in our case is
  # the <file-name> part; The file variable is used to
  # store the file name recently processed; if the ones
  # don't match up - then we know we encountered a new
  # file name:
  if($1 != file && $1 != "")
  {
    file=$1
    print "\n" $1 ":"
    ln = $2
    filestarted=0
  }

  # if the line number isn't greater than the last one by
  # one then we're dealing with the result from non-consecutive
  # line; let's mark it with vertical dots:
  if($2 > ln + 1 && filestarted != 0)
  {
    print "⁞"
  }

  # the substr function returns a substring of a given one
  # starting at a given index; we need to print out the
  # search result found in a file; here's a gotcha: the results
  # may contain the ':' character as well! simply printing
  # $3 could potentially left out some portions of it;
  # this is why we're using the whole line, cutting off the
  # part we know for sure we don't need:
  out=substr($0, length($1 ":" $2 ": "))

  # let's deal with only the lines that make sense:
  if($2 >= ln && $2 != "")
  {
    # sprintf function matches the one found in C lang;
    # here we're making sure the line numbers are properly
    # spaced:
    linum=sprintf("%-4s", $2)

    # print <line-number> <found-string>
    print linum " " out

    # assign last line number for later use
    ln=$2

    # ensure that we know that we "started" current file:
    filestarted=1
  }
}
```

Notice that the “middle” part of the script (the one with the patterns and actions) gets ran in an implicit loop - once for each input line.

To use the above awk script you could wrap it up with the following shell script:

```bash
#!/bin/bash

egrep -nR $@ | awk -f script.awk
```

Here we’re very trivially (and somewhat naively) passing all the arguments passed to the script to egrep with the use of $@.

This of course is a simple solution. Some care needs to be applied when trying to make it work with A, B and C switches, it’s not difficult either though. All it takes is to e.g pipe it through sed (another great Unix tool - the “stream editor”) to replace the initial '-' characters in the [filename]-[line-number] parts to match our assumptions of having “:“ as the separator in the awk script.

### In praise of “what-already-works”

The simple script like shown above could easily be placed in your GitHub, BitBucket or GitLab account and fetched with curl on whichever machine you’re working on. With one call to curl and maybe another one to put the scripts somewhere in the local PATH you’d gain a productivity enhancing tool that doesn’t require anything else to work than what you already have.

I’ll keep learning “what we already have” to not fall too much into “what’s hot and new” unnecessarily.
