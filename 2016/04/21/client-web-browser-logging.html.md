---
author: Piotr Hankiewicz
gh_issue_number: 1221
tags: angular, javascript
title: Client web browser logging
---

### Introduction

The current state of development for web browsers is still problematic. We have multiple browsers, each browser has plenty of versions. There are multiple operating systems and devices that can be used. All of this makes it impossible to be sure that our code will work on every possible browser and system (unfortunately). With proper testing, we can make our product stable and good enough for production, but we can’t expect that everything will go smoothly, well, it won’t. He is always somewhere, a guy sitting in his small office and using outdated software, Internet Explorer 6 for example. Usually you want to try to support as many as possible users, here, I will explain how to help find them. Then you just need to decide if it is worth fixing an issue for them.

### Browser errors logging

What can really help us and is really simple to do is browser error logging. Every time an error occurs on the client side (browser will generate an error that the user most likely won’t see), we can log this error on the server side, even with a stack trace. Let’s see an example:

```javascript
window.onerror = function (errorMsg, url, lineNumber, column, errorObj) {
    $.post('//your.domain/client-logs', function () {
        errorMsg: errorMsg,
        url: url,
        lineNumber: lineNumber,
        column: column,
        errorObj: errorObj
    });

    // Tell browser to run its own error handler as well
    return false;
};
```

What do we have here? We bind a function to the window.onerror event. Every time an error occurs this function will be called. Some arguments are passed together:

- errorMsg — this is an error message, usually describing why an error occurred (for example: "Uncaught ReferenceError: heyyou is not defined"),
- url — current url location,
- lineNumber — script line number where an error happened,
- column — the same as above but about column,
- errorObj — the most important part here, an error object with a stack trace included.

What to do with this data? You will probably want to send it to a server and save it, to be able to go through this log from time to time like we do in our example:

```javascript
$.post('//your.domain/client-logs', function () {
    errorMsg: errorMsg,
    url: url,
    lineNumber: lineNumber,
    column: column,
    errorObj: errorObj
});
```

It’s very helpful, usually with proper unit and functional testing errors generated are minor, but sometimes you may find a critical issue before a bigger number of clients will actually discover it. It is a big profit.

### JSNLog

JSNLog is a library that helps with client error logging. You can find it here: http://jsnlog.com/. I can fully recommend using this one, it can also do the AJAX calls, timeout handling, and many more.

### Client error notification

If you want to be serious and professional every issue should be reported to a user in some way. On the other side, it’s sometimes dangerous to do if the user will be spammed with information that an error occurred because of some minor error. It’s not easy to find the best solution because it’s not easy to identify an error priority.

Just from experience, if you have a system where users are logged on, you can create a simple script that will send an email to a user with a question regarding an issue. You can set up a limit value to avoid sending too many messages. If the user will be interested he can always reply and explain an issue. Usually the user will appreciate this interest.

### Errors logging in Angular

It’s worth mentioning how we can handle error logging in the Angular framework, with useful stack traces and error descriptions. See an example below:

First we need to override default log functions in Angular:

```javascript
angular.module('logToServer', [])
  .service('$log', function () {
    this.log = function (msg) {
      JL('Angular').trace(msg);
    };
    this.debug = function (msg) {
      JL('Angular').debug(msg);
    };
    this.info = function (msg) {
      JL('Angular').info(msg);
    };
    this.warn = function (msg) {
      JL('Angular').warn(msg);
    };
    this.error = function (msg) {
      JL('Angular').error(msg);
    };
  });
```

Then override exception handler to use our function:

```javascript
factory('$exceptionHandler', function () {
    return function (exception, cause) {
      JL('Angular').fatalException(cause, exception);
      throw exception;
    };
  });
```

We also need an interceptor to handle AJAX call errors. This time we need to override $q object like this:

```javascript
factory('logToServerInterceptor', ['$q', function ($q) {
    var myInterceptor = {
      'request': function (config) {
          config.msBeforeAjaxCall = new Date().getTime();

          return config;
      },
      'response': function (response) {
        if (response.config.warningAfter) {
          var msAfterAjaxCall = new Date().getTime();
          var timeTakenInMs = msAfterAjaxCall - response.config.msBeforeAjaxCall;

          if (timeTakenInMs > response.config.warningAfter) {
            JL('Angular.Ajax').warn({
              timeTakenInMs: timeTakenInMs,
              config: response.config,
              data: response.data
            });
          }
        }

        return response;
      },
      'responseError': function (rejection) {
        var errorMessage = "timeout";
        if (rejection && rejection.status && rejection.data) {
          errorMessage = rejection.data.ExceptionMessage;
        }
        JL('Angular.Ajax').fatalException({
          errorMessage: errorMessage,
          status: rejection.status,
          config: rejection.config }, rejection.data);

          return $q.reject(rejection);
      }
    };

    return myInterceptor;
  }]);
```

How it looks all together:

```javascript
angular.module('logToServer', [])
  .service('$log', function () {
    this.log = function (msg) {
      JL('Angular').trace(msg);
    };
    this.debug = function (msg) {
      JL('Angular').debug(msg);
    };
    this.info = function (msg) {
      JL('Angular').info(msg);
    };
    this.warn = function (msg) {
      JL('Angular').warn(msg);
    };
    this.error = function (msg) {
      JL('Angular').error(msg);
    };
  })
  .factory('$exceptionHandler', function () {
    return function (exception, cause) {
      JL('Angular').fatalException(cause, exception);
      throw exception;
    };
  })
  .factory('logToServerInterceptor', ['$q', function ($q) {
    var myInterceptor = {
      'request': function (config) {
          config.msBeforeAjaxCall = new Date().getTime();

          return config;
      },
      'response': function (response) {
        if (response.config.warningAfter) {
          var msAfterAjaxCall = new Date().getTime();
          var timeTakenInMs = msAfterAjaxCall - response.config.msBeforeAjaxCall;

          if (timeTakenInMs > response.config.warningAfter) {
            JL('Angular.Ajax').warn({
              timeTakenInMs: timeTakenInMs,
              config: response.config,
              data: response.data
            });
          }
        }

        return response;
      },
      'responseError': function (rejection) {
        var errorMessage = "timeout";
        if (rejection && rejection.status && rejection.data) {
          errorMessage = rejection.data.ExceptionMessage;
        }
        JL('Angular.Ajax').fatalException({
          errorMessage: errorMessage,
          status: rejection.status,
          config: rejection.config }, rejection.data);

          return $q.reject(rejection);
      }
    };

    return myInterceptor;
  }]);
```

This should handle most of the errors that could happen in the Angular framework. Here I used the JSNLog library to handle sending logs to a server.

### Almost the end

There are multiple techniques for logging errors on a client side. It does not really matter which one you choose, it only matters that you do it. Especially when it’s really a little amount of time to invest and make it work and a big profit in the end.
