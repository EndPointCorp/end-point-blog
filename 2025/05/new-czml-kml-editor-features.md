---
title: "New Cesium KML-CZML Editor Features: Custom Data & Styling, Google 3D Tiles, and More"
author: Dmitry Kiselev
date: 2025-05-06
github_issue_number: x
featured:
  visionport: true
  image_url: 
tags:
- cesium
- google-earth
- gis
- open-source
- visionport
- kml
---

I have some new development on CZML editor. 

The most important changes are:

* I now support writing much more features including interpolation or time series for some properties.

	|||| clarify: interpolation of what exactly? And what type of time-series data is this referring to?

* Added export to kml and kmz
* Support for custom data and styling using that custom data
* And you can now use Google 3d tiles

Adding support for Google 3d tiles actually cause me to get that major version update. In a nutshell Cesium use it's own way to add reactivity to Entities and Vue doesn't always play nice with it. If I add Google 3d tiles to the scene, it looks like that Cesium Entities have some references to the scene and that causes Vue to apply reactive getters and setters to the whole scene.

So this time I've used React because it's easier to control what parts should be reactive and when and how you update Cesium Entities and UI components.

Next important piece is CZML exporter. Main issue here is that I might not have UI to edit some of the properties or do animations, but if a user loads a CZML document with a mixture of features I support editing and features and properties I don't support editing yet, I want to be able to export it. In other words I don't want to cut features even if I don't have support for it's editing.

|||| Is there a good visual example of the better-supported exporter?

That means that the exporter should be more robust and feature complete than editor itself.

I probably will separate the exporter as standalone package because it's valuable on it's own. I didn't find a way to export cesium entities as CZML as a part of the lib.

### Custom data & styling

Next part is my favorite. I have some experience creating maps, and when you are working with maps you are not focused on polygons or billboards you are focusing on the data and graphics are just a tool to represent it.

|||| I'd love to see an example of custom data

Previous iteration on CZML editor was more oriented on importing KML and massaging it to have the same look in Cesium as it would have been looking in Google Earth. And that puts focus on graphical features. This time I wanted to make it easy to edit data and style things based on associated it.

|||| add example images of custom styling here

See our previous blog post [introducing the Cesium CZML-KML Editor](/blog/2020/12/cesium-kml-czml-editor/) for more about the Cesium CZML-KML editor.
