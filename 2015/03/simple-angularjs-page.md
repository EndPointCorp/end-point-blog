---
author: Szymon Lipiński
title: Simple AngularJS Page
github_issue_number: 1105
tags:
- angular
- javascript
date: 2015-03-24
---

The best thing in [AngularJS](https://angularjs.org/) is the great automation of actualizing the data in the HTML code.

To show how easy Angular is to use, I will create a very simple page using AngularJS and [Github](http://github.org/).

Every GitHub user can get lots of notifications. All of them can be seen at [GitHub notification page](https://github.com/notifications). There is also the GitHub API, which can be used for getting the notification information, using simple HTTP requests, which return JSON.

I wanted to create a simple page with a list of notifications. With information if the notification was read (I used “!!!” for unread ones). And with automatical refreshing every 10 minutes.

To access the GitHub API, first I generated an application token on the [GitHub token page](https://github.com/settings/applications). Then I downloaded a file from the AngularJS page, and a [GitHub API JavaScript wrapper](https://github.com/michael/github/).

Then I wrote a simple HTML file:

```html
<html>
  <head>
    <script src="angular.min.js"></script>
    <script src="underscore-min.js"></script>
    <script src="github.js"></script>
    <script src="jscode.js"></script>
  </head>

  <body ng-app="githubChecker">
    <div ng-controller="mainController">
      <h3>Github Notifications</h3>
      <div ng-repeat="n in notifications">
        <div>
          <span ng-show="n.unread">!!!</span> {{ n.subject.title }}
        </div>
      </div>
    </div>
  </body>
</html>
```

This is the basic structure. Now we need to have some Angular code to ask GitHub for the notifications and fill that into the above HTML.

The code is also not very complicated:

```javascript
var githubChecker = angular.module('githubChecker', []);

githubChecker.controller("mainController", ['$scope', '$interval', function($scope, $interval){

  $scope.notifications = [];

  var github = new Github({
    username: "USERNAME",
    token:    "TOKEN",
    auth:     "oauth"
  });
  var user = github.getUser();

  var getNotificationsList = function() {
    user.notifications(function(err, notifications) {
      $scope.notifications = notifications;
      $scope.$apply();
    });
  };

  getNotificationsList();

  $interval(getNotificationsList, 10*60*1000);

}]);
```

First of all I’ve created an Angular application object. That object has one controller, in which I created a GitHub object, which gives me a nice way to access the GitHub API.

The function getNotificationsList calls the GitHub API, gets a response, and just stores it in the `$scope.notifications` object.

Then Angular’s magic comes into play. When the `$scope` fields are updated, Angular automatically updates all the declarations in the HTML page. This time it is not so automatic, as I had to call the `$scope.$apply()` function to trigger it. It will loop through the `$scope.notifications` and update the HTML.

For more information about Angular, and the commands I used, you can check the [AngularJS Documentation](https://docs.angularjs.org/api).
