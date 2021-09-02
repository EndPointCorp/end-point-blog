---
author: Greg Davidson
title: Mobile Emulation in Chrome DevTools
github_issue_number: 917
tags:
- browsers
- design
- environment
- html
- javascript
- tips
- tools
date: 2014-01-24
---



I have been doing some mobile development lately and wanted to share the new Mobile Emulation feature in Chrome Canary with y’all. [Chrome Canary](https://www.google.ca/intl/en/chrome/browser/canary.html) is a development build of Chrome which gets updated daily and gives you the chance to use the latest and greatest features in Chrome. I’ve been using it as my primary browser for the past year or so and it’s been fairly stable. What’s great is that you can run Chrome Canary side-by-side with the stable release version of Chrome. For the odd time I do have issues with stability etc., I can just use the latest stable Chrome and be on my way. If you need more convincing, Paul Irish’s [Chrome Canary for Developers](http://www.paulirish.com/2012/chrome-canary-for-developers/) post might be helpful.

I should mention that Chrome Canary is only available for OS X and Windows at this point. I tested [Dev channel Chromium](http://www.chromium.org/getting-involved/dev-channel#TOC-Linux) on Ubuntu 13.10 this afternoon and the new mobile emulation stuff is not ready there yet. It should not be long though.

 

### Mobile Emulation in Chrome Dev Tools

<img alt="Mobile emulation chrome canary" border="0" height="334" src="/blog/2014/01/mobile-emulation-in-chrome-devtools/image-0.png" title="mobile-emulation-chrome-canary.png" width="559"/> 

Once enabled, the Emulation panel shows up in the Dev Tools console drawer. It gives you the option of emulating a variety devices (many are listed in the drop-down) and you also have the ability to fine tuning the settings à la carte. If you choose to emulate the touchscreen interface the mouse cursor will change and operate like a touch interface. Shift+drag allows you to pinch and zoom. There are some cool features for debugging and inspecting touch events as well.

### Learning More

If you would like to learn more, be sure to check out the [Mobile emulation documentation](https://developers.google.com/chrome-developer-tools/docs/mobile-emulation) at the Chrome DevTools docs site.


