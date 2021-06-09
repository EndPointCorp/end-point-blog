---
author: "Ardyn Majere"
title: "Lazy Isn’t Bad: Write Lazy Scripts"
tags: automation, tips
---

![](/blog/2021/06/09/lazy-isnt-bad-write-lazy-scripts/banner.jpg)
[Photo](https://www.pexels.com/photo/woman-in-white-and-blue-striped-dress-shirt-using-laptop-4626344/) by [cottonbro](https://www.pexels.com/@cottonbro)

A quote attributed to Bill Gates says, “I choose a lazy person to do a hard job. Because a lazy person will find an easy way to do it.” Larry Wall’s list of the virtues of a programmer begins with “laziness,” which of course is a particular kind of laziness: the desire to automate things that a human has previously done manually and painstakingly.

It’s a philosophy that is generally good to adopt. Are you doing repetitive tasks that you hate every day? Weekly? At the end of every month? That’s probably a clue that you could take some pain out of your workday. If there’s some task that comes up repeatedly that requires you to fiddle with data which can be automated, even if it’s relatively easy to do manually, why not do it?

There are many ways in which people try to improve productivity. One of the more famous, [Kanban](https://en.wikipedia.org/wiki/Kanban_\(development\)), involves removing work in progress and optimizing flow. While implementing full Kanban is probably more than you want to do, we can do it the lazy way.

The lazy way means you put time and effort into your infrastructure, creating code or scripts that will do the job for you. Many people don’t think they have the time to put some hours into making this work. It is indeed a time sink, but you only write the script once, compared to many many times of doing the job. The time saved in the long run can be immense. Additionally, the job can be done more accurately; less human interaction means less human error.

Look at a few factors: What task is the most boring and repetitive, what task takes the longest, and what task is most easily automatable? Pick one and write a script for it. Don’t make it too fancy; just make something to get the work done. If you find yourself with extra time left over after the next time you do the task, repeat the process and see if you can shave off more time.

While writing this post, I have a particular client and situation in mind, but we’ve seen it play out similarly many times over the years: we have a longstanding client who needs information gathered from a database. The manual process requires a lot of eye-scanning, copying, and pasting individual data items, fiddling with data formats, reformatting ID numbers from one set to another, and so on. While our example scenario is complex and has several different steps where it can fork in different directions, each step is easy to automate on its own.

Part of this task involves copying numbers from a spreadsheet, changing the number format (stripping out excess characters), deduplicating the numbers, applying a database call to those numbers, and writing the success or failure back to the document.

The most time-consuming part was searching through large log files, trying to identify the right string from just the numbers — this was also the easiest part to automate.

While writing a script that could access the spreadsheet and the database might take an hour, writing a script that does the data processing and spits out a database query took perhaps ten minutes, and has easily saved me that long after only a few uses. I also don’t have to worry about getting the call wrong; it’s preformatted for me.

Another part of the task was downloading several files with different extensions from different directories. This didn’t take too long to set up manually, perhaps 30 seconds. But with a script to grab the files for me, it takes five, and only one command instead of downloading five different files by hand.

This customer has had this pop up several times per month, sometimes per week, and would have saved thousands of dollars in fees in the long run — not to mention delays and fuss — if they’d had us write an application so they could self-serve this. Sometimes, you only realise this in hindsight, but that’s no reason to put off biting the bullet now. There are always more iterations of data handling coming in the future.

Of course these smaller scriptlets didn’t automate the whole process completely. But each step was easily done, and the time taken for the whole task is vastly reduced. If something feels too big to automate in one go, but you can see a bit that could be scripted alone, only script that part. It’ll make you feel good about that part every time you fire the script off. And maybe you can find a way to automate another part later. And so on.

Could I have made the task a simple push of the button, or completely hands off, by fully automating it? Probably. But it would take many hours to integrate all the components, and might only save time in the very long term, while the process might change in the mean time. Writing a half-measure helper script to partially automate the process isn’t fully solving the problem, but it’s lazy — in the good way!
