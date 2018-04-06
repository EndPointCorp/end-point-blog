---
author: Szymon Lipiński
gh_issue_number: 765
tags: python
title: Installing Python in local directory
---

On one of our client’s Ubuntu 10.04 machines, I needed to upgrade Python
from 2.6 to 2.7. Unfortunately, after installing Python 2.7 from apt
the virtualenv, version 1.4.5, did not work
correctly. This bug was fixed in a newer virtualenv version, however
there were no Ubuntu packages available.

I thought about trying something else: why not install all the software
locally in my home directory on the server?
When virtualenv is used to create a new environment, it copies the
Python executable in to the virtualenv directory.

First I install pythonbrew, which is great software for
installing many different Python versions in a local directory.

```bash
$ curl -kL http://xrl.us/pythonbrewinstall | bash
```

Then I activate pythonbrew with:

```bash
$ source "$HOME/.pythonbrew/etc/bashrc"
```

And install the Python version I want:

```bash
$ pythonbrew install 2.7.3
```

The installation took a couple of minutes. The script downloaded the
tarball with the Python source code for the required version, compiled
it and installed.
It was writing all the information into a log file, which I was looking
at by running the command below in another console:

```bash
$ tail -f $HOME/.pythonbrew/log/build.log
```

You can also add the following lines to ~/.bashrc to activate this python after starting new bash session.

```bash
[[ -s "$HOME/.pythonbrew/etc/bashrc" ]] && source $HOME/.pythonbrew/etc/bashrc
pythonbrew switch 2.7.3
```

I run the below command to activate the pythonbrew script:

```bash
$ source $HOME/.pythonbrew/etc/bashrc
```

The python version changed:

```bash
$ python --version
Python 2.6.5

$ source $HOME/.pythonbrew/etc/bashrc

$ python --version
Python 2.7.2
```

As you can see, Python from my local installation is used:

```bash
$ which python
/home/szymon/.pythonbrew/pythons/Python-2.7.3/bin/python
```

The only thing left is to create the virtual environment for the new
Python version. I use virtualenvwrapper for managing virtualenv, so the
obvious way to create a new environment is:

```bash
$ mkvirtualenv --no-site-packages envname
```

Unfortunately, it creates an environment with the wrong Python version:

```bash
$ which python
/home/szymon/.virtualenvs/envname/bin/python

$ python --version
Python 2.6.5
```

So let’s try to tell virtualenvwrapper which Python file should be used:

```bash
$ deactivate

$ rmvirtualenv envname
Removing envname...

$ mkvirtualenv --no-site-packages -p /home/szymon/.pythonbrew/pythons/Python-2.7.3/bin/python envname
```

Unfortunately this ended with an error:

```bash
Running virtualenv with interpreter /home/szymon/.pythonbrew/pythons/Python-2.7.3/bin/python
New python executable in envname/bin/python
Traceback (most recent call last):
  File "/home/szymon/.virtualenvs/envname/lib/python2.7/site.py", line 67, in <module>
    import os
  File "/home/szymon/.virtualenvs/envname/lib/python2.7/os.py", line 49, in <module>
    import posixpath as path
  File "/home/szymon/.virtualenvs/envname/lib/python2.7/posixpath.py", line 17, in <module>
    import warnings
ImportError: No module named warnings
ERROR: The executable envname/bin/python is not functioning
ERROR: It thinks sys.prefix is '/home/szymon/.virtualenvs' (should be '/home/szymon/.virtualenvs/envname')
ERROR: virtualenv is not compatible with this system or executable
</module></module></module>
```

The problem is that the virtualenv version, used by virtualenvwrapper, doesn’t work with Python 2.7. As I wrote at the begining, there is no newer version available via apt.
The solution is pretty simple. Let’s just install the newer virtualenvwrapper and virtualenv version using pip.

```bash
$ pip install virtualenv
Requirement already satisfied: virtualenv in /usr/lib/pymodules/python2.6
Installing collected packages: virtualenv
Successfully installed virtualenv
```

As you can see, there is a problem. The problem is that there is used pip from system installation. There is no pip installed in my local Python 2.7 version. However there is easy_install:

```bash
$ which pip
/usr/bin/pip

$ which easy_install
/home/szymon/.pythonbrew/pythons/Python-2.7.3/bin/easy_install
```

So let’s use it for installing virtualenv and virtualenvwrapper:

```bash
$ easy_install virtualenv virtualenvwrapper
```


I’ve checked the whole installation procedure once again, it turned out that there was some network error while downloading pip, but unfortunately I didn’t notice the error. If everything is OK, then pip should be installed, and you should be able to install virtualenv using pip as well with:

```bash
$ pip install virtualenv virtualenvwrapper
```

Cool, let’s check which version is installed:

```bash
$ which virtualenv
/home/szymon/.pythonbrew/pythons/Python-2.7.3/bin/virtualenv

$ virtualenv --version
1.8.4
```

Before creating the brand new virtual environment, I have to activate the new virtualenvwrapper. I have the following line in my ~/.bashrc file:

```bash
source /usr/local/bin/virtualenvwrapper.sh
```

I just have to change it to the below line and login once again:

```bash
source /home/szymon/.pythonbrew/pythons/Python-2.7.3/bin/virtualenvwrapper.sh
```

Let’s now create the virtual environment using the brand new Python version:

```bash
$ mkvirtualenv --no-site-packages -p $HOME/.pythonbrew/pythons/Python-2.7.3/bin/python envname
```

I want to use this environment each time I log into this server, so I’ve added this line to my ~/.bashrc:

```bash
workon envname
```

Let's check if it works. I've logged out and logged in to my account on this server before running the following commands:

```bash
$ which python
/home/szymon/.virtualenvs/envname/bin/python

$ python --version
Python 2.7.3
```

Looks like everything is OK.
