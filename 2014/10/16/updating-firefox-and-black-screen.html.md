---
author: Jeff Boes
gh_issue_number: 1045
tags: browsers, graphics, windows
title: Updating Firefox and the Black Screen
---

If you are updating your [Firefox installation](https://support.mozilla.org/en-US/kb/update-firefox-latest-version) for Windows and you get a puzzling black screen of doom, here's a handy tip: disable graphics acceleration.

The symptoms here are that after you upgrade Firefox to version 33, the browser will launch into a black screen, possibly with a black dialog box (it's asking if you want to choose Firefox to be your default browser). Close this as you won't be able to do much with it.

Launch Firefox by holding down the SHIFT key and clicking on the Firefox icon. It will ask if you want to reset Firefox (Nope!) or launch in Safe mode (Yes).

Once you get to that point, click the "Open menu" icon (three horizonal bars, probably at the far right of your toolbar). Choose "Preferences", "Advanced", and uncheck "Use hardware acceleration when available".

Close Firefox, relaunch as normal, and you should be AOK. You can try re-enabling graphics acceleration if and when your graphics driver is updated.

Reference: [here](https://support.mozilla.org/questions/1025438).
