---
author: Charles Chang
title: 'Microsoft Deployment Toolkit (MDT) to Create Customize Bootable USB Key - Customsetting.ini'
tags: windows, iso, servers
gh_issue_number: 1457
---

### PART 1 - MDT and Customsetting.ini Parameters ###

#### Introduction ####
The customsetting.ini is a important part of the Microsoft Deployment Toolkit which sets rules on how your deployment will run. Would you need to disable certain interactive parts of the deployment? or would you want the person who's installing the operating system to interact with the installation. These are all possible by setting the customsetting.ini paramters. Please read below to get a better sense of how to use various customsetting.ini parameters. Happy reading!

#### Customsetting.ini Parameters ####
<table width=100% border=1>
  <tr>
    <th width=33%><b>Skip this wizard page</b></th>
    <th width=30%><b>Using this property</b></th>
    <th width=37%><b>Configure these properties</b></th>
  </tr>
  
    <tr valign=top>
    <th>Welcome</th>
    <th>SkipBDDWelcome</th>
    <th></th>
  </tr>
  
  <tr valign=top>
    <th>Specify credentials for connecting to network shares</th>
    <th>Skipped by providing properties in next column</th>
    <th>·  UserID<BR>·  UserDomain<BR>·  UserPassword</th>
  </tr>
  
    <tr valign=top>
    <th>Task Sequence</th>
    <th>SkipTaskSequence</th>
    <th>·  TaskSequenceID</th>
  </tr>
  
      <tr valign=top>
    <th>Computer Details</th>
    <th>SkipComputerName, SkipDomainMembership</th>
    <th>·  OSDComputerName<br>·  JoinWorkgroup<br>–or–<br>·  JoinDomain<br>·  DomainAdmin</th>
  </tr>
  
      <tr valign=top>
    <th>User Data</th>
    <th>SkipUserData</th>
    <th>·  UDDir <br>·  UDShare<br>·  UserDataLocation</th>
  </tr>
  
      <tr valign=top>
    <th>Move Data and Settings</th>
    <th>SkipUserData</th>
    <th>·  UDDir<br>·  UDShare<br>·  UserDataLocation</th>
  </tr>
  
      <tr valign=top>
    <th>User Data (Restore)</th>
    <th>SkipUserData</th>
    <th>·  UDDir<br>·  UDShare<br>·  UserDataLocation</th>
  </tr>
  
      <tr valign=top>
    <th>Computer Backup</th>
    <th>SkipComputerBackup</th>
    <th>·  BackupDir<br>·  BackupShare<br>·  ComputerBackupLocation</th>
  </tr>
  
      <tr valign=top>
    <th>Product Key</th>
    <th>SkipProductKey</th>
    <th>·  ProductKey<br>–or–<br>·  OverrideProductKey</th>
  </tr>
  
      <tr valign=top>
    <th>Language Packs</th>
    <th>SkipPackageDisplay</th>
    <th>·  LanguagePacks</th>
  </tr>
  
      <tr valign=top>
    <th>Locale and Time</th>
    <th>SkipLocaleSelection, SkipTimeZone</th>
    <th>·  KeyboardLocale<br>·  UserLocale<br>·  UILanguage<br>·  TimeZone<br>·  TimeZoneName</th>
  </tr>
  
      <tr valign=top>
    <th>Roles and Features</th>
    <th>SkipRoles</th>
    <th>·  OSRoles<br>·  OSRoleServices<br>·  OSFeatures</th>
  </tr>
  
      <tr valign=top>
    <th>Applications</th>
    <th>SkipApplications</th>
    <th>·  Applications</th>
  </tr>
  
      <tr valign=top>
    <th>Administrator Password</th>
    <th>SkipAdminPassword</th>
    <th>·  AdminPassword</th>
  </tr>
  
      <tr valign=top>
    <th>Local Administrators</th>
    <th>SkipAdminAccounts</th>
    <th>·  Administrators</th>
  </tr>
  
      <tr valign=top>
    <th>Capture Image</th>
    <th>SkipCapture</th>
    <th>·  ComputerBackupLocation</th>
  </tr>
  
      <tr valign=top>
    <th>Capture Image</th>
    <th>SkipCapture</th>
    <th>·  ComputerBackupLocation</th>
  </tr>
  
      <tr valign=top>
    <th>Bitlocker</th>
    <th>SkipBitLocker</th>
    <th>·  BDEDriveLetter<br>·  BDEDriveSize<br>·  BDEInstall<br>·  BDEInstallSuppress<br>·  BDERecoveryKey<br>·  TPMOwnerPassword<br>·  OSDBitLockerStartupKeyDrive<br>·  OSDBitLockerWaitForEncryption</th>
  </tr>
  
      <tr valign=top>
    <th>Ready to begin</th>
    <th>SkipSummary</th>
    <th></th>
  </tr>
  
    <tr valign=top>
    <th>Operating system deployment completed successfully</th>
    <th>SkipFinalSummary</th>
    <th></th>
  </tr>
  
    <tr valign=top>
    <th>Operating system deployment did not complete successfully</th>
    <th>SkipFinalSummary</th>
    <th></th>
  </tr>
</table>


#### Sample Customsetting.ini ####

Below is an sample of a few commonly used parameters in customsetting.ini.<br>

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

In Part 2, I will go over how to configure Microsoft Deployment Toolkit and build an customize OS install.

Continue to - <br>
**Link:** <A href=/blog/2018/09/12/Microsoft-Deployment-Toolkit-Initial-Configuration.html.md>Part 2 - MDT Initial Configuration Steps</a>
***
#### Related Articles ####
**Link:** <A href=/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key.html.md>Part 3 - Microsoft Deployment Toolkit (MDT) - Create Customize Bootable USB Key using ISO Produced by MDT</a>

**Link:**  <a href="http://renshollanders.nl/2013/02/mdt-2012-settings-for-fully-automated-lti-deployment-part-ii-customsettings-ini/">MDT 2012 Settings for fully automated LTI deployment, Part II: Customsettings.ini</a>
