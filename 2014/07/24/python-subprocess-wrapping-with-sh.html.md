---
author: Kirk Harr
gh_issue_number: 1016
tags: shell, python
title: Python Subprocess Wrapping with sh
---

When working with shell scripts written in bash/csh/etc. one of the primary tools you have to rely on is a simple method of piping output and input from subprocesses called by the script to create complex logic to accomplish the goal of the script. When working with python, this same method of calling subprocesses to redirect the input/output is available, but the overhead of using this method in python would be so cumbersome as to make python a less desirable scripting language. In effect you were implementing large parts of the I/O facilities, and potentially even writing replacements for the existing shell utilities that would perform the same work. Recently, python developers attempted to solve this problem, by updating an existing python subprocess wrapper library called pbs, into an easier to use library called sh.

Sh can be installed using pip, and the author has posted some documentation for the library here: [http://amoffat.github.io/sh/](http://amoffat.github.io/sh/)

### Using the sh library

After installing the library into your version of python, there will be two ways to call any existing shell command available to the system, firstly you can import the command as though it was itself a python library:

```python
from sh import hostname
print(hostname())
```

In addition, you can also call the command directly by just referencing the sh namespace prior to the command name:

```python
import sh
print(sh.hostname())
```

When running this command on my linux workstation (hostname atlas) it will return the expected results:

```python
Python 2.7.6 (default, Mar 22 2014, 22:59:56)
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import sh
>>> print(sh.hostname())
atlas
```

However at this point, we are merely replacing a single shell command which prints output to the screen, the real benefit of the shell scripts was that you could chain together commands in order to create complex logic to help you do work.

### Advanced Gymnastics

A common use of shell scripts is to provide administrators the ability to quickly filter log file output and to potentially search for specific conditions within those logs, to alert in the event that an application starts throwing errors. With python piping in sh we can create a simple log watcher, which would be capable of calling anything we desire in python when the log file contains any of the conditions we are looking for.

To pipe together commands using the sh library, you would encapsulate each command in series to create a similar syntax to bash piping:

```python
>>> print(sh.wc(sh.ls("-l", "/etc"), "-l"))
199
```

This command would have been equivalent to the bash pipe of "ls -l /etc | wc -l" indicating that the long listing of /etc on my workstation contained 199 lines of output. Each piped command is encapsulated inside the parenthesis of the command the precedes it.

For our log listener we will use the tail command along with a python iterator to watch for a potential error condition, which I will represent with the string "ERROR":

```python
>>> for line in sh.tail("-f", "/tmp/test_log", _iter=True):
...     if "ERROR" in line:
...         print line
```

In this example, once executed, python will call the tail command to follow a particular log file. It will iterate over each line of output produced by tail and if any of the lines contain the string we are watching for python will print that line to standard output. At this point, this would be similar to using the tail command and piping the output to a string search command, like grep. However, you could replace the third line of the python with a more complex action, emailing the error condition out to a developer or administrator for review, or perhaps initiating a procedure to recover from the error automatically.

### Conclusions

In this manner with just a few lines of python, much like with bash, one could create a relatively complex process without recreating all the shell commands which already perform this work, or create a convoluted wrapping process of passing output from command to command. This combination of the existing shell commands and the power of python; you get all the functions available to any python environment, with the ease of using the shell commands to do some of the work. In the future I will definitely be using this python library for my own shell scripting needs, as I have generally preferred the syntax and ease of use of python over that of bash, but now I will be able to enjoy both at the same time.
