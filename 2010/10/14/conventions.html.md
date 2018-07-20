---
author: Jon Jensen
gh_issue_number: 368
tags: tips
title: Conventions
---

Written and spoken communication involve language, and language builds on a lot of conventions. Sometimes choosing one convention over another is an easy way to reduce confusion and help you communicate more effectively. Here are a few areas I’ve noticed unnecessary confusion in communication, and some suggestions on how we can do better.

### 2-dimensional measurements

Width always comes first, followed by height. This is a longstanding printing and paper measurement custom. 8.5” x 11” = 8.5 inches wide by 11 inches high. Always. Of course it never hurts to say specifically if you’re the one writing: 8.5” wide x 11” high, or 360px wide x 140px high.

If a third dimension comes into play, it goes last: 10” (horiz.) x 10” (vertical) x 4” (deep).

### Dates

In file names, source code, databases, or spreadsheets, use something unambiguous and easily sortable. A good standard is [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601), which orders dates from most significant to least significant, that is, year-month-day, or YYYY-MM-DD. For example, 2010-01-02 is January 2, 2010. If you need to store a date as an integer or shave off 2 characters, the terser YYYYMMDD is an option with the same benefits but a little less readability.

For easier human reading, try “2 January 2010”, “2 Jan. 2010”, or “January 2, 2010”, which don’t sort easily but are still unambiguous. The most confusing form in common use is 1/4/08 or 01/04/08, which is ambiguous whenever the year of century or the day of month are 12 or less. That’s almost half of every month, and the first dozen years of each century! I’ve seen people mean by 01/04/08 any of April 8, 2001; April 1, 2008; or more commonly in the U.S., January 4, 2008. By avoiding this form entirely, you avoid a lot of confusion.

### Time zones

When dealing with anyone who isn’t at the some location you are, specify a time zone with every time. It’s easy. So many of us travel or interact with people in remote locations that we shouldn’t assume a single time zone.

You can save others some mental strain by translating times into the time zone of the majority of other participants, especially if there’s an overwhelming majority in one particular time zone. It’s polite.

In time zones, the word “standard” isn’t just filler meaning “normal time zones”—​it specifically means “not daylight saving time”! So don’t say “Eastern Standard Time” unless you really mean “Eastern Time outside of daylight saving”, referring to somewhere that doesn’t observe daylight saving time. It’s simplest and most often correct in conversation to just say “Eastern Time”. When people say “*Something* Standard Time” but daylight saving time is in effect, beware, because they probably actually just mean “*Something* Time, either daylight or not, whichever is in effect then”. It’s good to ask them and confirm what they meant.

Just to keep things interesting, the “S” doesn’t always mean “standard”. [British Summer Time](https://en.wikipedia.org/wiki/British_Summer_Time) is the British daylight saving time zone and is abbreviated BST.

### Close of business

I find it better to avoid the terms “end of business day” or “close of business” because people often stop working at different times, and most of us communicate with people in many time zones. Why not just say what time you really mean?

Likewise, “by the end of the week” is ambiguous both about what time on the last day, and which day you consider the end of the week. The end of the work week? Whose work week? European calendars show Sunday as the end of the week, while American calendars most often show Saturday as the end of the week. Again, by just saying which day you mean, you can avoid causing confusion.

-----------

What conventions have you found helpful or harmful in communication?
