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

  |  Skip this wizard page  								   |  Using this property  								  |  	Configure these properties                                                                                   |
  |------------------------------------------------------------|------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|
  |  Welcome                								   |  SkipBDDWelcome       								  |								                                                                                     |
  |  Specify credentials for connecting to network shares      |  Skipped by providing properties in next column      |  ·  UserID<BR>·  UserDomain<BR>·  UserPassword             												         |
  |  Task Sequence                							   |  SkipTaskSequence       							  |  ·  TaskSequenceID               			     														         |
  |  Computer Details                						   |  SkipComputerName, SkipDomainMembership       		  |  ·  OSDComputerName<br>·  JoinWorkgroup<br>–or–<br>·  JoinDomain<br>·  DomainAdmin                               |
  |  User Data                								   |  SkipUserData       								  |  ·  UDDir <br>·  UDShare<br>·  UserDataLocation                     									         |
  |  Move Data and Settings                				       |  SkipUserData       								  |  ·  UDDir<br>·  UDShare<br>·  UserDataLocation                  										         |
  |  User Data (Restore)                					   |  SkipUserData       								  |  ·  UDDir<br>·  UDShare<br>·  UserDataLocation                      									         |
  |  Computer Backup                						   |  SkipComputerBackup                                  |  ·  BackupDir<br>·  BackupShare<br>·  ComputerBackupLocation                    						         |
  |  Product Key                							   |  SkipProductKey       								  |  ·  ProductKey<br>–or–<br>·  OverrideProductKey                   										         |
  |  Language Packs                							   |  SkipPackageDisplay       							  |  ·  LanguagePacks                        														                 |
  |  Locale and Time                						   |  SkipLocaleSelection, SkipTimeZone       			  |  ·  KeyboardLocale<br>·  UserLocale<br>·  UILanguage<br>·  TimeZone<br>·  TimeZoneName                           |
  |  Roles and Features                						   |  SkipRoles       									  |  ·  OSRoles<br>·  OSRoleServices<br>·  OSFeatures                       								         |
  |  Applications                						       |  SkipApplications       							  |  ·  Applications                        																         |
  |  Administrator Password                					   |  SkipAdminPassword       							  |  ·  AdminPassword                   																	         |
  |  Local Administrators                					   |  SkipAdminAccounts       							  |  ·  Administrators                     																	         |
  |  Capture Image                							   |  SkipCapture       							      |  ·  ComputerBackupLocation                      														         |
  |  Bitlocker                								   |  SkipBitLocker       					              |  ·  BDEDriveLetter<br>·  BDEDriveSize<br>·  BDEInstall<br>·  BDEInstallSuppress<br>·  							 |
  |															   |	                                                  |  ·  BDERecoveryKey<br>·  TPMOwnerPassword<br>·  OSDBitLockerStartupKeyDrive<br>·  OSDBitLockerWaitForEncryption  |   	
  |  Ready to begin                							   |  SkipSummary       								  |                              																					 |
  |  Operating system deployment completed successfully        |  SkipFinalSummary       							  |                              																					 |
  |  Operating system deployment did not complete successfully |  SkipFinalSummary       							  |                              																				     |

  
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

**Continue to Next Article**- <A href=/blog/2018/09/12/Microsoft-Deployment-Toolkit-Initial-Configuration.html.md>Part 2 - MDT Initial Configuration Steps</a>

#### Related Articles ####
<A href=/blog/2018/09/13/Microsoft-Deployment-Toolkit-Bootable-USB-Key.html.md>Part 3 - Microsoft Deployment Toolkit (MDT) - Create Customize Bootable USB Key using ISO Produced by MDT</a>

<a href="http://renshollanders.nl/2013/02/mdt-2012-settings-for-fully-automated-lti-deployment-part-ii-customsettings-ini/">MDT 2012 Settings for fully automated LTI deployment, Part II: Customsettings.ini</a>
