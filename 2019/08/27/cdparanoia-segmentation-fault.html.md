---
author: Jon Jensen
title: "Fix for cdparanoia segmentation fault"
tags: tips, open-source, audio
gh_issue_number: 1551
---

<img src="/blog/2019/08/27/cdparanoia-segmentation-fault/5845424017_740bced716_o-edit.jpg" alt="Compact disc close-up" /> [Photo](https://www.flickr.com/photos/jacd74/5845424017/) by Alberto Cabrera, cropped, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/)

It had been a while since I last needed to rip a CD into audio files (and compress them), but the need recently arose. This particular disc was a language learning supplement to a book, and a CD was a reasonable way to distribute that.

(Even though audio file downloads and streaming have become a far more common way to distribute audio than physical CDs, electronic formats don’t preserve our same rights to resell, lend, and make backups. But that is a topic for another blog post!)

I was ripping the CD with [abcde](https://abcde.einval.com/wiki/) (A Better CD Encoder), a text-based CD ripping, tagging, and compressing front-end I have used often in the past. Unexpectedly I got an error, as shown in this terminal output:

```plain
Executing customizable pre-read function... done.
Getting CD track info... Querying the CD for audio tracks...
Grabbing entire CD - tracks:  01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42
abcde: attempting to resume from /home/user/Music/abcde.2a0e162a..
.
Grabbing track 28: Track 28...
cdparanoia III release 10.2 (September 11, 2008)

Ripping from sector  131363 (track 28 [0:00.00])
          to sector  148524 (track 28 [3:48.61])

outputting to /home/user/Music/abcde.2a0e162a/track28.wav

 (== PROGRESS == [ ! !!--!V V   ! ! !   >       | 143137 00 ] == :-) 0 ==)   /bin/abcde: line 3560: 21658 Segmentation fault      (core dumped) nice $READNICE $CDROMREADER -"$CDPARANOIACDROMBUS" "$CDROM" "${READTRACKNUMS:-$UTRACKNUM}" "$FILEARG" 1>&2
[ERROR] abcde: The following commands failed to run:
readtrack-28: cdparanoia  returned code 139
Finished. Not cleaning /home/user/Music/abcde.2a0e162a.
```

The command that abcde was running when it died is:

```bash
cdparanoia -d /dev/cdrom 28 /home/user/Music/abcde.2a0e162a/track28.wav
```

Getting a segmentation fault suggests that the software has a bug, not necessarily that there is anything wrong with the disc, drive, or USB interface or drivers. But when troubleshooting, it is good (and easy) to start by testing on different hardware and operating system, if possible, to narrow things down.

I was using Fedora 29 with an LG Blu-Ray USB drive. To rule out several of those possible factors, I tried ripping the disc again on another computer running Ubuntu 19.04 with a Samsung DVD USB drive. It crashed the same way on the same track.

While looking online for ideas, I found several people mention bugfixes to cdparanoia in the wild from the open source community, which have not resulted in a new release.

In fact, to my surprise, the popular cdparanoia can safely be classified as abandoned, since the last software release was almost 11 years ago, on 2008-09-11. More tellingly, the latest commit to the Subversion repository was on 2010-06-11.

In the meantime, another project called [libcdio](https://www.gnu.org/software/libcdio/) contains a port of cdparanoia that was originally forked to make it work on platforms other than Linux. More importantly for my purpose here, it is actively maintained and has had many bugfixes that can be seen in the [libcdio-paranoia Git repository](https://github.com/rocky/libcdio-paranoia).

Its executable is called cd-paranoia to distinguish it from the original cdparanoia, and abcde has an option (here specified in an environment variable) to use libcdio instead of the default cdparanoia. I invoked abcde this way:

```bash
CDROMREADERSYNTAX=libcdio abcde -d /dev/cdrom -o mp3,opus,flac -V -x -j 3
```

and then the processing worked fine.

An aside: You may notice my command above compresses into the `opus` format. If you are not yet familiar with this [Opus audio codec](https://opus-codec.org/), I recommend you take a look! Quoting their website, it is an:

> … open, royalty-free, highly versatile audio codec. Opus is unmatched for interactive speech and music transmission over the Internet, but is also intended for storage and streaming applications. It is standardized by the Internet Engineering Task Force (IETF) as RFC 6716 which incorporated technology from Skype’s SILK codec and Xiph.Org’s CELT codec.

It is supported by many more players than I suspected given its youth, and I am very impressed with its quality vs. data size. If you are writing your own software that includes audio, Opus is a great choice, since you can include a playback library that supports it if needed.

Anyway, back to cdparanoia: Sometimes it takes a bit of detective work to find the better-maintained free software, but often it is out there. Thanks to those who have kept working on cd-paranoia!
