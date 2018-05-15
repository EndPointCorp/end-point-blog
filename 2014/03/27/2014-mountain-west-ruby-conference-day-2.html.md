---
author: Brian Gadoury
gh_issue_number: 954
tags: functional-programming, javascript, conference, ruby, rails
title: 2014 Mountain West Ruby Conference Day 2
---

This past Friday concluded my second Mountain West Ruby Conference right here in my backyard of Salt Lake City, Utah. Just like the 2013 MWRC, this year’s conference was great. It was also nice to meet up with fellow remote co-worker Mike Farmer for both days. Here are a few of my personal favorites from day 2 of the conference, which I almost missed when I had the audacity to show up without a Macbook Air/Pro. (Kidding!)

### Randy Coulman — Affordances in Programming Languages

Affordances (“A quality of an object or environment that allows someone to perform an action”) are all around us. Randy opened with some examples of poor affordances such as a crosswalk button with two enticing-looking widgets that requires arrows drawn on the box to point to the one that actually is a button. Then, a counter-example showing the “walking” or “standing” footprints painted on an escalator and how they instantly and intuitively communicate how to best use the escalator.

Randy followed with a few examples of affordances in software. One of them was a simple Ruby implementation of an affordance called Deterministic Destructors. It was a method that acquired a resource, yielded to a block argument, then automatically released that resource when the block returned.

The last affordance Randy showed is most near and dear to my heart because it happens to be something I can use in my current project: Subclass iteration. Rather than use a registry pattern to explicitly register components that can handle specific file formats (for example), you can leverage Ruby’s built-in inherited(subklass) class method by overriding it in your parent class. That, along with a one-liner helper method, can be used to automagically register your subclasses. Implement a standard interface (can_handle_thing?) for your subclasses to advertise what type of data they can handle, then use your de facto subclass registry to delegate appropriately at runtime.

Ultimately, Randy’s list of takeaways summed it all up nicely:

- “Languages afford certain designs and inhibit others,” thereby shaping how we think about certain problems

- Learning new languages will increase your “solution space” and expose you to different approaches that may be applicable elsewhere.

Thanks for the talk, Randy! Here is his [“Affordances in Programming Languages” Slideshare](https://www.slideshare.net/randycoulman/affordances-in-programming-languages)

### John Athayde — The Timeless Way of Building

Patterns. Patterns in nature, human behavior, architecture. Patterns are only truly valuable when used appropriately, which, it is said, requires a certain amount of fluency in the language of patterns. Treating them as “a library of code templates” is a problem, says John. I would agree. Correctly applying design patterns in software development is more than finding a [GoF design pattern](https://en.wikipedia.org/wiki/Design_Patterns) and squeezing your problem through it like so much delicious looking [Play dough](http://www.kraftrecipes.com/recipes/kool-aid-play-dough-148569.aspx).

John discussed patterns using some interesting architectural examples and ran through a number of anti-patterns and their corresponding pattern “solutions” in a helpful before/after format. He touched on a number of such anti-patterns that one might see in the wild; code that walks the object graph a la @account.customer.address.state,) fat models in need of some module, concern, or gem treatment, and ActiveRecord callback soup.

John’s overall takeaway was that memorizing and applying patterns is neither the crux of the matter, nor is it even sufficient. True skill and the mark of proficiency is to be “fluent in the language of patterns.” This reminds me of the difference between being able to speak a foreign language and being able to *think* in that language and seamlessly express those thoughts without a need for intermediate translation.

John’s recommended reading: The Timeless Way of Building, A Pattern Language, The Oregon Experiment, Rails Antipatterns, Design Patterns in Ruby

### Ryan Davis — Nerd Party v3.1

Ryan’s talk covering the various “versions” of the Seattle.rb Ruby user group throughout the years gets an honorable mention because it convinced me to get involved with one of the Ruby user groups here in Salt Lake City.
