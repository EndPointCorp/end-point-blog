---
author: Benjamin Goldstein
title: Liquid Galaxy at Le Pavillon de l’Arsenal in Paris
github_issue_number: 524
tags:
- clients
- visionport
date: 2011-12-12
---

Today there was an exciting opening of a new 48-screen Liquid Galaxy display at [Le Pavillon de l’Arsenal](http://www.parismetropole2020.com/evenement/index_en.html) in Paris. The configuration and use of this display is distinct from other Liquid Galaxies in that it consists of six columns and eight rows of 55” bezel-less displays set out on the floor to show just the city of Paris. This Liquid Galaxy replaced a physical model of Paris that was previously set up in the same space. It has four podiums with touch screens that visitors can use to navigate about Paris. The museum produced an impressive video showing the setup of this project:

<iframe allowfullscreen="" frameborder="0" height="315" src="https://www.youtube.com/embed/BP6ZYBTjoXE" width="560"></iframe>

End Point had the pleasure of working for and with Google on this project. Pierre Lebeau of Google spearheaded the project—at least from our point of view. Pierre’s quick and clever thinking from a high-level perspective and his leadership were crucial for getting the project done on schedule. He’s posted [a nice blog article about the project](https://maps.googleblog.com/2011/12/new-view-of-google-earth-on-48-screens.html). In addition to the Googlers on site our engineers also had the opportunity to see the talented museum staff at work and to work with [JCDecaux](https://www.jcdecaux.fr/) who set up and are supporting the Planar Clarity displays. Kiel Christofferson and Adam Vollrath spent a couple of weeks each on the installation and customization (Adam is still there) and there was a lot of preparation beyond the on-site work that was required. So, hats off to Kiel and Adam!

Some new functionality and configuration for us that was incorporated in this setup of Liquid Galaxy included:

- Driving four displays with each of the rack-mounted computers, rather than the one or two displays that we have been accustomed to for each computer of the system
- Restricting the overall area of the display to just a specific region of the map, i.e., Paris in this case
- Deploying a new web interface developed by Google for the touch screen
- Integrating a new window manager to hide the menu bars in the displays
- Enabling the use of multiple podiums to control the display.

While all the Liquid Galaxies that we have worked on and set up previously provided a wrap-around view, the Liquid Galaxy in Le Pavillon de l’Arsenal simply provides a large flat-panel view. A particular challenge therefore was figuring out how to display Google Earth’s spherical view (necessitated by a single camera viewpoint) upon a flat display surface. With a lot of attention to detail and a reasonable amount of experimentation with various configuration parameters we organized the 48 different viewports to provide a crisp display while balancing the need for predictable user control.

My next visit to Paris will definitely be including a visit to Le Pavillon de l’Arsenal!
