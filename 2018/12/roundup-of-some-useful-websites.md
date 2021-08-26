---
author: Jon Jensen
title: Roundup of some useful websites
github_issue_number: 1478
tags:
- tips
- tools
date: 2018-12-21
---

<a href="/blog/2018/12/roundup-of-some-useful-websites/squoosh-demo-20181220b.png"><img src="/blog/2018/12/roundup-of-some-useful-websites/squoosh-demo-20181220a.jpg" /></a>

The world is a big place, and the Internet has gotten pretty big too. There are always new projects being created, and I want to share some useful and interesting ones from my growing list:

### Squoosh image compressor

Squoosh, hosted at [squoosh.app](https://squoosh.app/), is an open source in-browser tool for experimenting with image compression, made by the Chrome development team.

With Squoosh you can load an image in your browser, convert it to different image file formats (JPEG, WebP, PNG, BMP) using various compression algorithms and settings, and compare the result side-​by-​side with either the original image or the image compressed using other options.

The screenshot above demonstrates Squoosh running in Firefox 64 on Linux. Click on it to see a larger, lossless PNG screenshot. The photo was taken by my son Phin in northern Virginia, and is a typical imperfect mobile phone photo. On the left is the original, and on the right I am showing how bad gradients in the sky can look when compressed too much—​maybe a quality level of 12 (out of 100) was too low. It does make for a very compact file size, though. 😄

Squoosh’s interface has a convenient slider bar so you can compare any part of the two versions of the image side by side. You can zoom and pan the image as well.

It is neat to see JavaScript tools (in this case TypeScript specifically) doing work in the browser that has traditionally been done by native apps.

### Nerd Fonts

If you want access to an amazing number of symbols in a font, check out [nerdfonts.com](https://nerdfonts.com/). There you can mix and match symbols from many popular developer-​oriented fonts such as Font Awesome, Powerline Symbols, Material Design, etc.

I probably should have chosen some fun symbols to demonstrate it here, but I could tell that was a rabbit hole I would not soon emerge from!

### glot.io code pastebin

There are many public pastebins these days, but [glot.io](https://glot.io/) distinguishes itself by allowing you to run real code on their server in nearly 50 languages.

It offers both public and private pastes, has an API, and is open source.

### Firefox Send

Firefox Send at [send.firefox.com](https://send.firefox.com/) is a browser-​based service for securely sharing files temporarily, for only one download during a maximum of 24 hours.

Handy for keeping unwanted bloat out of email, chat, or shared file storage for ephemeral files.

### transfer.sh command-​line file sharing

Similarly, [transfer.sh](https://transfer.sh/) is a terminal-​based file upload and download tool.

As a command-​line tool it easily integrates with other standard tools, so you can pipe output from other programs directly to it. If you have sensitive data to share you don’t need to trust the service—​you can pipe your data through gpg or some other encryption tool before it leaves your computer.

transfer.sh is open source and can be self-​hosted too.

It even has a Tor onion service so uploads and/​or downloads can be as private as possible in hostile environments.

### Doing what you don’t want to do

And finally, some timeless tips for making our human “software” work.

Often just one or two annoying little things can block us from making progress on larger projects that overall we really enjoy. How can you motivate yourself to push ahead when you have work that needs to be done, but you don’t want to do it?

Read the brief but helpful article [10 Ways to Do What You Don’t Want to Do](https://zenhabits.net/unwanted/) by Leo Babauta to get some good ideas. A few of the points mentioned especially resonate with me:

* Why do I need to do it?
* What is stopping me?
* Embrace that it won’t be fun and do it anyway.
* Set constraints.

Then do at least a little bit of the work to get started. As our co-worker [Mike Heins](/team/mike-heins) has said to me on a few occasions over the years, you’ll never finish until you start.
