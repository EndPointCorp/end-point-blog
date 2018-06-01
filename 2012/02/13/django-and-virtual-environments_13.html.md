---
author: Szymon Lipiński
gh_issue_number: 553
tags: django, python
title: Django and Virtual Environments
---

When you have to work with a bunch of different Python applications, the usual problem is that you have to deal with plenty of different packages in different versions. Each application needs its own set of libraries. Usually the versions of the libraries vary between the applications.

To solve all the problems you could create Python virtual environments. There is a great tool: [virtualenv](http://pypi.python.org/pypi/virtualenv). It can create virtual environments for Python. Using it is not too nice. However there is a wrapper to it, called [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/). It wraps all the virtualenv commands into a couple of shell commands.

Let's assume that I need to work on two applications written in Django 1.2 and Django 1.3. Each of the applications needs different set of packages in different versions. I will create two virtual environments.

Installing virtualenvwrapper on Ubuntu is pretty easy:

```nohighlight
$ sudo apt-get install virtualenvwrapper
```

After the installation there is a couple of new commands. The basic one is: mkvirtualenv which creates a new environment. Let’s create one.

```nohighlight
$ mkvirtualenv django_demo_12
```

This command automatically switches to the new environment, so you might notice that the prompt changed. The prompt always starts with the name of current virtual environment.

Let’s create another one, called django_demo_13 (to use Django 1.3 there).

```nohighlight
(django_demo_12)$ mkvirtualenv django_demo_13
```

The list of environments is printed by the command workon, when called without arguments.

```nohighlight
$ workon
django_demo_12
django_demo_13
```

As you can see, there are two environments ready to use. You can pass the name of the virtual environment as parameter to the workon command. Now let’s install Django 1.2 on the environment django_demo_12.

First of all switch to the new environment:

```nohighlight
$ workon django_demo_12
```

Now the prompt changed, so you can always be sure which Python virtual environment you are using.

```nohighlight
(django_demo_12)$
```

Now Django should be installed. There is a couple of ways to install it. The one I prefer is to create a text file with names and versions of all needed packages. This file will be named requirements.txt and will contain only this one line so far (other packages will be added later):

```nohighlight
Django==1.2.7
```

To install the packages listed in the file, I will use the command “pip install -r requirements.txt”:

```nohighlight
(django_demo_12)$ pip install -r requirements.txt
Downloading/unpacking Django==1.2.7 (from -r requirements.txt (line 1))
Downloading Django-1.2.7.tar.gz (6.4Mb): 6.4Mb downloaded
Running setup.py egg_info for package Django

Installing collected packages: Django
Running setup.py install for Django
changing mode of build/scripts-2.7/django-admin.py from 664 to 775

changing mode of /home/szymon/.virtualenvs/django_demo_12/bin/django-admin.py to 775
Successfully installed Django
Cleaning up...
```

Now I can check which Django version is installed:

```nohighlight
(django_demo_12)$ django-admin.py --version
1.2.7
```

Now I will create a standard Django project:

```nohighlight
(django_demo_12)$ django-admin.py startproject django_demo_12
```

The only additional thing here is to move the requirements.txt file info the Django project:

```nohighlight
(django_demo_12)$ mv requirements.txt django_demo_12
```

To create application using Django 1.3 the steps are similar. The first thing is to switch to another virtual environment:

```nohighlight
(django_demo_12)$ workon django_demo_13
```

From this moment it will be almost the same as in the previous environment, with the change that the requirements file should contain:

```nohighlight
Django==1.3.1
```

The commands are:

```nohighlight
(django_demo_13)$ pip install -r requirements.txt
(django_demo_13)$ django-admin.py startproject django_demo_13
(django_demo_13)$ mv requirements.txt django_demo_13
```

So now there are two different Python environments, totally separated from each other. When I install something in one of them, it is not installed in the other, so I can have different packages for different Django versions.

The best way to install a package here is to update the requirements.txt file, and run the “pip install -r requirements.txt” once again. Later it will be easier to give the whole code to another programmer, who then could run the command on his computer and it will automatically install all needed packages (each in exactly needed version).

There is one simple command left. Sometimes you just want to remove the virtual environment from the path and use standard python libraries installed in the system. It can be done using this command:

```nohighlight
(django_demo_13)$ deactivate
```
