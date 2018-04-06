---
author: Mike Farmer
gh_issue_number: 784
tags: conference, ruby
title: Pounding Simplicity into Wiki
---

Day two of MountainWest Ruby Conference starts out with a bang! Notable developer and thought leader [Ward Cunningham](https://en.wikipedia.org/wiki/Ward_Cunningham) describes the how he is going about developing his latests ideas behind the wiki. While doing so, Cunningham teaches concepts of innovation and how creativity to help inspire ruby developers.

### Promise

The promise is a basic statement of the desired outcome. Not in a way a mock-up shows the finished product, but the way in which it will affect humanity. Wikipedia gives words, depth, and meaning that ordinary people can depend on every day. The promise of this new kind of wiki is to
give numbers depth and meaning that ordinary people can depend on every day.

This means data visualization intermixed with context. For example, a weather map can show you numbers on a map to tell you temperatures. A meteorologist doesn’t just see a number, he sees the actual weather, the hot and cold, the wind or the rain, etc. Data visualizations like a [wind map](http://hint.fm/wind/) excel at helping users to visually see the wind in region.

To accomplish this promise, Cunningham implemented a new kind of wiki. The main difference in this new wiki is that the data is federated among several different locations on the web and then assembled in the browser. You can think of it as a traditional mashup. The wiki content is both self generated and programatically generated from data on the web or attached to the web via some device.

### Process

- 0 Story: Pages with datasets, images and paragraphs with history (versions).
- 1 Binding: Attaches the data to different versions of the page revisions.
- 2 Attribution: Source is dynamically generated so that it can be tracked back.
- 3 Link Context: Links to other pages on other servers give hints to tell you where the data originates.
- 4 Neighborhood: Click on a page that doesn’t exist (red link) server looks for similar page on other wikis in the federated network.
- 5 Search: Global search looks in all the wikis in the federated network.

### Principle

The principle behind this project is one of discovery. As the development continues, the possibilities for it increase and new thoughts and ideas are discovered. This was talked about in a [talk by Bret Victor called Inventing on Principle](https://vimeo.com/36579366). If you were to compare this to agile, it might look like this:

<table>
<colgroup>
<col style="text-align:left;"/>
<col style="text-align:left;"/>
</colgroup>

<thead>
<tr>
 <th style="text-align:left;">Agile</th>
 <th style="text-align:left;">Principle</th>
</tr>
</thead>

<tbody>
<tr>
 <td style="text-align:left;">velocity</td>
 <td style="text-align:left;">smallest</td>
</tr>
<tr>
 <td style="text-align:left;">customer</td>
 <td style="text-align:left;">curiosity</td>
</tr>
<tr>
 <td style="text-align:left;">confidence</td>
 <td style="text-align:left;">wonder</td>
</tr>
</tbody>
</table>

### Plugins

Widgets are some markup that allow interactivity. Widgets have access to the content on the wiki page to allow it to be integrated into the markup. Widgets source code live on github. Widgets allow you to explore your data by breaking up the visualizations and put it in context with explanation and documentation of the wiki.

### Connecting Things to the Federated Wiki

The documentation page allows you to use a widget to talk to a connected computer or device. Cunningham demonstrated connecting the wiki to a small microcontroller that emitted sound and blinked an LED. From the wiki page he could see output from the device and send instructions to make the device do different things. All of the communication is handled over a websocket so the interaction is seamless and instant. The idea here is that different sensors could provide live data to the wiki to augment research and discovery.

Ward Cunningham has an amazing ability to bring small comprehensible things together into systems that show us the future of our interactions with the web. This sparks new ideas and explores realms of possibility that enhances our lives, just as that simple idea of throwing some markdown into a web server and displaying it for the world to see in a searchable and linkable way. That little idea that sparked a revolution in information discovery. The wiki.
