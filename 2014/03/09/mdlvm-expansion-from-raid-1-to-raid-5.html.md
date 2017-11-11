---
author: Josh Williams
gh_issue_number: 940
tags: linux, sysadmin
title: md+lvm expansion from RAID 1 to RAID 5
---

VHS is on the way out, or so they tell me.  A little while back I unearthed the family's collection of old tape recordings, and have been digitizing everything in an effort to preserve all the old youth sports games and embarassing birthday parties.  There's no way I'm going to let my brother forget those.  It's a lot of video, and that takes up quite a bit of space.  Between that, HD videos recorded more recently, Postgres test databases and source datasets, server backups, and so on, the 3TB of space on my local file server was quickly running out.

I know, right?  My first hard drive was 40MB, in two 20MB partitions.  And we were glad for that space!

Back in the present, now it was time to add another hard drive.  This (otherwise) tiny rooted plug server contained two 3TB USB hard drives in a RAID-1 configuration through the Linux md module.  On top of that is lvm.  lvm itself could have been used for the RAID-1, but has the disadvantage of not being able to optimize multiple reads, whereas md can allow both disks in the mirror serve different reads at the same time.

I bought a third disk of the same model, so it could be added in to a RAID-5 configuration.  These being big USB drives, operations that read and write the disks as a whole (such as RAID rebuild operations) take a while.  A long while.  I could have unmounted, disassembled the array, rebuilt it as RAID-5, and brought it back after, but keeping it offline for that amount of time wasn't too appealing.  Lets attempt an online conversion.

First up, confirming the disks are all the same exact size:

```
root@plug01:/backup# blockdev --getsize64 /dev/sdd2
2999557554176
root@plug01:/backup# blockdev --getsize64 /dev/sdc2
2999557554176
root@plug01:/backup# blockdev --getsize64 /dev/sdb2
2999557554176
```
mdadm says the array is in good shape, but it won't be for long.  We'll need to break the RAID-1 in order to recreate the RAID-5.  Yes, it's as scary as it sounds.  Backups were double checked.  Backups were triple checked.  To break the array set one of the devices as failed, then remove it:

```
Number Major Minor RaidDevice State
0 8 34 0 active sync /dev/sdc2
1 8 18 1 active sync /dev/sdb2
root@plug01:/backup# mdadm /dev/md0 -f /dev/sdc2 # Set as failed
mdadm: set /dev/sdc2 faulty in /dev/md0
root@plug01:/backup# mdadm /dev/md0 -r /dev/sdc2 # Remove from array
mdadm: hot removed /dev/sdc2 from /dev/md0
```
Now we have an ex-RAID-1 (sdb2) with two spare disks (sdc2 and sdd2.)  Those two spare partitions can then be put into a RAID-5 configuration.

Wait, what?  RAID-5 with two disks?  Sure, I could have created a 3-device RAID-5 with one marked as "missing" but I wanted to restore the redundancy as soon as possible, and so gave it a shot.  Lo and behold...

```
root@plug01:/backup# mdadm --create /dev/md1 --level=5 --raid-devices=2 /dev/sdc2 /dev/sdd2
mdadm: /dev/sdc2 appears to be part of a raid array:
level=raid1 devices=2 ctime=Sat Jan 12 05:25:51 2013
Continue creating array? y
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md1 started.
root@plug01:/backup# mdadm -D /dev/md1
/dev/md1:
Version : 1.2
Creation Time : Fri Jan 3 20:13:05 2014
Raid Level : raid5
Array Size : 2929253888 (2793.55 GiB 2999.56 GB)
Used Dev Size : 2929253888 (2793.55 GiB 2999.56 GB)
Raid Devices : 2
Total Devices : 2
Persistence : Superblock is persistent

Update Time : Fri Jan 3 20:13:05 2014
State : clean, degraded, recovering
Active Devices : 1
Working Devices : 2
Failed Devices : 0
Spare Devices : 1

Layout : left-symmetric
Chunk Size : 512K

Rebuild Status : 0% complete

Name : plug01:1 (local to host plug01)
UUID : 1d493c17:7a443a6d:e6c121b4:53e8b9a1
Events : 0

Number Major Minor RaidDevice State
0 8 34 0 active sync /dev/sdc2
2 8 50 1 spare rebuilding /dev/sdd2
```
Seems to have worked!  The array build will do its thing in the background, but we can start using it immediately.  Since we want the redundancy back sooner than later, lets start moving the data off the now single disk it resides on.  Since we're using lvm, this is just a matter of having it move the volume group from the old pv to the new one.  That process does take a long time.  Set up the physical volume structure, add it to the volume group, and start the move process:

