---
author: Ben Goldstein
gh_issue_number: 360
tags: liquid-galaxy
title: Two Cool Things about Liquid Galaxy
---

I. It uses COTS Hardware.

Liquid Galaxy is suitable for using with COTS (Commodity Off The Shelf) hardware. Yes, Google Earth itself is rather resource intensive, so it helps performance to use fiesty computers (including ones with SSDs) but it's still COTS hardware. Of course the very cool thing about using COTS hardware is that the price is right and gets better all the time.

II. A Simple, elegant and powerful Master/Slave configuration and communication approach

Liquid Galaxy works by configuring its "slave" systems to have offsets from the point of view of the master system that the system's user navigates on. The slave systems "know" their locations relative to the master system. The master system broadcasts its location to the slaves via UDP packets. It's then up to the slave systems to figure out what portion of a Google Earth globe they need to retrieve themselves relative to the coordinates broadcast from the master system.

With this approach it's easy to scale to a large number of slave systems. An interesting extension to this configuration and communication approach that the Google engineering team for the project provided for is the ability to configure one or more *remote* Liquid Galaxies to remotely mirror the views being displayed in a given "Master Galaxy". This will allow teams of users to remotely view the same Google Earth views within the awesome environment of distinct Liquid Galaxies. The remote Liquid Galaxies essentially "play" the same views as are seen in the Master Galaxy, but negligible network traffic is passed from system to system.
