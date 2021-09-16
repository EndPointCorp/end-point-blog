---
author: Miguel Alatorre
title: Python Imports
github_issue_number: 1017
tags:
- python
date: 2014-07-24
---



For a Python project I’m working on, I wrote a parent class with multiple child classes, each of which made use of various modules that were imported in the parent class. A quick solution to making these modules available in the child classes would be to use wildcard imports in the child classes:

```python
from package.parent import *
```

however, [PEP8 warns against this](http://legacy.python.org/dev/peps/pep-0008/#imports) stating “they make it unclear which names are present in the namespace, confusing both readers and many automated tools.”

For example, suppose we have three files:

```python
# a.py
import module1
class A(object):
    def __init__():
        pass
```

```python
# b.py
import module2
class B(A):
    def __init__():
        super(B, self).__init__()
```

```python
# c.py
class C(B):
    def __init__():
        super(C, self).__init__()
```

To someone reading just b.py or c.py, it is unknown that module1 is present in the namespace of B and that both module1 and module2 are present in the namespace of C. So, following PEP8, I just explicitly imported any module needed in each child class. Because in my case there were many imports and because it seemed repetitive to have all those imports duplicated in each of the many child classes, I wanted to find out if there was a better solution. While I still don’t know if there is, I did go down the road of how imports work in Python, at least for 3.4.1, and will share my notes with you.

Python allows you to import modules using the import statement, the built-in function __import__(), and the function importlib.import_module(). The differences between these are:

The import statement first “searches for the named module, then it binds the results of that search to a name in the local scope” ([Python Documentation](https://docs.python.org/3/reference/import.html)). Example:

```bash
Python 3.4.1 (default, Jul 15 2014, 13:05:56) 
[GCC 4.8.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import re
>>> re
<module 're' from '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/re.py'>
>>> re.sub('s', '', 'bananas')
'banana'
```

Here the import statement searches for a module named **re** then binds the result to the variable named **re**. You can then call **re** module functions with **re.function_name()**.

A call to function __import__() performs the module search but not the binding; that is left to you. Example:

```bash
>>> muh_regex = __import__('re')
>>> muh_regex
<module 're' from '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/re.py'>
>>> muh_regex.sub('s', '', 'bananas')
'banana'
```

Your third option is to use importlib.import_module() which, like __import__(), only performs the search:

```bash
>>> import importlib
>>> muh_regex = importlib.import_module('re')
>>> muh_regex
<module 're' from '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/re.py'>
>>> muh_regex.sub('s', '', 'bananas')
'banana'
```

Let’s now talk about how Python searches for modules. The first place it looks is in sys.modules, which is a dictionary that caches previously imported modules:

```bash
>>> import sys
>>> 're' in sys.modules
False
>>> import re
>>> 're' in sys.modules
True
>>> sys.modules['re']
<module 're' from '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/re.py'>
```

If the module is not found in sys.modules Python searches sys.meta_path, which is a list that contains finder objects. Finders, along with loaders, are objects in Python’s import protocol. The job of a finder is to return a module spec, using method [find_spec()](https://docs.python.org/3/library/importlib.html#importlib.abc.MetaPathFinder.find_spec), containing the module’s import-related information which the loader then uses to load the actual module. Let’s see what I have in my sys.meta_path:

```bash
>>> sys.meta_path
[<class '_frozen_importlib.BuiltinImporter'>, <class '_frozen_importlib.FrozenImporter'>, <class '_frozen_importlib.PathFinder'>]
```

Python will use each finder object in sys.meta_path until the module is found and will raise an ImportError if it is not found. Let’s call find_spec() with parameter ‘re’ on each of these finder objects:

```bash
>>> sys.meta_path[0].find_spec('re')
>>> sys.meta_path[1].find_spec('re')
>>> sys.meta_path[2].find_spec('re')
ModuleSpec(name='re', loader=<_frozen_importlib.SourceFileLoader object at 0x7ff7eb314438>, origin='/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/re.py')
```

The first finder knows how to find built-in modules and since **re** is not a built-in module, it returns None.

```bash
>>> 're' in sys.builtin_module_names
False
```

The second finder knows how to find frozen modules, which **re** is not. The third knows how to find modules from a list of path entries called an import path. For **re** the import path is sys.path but for subpackages the import path can be the parent’s __path__ attribute.

```bash
>>>sys.path
['', '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/site-packages/distribute-0.6.49-py3.4.egg', '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib', '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python34.zip', '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4', '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/plat-linux', '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/lib-dynload', '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/site-packages', '/home/miguel/.pythonbrew/pythons/Python-3.4.1/lib/python3.4/site-packages/setuptools-0.6c11-py3.4.egg-info']
```

Once the module spec is found, the loading machinery takes over. That’s as far as I dug but you can read more about the loading process by reading the [documentation](https://docs.python.org/3/reference/import.html#loading).


