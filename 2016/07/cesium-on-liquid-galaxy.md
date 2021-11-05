---
author: Dave Jenkins
title: Cesium on the Liquid Galaxy
github_issue_number: 1241
tags:
- cesium
- visualization
- javascript
- visionport
date: 2016-07-13
---

Data visualization continues to evolve, with ever-more complex data sets available openly, and a corresponding increased pace in visualization tools. In mapping GIS data, the Cesium app is gaining quite a bit of traction. As we continue to branch out with new functionality and visualization apps for the [Liquid Galaxy](https://liquidgalaxy.endpoint.com/), we wanted to try the Cesium app as well.

<iframe allowfullscreen="" frameborder="0" height="315" src="https://www.youtube.com/embed/e0xbeQGUoa8" width="560"></iframe>

Cesium is written all in JavaScript WebGL and offers some nice advantages over other engines: it’s open source, it’s flexible, and it’s quick. It can accept an array of points, shapefiles, 3D models, and even KML.  The JavaScript then chews these up and delivers a nice consistent 3D environment that we can fly through with the SpaceNav controller, set scenes in a presentation to tell a story, or mix together with video or graphic popups for a fully immersive multimedia experience. Cesium is open source, and provides a great deal of flexibility and accessibility to build different kinds of data visualizations and interactions. There are a lot of new startups exploiting this platform and we welcome the opportunity to work with them.

As we’ve written previously, the main advantage of the Liquid Galaxy platform is the ability to adjust the viewing angle on each screen to match the physical offset, avoiding (as much as possible) artificial distortions, fisheye views, or image stretching.  The trickiest bit of this project was setting the distributed camera driver, which takes input from the SpaceNav controller and correctly aligns the view position for each of the geometrically offset displays. Once the math is worked out, it’s relatively quick work to put the settings into a rosbridge WebSockets driver.  Once again, we’re really enjoying the flexibility that the ROS architecture grants this system.

Looking forward, we anticipate this can open up many more visualizations for the Liquid Galaxy. As we continue to roll out in corporate, educational, and archival environments such as real estate brokerages, hospitality service providers, universities, and museums, the Cesium platform will offer yet another way for our customers to visualize and interact with their data.
