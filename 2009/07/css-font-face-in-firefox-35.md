---
author: Jon Jensen
title: CSS @font-face in Firefox 3.5
github_issue_number: 172
tags:
- browsers
- css
date: 2009-07-15
---

This has been frequently mentioned around the web already, but it’s important enough that I’ll bring it up again anyway. Firefox 3.5 adds the CSS @font-face rule, which makes it possible to reference fonts not installed in the operating system of the browser, just as is done with images or other embedded content.

Technically this is not a complicated matter, but font foundries (almost all of whom have a proprietary software business model) have tried to hold it back hoping for magical DRM to keep people from using fonts without paying for them, which of course isn’t possible. As one of the original Netscape developers mentioned, if they had waited for such a thing for images, the web would still be plain-text only.

The quickest way to get a feel for the impact this change can have is to look at [Ian Lynam & Craig Mod’s article demonstrating @font-face](https://craigmod.com/journal/font-face/) in Firefox 3.5 side-by-side with any of the other current browsers. It is exciting to finally see this ability in a mainstream browser after all these years.
