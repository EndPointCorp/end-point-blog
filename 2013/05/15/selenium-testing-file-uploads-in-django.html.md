---
author: Adam Vollrath
gh_issue_number: 800
tags: django, testing
title: Selenium Testing File Uploads in Django Admin
---

The Django framework version 1.4 [added much better integration with Selenium](https://docs.djangoproject.com/en/dev/releases/1.4/#support-for-in-browser-testing-frameworks) for in-browser functional testing.  This made [Test-Driven Development](http://www.tdd-django-tutorial.com/) an even more obvious decision for our new [Liquid Galaxy Content Management System](http://code.google.com/p/liquid-galaxy/source/browse?repo=lg-cms).  This went very well until we needed to test file uploads in the Django admin interface.

A browser's file upload control has some [unique security concerns](http://my.opera.com/community/forums/findpost.pl?id=6604472) that [prevent JavaScript from setting its value](http://stackoverflow.com/questions/1696877/how-to-set-a-value-to-a-file-input-in-html).  Trying to do so may raise INVALID_STATE_ERR: DOM Exception 11.  Selenium's WebDriver may sometimes [send keystrokes directly into the input element](http://stackoverflow.com/a/10472542), but this did not work for me within Django's admin interface.

To work around this limitation, [Ryan Kelly developed a Middleware to emulate successful file uploads for automated testing](http://www.rfk.id.au/blog/entry/testing-file-uploads-in-django/).  This middleware inserts additional hidden fields into any forms sent to the client.  Setting their value causes a file upload to happen locally on the server.  (I used [a slightly newer version of this Middleware](https://bitbucket.org/proppy/playground/src/8f914e92a551/server/playground_editor/middleware.py) from [another project](http://playground.mekensleep.com/).)

However, [Selenium intentionally will not interact with hidden elements](http://code.google.com/p/selenium/wiki/FrequentlyAskedQuestions#Q:_Why_is_it_not_possible_to_interact_with_hidden_elements?).  To work around this, we must send JavaScript to be executed directly in the browser using [WebDriver's execute_script method](http://docs.seleniumhq.org/docs/03_webdriver.jsp#using-javascript).  You can see [an example of this here](http://code.google.com/p/liquid-galaxy/source/browse/lg_cms/functional_tests/tests.py?repo=lg-cms&r=cbbe777733f6734943e73e0dbd9d56b7f6b3f81b#181).

```python
        self.browser.execute_script("document.getElementsByName('fakefile_storage')[0].value='placemark_end_point.kml'")
```

This is a lot of hoops to jump through, but now we have functional tests for file uploads and their post-upload processing.  Hopefully the Selenium or Django projects can develop a better-supported method for file upload testing.
