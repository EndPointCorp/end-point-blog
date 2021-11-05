---
author: Neil Elliott
title: 'Nvidia: Invalid or Corrupted Push Buffer Stream'
github_issue_number: 1116
tags:
- linux
- visionport
- hardware
date: 2015-04-20
---

As a high-performance video rendering appliance, the Liquid Galaxy requires really good video cards—​better than your typical on-board integrated video cards. Despite ongoing attempts by competitors to displace them, Nvidia remains the best choice for high-end video, if you use the proprietary Nvidia driver for Linux.

In addition to providing regular security and system updates, End Point typically provides advanced remote monitoring of our customers’ systems for issues such as unanticipated application behavior, driver issues, and hardware errors. One particularly persistent issue presents as an error with an Nvidia kernel module.  Unfortunately, relying on proprietary Nvidia drivers so as to maintain an acceptable performance level limits the available diagnostic information and options for resolution.

The issue presents when the system ceases all video output functions as Xorg crashes. The kernel log contains the following error message:

```plain
2015-04-14T19:59:00.000083+00:00 lg2 kernel: [  719.850677] NVRM: Xid (0000:01:00): 32, Channel ID 00000003 intr 02000000
```

The message is repeated approximately 11000 times every second until the disk fills and the ability to log in to the system is lost. The only known resolution at this time is to power-cycle the affected machine. In the error state, the module cannot be removed from the kernel, which also prevents Linux from shutting down properly. All affected systems were running some version of Ubuntu x86-64. The issue seems to be independent of driver version, but is at least present in 343.36 and 340.65, and affects all Geforce cards. Quadro cards seem unaffected.

The Xid message in the kernel log contains an error code that provides a little more information. The [Nvidia docs](http://docs.nvidia.com/deploy/xid-errors/) list the error as “Invalid or corrupted push buffer stream”. Possible causes listed include driver error, system memory corruption, bus error, thermal error, or frame buffer error. All affected systems were equipped with ECC RAM and were within normal operating temperature range when the issue presented.

Dealing with bugs like these can be arduous, but until they can be fixed, we cope by monitoring and responding to problems as quickly as possible.
