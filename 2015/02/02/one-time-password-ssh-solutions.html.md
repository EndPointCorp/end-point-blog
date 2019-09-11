---
author: Greg Sabino Mullane
gh_issue_number: 1083
tags: chrome, security, ssh
title: One-time password SSH solutions
---

<div class="separator" style="clear: both; float:right; text-align: center; margin-bottom: 1.5em; margin-left: 3em; margin-right: 2em; "><a href="/blog/2015/02/02/one-time-password-ssh-solutions/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-left: 1em;"><img border="0" src="/blog/2015/02/02/one-time-password-ssh-solutions/image-0.jpeg"/></a><br/><small>[how encryption was done in the 18th century]</small></div>

In a [previous article](/blog/2015/01/21/ssh-one-time-passwords-otpw-on) I explained how I used a one‑time password system to enable SSH on my Chromebook. While this is still working great for me, there are a few problems that can pop 
up.

### Problem 1: Tripping the alarm

Normally a single password is asked for when logging in using one-time passwords via the [otpw program](https://www.cl.cam.ac.uk/~mgk25/otpw.html). However, otpw will issue a three‑password prompt when it thinks someone may be trying to perform a race attack (in other words, it think two people are trying to log in at once). The prompt will change from the normal one to this:

```
Password 206/002/011:
```

This alarm can be tripped from SSH timing out, or from getting pulled away from your computer mid‑login. In theory, it could be someone trying to break in to my laptop, but that is very unlikely. Needless to say, trying to squint at a paper and keyboard in the dark is hard enough with one password, much less three! It’s usually much easier (in most cases) for me to walk to my laptop and remove the **~/.otpw.lock** file, which will clear the “intruder alarm” and cause otpw to prompt for a single password again. Another solution is to set a timeout on clearing the lock, for example via a cronjob that removes the lock file if it was created more than 10 minutes ago. Finally, it may be helpful to have a way to remotely clear the lock. I’ve not written it yet, but one good approach would be to use [port knocking](http://portknocking.org/) to remove the lock file.

### Problem 2: Lost or compromised passwords

The physical sheet of paper containing your one‑time passwords is definitely a single point of failure—​but an easy one to remedy. Maybe you lost the paper, maybe your arch‑nemesis stole it, or maybe it got destroyed in a freak hunting accident. No worries at all, just generate a new one! Run the otpw‑bin command again:

```
$ otpw-gen -e 30 | lpr
```

When you do so, the old **~/.otpw** file is completely overwritten, and the old sheet of paper is now completely worthless. Solutions don’t get any easier than that. If your sheet is stolen and you need to quickly disable one‑time passwords, you can also just manually remove the .otpw file, which effectively turns off one‑time passwords for that account.

### Problem 3: Unusable passwords

The password to use for login is randomly determined, so one time you may be asked to look up password 312 and the next 031. Sometimes, however, you cannot use one of the passwords on your printout. Perhaps you spilled something on it. Perhaps (as has happened to me!) the paper was folded in such a way that the crease made it difficult to read the characters. Perhaps your keyboard has a really hard time typing a certain letter. :) Whatever the reason, there are two solutions. First, generate a new sheet by rerunning otpw‑bin as described in Problem 2 above. Second, you can mark the current password as “complete” and have otpw move on to the next number.

Forcing otpw to advance to the next number is slightly tricky. Basically, you need to modify the .otpw file and change the current password hash to a line of hyphens. Here is what the top of a .otpw file looks like after 3 successful logins:

```
OTPW1
392 3 12 5
---------------
---------------
---------------
077jA:EAgMCJ2uM
097yG3IDv%gyUB7
1077T7EQq%K7E/F
101xeS3I+zMw8GZ
109xCEBXYFb3%3v
121AzwjOJYyBqD%
068WewLA3EIsLmx
065Jdq=2WDwHZ9D
089npYNavK9MIVA
```

The first line states the format of the file, while the second line indicates the number of passwords generated, the digits per password number, the digits in the hash, and the digits in the actual passwords. All the other lines are passwords—​either an unused one consisting of the number and the hash, or a line of hyphens. The goal is to replace the current password with hyphens. Here’s a quick recipe to do so:

```
perl -ni -e 'print unless /^\d\d\d\S/ and ! $x++' ~/.otpw
```

We do an in‑place edit (**-i**) of the .otpw file, looping through a line at a time (**-n**), and run a command against each line (**-e ...**). The first time we find a line that starts with three numbers and then contains non‑whitespace, we skip it. Everything else is printed and thus goes back into the file.

Those are some ways to handle three of the common problems that can occur when using one‑time passwords. Have other problems, or better solutions to the above? Let me know in the comments.
