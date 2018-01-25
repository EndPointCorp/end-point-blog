---
author: Selvakumar Arumugam
gh_issue_number: 1158
tags: automation, linux, sysadmin, ubuntu, update
title: Install Tested Packages on Production Server
---



One of our customers has us to do scheduled monthly OS updates following a specific rollout process. First week of the month, we will update the test server and wait for a week to confirm that everything looks as expected in the application; then next week we apply the very same updates to the production servers.

Since not long ago we used to use aptitude to perform system updates. While doing the update on the test server, we also executed aptitude on production servers to “freeze” the same packages and version to be updated on following week. That helped to ensure that only tested packages would have been updated on the production servers afterward.

Since using aptitude in that way wasn’t particularly efficient, we decided to use directly apt-get to stick with our standard server update process. We still wanted to keep our test-production synced updated process cause software updates released between the test and the production server update are untested in the customer specific environment. Thus we needed to find a method to filter out the unneeded packages for the production server update.

In order to do so we have developed a shell script that automates the process and maintain the package version in test and production in sync during OS updates. I’ll explain the processes involved used on both the test and the production servers.

### Test Server Update Process:

- Update the repository index
- Get the list of installed packages and version before update
- Complete the dist-upgrade
- Get the list of installed packages and version after update
- Compare the packages before and after the update and generate a diff output which has the information about the packages installed, updated and removed

#### Example:

```bash
root@selva_test:~# ./auto-tested-server-update.sh -t test

    ##########################################################
    ############ Auto Tested Server Update Script ############
    ##########################################################

Packages index list and server update will be completed here...
```
Files were generated in default directory. after_* and before_* contains the installed packages list before and after server update. diff_* contains the changes of the packages in the system.

```bash
root@selva_test:~# ls tmp/
after_update_selva_test.2015-09-02.txt  before_update_selva_test.2015-09-02.txt  diff_server_update_selva_test.2015-09-02.txt

# head -5 tmp/before_update_selva_test.2015-09-02.txt 
accountsservice=0.6.15-2ubuntu9.6
acl=2.2.51-5ubuntu1
acpi-support=0.140.1
acpid=1:2.0.10-1ubuntu3
activity-log-manager-common=0.9.4-0ubuntu3.2

# head -5 tmp/after_update_selva_test.2015-09-02.txt 
accountsservice=0.6.15-2ubuntu9.6
acl=2.2.51-5ubuntu1
acpi-support=0.140.1
acpid=1:2.0.10-1ubuntu3
activity-log-manager-common=0.9.4-0ubuntu3.2

# cat tmp/diff_server_update_selva_test.2015-09-02.txt 
             > git=1:1.7.9.5-1ubuntu0.1
             > git-man=1:1.7.9.5-1ubuntu0.1
metacity=1:2.34.1-1ubuntu11          <
mysql-client=5.43-0ubuntu0.12.04.1         | mysql-client=5.5.43-0ubuntu0.12.04.1
ubuntu-desktop=1.267.1           <
unity-2d=5.14.0-0ubuntu1          <
             > wget=1.13.4-2ubuntu1
```

### Production Server Update Process:

- Get the diff output file (which has information about packages installed, updated and removed packages) from the test server
- Collect the packages which will be changed on server update
- Process the packages to categorize under install, upgrade and remove
- Filter the packages from test server installed, upgraded and removed packages
- Perform the install/upgrade/remove actions based on the filtered tested packages

#### Example:

```bash
root@selva_prod:~# ./auto-tested-server-update.sh -t prod -S selva_test -U root

    ##########################################################
    ############ Auto Tested Server Update Script ############
    ##########################################################

*** Production Server Update Process ***

      remote_user: root
      remote_server: selva_prod
      remote_path: /root/tmp
    
1./root/tmp/diff_server_update_selva_test.2015-09-02.txt
Enter a number to choose file: 1
INFO: You have selected the file: diff_server_update_selva_test.2015-09-02.txt
INFO: scp root@selva_test:/root/tmp/diff_server_update_selva_test.2015-09-02.txt /root/tmp
diff_server_update_selva_test.2015-09-02.txt                       100%  763     0.8KB/s   00:00  
  
INFO: Fetching the list of packages need to be changed...!

*********************** Installation *************************
INFO: No packages to install
**************************************************************

************************* Upgrade ****************************
apt-get install mysql-client=5.5.43-0ubuntu0.12.04.1
Reading package lists... Done
Building dependency tree
etc...
**************************************************************

************************** Removal ***************************
apt-get remove zenity=3.4.0-0ubuntu4 zenity-common=3.4.0-0ubuntu4
Reading package lists... Done
Building dependency tree
etc...
**************************************************************
```

As showed in the sample output above, the script will then run through different phases in which it will install/upgrade/remove all the needed packages in the target production system. 

In this way we ensure that all packages tested in the test environment will be replayed on the production server to minimize the chances of introducing bugs and maximize application stability during production system updates.

The Git repository below contains the script and a few additional information to use it.

[https://github.com/selvait90/auto-tested-server-update](https://github.com/selvait90/auto-tested-server-update)


