---
author: Joe Marrero
title: Mobile Device and Application Management (MAM vs. MDM)
github_issue_number: 1357
tags:
- mobile
- android
- ios
- security
date: 2017-12-20
---

Businesses of all sizes have been increasingly using mobile devices for all kinds of activities. Some of these activities are pretty common, like being able to read and respond to work email and manage work calendars. On the other hand, some companies are using mobile devices for more specific niche activities like checking in customers, using device cameras to read barcodes and UPC stickers, or even temporarily storing sensitive business related data.

As a result of the proliferation of mobile devices for work use, corporations and smaller businesses are finding the need the exhibit finer control over how their employees and customers use their devices. This is where mobile device management (MDM) and mobile application management (MAM) really shine and help solve many of these types of problems.

### What is MDM?

Mobile device management (MDM) is a software solution that allows organizations to manage the maintenance, deployment, and configuration of mobile devices that are issued to members of the organization. All of this magic tends to be done via a _store_ or _portal_ application that users download onto their devices.

The app begins an enrollment process when the user enters their credentials that the organization previously issued to the user (usually the user’s email and password). After the device is enrolled, the user gets prompted to accept if the device should be managed as a _work_ device. After the enrollment completes, the store app can push configuration, some device level policies for enforcement, and any required applications.

Some of the useful things you can do with MDM:

* **Install apps autonomously:** Some corporations have their own suite of mobile applications that they require all employees to use. MDM allows organizations to push down required apps to a device. When a newer app is available, the new app gets pushed down to devices automatically. This makes it easier to deploy apps to all employees and ensure users have the latest apps on their devices.
* **Configuration:** Push down sensitive or complex network configuration. Organizations can push down WiFi and VPN configurations. This is especially useful for allowing users to connect to work networks that have hidden SSIDs. You can also enforce use of PIN, and other security features.
* **Policy Enforcement:** Set global policies that can affect all or a portion of devices; Prevent third party apps from being installed.
* **Auditing:** See what devices have done, what versions of apps are deployed, and how a device has used your network.
* **Scale up:** MDM scales up nicely for thousands of devices. If you find yourself updating devices one at time then you definitely need an MDM solution.

### What is MAM?

Mobile application management (MAM) is a technology that primarily focuses on enforcing policies on mobile applications. To be able to have this finer level control over applications, an organization needs to _wrap_ the application.

Wrapping is the process of injecting code into an application despite not even having access to the application’s source code. The injected code can then listen for events that are related to certain policies. For example, if an application is not allowed to open the camera application, then the injected code will listen for the corresponding events that will bring up the camera.

How this is done is different on Android and iOS because the platforms handle these kinds things quite differently.

Some of the useful things you can do with MDM:

* Block certain applications from being able to handle certain types of data.
* Enforce filesystem level encryption even if the application was never designed to use encryption.
* Detect if an application is running on a rooted device and kill the app if desired.
* Force an application to use a VPN all the time or when outside of the allowed networks.
* Block devices from accessing the Internet or the local loop-back addresses (i.e. 127.0.0.1 or ::1).

### What are some MAM and MDM vendors?

Some of the major vendors of MAM and MDM solutions are:

* [XenMobile](https://www.citrix.com/products/xenmobile/)
* [AirWatch](https://www.air-watch.com)
* [MobileIron](https://www.mobileiron.com)

XenMobile and AirWatch are robust and mature MAM and MDM solutions. With respect to features, both offer single-sign on (SSO), a suite of productivity apps (email, browser, etc.), and mobile content management.

XenMobile’s email client is similar in capabilities to AirWatch’s email client. However, AirWatch also allows management of the native email clients on Android and iOS which tends to be buggier. Furthermore, AirWatch’s productivity apps may require additional VMware product licenses to unlock some of these capabilities.

In terms of the administration web app, XenMobile is a bit more complicated than AirWatch and may require a few tech support calls to get configured just right. Both products require mobile apps to be _wrapped_ with a _wrapping utility_ before they can be uploaded to the management console. And both offer SDKs that allow organizations to build apps that have MAM capabilities without needing to be wrapped.

Also, both products have great VPN capabilities. If your organization is already using Netscaler than it might make more sense to use XenMobile. Netscaler appears to be more feature-rich compared to VMware Tunnel, but Netscaler is also very hard to configure. With respect to price, AirWatch tends to be cheaper for smaller organizations than XenMobile because XenMobile offers fixed price tiers where as AirWatch has a per-device pricing model.

MobileIron is a bit less developed than XenMobile and AirWatch. However, this also makes it a bit more simpler and easier to administrate. In addition, MobileIron lacks a managed email application compared to XenMobile and AirWatch.

### Need Help?

End Point has tons of experience with MAM and MDM. If your organization needs expert-level consulting then we are available to help you!
