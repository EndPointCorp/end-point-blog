---
author: Marina Lohova
gh_issue_number: 1070
tags: angular, css, design, html, javascript
title: Angular Responsive Layout Directive
---



To all of you window.onResize aficionados, I dedicate this blog post because today we will be doing a lot of dynamic resizing in JavaScript. All of it will be done completely and effortlessly with my one-page long Angular directive.

Why do I need to attach an expensive onResize handler to my already overloaded page, you ask. The answer is very simple. Our app layout is pixel-perfect. Each element has the predefined width and margins. Yet, the app needs to look good on all kind of devices, from regular PC to tablet to iPhone. That's why I created the following Angular directive in /scripts/directives/tsResize.js:

```javascript
angular.module('angularApp')
.directive('tsResize', function($window) {
 return function(scope, element) {
   var w = angular.element($window);
   scope.getWindowDimensions = function () {
     return {
       'h': $window.innerHeight,
       'w': $window.innerWidth
     };
   };
   scope.$watch(scope.getWindowDimensions,
              function (newValue, oldValue) {
     scope.windowHeight = newValue.h;
     scope.windowWidth = newValue.w;

     scope.mainContainerStyle = function () {
       if (newValue.w > 890) {
         return {};
       } else {
         val = newValue.w/890;
         return {
           '-webkit-transform': 'scale(' + val + ')',
           '-o-transform': 'scale(' + val + ')',
           '-ms-transform': 'scale(' + val + ')',
           'transform': 'scale(' + val + ')',
           'transform-origin': 'left -10px',
           '-webkit-transform-origin': 'left -10px'
         };
       }
     };

     scope.topBarStyle = function () {
       if (newValue.w > 890) {
         return {};
       } else {
         val = newValue.w/890;
         return {
           '-webkit-transform': 'scale(' + val + ')',
           '-o-transform': 'scale(' + val + ')',
           '-ms-transform': 'scale(' + val + ')',
           'transform': 'scale(' + val + ')',
           'transform-origin': '0 2px 0',
           '-webkit-transform-origin': '0 2px 0'
         };
       }
     };
    }, true);

   w.bind('resize', function () {
     scope.$apply();
   });
  }
})
```

As you can see all the magic is done with transform:scale CSS attribute on the two of my main page components: the navigation and the contents container.

They styles are cross-browser.

```javascript
return {
  '-webkit-transform': 'scale(' + val + ')',
  '-o-transform': 'scale(' + val + ')',
  '-ms-transform': 'scale(' + val + ')',
  'transform': 'scale(' + val + ')'
};
```

It's important to set transform-origin, or the elements will be weirdly positioned on the page.

```javascript
return {
  'transform-origin': '0 top',
  '-webkit-transform-origin': '0 top'
};
```

The style calculations are attached to the changes of window dimensions.

```javascript
scope.getWindowDimensions = function () {
  return {
    'h': $window.innerHeight,
    'w': $window.innerWidth
  };
};
scope.$watch(scope.getWindowDimensions,
             function (newValue, oldValue) {
...
});
```

Few other things. My layout was sliced to the fixed width of 890px, that's why I took 890 as the pivotal point of my scale ratio formula. You should take the default width of the layout as the base of your calculation.

```javascript
if (newValue.w > 890) {
  return {};
} else {
  val = newValue.w/890;
  return {
    '-webkit-transform': 'scale(' + val + ')',
  }
});

```

With the directive in place it's time to plug it in:

```html
<script src="scripts/directives/tsResize.js"></script>
  <nav ng-style="topBarStyle()" ts-resize=""></nav>
  <div ng-style="mainContainerStyle()" ng-view="" ts-resize=""></div>
```

Be sure to use style "display:block" or "display:inline-block" and "position:relative" for all the inside components of the scaled elements with the default display. Otherwise they do not obey the scaling enforcement and grow way too long prompting a scrollbar.

```html
<div id="main-container"><div id="inner-block" style="position:relative; display:inline-block"></div></div>
```

It all worked nicely and I was able to enjoy the smoothly resizing layout.


