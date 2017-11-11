---
author: Emanuele “Lele” Calò
gh_issue_number: 1299
tags: redhat, linux, security, selinux, wordpress
title: SELINUX=disabled? Read this and think twice!
---

Not long ago, one of our customers had their website compromised because of a badly maintained, not-updated ***WordPress***. At **End Point** we love WordPress, but it really needs to be configured and hardened the right way, otherwise it's easy to end up in a real nightmare.

This situation is worsened even more if there's no additional security enforcement system to protect the environment on which the compromised site lives. One of the basic ways to protect your Linux server, especially RHEL/Centos based ones, is using **SELinux**.

Sadly, most of the interaction people has with SELinux happens while disabling it, first on the running system:

```
setenforce disabled
# or
setenforce 0
```

and then permanently by manually editing the file **/etc/sysconfig/selinux** to change the variable **SELINUX=enforcing** to **SELINUX=disabled**.

Is that actually a good idea though? While SELinux can be a bit of a headache to tune appropriately and can easily be misconfigured, here's something that could really convince you to think twice before disabling SELinux once and forever.

Back to our customer's compromised site. While going through the customer's system for some post-crisis cleaning, I found this hilarious piece of bash_history:

```
ls
cp /tmp/wacky.php .
ls -lFa
vim wacky.php
set
ls -lFa
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
fg
ls -lFa
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
vim wacky.php
php wacky.php 2&gt;&amp;1 | less
php wacky.php &gt; THE-EVIL 2&gt;&amp;1
vim THE-EVIL
ls -lFA
less wacky.php
ls
less THE-EVIL
less wacky.php
cat /selinux/enforce
ls
less THE-EVIL
exit
```

As you can see, what happened was that the attacker was able to manage having a shell connection as the customer user, and started using a *PHP files injected in /tmp* as a possible further vector of attack.

Sadly, for the attacker at least, what happened was that *SELinux was setup in enforcing* mode with some strict rules and prevented all kind of execution on that specific script so after a few frantic attempts the attacker surrendered.

Looking into the **/var/log/audit/auditd.log** file I found all the **type=AVC** denied errors that SELinux was shouting while forbidding the attacker to pursue his nefarious plan.

Hilarious and good props to SELinux for saving the day.

***less THE-EVIL, more SELinux!*** 🙂
