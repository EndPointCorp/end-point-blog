---
author: Josh Williams
title: "LinuxFest Northwest 2019"
tags: conference, linux, open-source, postgres
gh_issue_number: 1522
---

<a href="https://www.linuxfestnorthwest.org/conferences/2019"><img src="/blog/2019/05/03/linuxfest-northwest/LFNW2019.svg" alt="LinuxFest Northwest Logo Creative Commons Attribution-ShareAlike 4.0 International License" /></a>

I’m sitting in an airport, writing this in an attempt to stay awake. My flight is scheduled to depart at 11:59 PM, or 2:59 AM in the destination time zone which I’m still used to. This is the first red eye flight I’ve attempted, and I’m wondering why I’ve done this to myself.

I have dedicated a good portion of my life to free, open source software. I’ll occasionally travel to conferences, sitting on long flights and spending those valuable weekends in talks about email encryption and chat bots. I’ve also done this to myself. But even with all this I have zero regrets.

This little retrospective comes courtesy of my experience at [LinuxFest Northwest](https://www.linuxfestnorthwest.org/conferences/2019) this last weekend in Bellingham, Washington.

Specifically I think it was some of the talks, painting things in broad strokes, that did it. I attended Jon “maddog” Hall’s beard-growing [Fifty Years of Unix](https://lfnw.org/conferences/2019/program/proposals/247), and later sat in on the [Q&A](https://lfnw.org/conferences/2019/program/proposals/344), which was a bit less technical than expected. So I didn’t ask about the “2038 problem.” But that’s okay.

I felt a little guilty, on one hand, doing these general interest sessions instead of something on a much more specific topic, like ZFS, which would have arguably had a more direct benefit. On the other hand, doing those general interest talks helps me stay grounded, I suppose, helps me keep perspective.

I did attend some more specialized talks, naturally. LFNW was a packed conference, often times there were a number of discussions I would have liked to attend happening at the same time. I’m hoping recordings will become available, or at least slides or other notes will appear. Some of the other talks I attended included, in no particular order:

* [Audio Production on Linux](https://lfnw.org/conferences/2019/program/proposals/278)<br>
Like many other End Pointers, I dabble in a little bit of music. Unlike those other End Pointers, I’ve got no talent for it. Still, I try, and so I listened in on this one to find out a little more about how Jack works. I also caught wind of PipeWire, a project that’s aiming to supplant both PulseAudio and Jack. Neat!

* [Using GIS in Postgres](https://lfnw.org/conferences/2019/program/proposals/179)<br>
I’ve got a couple PostGIS-related projects coming up. So while this talk covered a few of the basics and some query types and didn’t touch much on indexing and such, it was still good to see. Plus it got me in place for mine.

* [Chat Ops](https://lfnw.org/conferences/2019/program/proposals/191)<br>
Internally we have a few scripts that connect in to our chat system and write status messages. But it’s all one-way communication, like alerts from our monitoring system. This talk proposed writing bots that can watch for and process messages written by others, and take actions. We could, for example, acknowledge alerts or set systems into downtime without having to switch out of the chat system. I want to look into options like that for sure.

* [We can fix email server encryption!](https://lfnw.org/conferences/2019/program/proposals/337)<br>
End Point (thankfully) is on the verge of turning down its internal email systems. But the current trouble with server-to-server email encryption was still valuable to learn about!

Yeah, I did one, too: [Get It Back, A New PostgreSQL Admin’s Guide to Redundancy and Recovery](http://lfnw.org/conferences/2019/program/proposals/327). I talked about the different methods of performing backups of a Postgres database, and the advantages and drawbacks of each. Plus a little about replication. The slides are up [here](https://joshwilliams.name/get-it-back/), but admittedly only about half the material is there, the rest would have been me talking at the slides. I’ll write it up in a subsequent post, promise. Afterward I stuck around to sit in on the [Consult the Experts](https://lfnw.org/conferences/2019/program/proposals/331) panel.

Plus my talk was attended by two other End Pointers, Greg Davidson and Greg Hanson. No pressure there.

But seriously, that was an added bonus. Being a distributed company much of the time our coworkers are right at our fingertips in one sense, but in another also out of reach. Getting that face time was very nice. LFNW had a couple general social activities, too, on Friday and Saturday. And of course I attended both, talking about Nagios and Haskell and Docker and anything else that came to mind. Florida to Washington was a long hike, but it was well worth it.

All that said, I do have one lingering regret: By the time I figured out *that* there were tie-dye shirts, a trademark of this conference, and *where* they were, they were all gone. Oh well. Next year.
