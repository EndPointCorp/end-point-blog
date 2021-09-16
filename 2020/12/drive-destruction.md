---
author: Ardyn Majere
title: Media erasure in the time of SSD
github_issue_number: 1705
tags:
- security
- storage
date: 2020-12-10
---

![](/blog/2020/12/drive-destruction/garbage.jpg)
[Photo](https://www.pexels.com/photo/garbage-lot-2967770/) by [Alex Fu](https://www.pexels.com/@alexfu) from Pexels

How valuable is your data? Losing it to a third party is usually a business’s worst nightmare—​and can cause legal or even criminal repercussions, depending on the drive’s contents and the business’s jurisdiction.

Every system adminstrator worth their salt knows that running “rm” (or equivalent delete operations) doesn’t actually remove data, it simply removes the file name from the filesystem and leaves the data in place on the disk.

When dealing with traditional storage, destroying (intentionally or otherwise) your data used to be relatively easy. A wise system admin could simply run:

```bash
shred /dev/sda
```

And be fairly certain of the result. A cautious one might run a demagnetizing wand over the drive. Only the most paranoid might destroy it physically.

### The Age of SSDs

Nowadays, most servers have switched away from storing data on rotating metal or glass platters. Solid state drives, or SSDs, are faster, less prone to errors from physical impact, and generally more sought after.

SSDs have issues with speed if the drives are too full, and have a limited lifespan—​only a certain number of write operations can be achieved. This is less of an issue with modern drives thanks to wear leveling built into the firmware of the drives. However, this leads to some issues as well.

### Complicated systems introduce issues

Because SSDs manage which blocks of storage they write to, a simple shred won’t do. There could be hundreds of bytes, or even kilobytes or megabytes, of data that the shred doesn’t reach.

Even some “traditional” storage can run into such issues these days. Hybrid drives offer some speed advantages: By leveraging a small amount of SSD storage, these drives save data to SSD first, then write it at slower speeds to the actual magnetic platters. The same issues with SSD storage can affect this cache of data.

So how to be sure?

Ideally, I would recommend using a combination of methods for security. Here are the main methods that are used at present:

### Run shred and hope for the best

This is an option, for sure. Writing to every block of the disk will generally wipe the data securely enough. However, if there are sectors that have been marked bad by the drive firmware, these won’t be covered.

### nwipe, DBAN, and other free options

Free software exists to securely run shred over operating systems. The old gold standard for this was Darik’s Boot and Nuke (DBAN), written by Darik Horn, but this software was acquired by Blancco, a for-profit data erasure company (more on them later). DBAN is [still available](https://dban.org/), but lacks features necessary for a 100% wipe.

A fork called [nwipe](https://github.com/martijnvanbrummelen/nwipe) exists, and is available on many live operating systems. nwipe does a more thorough job than shred, but it still can’t get to sectors the firmware hides from the operating system.

Wikipedia has a [list of data-erasing software](https://en.wikipedia.org/wiki/List_of_data-erasing_software). Most of these are open source or freeware, but it includes a few paid options.

### SATA secure erase with hdparm

Drive manufacturers have thought of this issue as well. Most drive manufacturers offer a secure erase program that works with their drives, and the [SATA](https://en.wikipedia.org/wiki/Serial_ATA) standard has a procedure in place for [securely erasing drive contents](https://ata.wiki.kernel.org/index.php/ATA_Secure_Erase).

```bash
hdparm --user-master u --security-set-pass TheEnd /dev/X
hdparm -I /dev/X  # Check that the master password is enabled
time hdparm --user-master u --security-erase TheEnd /dev/X
```

This will show some output indicating success or failure. Once this is done…

```bash
hdparm -I /dev/X  # Check that the master password is not enabled, which indicates the wipe was successful
```

This is likely the best option for a savvy home user, combined with shred/​nwipe. However, if you are going to attempt this, I highly recommend [reading the full instructions](https://ata.wiki.kernel.org/index.php/ATA_Secure_Erase)!

### Commercial software

Blancco, aforementioned as the purchasers of DBAN, offer an enterprise level product for destroying data called [Drive Eraser](https://www.blancco.com/products/drive-eraser/). Importantly, for business users, it provides certification that the data are gone for good.

There are also many other options. Ask your favourite security vendor and they will be happy to sell you a product for this, though you usually have to take them at their word.

### Be prepared—​encrypt your disk!

Encrypt your disk. This can be achieved by encrypting either your home folder or by encrypting your whole disk. One downside is that your password is required after every reboot—​a problem especially for servers, but even cloud providers offer virtual terminals these days, so for secure operations, this is the best option.

A secure, long password is usually enough to ensure the disk can’t be cracked, though be aware that cybersecurity changes quickly—​what’s impossible to brute-force today might not be in five years.

So how can we be really, really sure?

### Thermite

Physical destruction of the media is always the most secure way to destroy a disk—​crushing, drilling, or in the fanciful, dangerous dreams of some systems administrators, covering the disk in thermite and lighting it with a magnesium flare. **(Do not actually use thermite.)**

At home, [disassembling the drive](https://www.myfixguide.com/samsung-860-pro-ssd-teardown/) and taking a hammer to the data bearing chips will do the trick, though again, combine this with the above options to be sure.

For spinning disks, a similar procedure is advised, though there are other options, of course…

![a drive with several slugs embedded in it](/blog/2020/12/drive-destruction/drive_destruction.jpg)

>*Check your local laws and follow all safety procedures before engaging in creative drive destruction techniques!*

### Final thoughts

Use any or all of the above options and you’ll be ahead of the game. Taking the time to sanitize your data, or better, encrypting it from the beginning, is always a good investment.
