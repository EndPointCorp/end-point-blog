---
author: Piotr Hankiewicz
gh_issue_number: 1309
tags: browsers, conference, java, javascript
title: infoShare 2017 - JavaScript, JavaScript everywhere
---

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/27/infoshare-2017-javascript-javascript/image-0.jpeg" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="771" data-original-width="1600" src="/blog/2017/05/27/infoshare-2017-javascript-javascript/image-0.jpeg" style="max-width: 100%;"/></a></div>

The last week was really interesting for me. I attended the infoShare 2017, the biggest tech conference in central-eastern Europe. The agenda was impressive, but that’s not everything. There was a startup competition going on and really, I’m totally impressed.

infoShare in numbers:

- **5500** attendees
- **133** speakers
- **250** startups
- **122** hours of speeches
- **12** side events

Let’s go through each speech I was attending.

### Day 1

### Why Fast Matters by Harry Roberts from csswizardry.com

Harry tried to convince us that performance is important.

<a href="/blog/2017/05/27/infoshare-2017-javascript-javascript/image-1.png" imageanchor="1"><img border="0" data-original-height="206" data-original-width="620" src="/blog/2017/05/27/infoshare-2017-javascript-javascript/image-1.png"/></a>

Great speech, showing that it’s an interesting problem not only from a financial point of view.
You must see it, link to his presentation [here](https://speakerdeck.com/csswizardry/why-fast-matters)

### Dirty Little Tricks From The Dark Corners of Front-End by Vitaly Friedman from smashingmagazine.com

It was magic! I work a lot with CSS, but this speech showed me some new ideas and reminded me that the simplest solution is maybe not the best solution usually and that we should reuse CSS between components as much as possible.

Keep it DRY!

One of these tricks is a quantity query CSS selector. It’s a pretty complex selector that can apply your styles to elements based on the number of siblings. ([http://quantityqueries.com/](http://quantityqueries.com/))

### The Art of Debugging (browsers) by Remy Sharp

<a href="/blog/2017/05/27/infoshare-2017-javascript-javascript/image-2.png" imageanchor="1"><img border="0" data-original-height="428" data-original-width="640" src="/blog/2017/05/27/infoshare-2017-javascript-javascript/image-2.png" style="float:right; max-width: 300px;"/></a>

It was great to see some other developer and see his workflow during debugging. I usually work from home and it’s not easy to do it in my case.

Remy is a very experienced JavaScript developer and showed us his skills and tricks, especially interesting Chrome developer console integration.

I always thought that using the developer console for programming is not the best idea, maybe it’s not? It looked pretty neat.

### Desktop Apps with JavaScript by Felix Rieseberg from Slack

Felix from Slack presented and show the power of desktop hybrid apps. He used a framework called Electron. Using Electron you can build native, cross-system desktop apps using HTML, JavaScript and CSS. I don’t think that it’s the best approach for more complex applications and probably takes more system memory than native-native applications, but for simpler apps it can a way to go!

Github uses it to build their desktop app, so maybe it’s not so slow? :)

### RxJava in existing projects by Tomasz Nurkiewicz from Allegro

Tomasz Nurkiewicz from Allegro showed us his high programming skills and provided some practical RxJava examples. RxJava is a library for composing asynchronous and event-based programs using observable sequences for the Java VM.

Definitely something to read about.

### Day 2

### What does a production ready Kubernetes application look like? by Carter Morgan from Google

Carter Morgan from Google showed us practical uses of Kubernetes.

Kubernetes is an open-source system for automating deployment, scaling and management of containerized applications. It was originally designed by Google developers and I think that they really want to popularize it. It looked that Kubernetes has a low learning curve, but devops agents I spoke after the presentation were sceptical, saying that if you know how to use Docker Swarm then you don’t really need Kubernetes.

### Vue.js and Service Workers become Realtime by Blake Newman from Sainsbury's

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2017/05/27/infoshare-2017-javascript-javascript/image-3-big.png" imageanchor="1" style="clear: left; float: left; margin-bottom: 1em; margin-right: 1em;"><img border="0" data-original-height="427" data-original-width="640" height="214" src="/blog/2017/05/27/infoshare-2017-javascript-javascript/image-3.png" width="320"/></a></div>

Blake Newman is a JavaScript developer, member of the core Vue.js (trending, hot JavaScript framework) team. He explained how to use Vue.js with service workers.

The service workers are scripts that your browser runs in the background. Nice to see how it fits together, even though it’s not yet supported by every popular browser.

### Listen to your application and sleep by Gianluca Arbezzano from InfluxData

Gianluca showed us his modern and flexible monitoring stack. Great tips and mostly discussing and recommending InfluxDB and Telegraf, we use it a lot in End Point.

He was right that it’s easy to configure, open-source and really useful. Great speech!

### Summary

Amazing two days. All the presentations will be available on Youtube soon: [https://www.youtube.com/user/infoSharePL/videos](https://www.youtube.com/user/infoSharePL/videos).

I can fully recommend this conference, see you next time!
