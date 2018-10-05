---
author: Charles Chang
title: 'Microsoft Deployment Toolkit (MDT) Initial Configuration Steps'
tags: windows, iso, servers
gh_issue_number: 1458
---

### PART 2 - MDT Initial Configuration Steps ###

#### Prerequisites ####
Softwares needed to build the MDT server and customize ISO for ***Windows 2012R2 Server***.

To begin, go ahead and download the software needed from below links and install on a ***Windows 2012R2 Server***. Below steps would work on Windows 2008, and 2012. If installing on Windows Server 2016, you would need to find the MDT and ADK version for Windows 2016.

[Microsoft Deployment Toolkit (MDT)]
(https://www.microsoft.com/en-us/download/details.aspx?id=54259)  
[Microsoft Deployment Toolkit (MDT) 2013 Update 2]
(https://www.microsoft.com/en-us/download/details.aspx?id=50407)  
[Windows Assessment and Deployment Kit (Windows ADK) for Windows 8.1 Update]
(https://www.microsoft.com/en-us/download/details.aspx?id=39982)  

#### Introduction ####
The goal of this proof of concept was to create a customize Window Server ISO and embed customize powershell and bat scripts. Automation of the OS installation is done by compiling an ISO via MDT. Happy reading!

#### Deployment Shares ####
1\. Create a “New Deployment Share” by right clicking “Deployment Shares” on the left navigation.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image69.png" alt="New Deployment Share Folder for MDT" />

2\. Next step is to setup the deployment share path. Default is C:\DeploymentShare.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image50.png" alt="path to deployment shares" />

3\. Next step is to setup the share name of the folder. DeploymentShare$ is the default.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image18.png" alt="UNC path of Deployment Shares" />

4\. Next step is to give the deployment share a descriptive name.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image58.png" alt="Descriptive Name for Deployment Shares" />

5\. Next step is to toggle off all the checkbox like below. No checkbox should be selected unless you need some of the features. Click Next.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image33.png" alt="Deployment Shares Option" />

6\. This step is a summary of the deployment share configuration<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image19.png" alt="Deployment Shares Summary" />

7\. Once the Deployment Share setup completes, right click on the newly created Deployment Share and click “Properties”.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image42.png" alt="Deployment Shares Properties" />

8\. Once the properties open, first tab is “General”. All setting should stay as is, but look towards the bottom and deselect x86 which is for 32 bit system. Only leave x64 checked. If you need x86, then toggle the checkbox.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image20.png" alt="Deployment Shares Configuration" />

9\. Next Tab to check is the Rules Tab. This tab sets the customsetting.ini. The parameter below will skip part of the installation like summary window, task sequence selection, etc.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image9.png" alt="Deployment Share Rules" />

10\. On the Windows PE Tab, sub tab called “General”, the name of the iso created for deployment share is set here. Also the background graphic of the ISO GUI installer could be change here. To see some customsetting.ini parameter, please <a href=>click here</a> to read Part 1 on customsetting.ini.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image10.png" alt="Window PE tab of MDT" />

11\. On the Window PE tab, under sub tab called “Features”, put a check next to DISM cmdlets and Windows Powershell. The DISM is used for The Deployment Image Servicing and Management.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image75.png" alt="Deployment Share and Feature Packs" />

12\. On the Windows PE Tab, sub tab called "Drivers and Patches". You could select the profile here. To create a profile, scroll down to "Selection Profile" towards the bottom of the page. The profile consist of imported drivers, scripts, apps, etc. Also toggle “Include only drivers from the selection profile".<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image13.png" alt="WIndows PE and Drivers and Patches" />

#### Importing Operating System ####
1\. Below section shows how to import an operating system for the custom ISO build. Go ahead and right click on Operating Systems within the left navigation. Then click on “Import Operating System”.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image44.png" alt="Deployment Import Operating System" />

2\. First step to import the ISO is to select “Full set of source files”. Click “next”.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image25.png" alt="Import OS within MDT" />

3\. Then select the source directory.  To select a source destination, have to mount the ISO as a CDROM drive on the MDT server. Go to next step to see how.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image48.png" alt="Mount ISO Source Directory" />

4\. Go ahead and locate your ISO on the MDT server. Right click on the ISO and click on “Mount”. This will mount the ISO as a CDROM. If you point the source directory at the ISO directly, it would not recognize the ISO. Have to mount as a CDROM.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image72.png" alt="Mount ISO within Server" />

5\. Head back to the MDT GUI, and select the CDROM drive which should be mounted and accessible on the server.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image83.png" alt="CDROM as Source Directory" />

6\. This step will ask from a directory name to store the ISO files.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image51.png" alt="Destination Name" />

7\. Next page is the summary of the ISO import.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image61.png" alt="Summary of ISO Import" />

8\. The is the last step is a confirmation of the importing the operating system.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image23.png" alt="ISO Import Confirmation" />

9\. Next step for import operating system is to click on “Operating Systems” on the left navigation and the os imported should exist on the right side.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image76.png" alt="View ISO Imported" />

10\. On the right side, after you click on “Operating Systems”, go ahead and delete the OS version you do not need and only keep the OS you would like to customize. Below sample I went ahead and delete Datacenter Core and Desktop experience, and Server Core. The OS I kept was the Server Desktop experience version. You could keep all the OS but the customize ISO will be much larger in file size.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image32.png" alt="Delete ISO Import" />

11\. Below screenshot will show the Windows 2012R2 Server Desktop experience version. The other version were deleted.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image73.png" alt="deleted ISO Import" />

#### Import Drivers ####
1\.  This section called “Out-of-Box Drivers” will allow you to import drivers associated with the physical server you will run this customize ISO on. For the most server, we would go ahead and download the drivers from vendor's website and import the driver into the MDT server like below.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image67.png" alt="Import Drivers" />

2\. Go ahead and right click on “Out-of-Box Drivers” and click on “Import Drivers”.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image77.png" alt="How to Import Drivers" />

3\. Point the directory to the download driver from your vendor of choice. Make sure to unpack or extract the zip file or exe.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image78.png" alt="specify directory of drivers to import" />

4\. Once you click next, it should take you to the summary page of import Driver.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image38.png" alt="Import Driver Summary" />

5\. The last step of import driver is the confirmation page. Once you import, check the errors and see if the errors are relevant.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image45.png" alt="Import Driver Wizard Confirmation" />

#### Selection Profiles ####
1\. The selection profiles allows you to include certain aspect of the ISO build. Could choose to include or exclude applications, drivers, tasks, etc. <br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image57.png" alt="Selection Profile" /><br>

2\. On this section go ahead and toggle all the checkboxs.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image43.png" alt="Edit Selection Profile" /><br>

3\. Not much to do here but go ahead and complete the selection profile setup.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image26.png" alt="Complete Selection Profile" /><br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image12.png" alt="Complete Selection Profile" /><br><br>

4\. Screenshot below will show the profile you created.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image47.png" alt="Complete Selection Profile" /><br><br>

#### Task Sequence ####

1\. The “Task Sequence” will run through the steps to install the operating system onto your physical server. The steps will include scripts, ISO install, sysprep, etc. To begin, go ahead and right click on “Task Sequence” and click “New Task Sequence”.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image60.png" alt="New Task Sequence" />

2\. Next, go ahead and enter a “Task Sequence ID:” Below I enter USB03 as the ID.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image52.png" alt="New Task Sequence General Setting" />

3\. The next step is to select a task sequence template. Microsoft include a few template to choose from. It would also allow you to start with a bare template. For this setup, we will use the “Standard Server Task Sequence”.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image3.png" alt="Task Sequence Template" />

4\. On the next step, select the operating system we imported. <br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image82.png" alt="Select Imported OS" />

5\. On this step, select “Do not specify a product key at this time”. You could enter a product key if you would like but for this proof of concept, we do not want to specify a product key.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image28.png" alt="Specify Product Key" />

6\. On this step, go ahead and enter an Organization name. You could also change the Full Name. For the internet explorer, you could leave the default value. Click next.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image70.png" alt="OS Setting" />

7\. On this step, you could select “Do not specify an Administrator password at this time.” If in a domain environment, once the OS is install and join to the domain, the password should be assigned by the domain controller via group policy or a customize powershell script. Go ahead and click Next. The next two steps are the summary and progress which I will skip.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image7.png" alt="Do Not Specify a Administrator Account" />

8\. This step below will be the final step to creating a “task sequence”. Click Finish. <br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image46.png" alt="how to setup os deployment share folder" />

9\. Once the “Task Sequence” is complete. You should see the newly created task sequence on the right side.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image22.png" alt="Task Sequence Confirmation" />

10\. Go ahead and highlight the newly created task sequence and right click on "Properties".<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image8.png" alt="Task Sequence is complete" />

11\. Once the Properties window open, you could select “This can run on any platform” or choose a specific client platform. Also, make sure “Enable this task sequence” is toggled.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image39.png" alt="Task Sequence Properties" />

12\. Next step is the “Task Sequence” tab which will assist in the installation of the OS. On the left side of the window will have folders and each folder will have a sequence of events to prepare and execute the OS installation. You could also add custom scripts into the task sequence and run before or after the installation. The steps below were created base on the template we select when we created the initial task sequence using the wizard.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image16.png" alt="Task Sequence General Tab" />

13\. Majority of the task sequence is based on the standard server task sequence template selected in step 3. You could customize the task sequence but be aware some task sequence might be needed like sysprep tasks, os install task, etc. You could also add powershell or command line scripts to the task sequence if needed. Keep in mind, when embedding a custom powershell script within the task sequence, to execute the script, you would have to executw the scripts in custom tasks section within the task sequence. <br><br>

14\. To add a powershell script, in the task sequence, click on "Add", then "Powershell" script, then under powershell script section, enter the name of the powershell script here. For example, if your script is named setdrive.ps1, then type exactly the same, setdrive.ps1. No need to add %SCRIPTROOT%. The powershell script would then need to be copied to the script folder under DeploymentShares folder. This is where all the scripts should be stored.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image6.png" alt="Add powershell to Task Sequence" />

15\. To add a bat file to the task sequence, within the task sequence, click on "Add", then "Command Line",  then to the right of the task sequence screen, should be a textbox to enter %SCRIPTROOT%\nameofthefile.bat. Replace name of the file to the name of your file. When running a bat file, %SCRIPTROOT% is needed.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image27.png" alt="Add bat to Task Sequence" />

16\. To embed the powershell scripts, copy and paste the scripts in the "Scripts" folder.<br><br>
<img src="\blog\2018\09\12\Microsoft-Deployment-Toolkit-Initial-Configuration\image6.png" alt="Embed Powershell script" />

This will complete Part 2 of creating a customize ISO. In Part 3, I will discuss how to create a bootable USB key with the customize ISO.

Continue to - <br>
**Link:** <A href=/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key.html.md>Part 3 - Microsoft Deployment Toolkit (MDT) - Create Customize Bootable USB Key using ISO Produced by MDT</a>

#### Related Articles ####
**Link:** <A href=/blog/2018/09/11/Microsoft-Deployment-Toolkit-Customsettingini.html.md>Part 1 - MDT and Customsetting.ini Parameters</a>




