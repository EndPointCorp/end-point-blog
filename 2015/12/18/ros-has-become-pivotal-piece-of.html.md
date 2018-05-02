---
author: Jacob Minshall
gh_issue_number: 1183
tags: liquid-galaxy, python, ros
title: ROS architecture of Liquid Galaxy
---



[ROS](http://wiki.ros.org/ROS/Introduction) has become the pivotal piece of software we have written our new Liquid Galaxy platform on. We have also recently open sourced all of our ROS nodes [on GitHub](https://github.com/endpointcorp/lg_ros_nodes#liquid-galaxy). While the system itself is not a robot per se, it does have many characteristics of modern robots, making the ROS platform so useful.  Our system is made up of multiple computers and peripheral devices, all working together to bring view synced content to multiple displays at the same time. To do this we made use of [ROS’s messaging](http://wiki.ros.org/Messages) platform, and distributed the work done on our system to many small [ROS nodes](http://wiki.ros.org/Nodes).

### Overview

Our systems are made up of usually 3 or more machines:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/12/18/ros-has-become-pivotal-piece-of/image-0-big.png" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/12/18/ros-has-become-pivotal-piece-of/image-0.png"/></a></div>

- Head node: Small computer that runs roscore, more of a director in the system.
- display-a: Usually controls the center three screens and a touchscreen + spacenav joystick.
- display-b: Controls four screens, two on either side of the middle three.
- display-$N: Controls more and more screens as needed, usually about four a piece.

Display-a and display-b are mostly identical in build. They mainly have a powerful graphics card and a PXE booted Ubuntu image. ROS has become our means to communicate between these machines to synchronize content across the system. The two most common functions are running Google Earth with [KML](https://developers.google.com/kml/documentation/?hl=en) / browser overlays to show extra content, and panoramic image viewers like Google’s Street View. ROS is how we tell each instance of Google Earth what it should be looking at, and what should appear on all the screens.

### Ros Architecture

Here is a general description all our [ROS nodes](http://wiki.ros.org/Nodes).  Hopefully we will be writing more blog posts about each node individually, as we do links will be filled in below. The source to all nodes can be [found here on GitHub](https://github.com/endpointcorp/lg_ros_nodes).

- lg_activity: A node that measures activity across the system to determine when the system has become inactive. It will send an alert on a specific [ROS topic](http://wiki.ros.org/Topics) when it detects inactivity, as well as another alert when the system is active again.
- lg_attract_loop: This node will go over a list of tours that we provide to it. This node is usually listening for inactivity before starting, providing a unique screensaver when inactive.
- lg_builder: Makes use of the ROS build system to create Debian packages.
- lg_common: Full of useful tools and common message types to reduce coupling between nodes.
- lg_earth: Manages Google Earth, syncs instances between all screens, includes a KML server to automate loading KML on earth.
- lg_media: This shows images, videos, and text (or really any webpage) on screen at whatever geometry / location through [awesome window manager](http://awesome.naquadah.org/) rules.
- lg_nav_to_device: This grabs the output of the /spacenav/twist topic, and translates it back into an event device. This was needed because Google Earth grabs the spacenav event device, not allowing the [spacenav ROS node](http://wiki.ros.org/spacenav_node) access.
- lg_replay: This grabs any event device, and publishes its activity over a ROS topic.
- lg_sv: This includes a Street View and generic panoramic image viewer, plus a server that manages the current POV / image for either viewer.

### Why ROS

None of the above nodes specifically needs to exist as a ROS node. The reason we chose ROS is because as a ROS node, each running program (and sometimes any one of these nodes can exist multiple times at once on one machine) has an easy way to communicate with any other program. We really liked the pub/sub style for [Inter-Process Communication](https://en.wikipedia.org/wiki/Inter-process_communication) in ROS. This has helped us reduce coupling between nodes. Each node can be replaced as needed without detrimental effects on the system.

We also make heavy use of the ROS packaging/build system, [Catkin](http://wiki.ros.org/catkin/Tutorials). We use it to build Debian packages which are installed on the PXE booted images.

Lastly ROS has become a real joy to work with. It is a really dependable system, with many powerful features. The ROS architecture allows us to easily add on new features as we develop them, without conflicting with everything else going on.  We were able to re-implement our Street View viewer recently, and had no issues plugging the new one into the system. Documenting the nodes from a client facing side is also very easy. As long as we describe each [rosparam](http://wiki.ros.org/rosparam) and [rostopic](http://wiki.ros.org/rostopic) then we have finished most of the work needed to document a node. Each program becomes a small, easy to understand, high functioning piece of the system, similar to the [Unix philosophy.](https://en.wikipedia.org/wiki/Unix_philosophy) We couldn’t be happier with our new changes, or our decision to open source the ROS nodes.


