---
author: Joe Marrero
title: A Collaborative Timezone Utility
github_issue_number: 1334
tags:
- linux
- open-source
- tools
- c
date: 2017-10-30
---

<div style="float: right; width: 300px; padding: 0 0 1em 1em;">
  <div style="padding: 1em; border: 1px solid #ccc; border-radius: 6px;">
    <h3 style="margin: 0 0 1rem 0;">Try It Out Yourself</h3>
    <p>The code for this project is hosted on <a href="https://github.com/manvscode/timezoner">GitHub and can be cloned from here.</a></p>
  </div>
</div>

At [End Point Corporation](/), our team is spread out across 10 time zones. This gives us the advantage of being able to work around the clock on projects. When one co-worker leaves for day, another can take over. Consider this scenario. It's Monday evening and Martin needs to continue installing software on that Linux cluster, but it's already 6pm and his wife is going to murder him if he's not ready to go out for their anniversary dinner. Let's see who can take over... Ah, yes, Sanjay in Bangalore can continue with the maintenance. Tuesday morning, the client wakes up to be surprised that 16 hours of work was completed in a day. With respect to software development, the same efficiencies can be realized by parallelizing tasks across time-zones. Code reviews and further development can be continued after normal business hours.

With all the blessings of a distributed engineering team, collaborating with co-workers can be, occasionally, challenging. Some of these challenges stem from complexities of our system of time. Every co-worker may be operating in a timezone that is different than yours. Time-zones have an associated offset relative to [Coordinated Universal Time (UTC)](https://en.wikipedia.org/wiki/Coordinated_Universal_Time). These offsets are usually in whole hour increments but they may be any real-valued number.

For example, [Eastern Standard Time (EST)](https://en.wikipedia.org/wiki/Eastern_Time_Zone) has an offset of -5 (five hours behind UTC) and [Indian Standard Time (IST)](https://en.wikipedia.org/wiki/Indian_Standard_Time) has an offset of 5.5 (five and half hours ahead of UTC). Furthermore, these UTC offsets can be completely arbitrary. In 1995, [Kiribati](https://en.wikipedia.org/wiki/Kiribati), an island nation in the Pacific, changed its UTC offset from -10 to +14 so that all of its outlying islands can share the same time. To further complicate things, some regions may not observe [daylight savings time (DST)](https://en.wikipedia.org/wiki/Daylight_saving_time) while other regions do. In fact, in the United States, Indiana started observing DST on April 2, 2006. Some states like Arizona and Hawaii do not observe DST. Other countries, like Australia, have a similar situation where it's left to local governments to decide whether DST is observed or not. Moreover, although DST usually accounts for adding or subtracting an hour of time, it isn't always one hour. This has historically changed from time to time.

Now you may begin to imagine the headaches that arise when you need to coordinate with anything involving multiple time-zones. To make all of this easier, you can use a utility that we wrote to do all the time conversions for you. First, you have to add each co-worker's information to a configuration file stored at ~/.timezoner. This configuration file will describe all of your co-worker's contact information and their associated IANA time-zone. As an example, this is what the configuration file looks like:

```bash
# Timezone            Email                  Name              OfficePhone        MobilePhone
America/New_York      "edward@example.com"   "Edward Teach "   "n/a"              "+1 731 555 1234"
America/New_York      "henry@dexample.com"   "Henry Morgan"    "+1 646 555 5678"  "+1 954 555 5678"
America/New_York      "john@example.com"     "John Auger"      "n/a"              "+1 902 555 1234"
America/Denver        "sam@example.com"      "Samuel Bellamy"  "+1 347 535 1234"  "+1 994 555 5678"
America/Los_Angeles   "william@example.com"  "William Kidd"    "+1 330 555 5678"  "+1 305 555 1234"
America/Los_Angeles   "israel@example.com"   "Israel Hands"    "+1 507 555 1234"  "+1 208 555 5678"
```

Now when I need to coordinate a meeting, I can run the utility with the -T option to see each team member's local time.

<div class="separator" style="clear: both; text-align: center; margin-bottom: 1em;"><a href="/blog/2017/10/a-collaborative-timezone-utility/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="320" data-original-width="1600" height="172" src="/blog/2017/10/a-collaborative-timezone-utility/image-0.png" width="846" /></a></div>

With the -U option, you can display each contact separated in groups based on UTC offset.

<div class="separator" style="clear: both; text-align: center; margin-bottom: 1em;"><a href="/blog/2017/10/a-collaborative-timezone-utility/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" data-original-height="833" data-original-width="1600" height="333" src="/blog/2017/10/a-collaborative-timezone-utility/image-1.png" width="640" /></a></div>

Let us know what you think and if you found this tool helpful.
