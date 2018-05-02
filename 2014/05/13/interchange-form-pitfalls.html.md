---
author: Jeff Boes
gh_issue_number: 981
tags: interchange
title: Interchange form pitfalls
---



I’ll warn you going in: this is obscure Interchange internal form-wrangling voodoo, and even if you are familiar with that, it’s not going to be an easy trip to get from here to the end of the story. Fair warning!

Interchange form-handling has many, many features. Some of them are pretty obscure. One such is the concept of a “click map”: a snippet of named code, stored on the server. Specifically, it is stored within the user’s session, which is a chunk of storage associated with a browser cookie, and can contain all sorts of stuff—but which is primarily used for things like the shopping cart, the user’s identity, and so on.

But the tricky business here is when we put something into the session that says, in effect, “when we do *this*, do *that*, too”.

(Note: you don’t *have* to store your click map code in the session. In fact, it’s probably better not to, for a number of good reasons. You can put it in a sort of global configuration file, in which each individual snippet needs a unique name – which is precisely the requirement that would have prevented this bug, had I or one of my predecessors chosen to embrace that restriction.)

An Interchange *page* is both code and presentation (that is, variable assignments, ITL and/or Perl, plus HTML). No, this isn’t a great design feature—but it was considered so in an earlier, more innocent time.

I had one application that continued to present bugs that resisted solution, in fact they were virtually impossible to reproduce. Until one day, when I was testing a theory (which was totally wrong, but led me into the right spot): I landed on a page, then refreshed the page—and saw a totally different page. Here’s what happened, as simply as I can represent it.

```
Page1.html:
<form ...>
[set Continue]
mv_nextpage=Page2.html
[/set]
<input type="submit" name="mv_click" value="Continue"
</form>

Page2.html:
<form ...>
[set Continue]
mv_nextpage=Page3.html
[/set]
<input type="submit" name="mv_click" value="Continue"
</form>

```

When you request Page1.html, before the page is delivered to the browser, the session variable “Continue” is initialized with the code:

```
mv_nextpage=Page2.html

```

In Interchange terms, this tells Interchange where to go when form processing is complete. When we click on the “Continue” button, form processing happens on the server, and the “mv_click” button’s code is referenced * by name * as “Continue”. That takes us to “Page2.html”. When that page is prepared, Interchange overwrites the “Continue” variable with its new data, which is also a next-page setup.

Now, if we click the button on Page1.html, but then refresh the page on the resulting Page2, form processing is run again—but this time, our call-by-name to “Continue” executes the code that Page2 set up for its Continue button—not the Page1 setup. In other words: clicking the button on Page1.html sends us to page 2, but refreshing Page2.html * sends us to Page3.html*.

I can’t tell you what a relief this was to finally reproduce this bug. The simple fix was to just change the names involved, to “Continue1” and “Continue2”. There’s certainly a lot of power in Interchange form processing, but hoo boy—with great power comes great potential to shoot yourself in the foot.


