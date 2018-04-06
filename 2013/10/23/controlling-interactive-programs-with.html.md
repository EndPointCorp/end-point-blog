---
author: Miguel Alatorre
gh_issue_number: 865
tags: automation, python
title: Controlling interactive programs with pexpect-u
---



A client I am working with requires that various machines have Ubuntu 10.04.4 installed along with certain software dependencies prior to installation of their own software.

In order to have our client avoid the tedious task of spinning up a new machine for each new client of theirs, I decided to attempt to automate the process (minus the OS installation) in Python.

A couple of the software installations require the user to interact with a console application. For example, this is the Matlab Runtime Environment installer:

<a href="/blog/2013/10/23/controlling-interactive-programs-with/image-0.png" imageanchor="1"><img border="0" src="/blog/2013/10/23/controlling-interactive-programs-with/image-0.png"/></a>

and the Passenger installer:

<a href="/blog/2013/10/23/controlling-interactive-programs-with/image-1.png" imageanchor="1"><img border="0" src="/blog/2013/10/23/controlling-interactive-programs-with/image-1.png"/></a>

Here I used the Python package pexpect-u which allows you to spawn child applications and control them automatically.

To spawn the Matlab installer I run:

```python
import pexpect
child = pexpect.spawn("sudo ./MCRInstaller.bin -console")
```

Now we tell pexpect what to expect:

```python
child.expect("Press 1 for Next, 3 to Cancel or 5 to Redisplay \[1\]")
```

And we send a command with:

```python
child.sendline("1")
```

The package can be found [here](https://pypi.python.org/pypi/pexpect-u/) and the source code includes many more examples, one of which might be of use for this very client: hive.py

This client has various installations of a Rails application and each sends requests to the same location on a server. Because this location changes periodically, each of the Rails application installations need a configuration variable updated. I think the following should do the trick:

```bash
python hive.py user1:pass2@host1 user2:pass2@host2 ... userN:passN@hostN
grep -rl 'old_location_path_string' /path/to/config/file | xargs sed -i 's/old_location_path_string/new_location_path_string/'
```

Let’s see it in action. I’ve set up two Ubuntu virtual machines and will be changing a string in a file that exists on both machines in the same location. First I login:

<a href="/blog/2013/10/23/controlling-interactive-programs-with/image-2.png" imageanchor="1"><img border="0" src="/blog/2013/10/23/controlling-interactive-programs-with/image-2.png"/></a>

Let’s look at the contents of the files:

<a href="/blog/2013/10/23/controlling-interactive-programs-with/image-3.png" imageanchor="1"><img border="0" src="/blog/2013/10/23/controlling-interactive-programs-with/image-3.png"/></a>

Now I’ll replace the string “Hello” with “Goodbye”:

<a href="/blog/2013/10/23/controlling-interactive-programs-with/image-4.png" imageanchor="1"><img border="0" src="/blog/2013/10/23/controlling-interactive-programs-with/image-4.png"/></a>

Because the user of each machine has permissions over the test.conf file, I was able to modify it without sudo. If you’ll be needing to use sudo to make any changes, take a look at the [:sync](https://bitbucket.org/takluyver/pexpect/src/e7a5e48e16d368e7a3151236984f6198d4a4dd1b/pexpect/examples/hive.py?at=default#cl-96) example here, however, note that if your sudo passwords differ on at least one of the remote machines this will not work.


