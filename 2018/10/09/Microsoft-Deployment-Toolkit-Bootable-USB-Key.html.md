---
author: Charles Chang
title: 'Microsoft Deployment Toolkit (MDT) - Create Customize Bootable USB Key using ISO Produced by MDT'
tags: windows, iso, servers
gh_issue_number: 1459
---

### PART 3 - Create Customize Bootable USB Key using ISO Produced by MDT ###

#### Prerequisites ####

Software needed to create the Bootable USB Key is called Rufus. To begin, go ahead and download the software using the link below. 

[Rufus USB Bootable Creator]
(https://rufus.akeo.ie/)

#### Introduction ####
The 3rd part of this blog is to compile and embed the ISO onto a Bootable USB key for the purpose of physically installing the operating system on a standalone physical server. The iso could also be mounted to a virtual drive via console access if the server has this feature to use (like DRAC from Dell, iLO from HP, or IMM/RSA from IBM). The iso could also be used within a vSphere or Hyper-V environment and installation is the same as any other ISO installation within a virtualization environment. Below are the steps to achieve a boot USB using the ISO created by MDT.

#### Creating Bootable OS ISO ####

1\. To begin the process of creating the bootable ISO, look for “Advanced Configurations” and then “Media”. <br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image49.png" alt="Setup and Create Bootable Media with MDT" />

2\. Right click on “Media” and select “New Media”.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image81.png" alt="Create new Media with MDT" />

3\. The next step is to browse and create a Media Folder to store the ISO file. This could be in the same root location as the DeploymentShares Folder. Below example I created a folder called MediaPath.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image15.png" alt="Media path for ISO" />

4\. Next step is to view the summary.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image34.png" alt="MDT Summary" />

5\. Last step is to confirm the completion of the ISO build. Click Finish.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image63.png" alt="MDT ISO Build Confirmation" />

#### Configure ISO Media ####
1\. First step is to confirm the media exist on the right side of the MDT GUI under media. If it exist, go ahead and right click the ISO media and click “Properties”.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image14.png" alt="Configure ISO Media" />

2\. Next step is to check the media path and confirm. This is where the ISO will be stored. Next is to select a profile. Go ahead and select the customized selection profile created earlier during MDT setup. Toggle “Generate x64 boot image”. And if needed toggle the x86. Last setting is to toggle “Generate a Lite Touch bootable ISO image” and give the ISO a name. This will be the ISO we will use to install.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image29.png" alt="Configure ISO Media Properties" />

3\. Next step is to check the “Rules” tab which will contain the configsetting.ini. This same setting exist in the “DeploymentShares” folder properties within the MDT. If the configsetting.ini was edited, then copy and paste the same configsetting.ini to DeploymentShares properties.To get to the properties, look for “MDT Deployment Share” on MDT GUI, right click and click properties.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image54.png" alt="Setup Rule - Customesetting.ini" />

4\. Next step to configure is the “Window PE” Tab, and “General” subtab. Within the “General” tab, you could change the background of the ISO install. Basically that is the only setting to set in this section. If needed, next to “Platform”, there is a drop down where you could select x64 or x86. On x86, you could turn off everything that is possible to keep the ISO build strictly for x64.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image37.png" alt="General Tab - ISO Media Properties" />

5\. Next sub tab to configure is the “Features” tab. Make sure DISM cmdlets and Windows Powershell is selected.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image84.png" alt="MDT Media Propertie - Features Packs" />

6\. Last step in the ISO configuration is within the “Drivers and Patches” sub tab where we select the “Selection profile” created earlier on. Click OK when done.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image47.png" alt="Selection Profiles" />

7\. Once the Media has been configured, go ahead and right click the “Media” on the right side and click on “Update Media Content”. This will update the ISO with the latest configurations.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image35.png" alt="Update Media Content button" />

8\. Once the update is trigger, should see below confirmation.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image36.png" alt="Update Media Content and Confirmation" />

9\. You could also do the same for the MDT Deployment Share and click on “Update Deployment Share”. This will update the files store in the DeploymentShares folder. The DeploymentShares folder contain all files used to build the ISO like scripts, OS files to install, etc. This share folder could also be used to push out the ISO build from within the network. Go ahead and right click and select Update Deployment Share.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image80.png" alt="Update Deployment Shares" />

10\. Once you right click, should take you to below screen. Make sure the radio and checkbox are select like below to update. If not you could select the bottom option which would regenerate the boot images.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image53.png" alt="Update Deployment Shares Wizard" />

11\. Last step is the confirmation of the setting. Below will contain exit code but does not impact the ISO build. This will complete the ISO build process. Next step is to locate the ISO. <br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image1.png" alt="Update Deployment Shares Wizard Confirmation" />

#### Location of the Customize ISO ####
1\. Below are the two folders/path created during the MDT setup. Deployment Shares and MediaPath.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image11.png" alt="Location of Customize ISO" />

2\. Within the DeploymentShare folder, there are other folders used to build the ISO file. The most important one is the Scripts folder. <br><br>
Note: This is where we store the scripts used in the task sequence. Any customize scripts should be copy and paste into this folder. Then setup within the task sequence to execute. <br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image62.png" alt="Deployment Shares Folder Structure" />

3\. Below is the location where the ISO we customized will be located. Once you update the media, this ISO file will be updated. Below is the ISO to used on an USB key, or deployment software. Now we are ready to create a bootable ISO with the file below.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image59.png" alt="Location of the Customize ISO" />

#### To Create a Bootable USB using the ISO ####
1\. First step is to download a bootable media creator like [Rufus USB Bootable Creator] (https://rufus.akeo.ie/)<br><br>
2\. Once download is completed, go ahead and launch the Rufus application. Go ahead and connect the USB to the laptop/desktop. The Rufus application should auto detect the setting with the exception of selecting the ISO. Go ahead and click on “Select” and select the ISO we customize.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image24.png" alt="How to use Rufus Bootable USB creator" />

3\. Once you click on “Select”, should see below screen. Go ahead and choose the customized ISO we built. Click Open.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image68.png" alt="Add Customize ISO to Rufus" />

4\. Once the ISO has been selected, go ahead and check the setting where the red arrows are pointed at. For Partition scheme, there’s a option for MBR if needed and Target system with a value of BIOS. Go ahead and click “Start” and once Rufus completes the build, the USB key should contain the bootable customized ISO. This will complete the customized ISO build.<br><br>
<img src="/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key/image41.png" alt="Rufus Configuration" />

#### How to Use the Bootable ISO USB key ####
1\. To install the Operating System using the bootable USB key, go ahead and power up the physical server and go into BIOS. Determine if disabling Secure USB or enabling USB boot is needed. This is done through the BIOS. Once boot from USB is enabled, then next thing to do is boot to option. Usually F12 or F8. Various manufacturer have a shortcut key. Please check with your manufacturer. Once you are able to boot from USB, basically the installation will run automatically without user intervention. During the process, there will be several reboot of the server which is normal behavior. After the customize ISO runs and completes, the server should be ready to use.<br><br>
This will end Part 3 "Microsoft Deployment Toolkit (MDT) - Create Customize Bootable USB Key using ISO Produced by MDT". <br><br>

#### Related Articles ####
<A href=/blog/2018/09/11/Microsoft-Deployment-Toolkit-Customsettingini.html.md>Part 1 - MDT and Customsetting.ini Parameters</a><br>
<A href=/blog/2018/09/12/Microsoft-Deployment-Toolkit-Initial-Configuration.html.md>Part 2 - MDT Initial Configuration Steps</a><br>