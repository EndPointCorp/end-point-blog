---
author: "Selvakumar Arumugam"
title: "Shell Command Outputs Truncated in Python"
tags: python, shell
---

Recently I was working a python script to do some parsing and processing on the shell commands output in Ubuntu OS. The output showed up in python console was different from output of the shell. The below sections will walk through the debugging process to identify the root cause and implement a solution.

###Problem###
The following code block shows the output of shell commands which lists the installed packages name and version in Ubuntu.

```bash
# dpkg -l | grep ^ii | awk '{print $2 "    " $3}'
accountsservice    0.6.35-0ubuntu7.3
acl    2.2.52-1
adduser    3.113+nmu3ubuntu3
ant    1.9.3-2build1
ant-optional    1.9.3-2build1
apache2    2.4.7-1ubuntu4.18
apache2-bin    2.4.7-1ubuntu4.18
apache2-data    2.4.7-1ubuntu4.18
apache2-utils    2.4.7-1ubuntu4.18
apparmor    2.10.95-0ubuntu2.6~14.04.1
```

The above shell commands executed in python console but the output shows truncated values for few packages(accountsservice, adduser, apache2, etc...) version. Interesting right...

```python
>>> installed_packages = subprocess.check_output(['dpkg -l | grep ^ii | awk \'{print $2 "    " $3}\'']     shell=True)
>>> print installed_packages
accountsservice    0.6.35-0ubuntu7.
acl    2.2.52-1
adduser    3.113+nmu3ubuntu
ant    1.9.3-2build1
ant-optional    1.9.3-2build1
apache2    2.4.7-1ubuntu4.1
apache2-bin    2.4.7-1ubuntu4.1
apache2-data    2.4.7-1ubuntu4.1
apache2-utils    2.4.7-1ubuntu4.1
apparmor    2.10.95-0ubuntu2
```

###Root Cause###
To identify the root cause of the problem, start with source command `dpkg -l` without any filter and processing. I have noticed two different results for shell this command with and without less. The less command showed the complete result with scrolling as below.

```bash
# dpkg -l | less
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                                  Version                                    Architecture Description
+++-=====================================-==========================================-============-===============================================================================
rc  aacraid                               1.2.1-52011                                amd64        This driver supports Adaptec by PMC aacraid family of cards.
ii  accountsservice                       0.6.35-0ubuntu7.3                          amd64        query and manipulate user account information
ii  acl                                   2.2.52-1                                   amd64        Access control list utilities
ii  adduser                               3.113+nmu3ubuntu3                          all          add and remove users and groups
ii  ant                                   1.9.3-2build1                              all          Java based build tool like make
ii  ant-optional                          1.9.3-2build1                              all          Java based build tool like make - optional libraries
ii  apache2                               2.4.7-1ubuntu4.18                          amd64        Apache HTTP Server
ii  apache2-bin                           2.4.7-1ubuntu4.18                          amd64        Apache HTTP Server (binary files and modules)
ii  apache2-data                          2.4.7-1ubuntu4.18                          all          Apache HTTP Server (common files)
ii  apache2-utils                         2.4.7-1ubuntu4.18                          amd64        Apache HTTP Server (utility programs for web servers)
rc  apache2.2-common                      2.2.22-1ubuntu1.11                         amd64        Apache HTTP Server common files
ii  apparmor                              2.10.95-0ubuntu2.6~14.04.1                 amd64        user-space parser utility for AppArmor
```

But `dpkg -l` prints on the screen with truncated data due to the columns width constraint. The truncated values exactly matches with result of python console output. There we go, root cause of the problem is identified. 

```bash
# dpkg -l

Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                   Version          Architecture     Description
+++-======================-================-================-==================================================
rc  aacraid                1.2.1-52011      amd64            This driver supports Adaptec by PMC aacraid family
ii  accountsservice        0.6.35-0ubuntu7. amd64            query and manipulate user account information
ii  acl                    2.2.52-1         amd64            Access control list utilities
ii  adduser                3.113+nmu3ubuntu all              add and remove users and groups
ii  ant                    1.9.3-2build1    all              Java based build tool like make
ii  ant-optional           1.9.3-2build1    all              Java based build tool like make - optional librari
ii  apache2                2.4.7-1ubuntu4.1 amd64            Apache HTTP Server
ii  apache2-bin            2.4.7-1ubuntu4.1 amd64            Apache HTTP Server (binary files and modules)
ii  apache2-data           2.4.7-1ubuntu4.1 all              Apache HTTP Server (common files)
ii  apache2-utils          2.4.7-1ubuntu4.1 amd64            Apache HTTP Server (utility programs for web serve
rc  apache2.2-common       2.2.22-1ubuntu1. amd64            Apache HTTP Server common files
ii  apparmor               2.10.95-0ubuntu2 amd64            user-space parser utility for AppArmor
```

###Solution###
The subprocess module of python provides a option to get the exact output of the shell command when language is set to C as environment variable in check_output function argument. Below shell command in python console shows the output without any truncation by setting the language.

```
>>> installed_packages = subprocess.check_output(['dpkg -l | grep ^ii | awk \'{print $2 "    " $3}\''], shell=True, env={'LANG':'C'})
>>> print installed_packages
accountsservice    0.6.35-0ubuntu7.3
acl    2.2.52-1
adduser    3.113+nmu3ubuntu3
ant    1.9.3-2build1
ant-optional    1.9.3-2build1
apache2    2.4.7-1ubuntu4.18
apache2-bin    2.4.7-1ubuntu4.18
apache2-data    2.4.7-1ubuntu4.18
apache2-utils    2.4.7-1ubuntu4.18
apparmor    2.10.95-0ubuntu2.6~14.04.1
```

###Conclusion###
It is highly recommended to pass env={'LANG':'C'} argument to subprocess.check_output function whenever processing the shell commands output in python. It helps avoid unstable results in down the line due to truncated values.