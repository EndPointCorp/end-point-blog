---
author: "Ardyn Elisabeth Majere"
title: "Media erasure in the time of SSD"
tags: ssd, dban, security, storage, media, dd
---
How valuable is your data? Losing it to a third party is usually a business's worst nightmare- and can cause legal, or even criminal repercussions depending on what the data are and what jurisdiction is.

Every system adminstrator worth their salt knows running 'delete' doesn't actually remove data- It simply removes the file from the filesystem and leaves the data in place on the disk. 

When dealing with traditional storage, knowing you've (intentionally) destroyed your data used to be relatively easy. A wise system admin could simply run:
```
shred /dev/sda
```

And be fairly certain of the result. A cautious one might run a demagnetizing wand over the drive. Only the most paranoid might destroy it physically.

## The Age of SSD.

Nowadays, most servers have switched away from storing data on rotating metal or glass platters. Solid state drives, or SSD, are faster, less prone to errors from physical impact, and generally more sought after. 

They have issues when it comes to speed if the drives are filled up too far, and have a limited lifespan- only a certain number of read/write operations can be achieved, though with modern drives this is less of an issue due to wear leveling built in to the firmware of the drives.

This very invention, however, is the source of some issues.

### Complicated Systems Introduce Issues, Sometimes.
Because SSDs manage which blocks of storage they write to, a simple shred won't do. There could be hundreds of bytes, or even kilobytes or megabytes, of data that the shred doesn't reach.

Even some 'traditional' storage can run in to issues these days- hybrid drives offer some speed advantages, by leveraging a small amount of SSD storage, these drives save data to SSD first, then write it at slower speeds to the actual magnetic platters. The same issues with SSD storage can affect this cache of data.

So how to be sure?

Ideally, I would recommend using a combination of these methods for security, but here's the main methods that are used at present.

### Run Shred and Hope for the Best.

This is an option, to be sure. Writing to every block of the disk will generally wipe the data securely enough- however if there are sectors that have been marked bad by the drive firmware, these won't be accessible. 


### nwipe / Darik's Boot and Nuke (DBAN) / Other Free Options

Free software exists to securely run shred over operating systems. The old gold standard for this was called DBAN, written by Darik Horn, but this software was acquired by [Blancco](https://www.blancco.com/products/drive-eraser/). 

A fork called [nwipe](https://github.com/martijnvanbrummelen/nwipe) exists, and is available on many live operating systems.

Nwipe does a more thorough job than shred, though it still can't get to sectors the firmware isn't showing the operating system.

Wikipedia has a [list of data-erasing software[(https://en.wikipedia.org/wiki/List_of_data-erasing_software), most of these are freeware, though it includes a few paid options.

### SATA Secure Erase with hdparm.

Clearly, drive manufacturers have thought of the issue. Most drive manufacturers offer a secure erase program that works with their drives, and the [SATA protocol](https://en.wikipedia.org/wiki/Serial_ATA) standard has a procedure in place for [securely erasing drive contents](https://ata.wiki.kernel.org/index.php/ATA_Secure_Erase).

``` 
hdparm --user-master u --security-set-pass TheEnd /dev/X

hdparm -I /dev/X #ensure the master password is enabled

time hdparm --user-master u --security-erase TheEnd /dev/X
```

This will show some output indicating success or failure. Once this is done... 

```
hdparm -I /dev/X #ensure password now says not enabled  
   # This should indicates the wipe was succesfull.

```

This is likely the best option for a savvy home user, combined with shred/nwipe- However, if you are going to attempt this- I highly recommend [reading the full instructions](https://ata.wiki.kernel.org/index.php/ATA_Secure_Erase)!

### Commercial Software

Blancco, aforementioned as the purchasers of DBAN, offer an enterprise level product for destroying data- More importantly, for business users, it provides certification that the data are gone for good.

There are also many other options- ask your favourite security vendor and they will be happy to sell you a product for this- Though you usually have to take them at their word.

### Be Prepared- Encrypt your Disk!

Encrypt your disk. This can be achieved by encrypting either your home folder or by encrypting your whole disk. There are downsides- after a reboot, you will need someone to type the password in- a problem for servers, but even cloud providers offer virtual terminals these days, so for secure operations,s this is the best option.

With a secure, long password, this is usually enough to ensure the disk can't be cracked- though always be aware that encryption is always moving on- what's impossible to brute-force today won't be in five years.

So how to really, really be sure?

### Thermite.

Physical destruction of the media is always the most secure way to destroy a disk. Crushing, drilling, or in the fanciful, dangerous dreams of some systems administrators, covering the disk in thermite and lighting it with a magnesium flare.

***(Do not actually use thermite.)***

For the home, [disassembling the drive](https://www.myfixguide.com/samsung-860-pro-ssd-teardown/) and taking a hammer to the data bearing chips will do the trick, though again, combine this with the above options to be 100% sure.

For spinning disks, a similar procedure is advised, though there are other options, of course...

![Check your local laws and follow all safety procedures before engaging in creative drive destruction techniques! (depicted- a drive with several slugs embedded in it](/2020/12/05/drive_destruction/drive_destruction.jpg)

### Final thoughts.
Use any or all of the above options and you'll be ahead of the game. Taking the time to sanitize your data- or better, taking the time to encrypt it to begin with, is almost always a good investment.