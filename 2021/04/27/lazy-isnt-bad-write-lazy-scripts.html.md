---
author: "Ardyn Majere"
title: "Lazy isn't bad- write lazy scripts."
tags: Automation, scripting
---
Bill Gates has famously said "I choose a lazy person to do a hard job. Because a lazy person will find an easy way to do it." Larry Wall’s list of the virtues of a programmer includes "laziness", which of course is a particular kind of laziness: The desire to automate things that a human has previously done manually, painstakingly.

It’s a philosophy that is generally good to adopt. Are you doing repetitive tasks that you hate every day? Weekly? End of the month? It’s probably a clue that it might be a good idea to take some pain out of your workday. If there's some task that comes up repeatedly that requires you to fiddle with data in some way that's possible to automate, even if it's relatively easy to do manually - why not do it? 

The lazy way means you put time and effort into your infrastructure - creating code or script that will do the job for you. Many people don’t think they have the time to put some hours into making this work. It is indeed a time sink - but you only do this one time, compared to many many times of doing the job. The time saved in the long run can be immense. Additionally, the job is done more accurately - less human interaction means less human error.

When writing this blog, I have a particular client and situation in mind, but we’ve seen it play out similarly many times over the years: We have a longstanding client who needs information gathered from a database. The manual process requires a lot of eye-scanning, copying and pasting individual data items, fiddling with data formats, reformatting ID numbers from one set to another; and while it had several different stages where the task forked in different directions depending on the result of earlier tasks, each step was easy to automate on its own.

Part of this task involves copying numbers from a spreadsheet, changing the number format (stripping out excess characters), deduplicating the numbers, applying a database call to those numbers, and writing the success or failure back to the document.

While writing a script that could access the spreadsheet and the database might take an hour, writing a script that does the above and spits out a database query that can then be pasted in to the database took perhaps ten minutes, and has easily saved me that long in only a few times of working through the task- and I don't have to worry about getting the call wrong- It's preformatted for me.

Another part of the task was downloading several files from different directories that had different extensions- This didn’t take too long to set up manually, perhaps 30 seconds, but now with a script that goes out and grabs the files for me, it takes five, one step instead of copying out .

This customer has had this pop up several times a month, sometimes several times a week, and would have saved thousands of dollars in fees in the long run, not to mention saving themselves delays and fuss,  if they’d had us write an application so they could self-serve this. Sometimes, you only realise this in hindsight - but that’s no reason to put off biting the bullet now. There’s always more iterations of data handling coming in the future.

Of course these smaller scriptlets didn’t automate the whole process completely. But each step was easily done, and the time taken for the whole task is vastly reduced. If something feels too big to automate in one go, but you can see a bit that could be scripted - script just that. It will make you feel good about that part every time you fire the script off. And maybe you can find a way to automate another part later. And so on.

Could I have made the task a simple push of the button, or completely hands off, by fully automating it? Probably. But the time it would take to integrate all the components would be quite a few hours, and I don't know if it would save that much time except in the very long term - and the process might change in the meanwhile. Writing a half measure helper script to partially automate the process isn’t fully solving the problem, but it’s lazy - in the good way!

