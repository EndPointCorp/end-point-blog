---
author: Steph Skardal
title: 'Merging Two Google Accounts: My Experience'
github_issue_number: 681
tags:
- tools
date: 2012-08-21
---

Before I got married, I used a Gmail account associated with my maiden name (let's call this account A). And after I got married, I switched to a new gmail address (let's call this account B). This caused daily annoyances as my use of various Google services was split between the two accounts.

Luckily, there are some services in Google that allow you to easily toggle between two accounts, but there is no easy way to define which account to use as the default for which service, so I found myself toggling back and forth frequently. Unfortunately, Google doesn't provide functionality to merge multiple Google accounts. You would think they might, especially given my particular situation, but I can see how it's a bit tricky in logically determining how to merge data. So, instead, I set off on migrating all data to account B, described in this email.

### Consider Your Google Services

First things first, I took at look at the Google Services I used. Here's how things broke down for me:

- Gmail: Account A forwards to account B. I always use account B.
- Google+: Use through account A.
- Google Analytics: Various accounts divided between account A and account B.
- Blogger: Use through account A.
- Google Calendar: Various calendars split between account A and account B.
- Google Documents: Various documents split between account A and account B.
- Google Reader: Don't use.
- Google Voice: Use through account B.
- YouTube: Don't use (other than consumption).

After reviewing this list, I determined I would have to migrate Google+, several Google Analytics accounts, Blogger, Google Calendar, and Google Documents. I set off to look for various directions for merging or migrating data, broken down below.

### Google+

Google Plus was easy to migrate. I followed the directions described [here](http://www.rabbibob.com/index.php/Migrating_Google_Plus_Accounts), which essentially involves sharing circles from account A to account B and then importing circles in account B. It was quick and easy.

### Google Analytics

Google Analytics was a little more time consuming. In all accounts assigned to account A, logged in as account A, I added account B as an **Admin** user. Then, I logged in as account B, downgraded account A to a regular user from admin and deleted account A. Note that you must downgrade an account before you are allowed to delete the user, from my experience.

### Blogger

To migrate Blogger account settings, I invited account B to a blog logged in as account A in browser #1. In browser #2, I logged in as account B and accepted the invitation. In browser #1, I gave account B admin access logged in as account A. After verifying account B admin access in browser #2, I went back to browser #1 and removed account A from the blog. I repeated these steps until I had transitioned all blogs.

### Google Documents

The Google Documents migration was by far the most time consuming data migration for all the services. [This article from Lifehacker](http://lifehacker.com/5602545/how-to-migrate-your-entire-google-account-to-a-new-one) says, "If you're migrating to a regular Google account, transferring your Google Docs is easy. Just select all the documents you want to migrate, go to the More Actions drop down menu, and choose Change Owner. Type in Account 2's address in the box that comes up. You'll see all your documents in Account 2." For about 50% of the documents owned by account A, I was able to change the owner under the shared options from account A to account B.

But for an unexplained reason, I was not allowed to re-assign the owner for the remaining documents. I couldn't find any explanation why this was the case. So, I migrated the data by brute force: I downloaded the remaining data owned by account A's account, and uploaded it as account B. This was irksome and time consuming, but it was my last step in finishing the migration!

### Associated Email Accounts

One quick change I had to make here was to remove my End Point email association with account A and add it to account B, so that any documents shared with my End Point email address would be visible by account B. This was done under Google Account Settings.

### Conclusion

The time spent on the account migration was worth it, in retrospect! There are many available resources for merging other Google Services if you find yourself in a similar position. Google it ;)
