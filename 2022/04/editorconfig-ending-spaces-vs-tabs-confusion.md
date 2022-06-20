---
author: "Jon Jensen"
title: "EditorConfig: Ending the Spaces vs. Tabs Confusion"
date: 2022-04-30
tags:
- development
- tips
- intellij-idea
- vim
- emacs
github_issue_number: 1862
---

![](/blog/2022/04/editorconfig-ending-spaces-vs-tabs-confusion/20220316_184133.webp)
Photo by Garrett Skinner

### Varieties of text formatting 

Most everyone who has worked on a software development project with a group of other people has encountered the problem of source code being formatted in different ways by different text editors, IDEs, and operating systems.

The main variations go back to the 1970s or earlier, and include the questions:

* Will indentation be done by tabs (an ASCII control character) or spaces?
  * If indentation is done by spaces, how many spaces are used for each indentation level?
* What will indicate the end of each line (EOL)? The choices are:
  * a line feed (LF), used by the Unix family including Linux and modern macOS
  * a carriage return (CR), used by old pre-Unix Macintosh and some now-obscure operating systems
  * both together (CRLF) used by Windows and most Internet protocols
* Which character set encoding will be used? Common choices are:
  * Unicode UTF-8 encoding, used by Linux, macOS, and most other Unixes, and standard on the Internet
  * Unicode UTF-16 encoding (with either little-endian or big-endian encoding), used by modern Windows
  * legacy ISO-8859 and Windows "code page" encodings in older documents and codebases

### Editor configurations in conflict

Causing widespread frustration, by default, text editors and IDEs generally are each configured differently, and once set, the choices apply broadly from then on. But each developer can simply configure their editor to follow their team's standards, right? Well, maybe.

First, getting that to happen for every developer and every different editor being used isn't straightforward. It typically requires a document showing instructions and/or screenshots of how to configure each editor. It may have to be redone after a major upgrade or move to a new computer.

Second, and often a more persistent problem, standards may vary across different projects and even for different types of files within a given project. Ruby code is typically indented with 2 spaces, while perhaps in your project JavaScript uses 4 spaces and HTML uses tabs.

If you start a new project from scratch you can probably settle on a single standard, but in existing large codebases, it can make a lot of version control change "noise" to mess with that.

Computers are good at keeping track of lots of little details, so isn't there some way to have the computer deal with this?

### Storing configuration in the project

What if we store the text editor's or IDE's configuration in the project instead of per user, so it can go with the project to each new developer and tell their editor how to behave?

For many years that has been possible with some editors, but the configuration had to be set up separately for each editor, and often the feature is disabled by default.

Let's consider the two most popular terminal-based editors on Unix, partisans in a long-running editor war:

#### Vim

Vim has a feature called a "modeline" that allows for configuration settings to appear within the top or bottom 5 lines of the file.

For example, to instruct Vim to use spaces instead of tabs and 4-space tab stops, we can add to the top or bottom of our C source code file:

```c
/* vim: tabstop=4 shiftwidth=4 expandtab
 */
```

Since it gets tedious putting those special configuration comments in each file, Vim has an option to read a `.vimrc` file from the current directory, which applies to all files there and can be committed to version control.

This feature is disabled by default because Vim has in the past been vulnerable to files with malicious settings running arbitrary code.

You can `:set exrc secure` to enable the modeline feature in a code base you trust, and also to restrict what it can do.

#### Emacs

In Emacs the same thing can be done on the first or second line of the file. (Of course its setting names differ from Vim's.) For example consider this configuration in C source code:

```c
/* -*- mode: c; indent-tabs-mode: nil; c-basic-offset: 4; tab-width: 4 -*- */
```

Alternately you can use "Local Variables" set at the end of the file in as many lines as needed:

```c
/* Local Variables:      */
/* mode: c               */
/* indent-tabs-mode: nil */
/* c-basic-offset: 4     */
/* tab-width: 4          */
/* End:                  */
```

Emacs also has "Directory Variables" that can be set in the file `.dir-locals.el` for a directory and its subdirectories.

#### Others

Even if someone has gone to the trouble to set up such editor configuration files and add them to the project code repository, how often has that been done for your editor or IDE?

And how often is one out of sync with the others?

This is not the way to success.

### EditorConfig to the rescue

About 10 years ago Trey Hunner and Hong Xu shared with the world EditorConfig, their creation to solve this problem across ideally all editors.

They intentionally kept EditorConfig fairly limited in scope. It covers a limited number of the most important editor options so that the standard would be simple enough to be implemented for every editor either internally or as a plugin, and there would be no arbitrary code execution possible to cause security problems.

In EditorConfig the configuration for our examples and hypotheticals above lives in a `.editorconfig` file in the root of the project that looks like this:

```ini
# top-most EditorConfig file
root = true

# basics for all files in our project
[*]
charset = utf-8
end_of_line = lf

# C and JavaScript source get 4-space indents
[*.{c,js}]
indent_style = space
indent_size = 4

# Ruby gets 2-space indents
[*.rb]
indent_style = space
indent_size = 2

# HTML gets tab indents
[*.html]
indent_style = tab
```

In a big project you may want to have separate, smaller `.editorconfig` files in different directories. You can omit the `root = true` setting in subdirectories to inherit settings from the top-level `.editorconfig` file.

There are a couple of other options that are nice to specify.

This one removes any tabs or spaces from the end of lines:

```ini
trim_trailing_whitespace = true
```

Those are rarely needed or semantically meaningful, so it's nice to remove them. But there are a few cases where they can matter such as in Markdown.

This one determines whether the last line in the file will end with a newline:

```ini
insert_final_newline = true
```

By default some editors add to the last line a newline (such as Vim) and some don't (such as Emacs), leading to needless changes as various developers change files.

Typically every line should end with a newline, so that's a good editor feature to enable. But you could have some text template that should *not* end with a newline, so might need to specify `false` for that type of file.

And those are most of the features of EditorConfig! [The file format details](https://editorconfig.org/#file-format-details) are easy to digest.

### Editor &amp; IDE support

EditorConfig is now widely supported. These popular editors &amp; IDEs recognize `.editorconfig` files with no extra work:

* IntelliJ IDEA and most of its language-specific variants
* GitHub
* GitLab
* Visual Studio
* BBEdit
* and others

And these support it with a plugin:

* VS Code
* Vim
* Emacs
* Sublime Text
* TextMate
* Eclipse
* Atom
* Notepad++
* Geany
* and others

The plugins are typically easy to install system-wide from your operating system's package manager, or else locally for your user only.

### Do you need it?

Yes, I think you do.

I know of no reason for any developer not to use EditorConfig, in every editor, for every project. It's simple and at long last solves this small set of problems well.

One possible counterargument: If, before every version control commit, you run an automatic code formatter such as Prettier (in Node.js, for many languages) or a language-specific one such as `gofmt`, `rustfmt`, etc., you could perhaps live without your editor knowing how your files should be saved.

But isn't it better if your editor knows what kind of line endings and indents to use, rather than waiting for a code formatter to correct such fundamental things after you save? It is easy to start with a single `.editorconfig` file long before you have a continuous integration set up for the project.

And many projects don't format code automatically, and instead just "lint" it to report on deviations from the project standards. But that requires work to correct, and can be ignored if not enforced.

Many [open source projects large and small use EditorConfig](https://github.com/editorconfig/editorconfig/wiki/Projects-Using-EditorConfig), including this blog itself. But in recent months I have found several developers who had not yet heard of EditorConfig, so I want to spread awareness of it. I hope you'll [use EditorConfig](https://editorconfig.org/) too!
