---
title: "Backing up your SaaS data with Google Takeout"
author: Seth Jensen
date: 2022-05-31
github_issue_number: 1867
tags:
- backups
- saas
---

![A concrete building with rectangular windows at sunset](/blog/2022/05/backing-up-your-saas-data-with-google-takeout/banner.webp)

Keeping backups is extremely important.

Losing important files can feel like a far-off problem, but the chance of misplacing a drive, theft, drive failure, accidental deletion, house fire, flood, etc., is much greater than we may think. The benefits outweigh the cost of backups, for files that matter at all. So everyone should make regular backups of data that they care about and that can't be replaced.

Even among people who regularly make backups, there is one area many of us neglect: all of that data on various online services, also called software as a service or SaaS: Google Drive, Apple iCloud, Microsoft OneDrive, Dropbox, Box, etc.

It's true, the most volatile files are the ones sitting in a single location on your laptop or thumb drive, not those on Google, WordPress, or iCloud servers. The danger of losing files is not nearly as present with SaaS. You can't drop Google on the floor and lose a couple terabytes of data, like you can a hard drive, but you can be locked out of your account, accidentally delete files, and lose data by missing a notice about a service shutting down. Not to mention the possibility that your SaaS provider is hacked and loses your data.

I recently realized I had about five years of photos, nine years of Google Drive "stuff," and who knows what else, not backed up from my Google account. I decided to download it all with Google Takeout, the service Google provides for making account backups.

### Google Takeout

Google introduced Takeout in 2011 as a service to export and download your data stored in Google products. It seems like the perfect option to easily back up all your files from Google's servers. But how is the process, and how useful is the actual downloaded data?

[Downloading from Takeout](https://support.google.com/accounts/answer/3024190?hl=en) is quite painless. You select the services you want to back up, the formats you want them in (when there are multiple options), and start an export. When it's ready, you get an email linking to a compressed file containing your data. You can export either to a `.zip` archive or a `.tgz` (`.tar.gz`) archive. Zip is more universally accessible, so if you don't have or want extra software (such as 7-Zip), it is probably the better option.

One of the hardest things about keeping SaaS backups, even when they are easy to manage, is just remembering to do it. Backups become less useful if they're six months or even years out of date.

Fortunately, Google Takeout has an option to automatically create a new full export 6 times over the course of a year and email you a download link. I'm not great at remembering to renew backups, so I'm letting them email me every two months with a new export. This is a more important feature than I originally thought, as researching for this post dragged on over nearly two months, despite feeling like I had very recently backed my files up.

One concern I've had with downloading SaaS data is whether it could be used in other apps, or imported again. I would prefer that my backups aren't buried among thousands of lines of cruft. So I'd like to dive into the data and get a feel for how useful it would be if I actually needed it.

### How useful is the exported data?

Most of Google Takeout's data is reasonably well organized and usable — YouTube videos in MP4, calendars in ICS, photos in JPEG sorted by year as well as albums you've created. But there is plenty of inefficiency, and a few gotchas you need to watch for.

For some services, like Google Drive, you can select between a common usable format (DOCX for Docs, XLSX for sheets, etc) and a PDF render. There's not a ton of variety in choices, but the formats are generally common enough that you could easily open them in your program of choice.

My download came in three `.tgz` files, two around 50GB and one around 5GB. That's not awful, despite some odd choices on Google's part for space management. For example, Google Keep exports in a nice, usable JSON format, but also in HTML with a huge `style` tag. My JSON takes 500KB, while the HTML takes 1500KB. Luckily they don't seem to do this with YouTube, Google Photos, or Drive, or else I would be more concerned about bloat.

Some exports are somewhere in the middle, like YouTube playlists, which only include the ID of the YouTube video. Helpful in the case of losing your account, but not so much if any of those videos are deleted from YouTube.

### What does Takeout exclude?

Takeout includes most of the data you would care about: Gmail (in MBOX format, including attachments), Google Photos, Blogger, saved Maps places, your uploaded YouTube videos, etc. You can see a full list of services and formats in [Takeout itself](https://takeout.google.com/settings/takeout).

A major flaw with Takeout is that it only backs up data you are the owner of. That means that, for example, if a co-worker creates a document with nothing but a title and invites you to help work on it, you may have added dozens of pages of painfully earned writing, but Takeout doesn't consider it yours, so it won't get exported. You have to manually save your own copy, separately, for every shared file.

Sharing is one of the most useful things about Google's SaaS options, so not having shared files backed up could largely defeat the purpose of the backup. You can download shared files separately, but any added effort to make a complete backup quickly becomes a hassle, and defeats part of the purpose of using Takeout.

Be on the lookout for shared files that might not be backed up. For me, that's mostly Drive, Photos, and Calendar, but pay attention to other shared files you may want backed up.

While the data exports aren't perfect, the potential loss is so great that finding some way to back up SaaS data is a no-brainer.

Signing off with an image I found in my Blogger backup: my initials, created using the GIMP, circa 2009.

![S. R. J. initials with artificial sun background](/blog/2022/05/backing-up-your-saas-data-with-google-takeout/srj.jpg)
