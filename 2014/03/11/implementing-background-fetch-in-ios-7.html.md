---
author: Kamil Ciemniewski
gh_issue_number: 941
tags: ios
title: Implementing Background Fetch in iOS 7
---



With the iOS7 being out and gaining market share, great features it introduced are becoming available to more and more users.

One such new feature is a set of so-called "background modes".

## States the application can be in, in iOS

To explain this new set of modes, let me give you a really quick intro to what *modes* are. 

In iOS, at a given point in time, an app can be in one of the following states:

### Not running

There is no process for the app in the system.

### Inactive

The app is running in the foreground but currently is not receiving any events. (It may be executing other code though.) An app usually stays in this state only briefly as it transitions to a different state.

### Active

The application is running and is receiving user input. The main user interface is visible on the display.

### Background

The application is running. It's not receiving user input. Its code is being executed but it will be switched to the *suspended* state very soon by the system.

### Suspended

The app remains in memory, but it's not being executed. It remains dormant until a user chooses to activate it again **or a system switches it back to a background state to allow it to process certain kinds of data**.

## Background modes

The last paragraph described *certain kinds of data* an app may want to process even if it's not a receiver of user's actions.

This makes sense - there are apps that use GPS or audio system even when they aren't active. In fact those along with the VOIP were one of scenarios iOS creators designated as special in the previous versions of the system.

Inactive applications were allowed to run certain parts of their code in response to GPS or VOIP events. They were also allowed to play or record audio content. 

Those scenarios are what are called *background modes*. This just refers to situations under which iOS brings an app from the *suspended* state to *background*, to allow it to run its code.

Other background modes available in pre iOS 7 systems are:

- Newsstand downloads
- External accessory communication
- Bluetooth networking
- Bluetooth data sharing

## New background modes in iOS 7

With the newest version of the system, Apple introduced two new modes:

- Background fetch
- Remote notifications

The first one allows apps to periodically access web servers to download data. The second one allows apps to create notifications for users that some new content can be downloaded.

## A little bit about the use case I was working on

I was implementing the *background fetch mode* recently in the iOS application for the Locate Express platform. The platform allows its users to search in real time for service providers when they need e. g. to repair something at their homes.

One of the business rules in the system is that providers who are not actively using the application to make themselves available for searches - are marked as *pending*, which effectively excludes them from the results. The problem with this logic was that the client app would stop talking to the Locate Express system as soon as it entered the *suspended* state. The remedy for this was using the *location updates* background mode. The problem with this in turn was that iOS devices would quickly run out of battery. The *location updates* mode can be configured to report small changes, but it can also be configured only to report *significant* ones. Given that many service providers *do not* change their location *significantly* while they are at work - we were in need of a different solution.

The app itself, receives information about so called service requests from the web based portal located at: [www.locateexpress.com](http://www.locateexpress.com/). The natural path then was to use the new *background fetch* mode to improve user's experience by periodically synchronizing the list of requests. This allowed us to:

- present always up-to-date list of requests even when a user did not access the app from the remote notification that was bringing the information about any new request
- avoid any *waiting* time for the list of requests to refresh
- mark a provider as active frequently, without draining the battery

## The background fetch mode setup

Like any other background mode, you have to make few steps first to make the app able to use it. 

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/03/11/implementing-background-fetch-in-ios-7/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/03/11/implementing-background-fetch-in-ios-7/image-0.png"/></a></div>

1. In Xcode, Go to your project's settings by clicking on it and then accessing the "Capabilities" pane
1. Turn "Background Modes" on if it's not already
1. Check the "Background fetch" checkbox

## How frequently will the fetch be executed?

You can control this frequency only to *some* extent. In fact, to be able to fetch any data you still have to run the following code, some time when initializing your AppDelegate:

```c
[[UIApplication sharedApplication] setMinimumBackgroundFetchInterval:UIApplicationBackgroundFetchIntervalMinimum];
```

This sets the value telling iOS the *minimum* interval in which you want it to run the background fetch code. There is no *maximum* hint though. It means that you can tell iOS not to run the fetch more frequent than some time span. You cannot tell it to run not rarely than some other value.

The frequency is managed by iOS. You give it a hint with the above snippet of code and returning information if you were able to get any new data with the current fetch. Based on that in part - it is able to compute the most optimal (from its own stand point) frequency value.

## Implementing the fetching method

Last step is to implement the following method in your AppDelegate:

```c
(void) application:(UIApplication *)application performFetchWithCompletionHandler:(void (^)(UIBackgroundFetchResult))completionHandler
{
  NSLog(@"Background Fetch!");
  // fetching the data here ...
  if(failedFetch) { // use your own flag here
    completionHandler(UIBackgroundFetchResultFailed);
  }
  else {
    if(newDataFetched) { // use your own flag here
    completionHandler(UIBackgroundFetchResultNewData);
  }
  else {
    completionHandler(UIBackgroundFetchResultNoData);
  }
}
```

## More to read

- [Application states in iOS](https://developer.apple.com/library/ios/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/ManagingYourApplicationsFlow/ManagingYourApplicationsFlow.html)
- [What is new in iOS 7](https://developer.apple.com/library/ios/releasenotes/General/WhatsNewIniOS/Articles/iOS7.html)


