---
author: Charles Chang
title: 'Microsoft Deployment Toolkit (MDT) to Create Customize Bootable USB Key - Customsetting.ini'
tags: windows, iso, servers
gh_issue_number: 1452
---

###PART 1 - MDT and Customsetting.ini Parameters###

####Introduction####
The customsetting.ini is a important part of the Microsoft Deployment Toolkit which sets rules on how your deployment will run. Would you need to disable certain interactive parts of the deployment? or would you want the person who's installing the operating system to interact with the installation. These are all possible by setting the customsetting.ini paramters. Please read below to get a better sense of how to use various customsetting.ini parameters. Happy reading!

####Customsetting.ini Parameters####
<table width=100% border=1>
  <tr>
    <th width=33%><b>Skip this wizard page</b></th>
    <th width=30%><b>Using this property</b></th>
    <th width=37%><b>Configure these properties</b></th>
  </tr>
  
    <tr valign=top>
    <td>Welcome</td>
    <td>SkipBDDWelcome</td>
    <td></td>
  </tr>
  
  <tr valign=top>
    <td>Specify credentials for connecting to network shares</td>
    <td>Skipped by providing properties in next column</td>
    <td>·  UserID<BR>·  UserDomain<BR>·  UserPassword</td>
  </tr>
  
    <tr valign=top>
    <td>Task Sequence</td>
    <td>SkipTaskSequence</td>
    <td>·  TaskSequenceID</td>
  </tr>
  
      <tr valign=top>
    <td>Computer Details</td>
    <td>SkipComputerName, SkipDomainMembership</td>
    <td>·  OSDComputerName<br>·  JoinWorkgroup<br>–or–<br>·  JoinDomain<br>·  DomainAdmin</td>
  </tr>
  
      <tr valign=top>
    <td>User Data</td>
    <td>SkipUserData</td>
    <td>·  UDDir <br>·  UDShare<br>·  UserDataLocation</td>
  </tr>
  
      <tr valign=top>
    <td>Move Data and Settings</td>
    <td>SkipUserData</td>
    <td>·  UDDir<br>·  UDShare<br>·  UserDataLocation</td>
  </tr>
  
      <tr valign=top>
    <td>User Data (Restore)</td>
    <td>SkipUserData</td>
    <td>·  UDDir<br>·  UDShare<br>·  UserDataLocation</td>
  </tr>
  
      <tr valign=top>
    <td>Computer Backup</td>
    <td>SkipComputerBackup</td>
    <td>·  BackupDir<br>·  BackupShare<br>·  ComputerBackupLocation</td>
  </tr>
  
      <tr valign=top>
    <td>Product Key</td>
    <td>SkipProductKey</td>
    <td>·  ProductKey<br>–or–<br>·  OverrideProductKey</td>
  </tr>
  
      <tr valign=top>
    <td>Language Packs</td>
    <td>SkipPackageDisplay</td>
    <td>·  LanguagePacks</td>
  </tr>
  
      <tr valign=top>
    <td>Locale and Time</td>
    <td>SkipLocaleSelection, SkipTimeZone</td>
    <td>·  KeyboardLocale<br>·  UserLocale<br>·  UILanguage<br>·  TimeZone<br>·  TimeZoneName</td>
  </tr>
  
      <tr valign=top>
    <td>Roles and Features</td>
    <td>SkipRoles</td>
    <td>·  OSRoles<br>·  OSRoleServices<br>·  OSFeatures</td>
  </tr>
  
      <tr valign=top>
    <td>Applications</td>
    <td>SkipApplications</td>
    <td>·  Applications</td>
  </tr>
  
      <tr valign=top>
    <td>Administrator Password</td>
    <td>SkipAdminPassword</td>
    <td>·  AdminPassword</td>
  </tr>
  
      <tr valign=top>
    <td>Local Administrators</td>
    <td>SkipAdminAccounts</td>
    <td>·  Administrators</td>
  </tr>
  
      <tr valign=top>
    <td>Capture Image</td>
    <td>SkipCapture</td>
    <td>·  ComputerBackupLocation</td>
  </tr>
  
      <tr valign=top>
    <td>Capture Image</td>
    <td>SkipCapture</td>
    <td>·  ComputerBackupLocation</td>
  </tr>
  
      <tr valign=top>
    <td>Bitlocker</td>
    <td>SkipBitLocker</td>
    <td>·  BDEDriveLetter<br>·  BDEDriveSize<br>·  BDEInstall<br>·  BDEInstallSuppress<br>·  BDERecoveryKey<br>·  TPMOwnerPassword<br>·  OSDBitLockerStartupKeyDrive<br>·  OSDBitLockerWaitForEncryption</td>
  </tr>
  
      <tr valign=top>
    <td>Ready to begin</td>
    <td>SkipSummary</td>
    <td></td>
  </tr>
  
    <tr valign=top>
    <td>Operating system deployment completed successfully</td>
    <td>SkipFinalSummary</td>
    <td></td>
  </tr>
  
    <tr valign=top>
    <td>Operating system deployment did not complete successfully</td>
    <td>SkipFinalSummary</td>
    <td></td>
  </tr>
</table>


####Sample Customsetting.ini####

Below is an example of how customsetting.ini is setup.<br>

[Settings] <br>
Priority=Default<br>

[Default] <br>
SkipAdminPassword=YES<br>
SkipApplications=YES<br>
SkipBDDWelcome=YES<br>
SkipBitLocker=YES<br>
SkipComputerBackup=YES<br>
SkipComputerName=YES<br>
SkipDeploymentType=YES<br>
SkipDomainMembership=YES<br>
SkipUserData=YES<br>
SkipFinalSummary=YES<br>
SkipLocaleSelection=YES<br>
SkipPackageDisplay=YES<br>
SkipProductKey=YES<br>
SkipRoles=YES<br>
SkipSummary=YES<br>
SkipTaskSequence=YES<br>
SkipTimeZone=YES<br>
OSInstall=Y<br>
DoNotCreateExtraPartition=YES<br>
TimeZoneName=Eastern Standard Time<br>
AdminPassword=password<br>

 There are many possiblities within the customesetting.ini. Here is a great article on customsetting.ini written by Rens Hollanders.<br><br><a href="http://renshollanders.nl/2013/02/mdt-2012-settings-for-fully-automated-lti-deployment-part-ii-customsettings-ini/">MDT 2012 Settings for fully automated LTI deployment, Part II: Customsettings.ini</a>

This will end PART 1 for MDT and Customsetting.ini Parameters. In Part 2, I will show how to create a bootable ISO using MDT and creating a bootable USB key.

Procede to Part 2 -
<A href=/blog/2018/09/12/Microsoft-Deployment-Toolkit-Initial-Configuration.html.md>Part 2 - Microsoft Deployment Toolkit (MDT) to Create Customize Bootable USB Key</a>



