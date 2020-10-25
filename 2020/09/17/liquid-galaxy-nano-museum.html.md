---
author: "Dave Jenkins"
title: "Liquid Galaxy at the Nano Museum in Seoul"
tags: liquid-galaxy, clients
gh_issue_number: 1665
---

![21-screen Liquid Galaxy video wall in Seoul, South Korea](/blog/2020/09/17/liquid-galaxy-nano-museum/image-0.jpg)

We’re excited to share the news of another great project End Point has launched via our partner in South Korea! The Nano Museum in Seoul has added a brand new 21-screen Liquid Galaxy as part of their exhibits. This huge video wall is interactive and includes pre-programmed flights around the world, deep dives into Google Street View at select locations, and the ability to fly the screens with a 6-axis joystick and touchscreen.

This project presented some technical challenges for our hardware team: the 21-screen layout is 3× our normal 7-screen layout (but all very doable). For this configuration, we deployed an “LGOne” server stack which has a head node server for the core applications, media storage, and overall management. It also has a large display node server with multiple Nvidia video cards to power the displays. For this large array of screens, we are able to ‘bridge’ the video cards together (not unlike a RAID array for video cards) to produce multiple hi-resolution video outputs. These video outputs then go to the screens, where they are tiled by the displays’ own built-in capabilities.

We wrote these specific configurations in our build lab in Tennessee, then shipped everything to our partner A-Zero in Seoul. They installed the servers, connected them to the displays, and after some short video conferences to confirm some configuration changes, everything looks great!

If your museum has a large video wall, and you want to bring the entire Earth, Moon, and Mars, and Ceres to your guests, please [contact us](/contact) today!
