---
author: Dave Jenkins
gh_issue_number: 1287
tags: cesium, liquid-galaxy
title: Full Cesium Mapping on the Liquid Galaxy
---



A few months ago, we shared a video and some [early work](http://blog.endpoint.com/2016/07/cesium-on-liquid-galaxy.html) we had done with bringing the Cesium open source mapping application to the Liquid Galaxy. We've now completed a full deployment for [Smartrac](https://www.smartrac-group.com/), a retail tracking analytics provider, using Cesium in a production environment!  This project presented a number of technical challenges beyond the early prototype work, but also brought great results for the client and garnered a fair amount of attention in the press, to everyone's benefit.

<iframe allowfullscreen="" frameborder="0" height="315" src="https://www.youtube.com/embed/CntuRx3Nig4" width="560"></iframe>

Cesium is an open source mapping application that separates out the tile sets, elevation, and markup language. This separation allows for flexibility at each major element:

- We can use a specific terrain elevation data set while substituting any one of several map "skins" to drape on that elevation: a simple color coded map, a nighttime illumination map, even a water-colored "pirate map" look.
- For the terrain, we can download as much or as little is needed: As the Cesium viewer zooms in on a given spot, Cesium uses a sort of fractal method to download finer and finer resolution terrains in just the surrounding area, eventually getting to the data limit of the set. This gradual approach balances download requirements with viewable accuracy. In our case, we downloaded an entire terrain set up to level 14 (Earth from high in space is level 1, then zooms in to levels 2, 3, 4, etc.) which gave us a pretty good resolution while conserving disk space. (The data up to level 14 totaled about 250 GB.)
- Using some KML tools we have developed for past projects and adapting to CZML ("cesium language", get it?), we were able to take Smartrac's supply chain data and show a comprehensive overview of the product flow from factories in southeast Asia through a distribution center in Seattle and on to retail stores throughout the Western United States.

The debut for this project was the National Retail Federation convention at the Javitz Center in New York City. Smartrac (and we also) wanted to avoid any show-stoppers that might come from a sketchy internet connection. So, we downloaded the map tiles, a terrain set, built our visualizations, and saved the whole thing locally on the head node of the Liquid Galaxy server stack, which sat in the back of the booth behind the screens.

The show was a great success, with visitors running through the visualizations almost non-stop for 3 days. The client is now taking the Liquid Galaxy and the Cesium visualizations on to another convention in Europe next month. The NRF, IBM, and several other ecommerce bloggers wrote up the platform, which brings good press for Smartrac, Cesium, and the Liquid Galaxy.


