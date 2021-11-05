---
author: Dave Jenkins
title: ROS Platform Upgrades for Liquid Galaxy
github_issue_number: 1182
tags:
- gis
- google-earth
- visionport
- ros
date: 2015-12-14
---

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/12/ros-platform-upgrades-for-liquid-galaxy/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/12/ros-platform-upgrades-for-liquid-galaxy/image-0.jpeg"/></a></div>

For the last few months, End Point has been rolling out a new application framework along with updated display applications and monitoring infrastructure for the Liquid Galaxy Display Platform.  These upgrades center on the ROS framework and allow a great number of functionality extensions and enhancements for the end user, as well as improvements to the stability and security of the core systems. It is intended that the 50+ systems that we currently maintain and support on behalf of our enterprise clients will be upgraded to this new platform.

### ROS Overview

ROS is short for “Robot Operating System”.  Just as it sounds, it is a framework used for controlling robots, and handles various environmental ‘inputs’ and ‘outputs’ well.  End Point chose this framework in conjunction with related ongoing development projects on behalf of our enterprise clients.  This system allows complex interactions from a touchscreen, camera, SpaceNav, or other device to be interpreted conditionally and then invoke other outputs such as displaying Google Earth, Street View, or other content on a given screen, speaker, or other output device.  For more details, see: [http://www.ros.org](http://www.ros.org)

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/12/ros-platform-upgrades-for-liquid-galaxy/image-1-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/12/ros-platform-upgrades-for-liquid-galaxy/image-1.jpeg"/></a></div>

### Liquid Galaxy Enhancements

This new platform brings a number of improvements to the back-end systems and viewing customer experience.

#### Improved Street View Panospheres

The new Street View viewer draws Street View tiles inside a WebGL sphere.  This is a dramatic performance and [visual enhancement](https://www.youtube.com/watch?v=YvQ5JmXx3Bg) over the older method, and can now support spherical projection, hardware acceleration, and seamless panning.  For a user, this means tilting the view vertically as well as horizontally, zooming in and out, and improved frame rates.

#### Improved Panoramic Video

As with the panoramic Street View application, this new platform improves the panoramic video playback as well.  YouTube and Google have announced major initiatives to start actively supporting 360° panoramic video, including the financial backing of some high profile projects as  example use cases.  The Liquid Galaxy, with its panoramic screen layout already in place, is ideally suited for this new media format.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/12/ros-platform-upgrades-for-liquid-galaxy/image-2-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/12/ros-platform-upgrades-for-liquid-galaxy/image-2.png"/></a></div>

#### Improved Touchscreen

The touchscreen incorporates a templated layout for easier modification and customization.  The scene view selector is now consolidated to a single interface and no longer requires sub-pages or redundant touches.  The Street View interface, complete with the ‘pegman’ icon, is a photo-realistic map with pinch and zoom just like a tablet interface.

#### Browser Windows

The Liquid Galaxy can control multiple browser windows that can appear anywhere on the screens, often across multiple screens.  These browser windows can show anything that can appear in a desktop web browser: web pages, videos, social media updates, data visualizations, etc.

#### Content Management System

Beginning in 2014, End Point began to upgrade the content management system for the Liquid Galaxy.  With the new ROS platform, we have updated this application to Roscoe (the ROS content experience).  Roscoe gives registered users the ability to create complex presentations with specific scenes.  Each scene can have a specific global location to guide the Google Earth or Street View, and then invoke overlays that appear across the screens.  These overlays can include photos,  data graphs, videos, or web pages.  Each scene can also include a specific KML data set e.g., population density data, property value data, etc.) that can appear as 3D bar graphs directly in the ‘Earth’ view.

#### Content Isolation

Isolating the entire presentation layer in ROS makes it easy to develop exhibits without a full-fledged Liquid Galaxy system.  The entire ROS stack can be installed and run on an Ubuntu 14.04 computer or within a Docker container.  This ROS stack can be used by a developer or designer to build out presentations that will ultimately run on a Liquid Galaxy system.

#### App Modularization

Each component of a Liquid Galaxy exhibit is a configurable ROS node, allowing us to reuse large swaths of code and distribute the exhibit across any number of machines. This architecture brings two strong advantages: 1) each ROS node does one specific thing, which increases portability and modularity, and 2) each node can be tested automatically, which improves reliability.

#### Enhanced Platform Stability

By unifying all deployments on a common base, End Point is able to deploy bug fixes, monitoring scripts, and ongoing enhancements much more quickly and safely.  This has enhanced the overall stability for all supported and monitored Liquid Galaxy platforms.

### Product Roadmap

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/12/ros-platform-upgrades-for-liquid-galaxy/image-3-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/12/ros-platform-upgrades-for-liquid-galaxy/image-3.png"/></a></div>

The items described above are the great things that we can do already with this new platform.  Even greater things are coming soon:

#### LiDAR Point Clouds

End Point has already built early prototypes for the Liquid Galaxy platform that can view LiDAR point clouds.  LiDAR is rapidly gaining traction in the architecture, surveyor, and construction industries.  With the large viewing area of the Liquid Galaxy, these LiDAR point clouds become much more impactful and useful to the command and control center.

#### Google Earth and Google Maps Upgrades

End Point continues to work with the latest developments in the Google Earth and Google Maps platforms and is actively working to integrate new features and functionality. These new capabilities will be rolled out to the fleet of Liquid Galaxies as available.

#### 3D WebGL Visualizations

The Liquid Galaxy will be enhanced to view completely virtual 3D environments using WebGL and other common formats.  These environments include complex data visualizations, interior space renderings for office planning, and even games.

### Next Steps

If you’re considering the Liquid Galaxy platform, [contact us](https://liquidgalaxy.endpoint.com/#contact) to discuss these latest enhancements and how they can improve the communications and presentation tools for your organization.
