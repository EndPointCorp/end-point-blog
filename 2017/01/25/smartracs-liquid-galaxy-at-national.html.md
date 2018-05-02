---
author: Ben Witten
gh_issue_number: 1285
tags: cesium, conference, event, liquid-galaxy, unity
title: Smartrac’s Liquid Galaxy at National Retail Federation
---

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/01/25/smartracs-liquid-galaxy-at-national/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" height="300" src="/blog/2017/01/25/smartracs-liquid-galaxy-at-national/image-0.jpeg" width="400"/></a></div>

Last week, Smartrac exhibited at the retail industry’s BIG Show, [NRF 2017](https://nrfbigshow.nrf.com/), using a [Liquid Galaxy](https://liquidgalaxy.endpoint.com/) with custom animations to showcase their technology.

[Smartrac](https://www.smartrac-group.com/) provides data analytics to retail chains by tracking physical goods with NFC and Bluetooth tags that combine to track goods all the way from the factory to the distribution center to  retail stores.  It’s a complex but complete solution.  How best to visualize all that data and show the incredible value that Smartrac brings?  Seven screens with real time maps in Cesium, 3D store models in Unity, and browser-based dashboards, of course. End Point has been working with Smartrac for a number of years as a development resource on their SmartCosmos platform, helping them with UX and back-end database interfaces. This work included development of REST-based APIs for data handling, as well as a Virtual Reality project utilizing the Unity game engine to visualize data and marketing materials directly on several platforms including the Oculus Rift, the Samsung Gear 7 VR, and WebGL.  Bringing that back-end work forward in a highly visible platform for the retail conference was a natural extension for them, and the Liquid Galaxy fulfilled that role perfectly. The large Liquid Galaxy display allowed Smartrac to showcase some of their tools on a much larger scale.

For this project, End Point deployed two new technologies for the Liquid Galaxy:

- **Cesium Maps** - Smartrac had two major requirements for their data visualizations: show the complexity of the solution and global reach, while also making the map data offline wherever possible to avoid the risk of sketchy Internet connections at the convention center (a constant risk).  For this, we deployed [Cesium](http://www.cesiumjs.org) instead of Google Earth, as it allowed for a fully offline tileset that we could store locally on the server, as well as providing a rich data visualization set ([we’ve shown other examples before](https://www.youtube.com/watch?v=e0xbeQGUoa8)).
- **Unity3D Models** - Smartrac also wanted to show how their product tracking works in a typical retail store.  Rather than trying to wire a whole solution during the short period for a convention, however, they made the call to visualize everything with [Unity](https://unity3d.com/), a very popular 3D rendering engine.  Given the multiple screens of the Liquid Galaxy, and our ability to adjust the view angle for each screen in the arch around the viewers, this Unity solution would be very immersive and able to tell their story quite well.

Smartrac showcased multiple scenes that incorporated 3D content with live data, labels superimposed on maps, and a multitude of supporting metrics. End Point developers worked on custom animation to show their tools in a engaging demo. During the convention, Smartrac had representatives leading attendees through the Liquid Galaxy presentations to show their data. Video of these presentations can be viewed below.

<iframe allowfullscreen="" frameborder="0" height="394" src="https://www.youtube.com/embed/CntuRx3Nig4" width="700"></iframe>

Smartrac’s Liquid Galaxy received positive feedback from everyone who saw it, exhibitors and attendees alike. Smartrac felt it was a great way to walk through their content, and attendees both enjoyed the content and were intrigued by the display on which they were seeing the content. Many attendees who had never seen Liquid Galaxy inquired about it.

If you’d like to learn more about Liquid Galaxy or new projects we are working on or having custom content developed, please visit our [Liquid Galaxy website](https://liquidgalaxy.endpoint.com/) or [contact us here](https://liquidgalaxy.endpoint.com/#contact).
