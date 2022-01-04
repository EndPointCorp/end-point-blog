---
author: Zdeněk Maxa
title: Testing Django Applications
github_issue_number: 1181
tags:
- django
- jenkins
- python
- testing
- cms
- visionport
date: 2015-12-14
---

This post summarizes some observations and guidelines originating from introducing the [pytest](http://pytest.org/latest/) unit testing framework into our CMS (Content Management System) component of the [Liquid Galaxy](https://www.visionport.com/).
Our Django-based CMS allows users to define scenes, presentations and assets (StreetView, Earth tours, panos, etc) to be displayed on the
[Liquid Galaxy](https://www.youtube.com/watch?v=2VonXkA6YYg).

The purpose of this blog post is to capture my [Django](https://www.djangoproject.com/) and testing study points, summarize useful resource links as well as to itemize some guidelines for implementing tests for newcomers to the project. It also provides a comparison between Python’s standard [unittest library](https://docs.python.org/2/library/unittest.html) and the aforementioned pytest. Its focus is on Django database interaction.

### Versions of software packages used

This post describes some of our experiences at End Point in designing and working on comprehensive QA/CI facilities for a new system which is closely related to the Liquid Galaxy.

The experiments were done on Ubuntu Linux 14.04:

- python (2.7.6) and its corresponding version of unittest
- django 1.7 (current recent is 1.9 but our CMS uses still 1.7 version)
- [pytest-django 2.8.0](https://pytest-django.readthedocs.org/en/latest/)
- pytest 2.7.2 (with py 1.4.30)
- [virtualenv 13.1.2](https://pypi.python.org/pypi/virtualenv)
- [factory_boy 2.6.0](https://factoryboy.readthedocs.org/en/latest/)

### Testing Django Applications

We probably don’t need to talk much about the importance of testing. Writing tests along with the application code has become standard over the years. Surely, developers may fall into a trap of their own prejudice when creating testing conditions which would still result in faulty software but the likelihood of buggy software is certainly higher on a code that has no QA measures. If the code works and is untested, it means it works by accident, they say.

As a rule of thumb, unit tests should be very brief testing items seldom interacting with any external services such as the database. Integration tests on the other hand often communicate with external components.

This post will heavily reference an example minimal Django application written for the purpose of experimenting on
[Django testing](https://github.com/zdenekmaxa/examples/tree/master/python/django-testing).
Its README file contains some set up and requirement notes. Also, I am not going to list (m)any code snippets here but rather reference the functional application and its test suite. Hence the points below qualify for more or less assorted little topics or observations.

In order to benefit from this post, it will be helpful to follow the README and interact (run tests that is) with the demo django-testing application.

### Basic Django unittest versus pytest basic examples

This pair of test modules shows the differences between Django TestCase (unittest) and pytest-django (pytest) frameworks.

- [test_unittest_style.py](https://github.com/zdenekmaxa/examples/blob/master/python/django-testing/tests/test_unittest_style.py)

The base Django TestCase class derives along this tree:

```
    django.test.TestCase
        django.test.TransactionTestCase
            django.test.SimpleTestCase
                unittest.TestCase
```

Django adds (among any other aspects) handling of database, the documentation is
[here](https://docs.djangoproject.com/en/1.7/topics/testing/overview/), on top of the Python standard unittest library.

- [test_pytest_style.py](https://github.com/zdenekmaxa/examples/blob/master/python/django-testing/tests/test_pytest_style.py)

this is a pytest style implementation of the same tests and pytest-django plug-in adds, among other features, Django database handling support.

The advantage of unittest is that it comes with the Python installation—​it’s a standard library. That means that one does not have to install anything for writing tests, unlike pytest which is a third-party library and needs to be installed separately. While the absence of additional installation is certainly a plus, it’s dubious whether being a part of Python distribution is a benefit. I seem to recall Guido Van Rossum during Europython 2010 having said the the best thing for pytest is not being part of the Python standard set of libraries for its lively development and evolution would be slowed down by the inclusion.

There are very good talks and articles summarizing advantages of pytest. For me personally, the reporting of error
context is supreme. No boiler-plate (no inheritance), using plain Python asserts instead of
many [assert* methods](https://docs.python.org/2/library/unittest.html#assert-methods) and
flexibility (function, class) are other big plus points

- [Testing Django applications with py.test (EuroPython 2013)](https://speakerdeck.com/pelme/testing-django-applications-with-py-dot-test-europython-2013) (very good)
- [pytest presentation from its author](https://prezi.com/knnfwewm7lvw/pytest-rapid-multi-purpose-testing/)
- [very brief pytest introduction](http://www.pydanny.com/pytest-no-boilerplate-testing.html)
- [switch to pytest](http://mathieu.agopian.info/presentations/2015_06_djangocon_europe/), rich features descriptions, has some Django touches

As the comment in the **test_unittest_style.py** file says, this particular unittest-based test module can be run by both
Django **manage.py** (which boils down to unittest lookup discovery on a lower layer) or by **py.test** (pytest).

It should also be noted, that pytest’s flexibility can [bite back](http://stackoverflow.com/questions/21430900/py-test-skips-test-class-if-constructor-is-defined) if something gets overlooked.

### Django database interaction unittest versus pytest (advanced examples)

- [test_unittest_advanced.py](https://github.com/zdenekmaxa/examples/blob/master/python/django-testing/tests/test_unittest_advanced.py)

Since this post concentrates on pytest and since it’s the choice for our LG CMS project
(naturally :-), this unittest example just shows how the
**test (fresh) database** is determined and how Django migrations are run at each test suite execution. Just as described in
the [Django documentation](https://docs.djangoproject.com/en/1.7/topics/testing/overview/): “If your tests rely on database access such as creating or querying models, be sure to create your test classes as subclasses of django.test.TestCase rather than unittest.TestCase.”

That is true for database interaction but not completely true when using pytest. And “Using unittest.TestCase avoids the cost of running each test in a transaction and flushing the database, but if your tests interact with the database their behavior will vary based on the order that the test runner executes them. This can lead to unit tests that pass when run in isolation but fail when run in a suite.”
**django.test.TestCase**, however, ensures that each test runs inside a transaction to provide isolation.
The transaction is rolled back once the test case is over.




- [test_pytest_advanced.py](https://github.com/zdenekmaxa/examples/blob/master/python/django-testing/tests/test_pytest_advanced.py)

This file represents the actual core of the test experiments for this blog / demo app and shows various pytest features and approaches typical for this framework as well as Django (pytest-django that is) specifics.



### Django pytest notes (advanced example)

Much like the unittest documentation, the [pytest-django](https://pytest-django.readthedocs.org/en/latest/) recommends avoiding database interaction in unittest and concentrate only on the logic which should be designed in such a fashion that it can be tested without database.

- test database name prefixed “test_” (just like at the unittest example), the base value is taken from the database section of
the **settings.py**. As a matter of fact, it’s possible to run the test suite after previously dropping the main database,
the test suite interacts only with “test_” + DATABASE_NAME
- migration execution before any database interaction is carried out (similarly to unittest example)
- database interaction marked by a Python decorator **@pytest.mark.django_db** on the method or class level (or stand-alone function level). It’s in fact the **first** occurrence of this marker which triggers the database set up (its creation and migrations handling). Again analogously to unittest (django.test.TestCase), the test case is wrapped in a database transaction which puts the database back into the state prior to the test case. The database “test_” + DATABASE_NAME itself is dropped once the test suite run is over. The database is not dropped if **--db-reuse** option is used. The production DATABASE_NAME remains untouched during the test suite run (more about this below)
- **pytest_djangodb_only.py — setup_method** — run this module separately and the data created in setup_method end up **NOT** in the “test_” + DATABASE_NAME database but in the standard one (as configured in the **settings.py** which would be the production database likely)! Also this data won’t be rolled back. When run separately, this test module will pass (but still the production database would be tainted). It may or may not fail on the second and subsequent run depending whether it creates any unique data. When run within the test suite, the database call from the setup_method will fail despite the presence of the class django_db marker. This has been very important to realize.
Recommendation: do not include database interaction in the pytest special methods
(such assetup_method or teardown_method, etc), **only include database interaction in the test case methods**
- The error message `Failed: Database access not allowed, use the "django_db" mark to enable` was seen on a database error on a method which actually had the marker. This output is not to be 100% trusted
- data model **factories** are discussed separately below
- lastly the test module shows Django Client instance and calling an HTTP resource

### pytest setup_method

While the fundamental differences between unittest and pytest were discussed, there is something to be said about Django
specific differences of the two. There is different database-related behaviour of
**unittest setUp method** versus the **pytest setup_method method**. The setUp is included in the transaction and database interactions are rolled back once the test case is over. The setup_method is not included in the transaction. Moreover, interacting with the database from setup_method results in faulty behaviour and difference depending whether the test module is run on its own or as a part of the whole test suite.

The bottom line is: do not include database interaction in setup_method. This setUp, setup_method behaviour was already shown in the basic examples. And more description and demonstration of this behaviour is in the file: **pytest_djangodb_only.py**. This actually revealed the fact that using django_db database fixture is not supported in special pytest methods and the aforementioned error message is misleading (more references [here](https://github.com/pytest-dev/pytest-django/issues/297) and
[here](http://stackoverflow.com/questions/34089425/django-pytest-setup-method-database-issue)).

When running the whole test suite, this file won’t be collected (its name lacks “test_” string).
It needs to be renamed to be included in the test suite run.

### JSON data fixtures versus factories (pytest advanced example)

The traditional way of interacting with some test data was to perform following steps:

- have data loaded in the database
- python manage.py dumpdata
- the produced JSON file is dragged along the application test code
- **call_command("loaddata", fixture_json_file_name)** happens at each test suite run

The load is expensive, the JSON dump file is hard to maintain manually if the original modified copy and the current needs diverge (the file has integer primary keys value, etc). Although even the recent Django testing documentation mentions usage of JSON data fixtures, the approach is considered discouraged and the goal is recommended to achieve by means of loading the data in migrations or using model data factories.

[This talk](https://www.caktusgroup.com/blog/2013/07/17/factory-boy-alternative-django-testing-fixtures/) for example compares the both approaches in favour of [factory_boy library](https://factoryboy.readthedocs.org/en/latest/).
A quote from the article:
“Factory Boy is a Python port of a popular Ruby project called Factory Girl. It provides a declarative syntax for how new instances should be created. ... Using fixtures for complex data structures in your tests is fraught with peril. They are hard to maintain and they make your
tests slow. Creating model instances as they are needed is a cleaner way to write your tests which will make them faster and more maintainable.”

The file **test_pytest_advanced.py** demostrates interaction with factories defined in the module
**factories.py**, the basic very easy-to-use features.

Despite its ease of use, the factory_boy is a powerful library capable of modeling
[Django’s ORM many-to-many relationships](http://factoryboy.readthedocs.org/en/latest/recipes.html#many-to-many-relation-with-a-through), among other features.

### Additional useful links

- [Django 1.7 testing](https://docs.djangoproject.com/en/1.7/topics/testing/overview/) — version used in the demo application
- [Django 2.0 testing](https://docs.djangoproject.com/en/2.0/topics/testing/overview/) — latest stable version
- [Effective Django](http://www.effectivedjango.com/) — testing covered already in the second chapter of the book
- [Effective Django factory_boy](http://www.effectivedjango.com/orm.html#factoryboy-example)
- [Django testing](http://carljm.github.io/django-testing-slides) — excellent PyCon talk, slides covering pytest, fixtures vs factories, etc

### Conclusion

You should have a good idea about testing differences via unittest and pytest in the Django environment. The emphasis has been put on pytest (django-pytest) and some recommended approaches. The demo application django-testing brings functional test cases demonstrating the behaviour and features discussed. The articles and talks listed in this post were extremely helpful and instrumental in gaining expertise in the area and introducing rigorous testing approach into the production application.

Any discrepancy between the behaviour described above and on your own setup may originate from different software versions. In any case, if anything is not clear enough, please let me know in the comments.
