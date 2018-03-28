---
author: Miguel Alatorre
gh_issue_number: 897
tags: python
title: Python decorator basics
---



Python decorators have been around since 2005, when they were included in the release of Python 2.4.1. A decorator is nothing more than syntax for passing a function to another function, or wrapping functions. Best put, a decorator is a function that takes a function as an argument and returns either the same function or some new callable. For example,

```python
@foo
@bar
@baz
@qux
def f():
    pass
```

is shorthand for:

```python
def f():
    pass
f = foo(bar(baz(qux(f))))
```

Say we have some functions we are debugging by printing out debug comments:

```python
def mul(x, y):
    print __name__
    return x*y

def div(x, y):
    print __name__
    return x/y
```

The printing in the functions can be extracted out into a decorator like so:

```python
def debug(f):            # debug decorator takes function f as parameter
    msg = f.__name__     # debug message to print later
    def wrapper(*args):  # wrapper function takes function f's parameters
        print msg        # print debug message
        return f(*args)  # call to original function
    return wrapper       # return the wrapper function, without calling it
```

Our functions get decorated with:

```python
@debug
def mul(x, y):
    return x*y

@debug
def div(x, y):
    return x/y
```

Which again is just shorthand for:

```python
def mul(x, y):
    return x*y
mul = debug(mul)

def div(x, y):
    return x/y
div = debug(div)
```

Looking at the definition of the debug function we see that debug(mul) returns wrapper, which becomes the new mul. When we now call mul(5, 2) we are really calling wrapper(5, 2). But how do subsequent calls to wrapper have access to the initial f parameter passed to debug and to the msg variable defined in debug? Closures. Taken from aaronasterling’s response to [this](https://stackoverflow.com/questions/4020419/closures-in-python) stackoverflow question, “A closure occurs when a function has access to a local variable from an enclosing scope that has finished its execution.” You can read more about closures [here](https://www.learnpython.org/en/Closures), [here](http://ynniv.com/blog/2007/08/closures-in-python.html), and [here](https://www.protechtraining.com/content/python_fundamentals_tutorial-functional_programming). So, at the moment that mul is decorated, debug(mul) is executed returning wrapper, which has access to the original mul function and to the msg variable, which is then set as the new mul.

By decorating, we remove code duplication and if the need to ever change the debug logic arises, we only need to do so in one place. Now, decorators with (non-optional) arguments get a bit trickier, but only because the syntax is a bit hard to grasp at first sight. Say that we want to pass the debug message as a parameter to the decorator like so:

```python
@debug("Let's multiply!")
def mul(x, y)
    return x*y
```

Then the debug decorator would be:

```python
def debug(msg):
    def actual_decorator(f):    # from here to
        def wrapper(*args):     # ...
            print msg           # ...
            return f(*args)     # ...
        return wrapper          # here, looks just like our debug decorator from above!
    return actual_decorator
```

A decorator with arguments should return a function that takes a function as an argument and returns either the same function or some new callable (what a mouthful, eh?). In other words, a decorator with arguments returns a decorator without arguments.

Looking at what the decorator syntax is shorthand for we can follow along as debug gets executed:

```python
mul = debug("Let's multiply")(mul)
```

The debug function returns actual_decorator, to which we pass the mul function as the parameter, which then returns wrapper. So again, mul becomes wrapper which has access to msg and f because of closure.

What about decorators with optional arguments? That I’ll leave for a future blog post :)


