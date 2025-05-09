---
title: "New Cesium KML-CZML Editor Features: Custom Data & Styling, Google 3D Tiles, and More"
author: Dmitry Kiselev
date: 2025-06-13
github_issue_number: 2120
featured:
  visionport: true
  image_url: /blog/2025/06/new-czml-kml-editor-features/banner.webp
tags:
- cesium
- google-earth
- gis
- open-source
- visionport
- kml
---

![To the right, a satellite imagery map with blue and red gradient polygons drawn over it. To the left, controls for an app, including import/export, create entities, and a list of entities.](/blog/2025/06/new-czml-kml-editor-features/banner.webp)

I have made some updates to the [Cesium KML-CZML editor](https://www.visionport.com/cesium-kml-czml-editor/) I created and maintain.

The most important additions and changes are:

* Support for Google 3D tiles
* Support for writing many more features, including interpolation and time series data for some properties. There are still no editing capabilities for these properties, but while previously the editor would strip these values from the data, it will now copy them into the output file.
* Export to KML and KMZ
* Support for custom data and styling using that custom data
* Switched frontend framework from Vue to React

Adding support for Google 3D tiles is what caused me to create this major version update. In a nutshell, Cesium has its own way of adding reactivity to Entities and Vue doesn't always play nice with it. If I add Google 3D tiles to the scene, it looks like that Cesium Entities have some references to the scene and that causes Vue to apply reactive getters and setters to the whole scene.

So, I've switched to using React because it's easier to control which parts should be reactive, as well as when and how you update Cesium Entities and UI components.

The next important piece is the CZML exporter. The main issue here is that I don't want to strip away features even if I don't support editing them.

Even if I don't have the UI to edit certain properties or animations for properties, a user can load a CZML document with a mixture of supported and unsupported features without losing the unsupported features. That means that the exporter should be more robust and feature complete than editor itself.

I will probably separate the exporter as standalone package because it is valuable on its own — I couldn't find a way to export Cesium entities as CZML within the library.

### Custom data & styling

This part is my favorite. I have some experience creating maps, and when you are working with maps you are not focused on polygons or billboards, you are focused on the data, while graphics are just a tool to represent it.

The previous iteration of the KML-CZML editor was more oriented toward importing KML and massaging it to have the same look in Cesium as it would in Google Earth. That puts focus on graphical features. This time I wanted to make it easy to edit data and style things based on the data.

#### Demo

We'll load in some demo data from New York elections in `Mike4326.geojson`.

![The CZML editor with all yellow polygons drawn over a region of New York](/blog/2025/06/new-czml-kml-editor-features/map-with-geojson.webp)

From here, we'll click on the "Data table & Conditional Styling" button. Then, in the menu that opens, we'll set up Color by value so that we can display different regions differently by our selected attribute. Note the "Mike_prc" column which displays a percent value. The app will select a color from the gradient based on this value.The app will select a color from the gradient based on this value.

![The editor with a full screen popup reading "conditional styling". There are three main tabs, "Color by value", "Labels", and "Extrusion and scale". The first is selected. Under the tabs it reads "Set entities colors by value of an attribute". Under a dropdown reading "Attribute", "Mike_prc" is selected. A blue to red gradient is below, with a continuous range of colors. At the bottom is a table with polygon 1, polygon 2, etc. Then a style column, all of which have a yellow box. The rightmost column is "Mike_prc", and reads a percent number from 0 to 100.](/blog/2025/06/new-czml-kml-editor-features/color-by-value-selecting-Mike_prc.webp)

To group values together, we'll toggle the "Fixed gradations" switch. Then hit the "Preview" button. By default, there are 9 gradations.

![The same view, with the gradient now reduced to only 9 values. There is an additional column next to "style" which shows colors from the gradient corresponding to the Mike_prc value.](/blog/2025/06/new-czml-kml-editor-features/fixed-gradations-9-preview.webp)

We want fewer gradations than that. Let's try out 6.

![The same view, but now there are only 6 values in the gradient. Most of the preview colors are the same, but a few have been changed to match the 6 values.](/blog/2025/06/new-czml-kml-editor-features/fixed-gradations-6-preview.webp)

Not much difference, but we'll go with the 6 gradations. I'll hit apply, and you can see the colors are now displayed in the "Style" column, while the "Preview" column has been hidden.

![The same view, but now the red to blue colors appear in the "style" column, and the "preview column is hidden.](/blog/2025/06/new-czml-kml-editor-features/fixed-gradations-6-applied.webp)

Let's see how it looks on the map.

![The original view of the CZML editor. The electoral districts now show a gradient from blue to red, corresponding to the polygon styling we saw, rather than all being yellow as it started.](/blog/2025/06/new-czml-kml-editor-features/map-with-6-gradations.webp)

Very nice! Now let's add some labels for a different attribute, the election district.

![The conditional styling menu, this time in the "Labels" tab. Text reads "Set Labels and Label text using entities attribute value. The selected attribute is "Election_D". There is a box displaying pure black color above the table of polygons.](/blog/2025/06/new-czml-kml-editor-features/label-Election_D-selected.webp)

You can see the text color defaults to black, which won't read well on our colored districts. Let's change it by hitting the "edit" button next to the color.

![The same screen, now with added color sliders next to the color square. The color has been changed to a near-white gray.](/blog/2025/06/new-czml-kml-editor-features/label-color-selected.webp)

I changed it to a light gray. Let's look at the map now.

![A closer view of the map with the red-blue colored districts, now with many light gray labels displaying the name of the election district.](/blog/2025/06/new-czml-kml-editor-features/map-with-labels.webp)

Lots of labels! This is quite a dense area, so you would probably want to zoom in further to see the labels more clearly.

See my previous blog post [introducing the Cesium CZML-KML Editor](/blog/2020/12/cesium-kml-czml-editor/) for more about the Cesium CZML-KML editor.