```
root@plug01:/backup# pvcreate /dev/md1
Found duplicate PV gejBFzirMdX0KSGMO6S1TYQSOBJTUqOw: using /dev/md0 not /dev/md1
get_pv_from_vg_by_id: vg_read_internal failed to read VG plug01
Physical volume "/dev/md1" successfully created
root@plug01:/backup# vgextend array1 /dev/md1
Volume group "array1" successfully extended
root@plug01:/backup# pvmove /dev/md0 /dev/md1
/dev/md0: Moved: 0.0%
/dev/md0: Moved: 0.0%
&lt;snip&gt;
/dev/md0: Moved: 99.9%
/dev/md0: Moved: 100.0%
/dev/md0: Moved: 100.0%
```
Clean up the now-abandoned disk, then add it to the new RAID-5...

```
root@plug01:/backup# vgreduce array1 /dev/md0
Removed "/dev/md0" from volume group "array1"
root@plug01:/backup# vgs
VG #PV #LV #SN Attr VSize VFree
array1 1 1 0 wz--n- 2.73t 28.75g
root@plug01:/backup# pvremove /dev/md0
Labels on physical volume "/dev/md0" successfully wiped
root@plug01:/backup# mdadm --stop /dev/md0
mdadm: stopped /dev/md0
root@plug01:/backup# mdadm --add /dev/md1 /dev/sdb2
mdadm: added /dev/sdb2
root@plug01:/backup# mdadm --grow --raid-devices=3 --backup-file=/root/tmp/md1.bak /dev/md1
mdadm: /dev/md1 is performing resync/recovery and cannot be reshaped
```
Oh, our pvmove activity superseded the array build procedure, so we have to wait until that finishes before we can grow the RAID-5.  While we're waiting, I'll note that the operation backs up some of the metadata to an external file at the very start of the procedure, just in case something happens early on in the process.  It doesn't need it for long.

There, that's probably enough waiting...

```
root@plug01:/backup# mdadm --grow --raid-devices=3 --backup-file=/root/tmp/md1.bak /dev/md1
mdadm: Need to backup 1024K of critical section..
root@plug01:~# cat /proc/mdstat
Personalities : [raid1] [raid6] [raid5] [raid4]
md1 : active raid5 sdb2[3] sdd2[2] sdc2[0]
2929253888 blocks super 1.2 level 5, 512k chunk, algorithm 2 [3/3] [UUU]
[&gt;....................] reshape = 0.5% (16832872/2929253888) finish=9666.3min speed=5021K/sec

unused devices:
```
More waiting.  After that completes we're then able to resize the pv to take up that space, and then resize the lv.  Note that the lv doesn't take up the entirety of the pv and has a little bit of space reserved for snapshots.

```
root@plug01:/backup# pvresize /dev/md1
Physical volume "/dev/md1" changed
1 physical volume(s) resized / 0 physical volume(s) not resized
root@plug01:/backup# lvextend -L 5558g /dev/mapper/array1-vol1
Extending logical volume vol1 to 5.43 TiB
Logical volume vol1 successfully resized
root@plug01:/backup# pvs
PV VG Fmt Attr PSize PFree
/dev/md1 array1 lvm2 a- 5.46t 29.11g
root@plug01:/backup# vgs
VG #PV #LV #SN Attr VSize VFree
array1 1 1 0 wz--n- 5.46t 29.11g
root@plug01:/backup# lvs
LV VG Attr LSize Origin Snap% Move Log Copy% Convert
vol1 array1 -wi-ao 5.43t
```
And the last step, perform an online resize of the ext4 volume:

```
root@plug01:/backup# resize2fs /dev/mapper/array1-vol1
resize2fs 1.41.12 (17-May-2010)
Filesystem at /dev/mapper/array1-vol1 is mounted on /mnt/disk01; on-line resizing required
old desc_blocks = 173, new_desc_blocks = 348
Performing an on-line resize of /dev/mapper/array1-vol1 to 1456996352 (4k) blocks.
The filesystem on /dev/mapper/array1-vol1 is now 1456996352 blocks long.

root@plug01:/backup# df -h /dev/mapper/array1-vol1
Filesystem Size Used Avail Use% Mounted on
/dev/mapper/array1-vol1 5.4T 2.6T 2.6T 50% /mnt/disk01
```
There, a completely new array structure and a bunch more space without having to unmount the filesystem for a moment!
