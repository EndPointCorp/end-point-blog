---
author: Miguel Alatorre
gh_issue_number: 930
tags: python
title: Python decorator basics, part II
---



This is a continuation of my previous post: [Python decorator basics](/blog/2013/12/13/python-decorator-basics). Here I’ll talk about a decorator with optional arguments. Let’s say we want to pass an optional argument to the same debug decorator:

```python
def debug(msg=None):
    def actual_decorator(f):
        def wrapper(*args):
            if msg:
                print msg
            return f(*args)
        return wrapper
    return actual_decorator

@debug("Let's multiply!")
def mul(x, y):
    return x*y
```

Calling mul:

```python
mul(5, 2)
Let's multiply!
10
```

Excellent. Now let’s decorate without a msg and call mul:

```python
@debug
def mul(x, y):
    return x*y

mul(5, 2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: actual_decorator() takes exactly 1 argument (2 given)
</module></stdin>
```

Oh oh. Let’s see what happens at time of decoration:

```python
mul = debug(mul)
```

Hmmm, mul gets passed to debug as it’s argument and then the arguments (5, 2) are passed to actual_decorator, since debug returns actual_decorator. To resolve this we need to always call the decorator as a function:

```python
@debug()
def mul(x, y):
    return x*y

mul(5, 2)
10
```

Assuming that we always expect the msg parameter to be a non-callable, another option would be to check the type of argument passed to the debug decorator:

```python
def debug(msg=None):
    def actual_decorator(f):
        def wrapper(*args):
            if msg:
                print msg
            return f(*args)
        return wrapper
    if callable(msg):
        # debug decorator called without an argument so
        # msg is the function being decorated
        return debug()(msg)
    return actual_decorator

@debug
def mul(x, y):
    return x*y

mul(5, 2)
10

@debug("Let's multiply!")
def mul(x, y):
    return x*y

mul(5, 2)
Let's multiply!
10
```

