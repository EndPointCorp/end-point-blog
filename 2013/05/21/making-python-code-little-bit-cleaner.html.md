---
author: Szymon Lipiński
gh_issue_number: 803
tags: python
title: Making Python Code a Little Bit Cleaner
---

When you develop a program in a group of programmers, it is really important to have some standards. Especially helpful are standards of naming things and formatting code. If all team members format the code in the same way and use consistent names, then it is much easier to read the code. This also means that the team works faster.

The same rules apply when you develop software in Python.

For Python there is a document which describes some of the most desirable style features for Python code [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/). However there are some problems with that, as even the standard Python library has some libraries which are not consistent. This shouldn’t be an excuse for your team to be inconsistent as well. Ensuring that the code is nice and readable is worth working for a moment on that.

In Python there are two tools which I use for writing code in Python—[Python style guide checker](https://pypi.org/project/pep8/) and [Python code static checker](https://pypi.org/project/pylint/).

### pep8

Program pep8 is a simple tool checking Python code against some of the style conventions in PEP 8 document.

#### Installation

You can install it within your virtual environment with simple:

```
pip install pep8
```

#### Usage

Let’s test the pep8 command on such an ugly Python file named test.py:

```
"this is a very long comment line this is a very long comment line this is a very long comment line"
def sth  (  a ):
    return  "x"+a
def sth1 ( a,b,c):
    a+b+c
```

The basic usage of the program is:

```
pep8 test.py
```

The above command prints:

```
test.py:1:80: E501 line too long (100 > 79 characters)
test.py:2:1: E302 expected 2 blank lines, found 0
test.py:2:11: E201 whitespace after '('
test.py:2:14: E202 whitespace before ')'
test.py:2:8: E211 whitespace before '('
test.py:3:16: E225 missing whitespace around operator
test.py:4:1: E302 expected 2 blank lines, found 0
test.py:4:11: E201 whitespace after '('
test.py:4:13: E231 missing whitespace after ','
test.py:4:15: E231 missing whitespace after ','
test.py:4:9: E211 whitespace before '('
test.py:5:6: E225 missing whitespace around operator
test.py:5:8: E225 missing whitespace around operator
test.py:6:1: W391 blank line at end of file
```

#### Configuration

Pep8 is highly configurable. The most important options allow to choose which errors should be ignored. For this there is an argument --ignore. There is also one thing in PEP8 document, which I don’t agree with. This document states that the length of the line shouldn’t be bigger than 80 characters. Usually terminals and editors I use are much wider and having 100 characters doesn’t make your program unreadable. You can set the allowed length of your line with --max-line-length.

So if I want to ignore the errors about empty lines at the end of file and set maximum line length to 100, then the whole customized command is:

```
pep8 --ignore=W391 --max-line-length=100  test.py
```

The output is different now:

```
test.py:2:1: E302 expected 2 blank lines, found 0
test.py:2:11: E201 whitespace after '('
test.py:2:14: E202 whitespace before ')'
test.py:2:8: E211 whitespace before '('
test.py:3:16: E225 missing whitespace around operator
test.py:4:1: E302 expected 2 blank lines, found 0
test.py:4:11: E201 whitespace after '('
test.py:4:13: E231 missing whitespace after ','
test.py:4:15: E231 missing whitespace after ','
test.py:4:9: E211 whitespace before '('
test.py:5:6: E225 missing whitespace around operator
test.py:5:8: E225 missing whitespace around operator
```

##### Config file

The same effect can be achieved using a config file. PEP8 searches for this file at the project level, the file must be named .pep8 or setup.cfg. If such a file is not found, then it looks for a file ~/.config/pep8. Only the first file is taken into consideration. After finding a file, it looks for a pep8 section in, if there is no such section, then no custom settings are used.

To have the same settings as in the above example, you can create a file .pep8 in the project directory with the following content:

```
[pep8]
ignore = W391
max-line-length = 100
```

The list of all all possible errors you can find at [PEP8 documentation page](http://pep8.readthedocs.io/en/latest/intro.html#error-codes).

##### Statistics

Another nice option which I use for checking the code is --statistics. It prints information about the type and number of problems found. I use it along with -qq option which causes pep8 to hide all other informations. The sort -n 1 -k -r part sorts the pep8 output in reverse order (biggest numbers come first) by first column treating that as numbers:

```
pep8 --statistics -qq django | sort -k 1 -n -r
```

The first 10 lines of the above command run against Django 1.5.1 code look like:

```
4685    E501 line too long (80 > 79 characters)
1718    E302 expected 2 blank lines, found 1
1092    E128 continuation line under-indented for visual indent
559     E203 whitespace before ':'
414     E231 missing whitespace after ','
364     E261 at least two spaces before inline comment
310     E251 no spaces around keyword / parameter equals
303     E701 multiple statements on one line (colon)
296     W291 trailing whitespace
221     E225 missing whitespace around operator
```

### pylint

Pylint is a program very similar to pep8, it just checks different things. The pylint’s goal is to look for common errors in programs and find potential code smells.

#### Installation

You can install pylint in a similar way as pep8:

```
pip install pylint
```

#### Usage

Usage is similar as well:

```
pylint --reports=n test.py
```

Notice there is --reports argument. Without it, the output is much longer and quiet messy.

The output of the above command is:

```
No config file found, using default configuration
************* Module test
C:  1,0: Line too long (100/80)
C:  2,0:sth: Invalid name "a" for type argument (should match [a-z_][a-z0-9_]{2,30}$)
C:  2,0:sth: Missing docstring
C:  2,12:sth: Invalid name "a" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
C:  4,0:sth1: Comma not followed by a space
def sth1 ( a,b,c):
            ^^
C:  4,0:sth1: Invalid name "a" for type argument (should match [a-z_][a-z0-9_]{2,30}$)
C:  4,0:sth1: Invalid name "b" for type argument (should match [a-z_][a-z0-9_]{2,30}$)
C:  4,0:sth1: Invalid name "c" for type argument (should match [a-z_][a-z0-9_]{2,30}$)
C:  4,0:sth1: Missing docstring
C:  4,11:sth1: Invalid name "a" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
C:  4,13:sth1: Invalid name "b" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
C:  4,15:sth1: Invalid name "c" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
W:  5,4:sth1: Statement seems to have no effect
```

#### Configuration

For pylint you can decide which problems should be ignored as well. If I want to ignore some errors, you have to know its number first. You can get the number in two ways, you can check at [pylint errors list](http://pylint-messages.wikidot.com/all-messages) or add the message number with argument --include-ids=y:

```
pylint --reports=n --include-ids=y test.py
No config file found, using default configuration
************* Module test
C0301:  1,0: Line too long (100/80)
C0103:  2,0:sth: Invalid name "a" for type argument (should match [a-z_][a-z0-9_]{2,30}$)
C0111:  2,0:sth: Missing docstring
C0103:  2,12:sth: Invalid name "a" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
C0324:  4,0:sth1: Comma not followed by a space
def sth1 ( a,b,c):
            ^^
C0103:  4,0:sth1: Invalid name "a" for type argument (should match [a-z_][a-z0-9_]{2,30}$)
C0103:  4,0:sth1: Invalid name "b" for type argument (should match [a-z_][a-z0-9_]{2,30}$)
C0103:  4,0:sth1: Invalid name "c" for type argument (should match [a-z_][a-z0-9_]{2,30}$)
C0111:  4,0:sth1: Missing docstring
C0103:  4,11:sth1: Invalid name "a" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
C0103:  4,13:sth1: Invalid name "b" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
C0103:  4,15:sth1: Invalid name "c" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
W0104:  5,4:sth1: Statement seems to have no effect
```

Now I know the number of the problem I want to ignore, let’s assume it is C0103, then I can ignore it with:

```
pylint --reports=n --include-ids=y --disable=C0103 test.py
No config file found, using default configuration
************* Module test
C0301:  1,0: Line too long (100/80)
C0111:  2,0:sth: Missing docstring
C0324:  4,0:sth1: Comma not followed by a space
def sth1 ( a,b,c):
            ^^
C0111:  4,0:sth1: Missing docstring
W0104:  5,4:sth1: Statement seems to have no effect
```

##### Config file

Pylint also supports setting the options in a config file. This config file can be a little bit complicated, and I think the best way is to let pylint generate the file, this can be done with the --generate-rcfile argument:

```
pylint --reports=n --include-ids=y --disable=C0103 --generate-rcfile > .pylint
```

This will create config file with all default settings and the changes from the command line.

To use the new config file, you should use the --rcfile argument:

```
pylint --rcfile=.pylint test.py
```

### Remarks

Pylint is great—sometimes even too great.

I usually ignore many of the errors, as too often the changes needed to satisfy pylint are not worth time spending on them. One of common problems found by pylint is that the variable name is too short. It has a rule that all the names should have between 2 and 30 characters. There is nothing bad with one letter variable, especially when it is something like Point(x, y) or it is a small local variable, something like for i in xrange(1,1000).

However on the other hand when a variable has much broader usage, or it should have some meaningful name to have code easier to read, it is a good idea to change the code.

For me it is good to have pylint checking such errors, so I don’t want pylint to ignore them. Sometimes it is OK to have code which violates those rules, so I just ignore them after ensuring that it is on purpose.
