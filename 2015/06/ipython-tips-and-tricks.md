---
author: Kannan Ponnusamy
title: IPython Tips and Tricks
github_issue_number: 1136
tags:
- python
- tips
- tools
date: 2015-06-18
---

Recently I have been working on Python automation scripts. Very often I use IPython to develop/debug the code.

IPython is an advanced interactive python shell. It is a powerful tool which has many more features. However, here I would like to share some of the cool tricks of IPython.

### Getting help

Typing object_name? will print all sorts of details about any object, including docstrings, function definition lines (for call arguments) and constructor details for classes.

```python
In [1]: import datetime
In [2]: datetime.datetime?
Docstring:
datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints or longs.
File:      /System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/lib-dynload/datetime.so
Type:      type
```

### Magic commands

### Edit

This will bring up an editor to type multiline code and execute the resulting code.

```python
In [3]: %edit
IPython will make a temporary file named: /var/folders/xh/2m0ydjs51qxd_3y2k7x50hjc0000gn/T/ipython_edit_jnVJ51/ipython_edit_NdnenL.py
```
```python
In [3]: %edit -p
```
This will bring up the editor with the same data as the previous time it was used or saved. (in the current session)

### Run a script

This will execute the script and print the results. 

```python
In [12]: %run date_sample.py
Current date and time:  2015-06-18 16:10:34.444674
Or like this:  15-06-18-16-10
Week number of the year:  24
Weekday of the week:  4
```

### Debug

Activate the interactive debugger.

```python
In [15]: %run date.py
Current date and time:  2015-06-18 16:12:32.417691
Or like this: ---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
/Users/kannan/playground/date.py in <module>()
      3 
      4 print "Current date and time: " , datetime.datetime.now()
----> 5 print "Or like this: " ,datetime.datetime.strftime("%y-%m-%d-%H-%M")
      6 print "Week number of the year: ", datetime.date.today().strftime("%W")
      7 print "Weekday of the week: ", datetime.date.today().strftime("%w")

TypeError: descriptor 'strftime' requires a 'datetime.date' object but received a 'str'

In [16]: %debug
> /Users/kannan/playground/date.py(5)<module>()
      4 print "Current date and time: " , datetime.datetime.now()
----> 5 print "Or like this: " ,datetime.datetime.strftime("%y-%m-%d-%H-%M")
      6 print "Week number of the year: ", datetime.date.today().strftime("%W")

ipdb>
</module></module>
```
I made a error in the line number 5, it should have to look like this. So %debug command took me into the Python debugger. 

```python
print "Or like this: " ,datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
```

### Save

This will save the specified lines to a given file. You can pass any number of arguments separated by space. 

```python
In [21]: %save hello.py 1-2 2-3
The following commands were written to file `hello.py`:
import datetime
datetime.datetime?
%edit
%edit -p
```

### Recall

Repeat a command, or get command to input line for editing. 

```python
In [28]: %recall 21

In [29]: import datetime
```

### Timeit

Time execution of a Python statement or expression

It can be one line or multiline statement. In a one liner we can pass through multiple ones separated by semicolon. 

```python
In [33]: %timeit range(100)
1000000 loops, best of 3: 752 ns per loop
```

### Shell Commands

Basic UNIX shell integration (you can run simple shell commands such as cp, ls, rm, cp, etc. directly from the ipython command line)

To execute any other shell commands we just need to add “!” beginning of the command line. We can assign the result of the system command to a Python variable to further use. 

```python
In [38]: list_of_files = !ls

In [39]: list_of_files
Out[39]: 
['lg-live-build',
 'lg-live-image',
 'lg-peruse-a-rue',
 'lg_chef',
 'lg_cms',
 'playground']
```

### History

Print input history, with most recent last.

```python
In [41]: %history 20-22
ls
import datetime
datetime.datetime.now()
```
```python
%history ~1/4 #Line 4, from last session
```
This will list the previous session history.

### Pastebin

This will upload the specifed input commands to Github’s Gist paste bin, and display the URL

It will upload the code as anonymous user

```python
In [43]: %pastebin [-d “Date Example”] 20-23
Out[43]: u'https://gist.github.com/a660948b8323280a0d27'
```

For more info on this topic: 

[http://ipython.org/ipython-doc/dev/interactive/tutorial.html](http://ipython.org/ipython-doc/dev/interactive/tutorial.html)

[http://ipython.org/ipython-doc/dev/interactive/magics.html](http://ipython.org/ipython-doc/dev/interactive/magics.html)


