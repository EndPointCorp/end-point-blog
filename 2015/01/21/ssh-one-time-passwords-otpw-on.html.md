---
author: Greg Sabino Mullane
gh_issue_number: 1073
tags: chrome, security, ssh, sysadmin
title: SSH one-time passwords (otpw) on chromebook
---



<div class="separator" style="clear: both; float: right; margin-bottom: 1em; text-align: center;"><a href="/blog/2015/01/21/ssh-one-time-passwords-otpw-on/image-0-big.jpeg" imageanchor="1" style="clear: right; float: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2015/01/21/ssh-one-time-passwords-otpw-on/image-0.jpeg"/></a>
<br/><small><a href="https://flic.kr/p/e55Nqb">Henri Coandă Bucureşt Airport</a><br/>by <a href="https://www.flickr.com/photos/bortescristian/">Cristian Bortes</a></small></div>

A little while ago, I bought a [Chromebook](https://www.samsung.com/us/computer/chromebook) as an alternative to my sturdy-but-heavy laptop. So far, it has been great—quick boot up, no fan, long battery life, and light as a feather. Perfect for bringing from room to room, and for getting some work done in a darkened bedroom at night. The one large drawback was a lack of [SSH](https://en.wikipedia.org/wiki/Secure_Shell), a tool I use very often. I’ll describe how I used one-time passwords to overcome this problem, and made my Chromebook a much more productive tool.

The options for using SSH on [Chrome OS](https://en.wikipedia.org/wiki/Chrome_OS) are not that good. I downloaded and tried a handful of apps, but each had some significant problems. One flaw shared across all of them was a lack of something like [ssh-agent](https://en.wikipedia.org/wiki/Ssh-agent), which will cache your SSH passphrase so that you don’t have to type it every time you open a new SSH session. An option was to use a password-less key, or a very short passphrase, but I did not want to make everything less secure. The storage of the SSH private key was an issue as well—the Chromebook has very limited storage options, and relies on putting most things “in the cloud”.

What was needed was a way to use SSH in a very insecure environment, while providing as much security as possible. Eureka! A [one-time password](https://en.wikipedia.org/wiki/One-time_password) system is exactly what I needed. Specifically, the wonderful [otpw program](http://www.cl.cam.ac.uk/~mgk25/otpw.html). Chromebooks have a simple shell (accessed via ctrl-alt-t) that has SSH support. So the solution was to use one-time passwords and not store anything at all on the Chromebook.

Rather than trying to get otpw setup on all the servers I might need to reach, I simply set it up on my main laptop, carefully allowed incoming SSH connections, and now I can ssh from my Chromebook to my laptop. From there, to the world. Best of all, when I ssh in, I can use the already running ssh-agent on the laptop! All it takes is memorizing a single passphrase and securing a sheet of paper (which is far easier to secure than an entire Chromebook :)

Here are some details on how I set things up. On the Chromebook, nothing is needed except to open up a crosh tab with ctrl-alt-t, and run ssh. On the laptop side, the first step is to install the otpw program, and then configure PAM so that it uses it:

```
$ sudo aptitude install otpw-bin
$ sudo cat >> /etc/pam.d/ssh
  auth     required  pam_otpw.so
  session  optional  pam_otpw.so
```

That is the bare minimum, but I also wanted to make sure that only ‘local’ machines could SSH in. While there are a number of ways to do this, such as iptables or /etc/hosts.allow, I decided the best approach was to configure sshd itself. The “Match” directive instructs that the lines after it only take effect on a positive match. Thus:

```
$ sudo cat >> /etc/ssh/sshd_config
AllowUsers nobodyatall
Match Address 192.168.1.0/24,127.0.0.0
AllowUsers greg
$ service ssh restart
```

The next step is to create the one-time password list. This is done with the otwp-gen program; here is the command I use:

```
$ otpw-gen -e 30 | lpr
Generating random seed ...

If your paper password list is stolen, the thief should not gain access to your account with this information alone. Therefore, you need to memorize and enter below a prefix password. You will have to enter that each time directly before entering the one-time password (on the same line).

When you log in, a 3-digit password number will be displayed. It identifies the one-time password on your list that you have to append to the prefix password. If another login to your account is in progress at the same time, several password numbers may be shown and all corresponding passwords have to be appended after the prefix password. Best generate a new password list when you have used up half of the old one.

Enter new prefix password: 
Reenter prefix password: 

Creating '~/.otpw'.
Generating new one-time passwords ...
```

The otpw-gen command creates a file named **.otpw** in your home directory, which contains the hash of all the one-time passwords to use. In the example above, the **-e** controls the entropy of the generated passwords—in other words, how long they are. otpw-gen will not accept an entropy lower than 30, which will generate passwords that are five characters long. The default entropy, 48, generates passwords that are eight characters long, which I found a little too long to remember when trying to read from the printout in a dark room. :). Rather than show the list of passwords on the screen, or save them to a local file, the output goes directly to the printer. otpw-gen does a great job of formatting the page, and it ends up looking like this:

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/21/ssh-one-time-passwords-otpw-on/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/01/21/ssh-one-time-passwords-otpw-on/image-1.png"/></a></div>

Here are some close-ups of what the passwords look like at various entropies:

```
Sample output with a low entropy of 30:
OTPW list generated 2015-07-12 13:23 on gregsbox

000 GGS%F  056 bTqut  112 f8iJs  168 lQVjk  224 gNG2x  280 -x8ke  336 egm5n
001 urHLf  057 a/Wwh  113 -PEpV  169 9ABpK  225 -K2db  281 babfX  337 feeED
002 vqrX:  058 rZszx  114 r3m8a  170 -UzX3  226 g74RI  282 gusBJ  338 ;Tr4m
003 fa%6G  059 -i4FZ  115 nPEaJ  171 o64FR  227 uBu:h  283 uBo/U  339 ;pYY8
004 -LYZY  060 vWDnw  116 f5Sb+  172 hopr+  228 rWXvb  284 rksPQ  340 ;v6GN
```

```
Sample output with the default entropy of 48:
OTPW list generated 2015-15-05 15:53 on gregsbox

000 tcsx qqlb  056 ougp yuzo  112 lxwt oitl  168 giap vqsj  224 vtvk rjc/
001 mfui ukph  057 wbpw aktt  113 kert wozj  169 ihed psyx  225 ducx pze=
002 wwsj hdcr  058 jmwa mguo  114 idtk zrzw  170 ecow fepm  226 ikru hty+
003 aoeb klnz  059 pvie fbfc  115 fmlb sptb  171 ftrd jotb  227 mqns ivq:
004 yclw hyml  060 slvj ezfi  116 djsy ycse  172 butg guzm  228 pfyv ytq%
005 eilj cufp  061 zlma yxxl  117 skyf ieht  173 vbtd rmsy  229 pzyn zlc/
```

```
Sample output with a high entropy of 79:
OTPW list generated 2015-07-05 18:74 on gregsbox

000 jeo SqM bQ9Y ato  056 AyT jsc YbU0 rXB  112 Og/ I3O 39nY W/Z
001 AFk W+5 J+2m e1J  057 MXy O9j FjA8 8q;  113 a6A 8R9 /Ofr E4s
002 02+ XPB 8B2S +qT  058 Cl4 6g2 /9Bk KO=  114 HEK vd3 T2TT Rr.
003 Exb jqE iK49 rfX  059 Qhz eU+ J2VG kwQ  115 aJ7 tg1 dJsr vf.
004 Bg1 b;5 p0qI f/m  060 VKz dpa G7;e 7jR  116 kaL OSw dC8e kx.
```

The final step is to SSH from the Chromebook to the laptop! Hit ctrl-alt-t, and you will get a new tab with a crosh prompt. From there, attempt to ssh to the laptop, and you will see the usual otpw prompt:

```
$ ssh greg@192.168.1.10
Password 140: 
```

So you type in the passphrase you entered above when running the otpw-gen command, then pull out your sheet of paper and look up the matching password next to number 140. Voila! I am now connected securely to my more powerful computer, and can SSH from there to anywhere I am used to going to from my laptop. I can even run mutt as if I were at the laptop! A nice workaround for the limitations of the Chromebook.


