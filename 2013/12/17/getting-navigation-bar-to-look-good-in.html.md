---
author: Kamil Ciemniewski
gh_issue_number: 900
tags: ios
title: Getting navigation bar to look good in iOS7
---



Apple has recently released iOS 7 — a major upgrade to its operating system for mobile devices. Whether users like it or not — developers have to treat it seriously. There is nothing worse in the world of technology than being viewed as *passé*.

From the point of view of users, the new look and feel resembles somewhat the overall movement in the user interface design. The *[flat](http://fltdsgn.com/)* UI style is the new hotness nowadays.

On the developers' side of the fence though, this means lots of hard work. Apple has introduced lots of changes so that many iOS apps had to be changed and even redesigned to look acceptable in iOS 7.

### Some applications have already dropped support for older versions of iOS

One of them is... Evernote! Its team has decided that supporting older systems would be too costly and that they have decided to dump it. The only way to have the Evernote app is to have it installed before the release of its latest version.

### The troublesome navigation bar

One issue I encountered while working on an iOS app lately was that the app started to display oddly. The top bar was overlapping with the contents of the views.

The reason is because now the top bar overlaps with the UI underneath. It applies a blur on whatever there is behind, making apps look a bit more *integrated* with the OS.

### Solution hidden in the XIB designer

If you were using only the designer — you're very lucky. In the latest Xcode, there is an option to set *deltas* for UI element positions.

The UI delta is nothing more than a value that a particular measurement should be modified by if the app is being run on an iOS version lower than 7.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2013/12/17/getting-navigation-bar-to-look-good-in/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2013/12/17/getting-navigation-bar-to-look-good-in/image-0.png"/></a></div>

So keeping in mind that the top bar with the navigation view buttons area take 64 points of height — you have to provide -64 as **y** delta value. So that the UI in the designer looks great and it will also look nicely on a pre iOS 7 device.

### What about views consisting purely of code?

In my case, I had to resort to some workarounds in the code. Most views in the application I was working on were created dynamically. There were no *.xib files to edit with the editor, hence — no way to set those deltas.

The easiest solution I found was to just edit view's frame values. Making the **y** of the frame at 64 points.

```cpp
CGRect frame = tableViewController.view.frame;
frame.origin.y = 64;
tableViewController.view.frame = frame;
```

### Supporting older versions in code

The last step was to simulate the behavior of the designer and allow the code to apply changes based on the iOS system version on which the app is currently being executed:

```cpp
float topValue = 0;
if([[[UIDevice currentDevice] systemVersion] floatValue] >= 7.0f)
{
    topValue = 64;
}
CGRect frame = tableViewController.view.frame;
frame.origin.x = 0;
frame.origin.y = topValue;
tableViewController.view.frame = frame;
```

### More to read

[http://www.fastcolabs.com/3016423/open-company/developing-for-ios-7-the-good-the-bad-the-flat-and-the-ugly](http://www.fastcolabs.com/3016423/open-company/developing-for-ios-7-the-good-the-bad-the-flat-and-the-ugly)

[https://developer.apple.com/library/ios/documentation/userexperience/conceptual/transitionguide/Bars.html](https://developer.apple.com/library/ios/documentation/userexperience/conceptual/transitionguide/Bars.html)


