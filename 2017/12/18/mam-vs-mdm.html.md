---
author: "Joe Marrero"
title: "MAM vs MDM"
tags: mobile, android, ios, mam, mdm, airwatch, xenmobile, mobileiron
---

### MAM vs MDM

Businesses of all sizes are have been increasingly using mobile devices for all kinds of business activities.  Some of these activities are pretty common like
being able to read and respond to work email and manage work calenders.  While some companies are using mobile devices for more specific niche activities like
checking in customers, using device cameras to read barcodes and UPC stickers, or even temporarily storing sensitive business related data. As a result of the
proliferation of mobile devices for work, corporations and smaller businesses are finding the need the exhibit finer control over how their employees and customers
use their devices.  This is where mobile device management (MDM) and mobile application management (MAM) really shine and help solve many of these types of
problems.

#### What is MDM?

Mobile device management (MDM) is a software solution that allows organizations to manage the maintenance, deployment, and configuration of mobile devices that are
issued to members of the organization.  All of this magic tends to be done via a "store" or "portal" application that users download onto their devices.  The app begins
an enrollment process with the user's credentials that the organization issued to the user (usually the user's email and password). After the device is enrolled, the
user gets prompted to accept if the device should be managed as a "work" device.  After the enrollment completes, the store app can push VPN configuration, some
device level policies for enforcement, and any required applications.

Some of the useful things you can do with MDM:

* Install apps autonomously: Some corporations have their own suite of mobile applications that they require all employees to use. MDM allows
  organizations to push down required apps to devices.  When a newer app is available, the new app gets pushed down
  to devices automatically.
* Configuration: Push down sensitive or complex network configuration. Organizations can push down WiFi and VPN configuration.  This is especially useful for hidden network SSIDs.
* Policy Enforcement: Set global policies that can affect all or a portion of devices; Prevent third party apps from being installed.
* Auditing: See what devices do and access on your network.

#### What is MAM?

Mobile application management (MAM) is a technology that primarily focuses on enforcing policies on mobile applications.  To be able to have this finer level control
over applications, an organization needs to "wrap" the application.  Wrapping allows the injection of code into application despite not even having access to the
application's source code.  The injected code can then listen for events that are related to certain policies.  For example, if an application is not allowed to open
the camera application, then the injected code will listen for the corresponding events that will bring up the camera.  How this is done is different on Android and iOS
because the platforms do these kinds of things differently.

Some of the useful things you can do with MDM:
* Block certain applications from being able to handle certain types of data.
* Enforce file-system level encryption even if the application was never designed to use encryption.
* Detect if an application is running on a rooted device and kill the app if desired.
* Force an application to use a VPN all the time or when outside of the allowed networks.
* Block devices from accessing the Internet or the local loop-back addresses (i.e 127.0.0.1 or ::1)


#### What are some MAM and MDM vendors?

Here are some vendors of MAM and MDM solutions:

* [XenMobile](https://www.citrix.com/products/xenmobile/): This is a mature MAM/MDM solution; In addition to app-wrapping, Citrix also offers an SDK that allows organizations to build in MAM capabilities instead of wrapping.
* [Airwatch](https://www.air-watch.com): Another mature MAM/MDM solution.
* [MobileIron](https://www.mobileiron.com): A MDM solution.

#### Need Help?

Endpoint has tons of experience with MAM and MDM.  If your organization needs expert level consulting then we are always available to help you.
