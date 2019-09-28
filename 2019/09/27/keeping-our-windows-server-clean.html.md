---
author: "Juan Pablo Ventoso"
title: "Keeping our Windows Server clean"
tags: windows, iis, logging, sysadmin
gh_issue_number: 1557
---

<img src="/blog/2019/09/27/keeping-our-windows-server-clean/cover.jpg" alt="Keeping our Windows Server clean" /> [Photo](https://flic.kr/p/ofjEj4) by [Shawn O’Neil](https://www.flickr.com/photos/oneilsh/), used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), cropped from original


###Introduction

I have been running websites and web applications under Windows Server for years, for both work and personal purposes. Most of them were small websites with a few daily visitors, but one particular case (a <a href="https://www.pronosticoextendido.net" target="_blank">weather website</a> I originally created as a hobby) grew over time to around one million page views per month.

The website is mostly ASP.NET, with some services and components written in PHP and Python, and uses MySQL for persistence (as well as a bunch of XML/PNG files to cache weather forecasts and weather imagery). As months passed by, I’ve discovered that the default IIS and Windows log files will grow drastically so, while checking its content periodically to detect issues and vulnerabilities, we need to take action to preserve free disk space and server performance.


###Internet Information Services log files

In our IIS public folder (by default `C:\inetpub`) we will have a path `logs\LogFiles`. Inside that folder, the IIS service will create a set of folders, one per HTTP/FTP service that is running under our instance. How fast it will grow depends on many things, mainly traffic, but also website visibility and bad requests. But it will start to sooner or later consume our free disk space.

To prevent this, we can create a batch file that can be run on a daily basis from a scheduled task.

* <b>CleanIISLogs.bat</b>

```batch
forfiles /D -10 /P "C:\inetpub\logs\LogFiles" /S /C "cmd /c del /f /q @path"
```

This script traverses through all files on the folder passed by parameter that are more than 10 days old, and for each file, it executes the `del` command in quiet mode. This script will search for all files within the folder and all subfolders that are more than 10 days old and delete them. After running the task, we should confirm that the used space was reduced:

![Folder properties after cleanup](/blog/2019/09/27/keeping-our-windows-server-clean/logfiles-space-green-check.jpg)


###HTTP Error logs

There is another location where different operating system logs are stored: `C:\Windows\System32\LogFiles`. And when we navigate there, we will find an `HTTPERR` folder which will also start consuming free space as our websites are visited. The log files in that folder will save information regarding HTTP errors from any API/Service running on our IIS instance.

So depending on the web traffic our applications have, it will grow faster or slower. But in any case, I recommend creating a batch file to clean old log files using the `del` command, and to run that file on a daily basis by configuring a scheduled task.

* <b>CleanHTTPERRLogs.bat</b>

```batch
forfiles /D -10 /P "C:\Windows\System32\LogFiles\HTTPERR" /C "cmd /c del /f /q @path"
```

This script, just as the previous one, will search for all files more than 10 days old and delete them. We don’t need to search for subfolders in this case because of Windows storing all HTTPERR logs at the same level. After running the task, we can open the folder properties and check that the used space will be the roughly the same over the days:

![Folder properties after cleanup](/blog/2019/09/27/keeping-our-windows-server-clean/httperr-space-green-check.jpg)

(I know, still 1 GB after cleanup, gotta do something about those bad requests!)


###Compressing files

If we need to comply with strict security/​auditing policies, and if we don’t have a backup device with enough capacity, deleting old files might not be an option. If that’s the case, we can compress the files to save space on disk.

So an alternative would be to create a script to compress the files instead of deleting them using the `compact` command. This is an example of a batch file that will compress all files in the IIS LogFiles folder that are more than 10 days old.

* <b>CompressIISLogs.bat</b>

```batch
forfiles /D -10 /P "C:\inetpub\logs\LogFiles" /S /C "cmd /c compact @path"
```

And of course, we can create more scripts for other locations, like the `C:\Windows\Temp` folder for example. I mentioned earlier that my website creates a lot of XML and PNG files: I have another script whose mission is keeping those folders at bay, deleting forecast files that haven’t been used for more than one day (the local forecast will be outdated and would need to refresh it from the external web service anyway).


###More resources from Microsoft

* [forfiles syntax and usage](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/forfiles)
* [Configuring HTTP server logging](https://docs.microsoft.com/en-us/windows/win32/http/configuring-http-server-api-error-logging)
* [Managing IIS Log folder](https://docs.microsoft.com/en-us/iis/manage/provisioning-and-managing-iis/managing-iis-log-file-storage)
