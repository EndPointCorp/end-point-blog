---
author: Szymon Lipiński
title: Dictionary Comprehensions in Python
github_issue_number: 968
tags:
- python
date: 2014-04-23
---

Python has many features which usually stay unknown to many programmers.

### List Comprehensions

List comprehensions are much simpler way of creating lists. This is one feature which is rather widely used and I saw this in many examples and source of many libraries.

Imagine you have a function which returns a list of data. A good example of this is xrange(start, end) function which returns all numbers within the range [start, end), so it excludes the end. This is a generator, so it doesn’t return all numbers at once, but you need to call this function many times, and each time it returns the next number.

Getting all numbers from range [1, 10] using this function can be done like this:

```python
numbers = []
for i in xrange(1, 10):
    numbers.append(i)
```

If you want to get only the even numbers, then you can write:

```python
numbers = []
for i in xrange(1, 11):
    if i % 2 == 0:
      numbers.append(i)
```

List comprehensions can make the code much simpler.

The whole expression evalutes to a list, and the main syntax is:

```python
[ expression for item in list if conditional ]
```

The first example can be then written as:

```python
numbers = [i for i in xrange(1, 11)]
```

and the second:

```python
numbers = [i for i in xrange(1, 11) if i % 2 == 0]
```

Of course this syntax can be a little bit strange at the very first moment, but you can get used to it, and then the code can be much easier.

### Removing Duplicates

Another common usage of collections is to remove duplicates. And again there are plenty of ways to do it.

Consider a collection like this:

```python
numbers = [i for i in xrange(1,11)] + [i for i in xrange(1,6)]
```

The most complicated way of removing duplicates I’ve ever seen was:

```python
unique_numbers = []
for n in numbers:
    if n not in unique_numbers:
        unique_numbers.append(n)
```

Of course it works, but there is another much easier way, you can use a standard type like set. Set cannot have duplicates, so when converting a list to set, all duplicates are removed. However at the end there will be set, not list, if you want to have list, then you should convert it again:

```python
unique_numbers = list(set(numbers))
```

### Removing Object Duplicates

With objects, or dictionaries, the situation is a little bit different. You can have a list of dictionaries, where you use just one field for identity, this can look like:

```python
data = [
  {'id': 10, 'data': '...'},
  {'id': 11, 'data': '...'},
  {'id': 12, 'data': '...'},
  {'id': 10, 'data': '...'},
  {'id': 11, 'data': '...'},
]
```

Removing duplicates, again, can be done using more or less code. Less is better, of course. With more code it can be:

```python
unique_data = []
for d in data:
    data_exists = False
    for ud in unique_data:
        if ud['id'] == d['id']:
          data_exists = True
          break
    if not data_exists:
        unique_data.append(d)
```

And this can be done using a thing I discoverd a couple of days ago, this is dictionary comprehension. It has a similar syntax as list comprehension, however evaluates to dicionary:

```python
{ key:value for item in list if conditional }
```

This can be used to make a list without all duplicates using a custom field:

```python
{ d['id']:d for d in data }.values()
```

The above code creates a dictionary with key, which is the field I want to use for uniqueness, and the whole dictionary as value. The dictionary then contains only one entry for each key. The values() function is used to get only values, as I don’t need the key:value mappings any more.
