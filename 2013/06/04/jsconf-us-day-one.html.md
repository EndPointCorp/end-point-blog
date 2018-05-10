---
author: Greg Davidson
gh_issue_number: 813
tags: community, conference, css, html, javascript, open-source, tips, tools
title: "JSConf US 2013 —​ Day One"
---



<a href="https://www.flickr.com/photos/geigercounter/8951325076/" title="Room With A View by Geiger Counter, on Flickr"><img alt="Room With A View" height="217" src="/blog/2013/06/04/jsconf-us-day-one/image-0.jpeg" width="640"/></a>

 

I attended JSConf in Amelia Island, FL last week. As you can see, the venue was pretty spectacular and the somewhat remote location lent itself very well to the vision set by the conference organizers. Many developers myself included, often find the line between work and play blurring because there is much work to be done, many new open source projects to check out, constant advancements in browser technology, programming languages, you name it. Keeping up with it all is fun but can be challenging at times. While the talks were amazing, the focus and ethos of JSConf as I experienced it was more about people and building on the incredible community we have. I highly recommend attending meetups or conferences in your field if possible.

Without further ado, I’ve written about some of the talks I attended. Enjoy!

### Day One

#### Experimenting With WebRTC

[Remy Sharp](https://remysharp.com/) presented the first talk of the day about his experience building a [Google Chrome Experiment](https://experiments.withgoogle.com/collection/chrome) with WebRTC and the peer to peer communication API. The game ([headshots](https://web.archive.org/web/20130816024030/https://headshots.leftlogic.com/)), was built to work specifically on Chrome for Android Beta. Because WebRTC is so young, the libraries supporting it (Peer.js, easyRTC, WebRTC.io, SimpleWebRTC) are very young as well and developing quickly. He found that “Libraries are good when you’re fumbling, bad when stuff doesn’t work”. The “newness” of WebRTC ate much more time than he had anticipated. Remi demoed the game and it looked like good fun. If you’re interested in checking out headshots further, the [source code](https://github.com/leftlogic/headshots) is up on GitHub. 

#### JavaScript Masterclass

[Angelina Fabbro](https://twitter.com/angelinamagnum) gave a talk about levelling up your skills as a developer. She first broke everyone’s heart by telling us “we’re not special” and that nobody is a natural born programmer. She presented some data (studies etc) to support her point and argued that early exposure to the practice of logical thinking and practicing programming can make you seem like a natural.

She described several ways to know you’re not a beginner: 

- You can use the fundamentals in any language
- You are comfortable writing code from scratch
- You peek inside the libraries you use
- You feel like your code is mediocre and you’re unsure what to do about it

...and ways to know you’re not an expert: 

- You don’t quite grok (understand) all the code you read
- You can’t explain what you know
- You aren’t confident debugging
- You rely on references/docs too much

> “Welcome to the ambiguous zone of intermediate-ness”.

Angelina suggested several ways to improve your skills. Ask “why?” obsessively, teach or speak at an event, work through a suggested curriculum, have opinions, seek mentorship, write in another language for a while etc. One book she specifically recommended was Secrets of the JavaScript Ninja by John Resig.

#### JavaScript is Literature is JavaScript

[Angus Croll](http://anguscroll.com/) from Twitter presented a hilariously entertaining talk in which he refactored some JavaScript functions in the literary styles of Hemingway, Shakespeare, Bolaño, Kerouac, James Joyce and other literary figures. The talk was inspired by a [blog post](http://byfat.xxx/if-hemingway-wrote-javascript) he’d written and had the entire conference hall erupting with laughter throughout. 

<a href="http://www.flickr.com/photos/geigercounter/8950136537/" title="poolside.js by Geiger Counter, on Flickr"><img alt="poolside.js" height="500" src="/blog/2013/06/04/jsconf-us-day-one/image-0.jpeg" width="375"/></a>

#### Learning New Words

[Andrew Dupont](http://andrewdupont.net/) continued in the literary, language-oriented vein, giving a talk which drew a parallel between olde english purists who did not want to adopt any “new” words and the differing views surrounding the EcmaScript 6 specification process. Dupont’s talk was very thought-provoking especially in light of the resistance to some proposals in the works (e.g. [ES6 modules](https://web.archive.org/web/20130820143217/http://wiki.ecmascript.org/doku.php?id=harmony:modules)). Check out [his slides](https://www.slideshare.net/savetheclocktower/learning-new-words-22244915)—​the video will also be published in future. 

#### Flight.js

<img alt="Flight twitter" border="0" height="258" src="/blog/2013/06/04/jsconf-us-day-one/image-2.png" style="display:block; margin-left:auto; margin-right:auto;" title="flight-twitter.png" width="375"/> 

[Dan Webb](https://twitter.com/danwrong) spoke about [Flight](https://web.archive.org/web/20130520095336/http://twitter.github.io/flight/), a client-side framework developed by the team at Twitter and released this past January. They have been using it to run lots of twitter.com and most of tweetdeck as well. Webb got a laugh out of the room when he recalled the first comment on Hacker News after [Flight was announced](https://web.archive.org/web/20130518044937/http://engineering.twitter.com/2013/01/introducing-flight-web-application.html): “Why not use [Angular](https://angularjs.org/)?”. The motivation behind Flight’s design was to make a “system that’s easy to think about”. This aim was achieved by decoupling components (entirely self-contained).

A Flight component is just a JavaScript object with a reference to a DOM node. The component can be manipulated, trigger events and listen to events (from other components). Applications are constructed by attaching Flight components to pieces of the DOM. Keeping the components independent in this way makes testing very easy. Complexity can be layered on but does not require any additional mental overhead. Dan suggested that Flight’s design and architecture would work very well with Web Components and [Polymer](https://polymer-project.appspot.com/) in future.


