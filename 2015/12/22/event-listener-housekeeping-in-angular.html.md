---
author: Greg Davidson
gh_issue_number: 1184
tags: html, javascript
title: Event Listener Housekeeping in Angular Apps
---



I was recently debugging an issue where a large number of errors suddenly cropped up in an [angular](https://angularjs.org/) application. The client reported that the majority of the errors were occurring on the product wall which was an area of application I was responsible for. After some sleuthing and debugging I determined the culprit was a scroll event listener in an unrelated angular controller. When customers viewed this section of the application, the scroll listener was added to manage the visibility of some navigation elements. However, when the customer moved on to other sections of the site the listener continued to fire in a context it was not expecting.

Scroll event listeners fire very often so this explained the sheer volume of errors. The product wall is a tall section of the site with lots of content so this explained why the bulk of the errors were happening there. The solution was to simply listen to the [$destroy event](https://docs.angularjs.org/api/ng/type/$rootScope.Scope#$destroy) in the controller and unbind the troublesome scroll listener: 

```javascript
$scope.$on('$destroy', function() {
  $window.unbind('scroll');
});
```

Single page apps do not have the benefit of getting a clean state with each page load. Because of this it’s important to keep track of any listeners that are added—​especially those that are outside of angular (e.g. window and document) and make sure to clean those up when the related controllers and directives are destroyed. 


