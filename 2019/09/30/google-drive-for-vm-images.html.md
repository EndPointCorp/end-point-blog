---
title: "Google Drive for virtual machine images"
author: Jon Jensen
tags: sysadmin, cloud, storage
gh_issue_number: 1559
---

<img src="/blog/2019/09/30/google-drive-for-vm-images/20190704-143912-sm.jpg" alt="Pine Creek Pass, Teton Valley, Idaho" />

<!-- Photo by Jon Jensen -->

Recently we decommissioned an old database server. We wanted to keep a copy of its 53.7 GB virtual machine disk image in an archive in case there is ever any need to revive it. It is really unlikely that we will need it any time soon, or maybe ever, so we thought of putting it in one of the cloud storage services.

### Cloud storage

Cloud service pricing is often metered by storage, network, operations, and other fees, making it complicated to calculate what you will pay. We already use Amazon S3, Azure Storage, and [Google Cloud Storage](https://cloud.google.com/storage/) and they are all no exception. For our example 53.7 GB disk image, the Google Cloud Storage [Standard Storage pricing](https://cloud.google.com/storage/pricing) is currently:

* No charge for network ingress when we upload it
* About $1.08 to $1.40 USD per month to store the file in the US or EU
* About $6.50 each time we download the file to most places in the world!

These days a ~50 GB disk image is on the small side, so you can imagine the cost going up rapidly with larger disk sizes.

Some cloud storage providers offer lower prices for slow-availability semi-offline storage, such as Amazon S3 Glacier or Google Coldline Storage. Those would indeed save us some money for monthly storage, but the most expensive aspect is the network egress cost, which is the same.

### Local storage

External USB disk drives have gotten very inexpensive in recent years, so we considered just spending roughly $180 for a 6 TB hard disk and storing our disk image there. We can fit over 100 VM images of this size on such a disk, so the cost works out to a one-time cost of about $1.80 each.

But there are downsides to local storage, including:

* It is a single point of failure. The disk can:
  * fail
  * be lost or stolen
  * be damaged by water, an impact such as someone dropping it or a horse kicking it 🐴😀, or a power surge or static electricity
  * be forgotten if the employee who has it leaves and nobody remembers to take it over.
* The data would likely be inaccessible while the employee is out of the office.
* Retrieval speed is limited by the upstream network bandwidth which is often fairly slow for consumer Internet connections and even crowded office networks.

For “just in case” old archival data, these risks are pretty reasonable and the price is good. But it would be nice to decouple the storage from any individual employee’s network speed.

### Google Drive

Then we remembered that we have Google Drive as part of G Suite, and even though we don’t normally use it this way, it could be a place to store infrequently-needed large archival data such as this.

Google’s G Suite Business edition currently costs $12 USD per user per month (plus tax). It includes 1 TB of cloud storage per user if you have fewer than 5 users, and unlimited cloud storage if you have 5 or more users. “Unlimited” sounds pretty helpful for this scenario. 😉

Many of us think of Google Drive primarily as its browser-based folder and file interface, a graphical consumer or business user service. So our instinct is to first download a file our desktop and then upload it from there to Google Drive using the browser.

For our large, multi-gigabyte files on a server, that is cumbersome and slow, at least twice as slow as it should be. We really would prefer to upload them directly from the server to Google Drive. And to use the old archived images, we would want to download them from Drive directly to a remote server, not first to a desktop.

#### Uploading

Conveniently for us, Google Drive has a [web service API](https://developers.google.com/drive/) we can use! [Oliver Marshall’s nice article](http://olivermarshall.net/how-to-upload-a-file-to-google-drive-from-the-command-line/) shows how to use the open source [gdrive command-line tool](https://github.com/gdrive-org/gdrive) to access it.

The easiest thing to do after we have gdrive authenticate with our Google account is:

```
gdrive upload /path/to/file
```

which will put it in the base folder of My Drive.

You can also use `gdrive list …` to find a specific folder you would like to upload it into.

To give an idea of the speed, I had several files to upload from a Linux server, and measured speed of about 12 MB/sec. for each of 3 parallel uploads on a 100 Mbps server connection.

#### Verifying

Did the huge files make it without error? Google Drive doesn’t show them until they’re complete, which is good, so we will not see any partial files. To confirm, let’s check file size and MD5 hash value, which isn’t visible in the Drive web interface, but is via the API, along with the view & download URLs:

```
# gdrive info 1YMEoEWWOvuBGSk0GJBv7c0E4cSEOoc6n
Id: 1YMEoEWWOvuBGSk0GJBv7c0E4cSEOoc6n
Name: prod-db-20190731
Path: VM images/Database server/prod-db-20190731
Mime: application/octet-stream
Size: 53.7 GB
Created: 2019-08-08 21:20:50
Modified: 2019-08-08 21:20:50
Md5sum: 43f7e727047cb2bbbfb54b413752c229
Shared: True
Parents: 1HBkixF0UxraH6nHyD1Fiwx5X5k7dfaKm
ViewUrl: https://drive.google.com/a/your.domain/file/d/1YMEoEWWOvuBGSk0GJBv7c0E4cSEOoc6n/view?usp=drivesdk
DownloadUrl: https://drive.google.com/a/your.domain/uc?id=1YMEoEWWOvuBGSk0GJBv7c0E4cSEOoc6n&export=download
```

When we run `md5sum` (or `md5` on BSD systems such as macOS) on the original file or block device on our server, the resulting hash value should match the Md5sum value gdrive shows.

#### Cautions

Regular Google Drive accounts are tied to the user, so if you leave the organization and they remove your account, your files will need to be deleted or reassigned to another user.

Use a Shared Drive (formerly called Team Drive) to avoid having the files tied to a specific user. There is even an [API for G Suite admins](https://developers.google.com/drive/api/v3/search-shareddrives) to search all shared drives in their account.

I haven’t seen anything to make me think this API is any less reliable than anything in Google Cloud Platform, but it certainly is not promoted as being something to use for a busy production web application. It seems safest to use it for archival storage like this that will be accessed rarely, by a human.

Once authorized, your gdrive command-line tool has access to all your Google Drive files. That isn’t something you want to leave sitting around for ill-intentioned people to perhaps access. So when you’re done uploading your files, remove the app authorization until the next time you need it. In your browser go to: Google&nbsp;Drive > Settings (gear&nbsp;icon) > Manage&nbsp;Apps > GDrive > Options > Remove&nbsp;app.
