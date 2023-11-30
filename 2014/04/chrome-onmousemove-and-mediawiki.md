---
author: Greg Sabino Mullane
title: Chrome, onmousemove, and MediaWiki JavaScript
github_issue_number: 966
tags:
- browsers
- chrome
- mediawiki
- troubleshooting
date: 2014-04-18
---



<div class="separator" style="clear: both; float: right; text-align: center;"><a href="/blog/2014/04/chrome-onmousemove-and-mediawiki/image-0-big.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/04/chrome-onmousemove-and-mediawiki/image-0.jpeg"/></a>
<br/><small><a href="https://flic.kr/p/aM4L46">Image</a> by Flickr user <a href="https://www.flickr.com/photos/archer10/">Dennis Jarvis</a></small></div>

*tl;dr: avoid using onmousemove events with Google Chrome.*

I recently fielded a complaint about not being able to select text with the mouse on a wiki running the [ MediaWiki software](https://www.mediawiki.org/wiki/MediaWiki). After some troubleshooting and research, I narrowed the problem down to a bug in the Chrome browser regarding the onmousemove event. The solution in this case was to tweak JavaScript to use onmouseover instead of onmousemove.

The first step in troubleshooting is to duplicate the problem. In this case, the page worked fine for me in Firefox, so I tried using the same browser as the reporter: Chrome. Sure enough, I could no longer hold down the mouse button and select text on the page. Now that the browser was implicated, it was time to see what it was about this page that caused the problem.

It seemed fairly unlikely that something like this would go unfixed if it was happening on the flagship MediaWiki site, Wikipedia. Sure enough, that site worked fine, I could select the text with no problem. Testing some other random sites showed no problems either. Some googling indicated others had similar problems with Chrome, and gave a bunch of workarounds for selecting the text. However, I wanted a fix, not a workaround.

There were hints that JavaScript was involved, so I disabled JavaScript in Chrome, reloaded the page, and suddenly everything started working again. Call that big clue number two. The next step was to see what was different between the local MediaWiki installation and Wikipedia. The local site was a few versions behind, but I was fortuitously testing an upgrade on a test server. This showed the problem still existed on the newer version, which meant that the problem was something specific to the wiki itself.

The most likely culprit was one of the many installed [MediaWiki extensions](https://www.mediawiki.org/wiki/Manual:Extensions), which are small pieces of code that perform certain actions on a wiki. These often have their own JavaScript that they run, which was still the most likely problem.

Then it was some basic troubleshooting. After turning JavaScript back on, I edited the LocalSettings.php file and commented out all the user-supplied extensions. This made the problem disappear again. Then I commented out half the extensions, then half again, etc., until I was able to narrow the problem down to a single extension.

The extension in question, known simply as “[balloons](https://www.mediawiki.org/wiki/Extension:Balloons)”, has actually been removed from the MediaWiki extensions site, for “prolonged security issues with the code.” The extension allows creation of very nice looking pop up CSS “balloons” full of text. I’m guessing the concern is because the arguments for the balloons were not sanitized properly. In a public wiki, this would be a problem, but this was for a private intranet, so we were not worried about continuing to use the extension. As a side note, such changes would be caught anyway as this wiki sends an email to a few people on any change, including a full text diff of all the changes.

 

Looking inside the JavaScript used by the extension, I was able to narrow the problem down to a single line inside balloons/js/balloons.js:

```javascript
  // Track the cursor every time the mouse moves
  document.onmousemove = this.setActiveCoordinates;
```

Sure enough, duck-duck-going through the Internet quickly found [a fairly incriminating Chromium bug](https://code.google.com/p/chromium/issues/detail?id=170631), indicating that onmousemove did not work very well at all. Looking over the balloon extension code, it appeared that onmouseover would probably be good enough to gather the same information and allow the extension to work while not blocking the ability for people to select text. One small replacement of “move” to “over”, and everything was back to working as it should!

So in summary, if you cannot select text with the mouse in Chrome (or you see any other odd mouse-related behaviors), suspect an onmousemove issue.


