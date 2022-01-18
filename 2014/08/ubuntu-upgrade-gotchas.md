---
author: Greg Sabino Mullane
title: Ubuntu upgrade gotchas
github_issue_number: 1022
tags:
- linux
- ubuntu
date: 2014-08-16
---

<div class="separator" style="clear: both; float:right; text-align: center;"><a href="/blog/2014/08/ubuntu-upgrade-gotchas/image-0.jpeg" imageanchor="1" style="clear: right; margin-bottom: 1em; margin-left: 1em;"><img border="0" src="/blog/2014/08/ubuntu-upgrade-gotchas/image-0.jpeg"/></a><br/><small><a href="https://flic.kr/p/4ZTY63">African penguins</a> by <a href="https://www.flickr.com/photos/aresauburnphotos/">Nick Ares</a></small></div>

I recently upgraded my main laptop to [Ubuntu 14.04](https://en.wikipedia.org/wiki/Ubuntu_%28operating_system%29), and had to solve a few issues along the way. Ubuntu is probably the most popular Linux distribution. Although it is never my first choice (that would be FreeBSD or Red Hat), Ubuntu is superb at working “out of the box”, so I often end up using it, as the other distributions all have issues.

Ubuntu 14.04.1 is a major “LTS” version, where LTS is “long term support”. The [download page](https://www.ubuntu.com/download/desktop) states that 14.04 (aka “Trusty Tahr”) comes with “five years of security and maintenance updates, guaranteed.” Alas, the page fails to mention the release date, which was July 24, 2014. When a new version of Ubuntu comes out, the OS will keep nagging you until you upgrade. I finally found a block of time in which I could survive without my laptop, and started the upgrade process. It took a little longer than I thought it would, but went smoothly except for one issue:

### Issue 1: xscreensaver

During the install, the following warning appeared:

> “One or more running instances of xscreensaver or xlockmore have been detected on this system. Because of incompatible library changes, the upgrade of the GNU libc library will leave you unable to authenticate to these programs. You should arrange for these programs to be restarted or stopped before continuing this upgrade, to avoid locking your users out of their current sessions.”

First, this is a terrible message. I’m sure it has caused lots of confusion, as most users probably do not know what what xscreensaver and xlockmore are. Is it so hard for the installer to tell which one is in use? Why in the world can the installer not simply stop these programs itself?! The solution was simple enough: in a terminal, I ran:

```plain
pgrep -l screensaver
pkill screensaver
pgrep -l screensaver
```

The first command was to see if I had any programs running with “screensaver” in their name (I did: xscreensaver). As it was the only program that matched, it was safe to run the second command, which stopped xscreensaver. Finally, I re-ran the pgrep to make sure it was stopped and gone. Then I did the same thing with the string “lockmore” (which found no matches, as I expected). Once xscreensaver was turned off, I told the upgrade to continue, and had no more problems until after Ubuntu 14.04 was installed and running. The first post-install problem appeared after I suspended the computer and brought it back to life—​no wireless network!

### Issue 2: no wireless after suspend

Once suspended and revived, the wireless would simply not work. Everything looked normal: networking was enabled, wifi hotspots were detected, but a connection could simply not be made. After going through bug reports online and verifying the sanity of the output of commands such as “nmcli nm” and “lshw -C network”, I found a solution. This was the hardest issue to solve, as it had no intuitive solution, nothing definitive online, and was full of red herrings. What worked for me was to *remove* the suspension of the iwlwifi module. I commented out the line from **/etc/pm/config.d/modules**, in case I ever need it again, so the file now looks like this:

```plain
# SUSPEND_MODULES=“iwlwifi”
```

Once that was commented out, everything worked fine. I tested by doing **sudo pm-suspend** from the command-line, and then bringing the computer back up and watching it automatically reconnect to my local wifi.

### Issue 3: color diffs in Git

I use the command-line a lot, and a day never goes by without heavy use of
[Git](https://en.wikipedia.org/wiki/Git_%28software%29) as well. On running a `git diff` in the new Ubuntu version, I was surprised to see a bunch of escape codes instead of the usual pretty colors I was used to:

```palin
ESC[1mdiff --git a/t/03dbmethod.t b/t/03dbmethod.tESC[m
ESC[1mindex 108e0c5..ffcab48 100644ESC[m
ESC[1m--- a/t/03dbmethod.tESC[m
ESC[1m+++ b/t/03dbmethod.tESC[m
ESC[36m@@ -26,7 +26,7 @@ESC[m ESC[mmy $dbh = connect_database();ESC[m
 if (! $dbh) {ESC[m
    plan skip_all => 'Connection to database failed, cannot continue testing';ESC[m
 }ESC[m
ESC[31m-plan tests => 543;ESC[m
ESC[32m+ESC[mESC[32mplan tests => 545;ESC[m
```

After poking around with terminal settings and the like, a coworker suggested I simply tell git to use an intelligent pager with the command `git config --global core.pager "less -r"`. The output immediately improved:

```diff
diff --git a/t/03dbmethod.t b/t/03dbmethod.t
index 108e0c5..ffcab48 100644
--- a/t/03dbmethod.t
+++ b/t/03dbmethod.t
@@ -26,7 +26,7 @@ my $dbh = connect_database();
 if (! $dbh) {
    plan skip_all => 'Connection to database failed, cannot continue testing';
 }
-plan tests => 543;
+plan tests => 545;
```

Thanks, [Josh Williams](/team/josh-williams/)! The above fix worked perfectly.

### Issue 4: cannot select text in emacs

The top three programs I use every day are ssh, git, and [emacs](https://en.wikipedia.org/wiki/Emacs). While trying (post-upgrade) to reply to an email inside [mutt](https://en.wikipedia.org/wiki/Mutt_%28e-mail_client%29), I found that I could not select text in emacs using ctrl-space. This is a critical problem, as this is an extremely important feature to lose in emacs. This problem was pretty easy to track down. The program “ibus” was intercepting all ctrl-space calls for its own purpose. I have no idea why ctrl-space was chosen, being used by emacs since before Ubuntu was even born (the technical term for this is “crappy default”). Fixing it requires visiting the ibus-setup program. You can reach it via the system menu by going to **Settings Manager**, then scroll down to the **“Other”** section and find **“Keyboard Input Methods”**. Or you can simply run **ibus-setup** from your terminal (no sudo needed).

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/08/ubuntu-upgrade-gotchas/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/08/ubuntu-upgrade-gotchas/image-1.png"/></a><br/>The ibus-setup window</div>

However you get there, you will see a section labelled “Keyboard Shortcuts”. There you will see a “Next input method:” text box, with the inside of it containing **<Control>space**. Aha! Click on the three-dot button to the right of it, and change it to something more sensible. I decided to simply add an “Alt”, such that going to the next input method will require Ctrl-Alt-Space rather than Ctrl-Space. To make that change, just select the “Alt” checkbox, click “Apply”, click “Ok”, and verify that the text box now says **<Control><Alt>space**.

So far, those are the only issues I have encountered using Ubuntu 14.04. Hopefully this post is useful to someone running into the same problems. Perhaps I will need to refer back to it in a few years(?) when I upgrade Ubuntu again! :)
