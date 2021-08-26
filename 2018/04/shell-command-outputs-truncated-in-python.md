---
author: Selvakumar Arumugam
title: Shell Command Outputs Truncated in Python
github_issue_number: 1403
tags:
- python
- shell
- environment
date: 2018-04-05
---

<img src="/blog/2018/04/shell-command-outputs-truncated-in-python/programmers-reviewing-code-on-computer_925x.jpg" alt="Two guys working at computers" /><br />
<small>[Photo by Sarah Pflug of Burst](https://burst.shopify.com/photos/programmers-reviewing-code-on-computer)</small>

Recently I was working on a Python script to do some parsing and processing on the output of shell commands in Ubuntu. The output that showed up was truncated.

The below sections will walk through the debugging process to identify the root cause and implement a solution with detailed explanation, using Python 2.

### Problem

The following code block shows the output of a shell command which lists the installed packages, name and version, in Ubuntu.

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

The same shell command executes in the Python console but the output shows truncated values for a few packages’ versions, for example, accountsservice, adduser, apache2, etc.

```python
>>> import subprocess
>>> installed_packages = subprocess.check_output(['dpkg -l | grep ^ii | awk \'{print $2 "    " $3}\''], shell=True)
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

### Root Cause

To identify the root cause of the problem, I started with source command `dpkg -l` command without any filters and processing. I have noticed two different results for this command, with and without less command. The less command showed the complete result with scrolling as below.

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

But `dpkg -l` prints on the screen with truncated data due to the columns width constraint. The truncated values exactly match the Python console output. The output column width is decided by environment variable COLUMNS and commands restrict the column width in output based on COLUMNS value.

```bash
# echo $COLUMNS
127

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

### Solution

The subprocess module of Python provides complete untruncated output of the shell command when the argument `env={}` is passed to check_output function:

```
>>> installed_packages = subprocess.check_output(['dpkg -l | grep ^ii | awk \'{print $2 "    " $3}\''], shell=True, env={})
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

### Explanation

Curious to know what is happening behind the scenes? The check_output function uses C library functions `execv` or `execve` for processing. It chooses the function based on the `env` argument.

Reference:

 - [subprocess documentation](https://docs.python.org/2/library/subprocess.html)

 - [subprocess.py source](https://github.com/python/cpython/blob/master/Lib/subprocess.py)

 - [posixsubprocess.c source](https://github.com/google/python-subprocess32/blob/master/_posixsubprocess.c)

When no env argument is passed to `subprocess.check_output`, the `os.execv` function is called.

When an env argument is passed to `subprocess.check_output`, the `os.execve` function is called.

```c
for (i = 0; exec_array[i] != NULL; ++i) {
    const char *executable = exec_array[i];
    if (envp) {
        execve(executable, argv, envp);
    } else {
        execv(executable, argv);
    }
```

What makes the `execv` and `execve` functions produce different output?

The `execv` function passes through the shell COLUMNS variable which leads to truncating output columns to 127 width, like our reference system.

```
# echo $COLUMNS
127

>>> print subprocess.check_output(['dpkg -l | grep libqtcore4'], shell=True)
ii  libqtcore4:amd64          4:4.8.5+git192-g0 amd64             Qt 4 core module

>>> print subprocess.check_output(['dpkg -l | grep libqtcore4'], shell=True, env={'COLUMNS':'127'})
ii  libqtcore4:amd64          4:4.8.5+git192-g0 amd64             Qt 4 core module
```

The `execve` function uses additional argument environment variables and it is based on the `environ` function. It uses environment variables available in env command which doesn't have COLUMNS initialised. So output values returned without any column width restriction.

```
>>> print subprocess.check_output(['dpkg -l | grep libqtcore4'], shell=True, env={})
ii  libqtcore4:amd64                      4:4.8.5+git192-g085f851+dfsg-2ubuntu4.1    amd64        Qt 4 core module

>>> print subprocess.check_output(['dpkg -l | grep libqtcore4'], shell=True, env={'COLUMNS':''})
ii  libqtcore4:amd64                      4:4.8.5+git192-g085f851+dfsg-2ubuntu4.1    amd64        Qt 4 core module

```

For more details refer to the man pages of `execv`, `execve`, `environ`.

### Conclusion

It is always good to pass `env={}` argument to `subprocess.check_output` function whenever processing shell command output in Python. It helps avoid unstable results down the line due to truncated values.
