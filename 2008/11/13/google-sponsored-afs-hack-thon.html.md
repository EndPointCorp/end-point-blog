---
author: Max Cohan
gh_issue_number: 75
tags: openafs, git, community, conference
title: Google Sponsored AFS Hack-A-Thon
---

Day One:

Woke up an hour early, due to having had a bit of confusion as to the start time (the initial email was a bit optimistic as to what time AFS developers wanted to wake up for the conference).

Met up with Mike Meffie (an AFS Developer of [Sine Nomine](https://www.sinenomine.net/)) and got a shuttle from the hotel to the ‘Visitors Lobby’; only to find out that **each building** has a visitors lobby. One neat thing, Google provides free bikes (beach cruisers) to anyone who needs them. According to the receptionist, any bike that isn’t locked down is considered public property at Google. However, it’s hard to pedal a bike and hold a briefcase; so off we went hiking several blocks to the correct building. Mike was smart enough to use a backpack, but hiked with me regardless.

The food was quite good, a reasonably healthy breakfast including fresh fruit (very ripe kiwi, and a good assortment). The coffee was decent as well! After much discussion, it was decided that Mike & I would work towards migrating the community CVS repository over to Git. Because Git sees the world as ‘patch sets’ instead of just individual file changes, migrating it from a view of the ‘Deltas’ makes the most sense. The new Git repo. (when complete) should match 1:1 to the Delta history. There was a good amount of teasing as to whether Mike and I could make any measurable progress in 2 days. Derrick was able to provide pre-processed delta patches and the bare CVS repo. (though we spent a good amount of the day just transferring things around and determining what machine should be used for development).

Lunch (rather tasty sandwiches) and after lunch snacks were provided; Google definitely doesn’t skimp on the catering. Made good progress for one day of combined work, we now have a clear strategy for processing the deltas and initial code that is showing strong promise. Much teasing ensued that Mike & I should not be allowed to eat if we did not have the Git repo. ready for use. Dinner was a big group affair of food, beer, and Kerberos.

Day Two:

After arriving with Mike Meffie via the shuttle, we found out that Tom Keiser (also of Sine Nomine) had been left behind! The shuttle driver was kind enough to go pick up Tom (who ended up at a related, but **different** hotel than the conference recommended) and bring him for questioning (or development, as the case may be). Determined that the major issue in applying the deltas was simply due to inconsistencies in what the ‘base’ import should consist of... After several rounds of cleanup, all but a few of the deltas (and those were fixed by hand) applied cleanly!

On the food side, Google outdid itself with these cornbread ‘pizzas’ that were extremely good. Once we started having a few branches to play with, things came together quickly... generating much buzz and excitement (at least, for us). We all split off for dinner, with a few of us escorting Tom to his train then getting some Indian food (on a rather busy day, as it was the ‘Festival of Lights’).

In Conclusion:

We were able to get a clean specification **with consensus** for how we want to produce the public Git repository. The specifications are even available on the [OpenAFS wiki](https://www.dementia.org/twiki/bin/view/AFSLore/OpenAFSCVSToGitConversion). The tools (found at ‘/afs/sinenomine.net/public/openafs/projects/git_work/’) to produce this repo. are all in a rough working form, with only the ‘merge’ tool still needing some development effort. All of these efforts were definitely facilitated by Google providing a comfortable work environment, a solid internet connection and good food to keep us fueled through it all.

Things to do now:

- Clean up and document the existing tools
- Improve the merge process to simplify folding the branches
- Actually produce the Git repository
- Validate the consistency of the Git repository against the CVS repository
- Determine how tags are to be ported over and apply them
- Publish repo. publicly
