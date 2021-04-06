---
author: "Ardyn Majere"
title: "Lazy isn't bad- write lazy scripts."
tags: Automation, scripting
---

Bill Gates has famously said “I choose a lazy person to do a hard job. Because a lazy person will find an easy way to do it.” Larry Wall’s list of the virtues of a programmer includes “laziness”, which of course is a particular kind of laziness: The desire to automate things that a human has previously done manually, painstakingly.

So take some pain out of your day. If there's some task that's come up repeatedly in the last month that requires you to fiddle with data in some way that's quick and dirty to automate, even if it's easy to do manually, do it.

Be lazy. Take the possibility of errors out of your work and just enjoy the feeling of a machine doing the task for you, and do it in whatever language you're most versed in- Make it quickly.

This is a story about one particular client and situation, but we’ve seen it play out similarly many times over the years.

We have a longstanding client who needs information gathered from a database. The manual process requires a lot of eye-scanning, fiddling with data, reformatting ID numbers, and while it had several different stages where the task forked in different directions depending on the result of earlier tasks, each step was easy to automate on its own.

This customer has had this pop up several times a month, sometimes several times a week, and would’ve saved thousands of dollars and plenty of time and fuss if they’d had us write an application so they could self-serve this- Though of course, knowing that is only possible the benefit of hindsight.

Part of this task involves copying numbers from a spreadsheet, changing the number format (stripping out excess characters) deduplicating the numbers, applying a database call to those numbers, and writing the success or failure back to the document.

While writing a script that could access the spreadsheet and the database might take an hour, writing a script that does the above and spits out a database query that can then be pasted in to the database took perhaps ten minutes, and has easily saved me that long in only a few times of working through the task- and I don't have to worry about getting the call wrong- It's preformatted for me.

Another part of the task was downloading several files from different directories that had different extensions- This didn’t take too long to set up manually, perhaps 30 seconds, but now with a script that goes out and grabs the files for me, it takes five, one step instead of copying out .

Could I have made the task a simple push of the button, or completely hands off, by fully automating it? Probably- but again, the time it would take to integrate all the components would be quite a few hours, and I don't know if it would save that long. 

Writing a half measure helper script isn’t fully solving the problem, but it’s lazy- in the good way.
