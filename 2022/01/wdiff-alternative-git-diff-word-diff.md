---
author: "Jon Jensen"
title: "Word diff: Git as wdiff alternative"
date: 2022-01-05
tags:
- git
- terminal
- visual-studio-code
- intellij-idea
- tips
github_issue_number: 1816
---

![5 drinking fountains mounted on a wall at varying levels](/blog/2022/01/wdiff-alternative-git-diff-word-diff/20210823_183559-sm.jpg)

<!-- Image by Jon Jensen -->

The `diff` utility to show differences between two files was created in 1974 as part of Unix. It has been incredibly useful and popular ever since, and hasn't changed much since 1991 when it gained the ability to output the now standard "unified context diff" format.

The comparison `diff` makes is per line, so if anything on a given line changes, in unified context format we can tell that the previous version of that line was removed by seeing `-` at the beginning of the old line, and the following line will start with `+` followed by the new version.

For example see this Dockerfile that had two lines changed:

```diff
$ diff -u Dockerfile.old Dockerfile
--- Dockerfile.old	2022-01-05 22:16:21 -0700
+++ Dockerfile	2022-01-05 23:08:55 -0700
@@ -2,7 +2,7 @@
 
 WORKDIR /usr/src/app
 
-# Bundle app source
+# Bundle entire source
 COPY . .
 
-RUN /usr/src/app/test.sh
+RUN /usr/src/app/start.sh
```

That works well for visually reviewing changes to many types of files that developers typically work with.

It can also serve as input to the `patch` program, which dates to 1985 and is still in wide use as a counterpart to `diff`. With `patch` we can apply changes to a file and avoid the need to send an entire new file or apply changes by hand (which is very prone to error).

But let's leave that aside and focus on humans reading `diff` output.

### Diffing paragraphs

For a file containing paragraphs of prose each on their own long lines, it can look like the lines change completely when we change only a few words. This is often the case with HTML destined to be displayed in a web browser, email text, or the Markdown source for this blog post itself.

Consider this file with one long line of sample text gathered from pangrams and typing exercises:

```plain
$ cat -n paragraph.txt 
     1	The quick brown fox jumped over the lazy dog's back 1234567890 times. Now is the time for all good men to come to the aid of the party. Waltz, bad nymph, for quick jigs vex. Glib jocks quiz nymph to vex dwarf. Sphinx of black quartz, judge my vow. How vexingly quick daft zebras jump! The five boxing wizards jump quickly. Jackdaws love my big sphinx of quartz. Pack my box with five dozen liquor jugs.
```

If we change even one character of that, `diff` will show that its one line changed, but we have to painstakingly visually scan the entire long line to determine what exactly changed and where. That is not very useful.

We can wrap, or split up, the lines into multiple lines of a maximum of 75 characters with the classic Unix tool `fmt`:

```plain
$ fmt paragraph.txt | tee wrapped.txt
The quick brown fox jumped over the lazy dog's back 1234567890
times. Now is the time for all good men to come to the aid of the
party. Waltz, bad nymph, for quick jigs vex. Glib jocks quiz nymph
to vex dwarf. Sphinx of black quartz, judge my vow. How vexingly
quick daft zebras jump! The five boxing wizards jump quickly.
Jackdaws love my big sphinx of quartz. Pack my box with five dozen
liquor jugs.
```

With those shorter lines, changes will be easier to see than with one long line, but it is still hard to pick out small changes:

```diff
$ diff -u wrapped.txt wrapped2.txt         
--- wrapped.txt	2022-01-05 23:22:46 -0700
+++ wrapped2.txt	2022-01-05 23:38:14 -0700
@@ -1,7 +1,7 @@
 The quick brown fox jumped over the lazy dog's back 1234567890
-times. Now is the time for all good men to come to the aid of the
+times. Now is thy time for all good men to come to the aid of the
 party. Waltz, bad nymph, for quick jigs vex. Glib jocks quiz nymph
 to vex dwarf. Sphinx of black quartz, judge my vow. How vexingly
-quick daft zebras jump! The five boxing wizards jump quickly.
+quick daft zebras jump! Tho five boxing wizards jump quickly.
 Jackdaws love my big sphinx of quartz. Pack my box with five dozen
 liquor jugs.
```

And much worse, every line changes when we make a significant edit early in the text and reflow the paragraph to fit our maximum line length. Here is what happens after adding "an amazing count of" in the first line and re-wrapping the lines:

```diff
diff -u wrapped.txt wrapped3.txt
--- wrapped.txt	2022-01-05 23:22:46 -0700
+++ wrapped3.txt	2022-01-06 08:05:33 -0700
@@ -1,7 +1,7 @@
-The quick brown fox jumped over the lazy dog's back 1234567890
-times. Now is the time for all good men to come to the aid of the
-party. Waltz, bad nymph, for quick jigs vex. Glib jocks quiz nymph
-to vex dwarf. Sphinx of black quartz, judge my vow. How vexingly
-quick daft zebras jump! The five boxing wizards jump quickly.
-Jackdaws love my big sphinx of quartz. Pack my box with five dozen
-liquor jugs.
+The quick brown fox jumped over the lazy dog's back an amazing count
+of 1234567890 times. Now is thy time for all good men to come to
+the aid of the party. Waltz, bad nymph, for quick jigs vex. Glib
+jocks quiz nymph to vex dwarf. Sphinx of black quartz, judge my
+vow. How vexingly quick daft zebras jump! Tho five boxing wizards
+jump quickly.  Jackdaws love my big sphinx of quartz. Pack my box
+with five dozen liquor jugs.
```

That gives no aid to a human proofreader!

### Word diff to the rescue

In 1992 François Pinard wrote the word-based diff program `wdiff` which is now part of the GNU project. It solves this problem.

Here is how it shows us our example changing two words:

```plain
$ wdiff wrapped.txt wrapped2.txt   
The quick brown fox jumped over the lazy dog's back 1234567890
times. Now is [-the-] {+thy+} time for all good men to come to the aid of the
party. Waltz, bad nymph, for quick jigs vex. Glib jocks quiz nymph
to vex dwarf. Sphinx of black quartz, judge my vow. How vexingly
quick daft zebras jump! [-The-] {+Tho+} five boxing wizards jump quickly.
Jackdaws love my big sphinx of quartz. Pack my box with five dozen
liquor jugs.
```

Words removed are by default marked with `[-…-]` and words added with `{+…+}`.

It even knows how to accommodate word changes appearing on different lines! Trying it out on our example with the reflowed paragraph:

```plain
$ wdiff wrapped.txt wrapped3.txt
The quick brown fox jumped over the lazy dog's back {+an amazing count
of+} 1234567890 times. Now is [-the-] {+thy+} time for all good men to come to
the aid of the party. Waltz, bad nymph, for quick jigs vex. Glib
jocks quiz nymph to vex dwarf. Sphinx of black quartz, judge my
vow. How vexingly quick daft zebras jump! [-The-] {+Tho+} five boxing wizards
jump quickly.  Jackdaws love my big sphinx of quartz. Pack my box
with five dozen liquor jugs.
```

So this is very nice, although `wdiff` often isn't available by default on the various systems we find ourselves on, and it is perhaps a bit worrisome that the `wdiff` software has not been updated since 2014.

Too bad this word-diffing feature is not part of standard `diff`!

### A familiar friend

That's ok because you probably already have a `wdiff` alternative available on your computer: Git! More specifically, `git diff --word-diff`.

Maybe you already use that feature when working with your local clones of Git repositories, to look at what changed in the commit history or local edits. Did you know that `git diff` can act as a complete replacement of the standalone `diff` tool? Yes, `git diff` can also compare two arbitrary files that are not part of a Git repository when given the `--no-index` option!

And Git can usually tell you mean `--no-index` without you typing that explicitly because you're comparing at least one file that is not tracked in a Git clone, so you can just type:

```plain
$ git diff --word-diff <path1> <path2>
```

for any two file paths and it will work.

Trying this out with our sample paragraph:

<div class="highlight"><pre tabindex="0" style="background-color:#fff"><code class="language-diff" data-lang="diff">$ git diff --word-diff wrapped.txt wrapped2.txt
<span style="font-weight: bold">diff --git a/wrapped.txt b/wrapped2.txt
index b1c5775..59ff315 100644
--- a/wrapped.txt
+++ b/wrapped2.txt</span>
<span style="color:blue">@@ -1,7 +1,7 @@</span>
The quick brown fox jumped over the lazy dog's back 1234567890
times. Now is <span style="color:#000;background-color:tomato">[-the-]</span><span style="color:#000;background-color:lightgreen">{+thy+}</span> time for all good men to come to the aid of the
party. Waltz, bad nymph, for quick jigs vex. Glib jocks quiz nymph
to vex dwarf. Sphinx of black quartz, judge my vow. How vexingly
quick daft zebras jump! <span style="color:#000;background-color:tomato">[-The-]</span><span style="color:#000;background-color:lightgreen">{+Tho+}</span> five boxing wizards jump quickly.
Jackdaws love my big sphinx of quartz. Pack my box with five dozen
liquor jugs.
</code></pre></div>

It uses the same word deletion and insertion markers as `wdiff`, but to make them easier for our eyes to spot, by default `git diff` also shows them in different colors when output is going to an interactive terminal. You can disable the coloring with the additional option `--color=never`.

Use `git diff --word-diff=color` for a pretty view using *only* color to show the changes, without the `[-…-]` and `{+…+}` markers. This may be more readable when your input text is full of punctuation confusingly similar to the markers, and is useful if you want to copy from the terminal without any extra surrounding characters:

<div class="highlight"><pre tabindex="0" style="background-color:#fff"><code class="language-diff" data-lang="diff">$ git diff --word-diff=color wrapped.txt wrapped2.txt
<span style="font-weight: bold">diff --git a/wrapped.txt b/wrapped2.txt
index b1c5775..59ff315 100644
--- a/wrapped.txt
+++ b/wrapped2.txt</span>
<span style="color:blue">@@ -1,7 +1,7 @@</span>
The quick brown fox jumped over the lazy dog's back 1234567890
times. Now is <span style="color:#000;background-color:tomato">the</span><span style="color:#000;background-color:lightgreen">thy</span> time for all good men to come to the aid of the
party. Waltz, bad nymph, for quick jigs vex. Glib jocks quiz nymph
to vex dwarf. Sphinx of black quartz, judge my vow. How vexingly
quick daft zebras jump! <span style="color:#000;background-color:tomato">The</span><span style="color:#000;background-color:lightgreen">Tho</span> five boxing wizards jump quickly.
Jackdaws love my big sphinx of quartz. Pack my box with five dozen
liquor jugs.
</code></pre></div>

There is also the option `git diff --word-diff=porcelain` for an ugly but more easily code-parseable format useful for output sent as input to scripts:

```plain
$ git diff --word-diff=porcelain wrapped.txt wrapped2.txt
diff --git a/wrapped.txt b/wrapped2.txt
index b1c5775..59ff315 100644
--- a/wrapped.txt
+++ b/wrapped2.txt
@@ -1,7 +1,7 @@
 The quick brown fox jumped over the lazy dog's back 1234567890
~
 times. Now is 
-the
+thy
  time for all good men to come to the aid of the
~
 party. Waltz, bad nymph, for quick jigs vex. Glib jocks quiz nymph
~
 to vex dwarf. Sphinx of black quartz, judge my vow. How vexingly
~
 quick daft zebras jump! 
-The
+Tho
  five boxing wizards jump quickly.
~
 Jackdaws love my big sphinx of quartz. Pack my box with five dozen
~
 liquor jugs.
~
```

I have never needed that yet, but it is good to be aware of in case I ever do need to parse word diff output, to make it easier and more reliable.

### Customize word break definition

Other kinds of files can present challenges for readability in diff output.

For example consider trying to see small changes in the classic Unix `/etc/passwd` text "database" which has one user record per line, and within each record line uses `:` to delimit fields.

First we'll try traditional line diff:

```diff
$ git diff passwd passwd.mangled
diff --git a/passwd b/passwd.mangled
index 981736c..6531f10 100644
--- a/passwd
+++ b/passwd.mangled
@@ -24,22 +24,22 @@ polkitd:x:996:991:User for polkitd:/:/sbin/nologin
 rtkit:x:172:172:RealtimeKit:/proc:/sbin/nologin
 pulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologin
 chrony:x:995:988::/var/lib/chrony:/sbin/nologin
-abrt:x:173:173::/etc/abrt:/sbin/nologin
+abrt:x:173:1730::/etc/abrt:/sbin/nologin
 colord:x:994:987:User for colord:/var/lib/colord:/sbin/nologin
 rpcuser:x:29:29:RPC Service User:/var/lib/nfs:/sbin/nologin
 sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
 vboxadd:x:993:1::/var/run/vboxadd:/sbin/nologin
 dnsmasq:x:985:985:Dnsmasq DHCP and DNS server:/var/lib/dnsmasq:/sbin/nologin
-tcpdump:x:72:72::/:/sbin/nologin
+tcpdump:x:72:72::/:/bin/bash
 systemd-timesync:x:984:984:systemd Time Synchronization:/:/sbin/nologin
 pipewire:x:983:983:PipeWire System Daemon:/var/run/pipewire:/sbin/nologin
 gluster:x:982:982:GlusterFS daemons:/run/gluster:/sbin/nologin
-radvd:x:75:75:radvd user:/:/sbin/nologin
-saslauth:x:981:76:Saslauthd user:/run/saslauthd:/sbin/nologin
+radvd:x:76:75:radvd user:/:/sbin/nologin
+saslauth:x:981:76:Saslauthd user:/ran/saslauthd:/sbin/nologin
 usbmuxd:x:113:113:usbmuxd user:/:/sbin/nologin
 setroubleshoot:x:980:979::/var/lib/setroubleshoot:/sbin/nologin
 openvpn:x:979:978:OpenVPN:/etc/openvpn:/sbin/nologin
-nm-openvpn:x:978:977:Default user for running openvpn spawned by NetworkManager:/:/sbin/nologin
+mm-openvpn:x:978:977:Default user for running openvpn spawned by NetworkManager:/:/sbin/nologin
 qemu:x:107:107:qemu user:/:/sbin/nologin
 gdm:x:42:42::/var/lib/gdm:/sbin/nologin
 apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
```

It's not too hard to "eyeball" changes there if they add or remove characters and thus affect the line lengths. But a line with only a change to a single character isn't as easy.

Since blank space is not the relevant separator in this file, standard word diff doesn't help and in some cases is worse than line diff:

<div class="highlight"><pre tabindex="0" style="background-color:#fff"><code class="language-diff" data-lang="diff">$ git diff --word-diff passwd passwd.mangled
<span style="font-weight: bold">diff --git a/passwd b/passwd.mangled
index 981736c..6531f10 100644
--- a/passwd
+++ b/passwd.mangled</span>
<span style="color:blue">@@ -24,22 +24,22 @@</span> polkitd:x:996:991:User for polkitd:/:/sbin/nologin
rtkit:x:172:172:RealtimeKit:/proc:/sbin/nologin
pulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologin
chrony:x:995:988::/var/lib/chrony:/sbin/nologin
<span style="color:#000;background-color:tomato">[-abrt:x:173:173::/etc/abrt:/sbin/nologin-]</span><span style="color:#000;background-color:lightgreen">{+abrt:x:173:1730::/etc/abrt:/sbin/nologin+}</span>
colord:x:994:987:User for colord:/var/lib/colord:/sbin/nologin
rpcuser:x:29:29:RPC Service User:/var/lib/nfs:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
vboxadd:x:993:1::/var/run/vboxadd:/sbin/nologin
dnsmasq:x:985:985:Dnsmasq DHCP and DNS server:/var/lib/dnsmasq:/sbin/nologin
<span style="color:#000;background-color:tomato">[-tcpdump:x:72:72::/:/sbin/nologin-]</span><span style="color:#000;background-color:lightgreen">{+tcpdump:x:72:72::/:/bin/bash+}</span>
systemd-timesync:x:984:984:systemd Time Synchronization:/:/sbin/nologin
pipewire:x:983:983:PipeWire System Daemon:/var/run/pipewire:/sbin/nologin
gluster:x:982:982:GlusterFS daemons:/run/gluster:/sbin/nologin
<span style="color:#000;background-color:tomato">[-radvd:x:75:75:radvd-]</span><span style="color:#000;background-color:lightgreen">{+radvd:x:76:75:radvd+}</span> user:/:/sbin/nologin
saslauth:x:981:76:Saslauthd <span style="color:#000;background-color:tomato">[-user:/run/saslauthd:/sbin/nologin-]</span><span style="color:#000;background-color:lightgreen">{+user:/ran/saslauthd:/sbin/nologin+}</span>
usbmuxd:x:113:113:usbmuxd user:/:/sbin/nologin
setroubleshoot:x:980:979::/var/lib/setroubleshoot:/sbin/nologin
openvpn:x:979:978:OpenVPN:/etc/openvpn:/sbin/nologin
<span style="color:#000;background-color:tomato">[-nm-openvpn:x:978:977:Default-]</span><span style="color:#000;background-color:lightgreen">{+mm-openvpn:x:978:977:Default+}</span> user for running openvpn spawned by NetworkManager:/:/sbin/nologin
qemu:x:107:107:qemu user:/:/sbin/nologin
gdm:x:42:42::/var/lib/gdm:/sbin/nologin
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
</code></pre></div>

Another venerable program similar to `wdiff` that is still maintained is `dwdiff`. In its self-description we read something intriguing:

> It is different from wdiff in that it allows the user to specify what should be considered whitespace …

That sounds useful. But `dwdiff` is still a separate program and is even less common than `wdiff`. Can the versatile `git diff` help us here too?

Yes! `git diff` has the option `--word-diff-regex` to specify a regular expression to use instead of whitespace as a delimiter, like `dwdiff` does. The man page explanation notes:

> For example, `--word-diff-regex=.` will treat each character as a word and, correspondingly, show differences character by character.

It also notes that `--word-diff` is assumed and can be omitted when using `--word-diff-regex`.

So let's try that:

<div class="highlight"><pre tabindex="0" style="background-color:#fff"><code class="language-diff" data-lang="diff">$ git diff --word-diff-regex=. passwd passwd.mangled
<span style="font-weight: bold">diff --git a/passwd b/passwd.mangled
index 981736c..6531f10 100644
--- a/passwd
+++ b/passwd.mangled</span>
<span style="color:blue">@@ -24,22 +24,22 @@</span> polkitd:x:996:991:User for polkitd:/:/sbin/nologin
rtkit:x:172:172:RealtimeKit:/proc:/sbin/nologin
pulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologin
chrony:x:995:988::/var/lib/chrony:/sbin/nologin
abrt:x:173:173<span style="color:#000;background-color:lightgreen">{+0+}</span>::/etc/abrt:/sbin/nologin
colord:x:994:987:User for colord:/var/lib/colord:/sbin/nologin
rpcuser:x:29:29:RPC Service User:/var/lib/nfs:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin
vboxadd:x:993:1::/var/run/vboxadd:/sbin/nologin
dnsmasq:x:985:985:Dnsmasq DHCP and DNS server:/var/lib/dnsmasq:/sbin/nologin
tcpdump:x:72:72::/:/<span style="color:#000;background-color:tomato">[-s-]</span>bin/<span style="color:#000;background-color:tomato">[-nologin-]</span><span style="color:#000;background-color:lightgreen">{+bash+}</span>
systemd-timesync:x:984:984:systemd Time Synchronization:/:/sbin/nologin
pipewire:x:983:983:PipeWire System Daemon:/var/run/pipewire:/sbin/nologin
gluster:x:982:982:GlusterFS daemons:/run/gluster:/sbin/nologin
radvd:x:7<span style="color:#000;background-color:tomato">[-5-]</span><span style="color:#000;background-color:lightgreen">{+6+}</span>:75:radvd user:/:/sbin/nologin
saslauth:x:981:76:Saslauthd user:/r<span style="color:#000;background-color:tomato">[-u-]</span><span style="color:#000;background-color:lightgreen">{+a+}</span>n/saslauthd:/sbin/nologin
usbmuxd:x:113:113:usbmuxd user:/:/sbin/nologin
setroubleshoot:x:980:979::/var/lib/setroubleshoot:/sbin/nologin
openvpn:x:979:978:OpenVPN:/etc/openvpn:/sbin/nologin
<span style="color:#000;background-color:tomato">[-n-]</span><span style="color:#000;background-color:lightgreen">{+m+}</span>m-openvpn:x:978:977:Default user for running openvpn spawned by NetworkManager:/:/sbin/nologin
qemu:x:107:107:qemu user:/:/sbin/nologin
gdm:x:42:42::/var/lib/gdm:/sbin/nologin
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
</code></pre></div>

That's quite good, at least to my eyes.

### On the web

GitHub, GitLab, and Bitbucket do a good job of showing readable diffs for most common cases: line-oriented, but within each line also word or character diffs highlighted via color. Open up each of the following links to see how they present a few of our earlier examples as commit diffs:

* Change 2 letters in prose paragraph: [🔗 in GitHub](https://github.com/jonjensen/word-diff-examples/commit/07ab55f0acb6410e30688515a7a0bc95ed6a37b1), [🔗 in GitLab](https://gitlab.com/jonjensen/word-diff-examples/-/commit/07ab55f0acb6410e30688515a7a0bc95ed6a37b1), [🔗 in Bitbucket](https://bitbucket.org/jonjensen/word-diff-examples/commits/07ab55f0acb6410e30688515a7a0bc95ed6a37b1)
* Change a few characters in `/etc/passwd`: [🔗 in GitHub](https://github.com/jonjensen/word-diff-examples/commit/faa5f309a6d83a898a2b84fdf4c1c16189bb0be8), [🔗 in GitLab](https://gitlab.com/jonjensen/word-diff-examples/-/commit/faa5f309a6d83a898a2b84fdf4c1c16189bb0be8), [🔗 in Bitbucket](https://bitbucket.org/jonjensen/word-diff-examples/commits/faa5f309a6d83a898a2b84fdf4c1c16189bb0be8)

But GitHub and GitLab both break down on a reflowed paragraph, while Bitbucket shows a sensible diff of what logically changed, including spaces to newlines and vice versa:

* Insert words early in paragraph and reflow: [🔗 in GitHub](https://github.com/jonjensen/word-diff-examples/commit/986ab1450f434d675b69c60b67a837f4bf11c84f), [🔗 in GitLab](https://gitlab.com/jonjensen/word-diff-examples/-/commit/986ab1450f434d675b69c60b67a837f4bf11c84f), [🔗 in Bitbucket](https://bitbucket.org/jonjensen/word-diff-examples/commits/986ab1450f434d675b69c60b67a837f4bf11c84f)

It appears that GitLab may soon gain proper cross-line word diff ability as seen in the project's issue [Add word-diff option to commits view](https://gitlab.com/gitlab-org/gitlab/-/issues/325856), which states its "Problem to solve" as:

> When working with markdown (or any type of prose/text in general), the "classic" git-diff (intended for code) is of limited use.

Exactly right.

### IDEs

Visual Studio Code (VS Code) handles the above cases well out of the box for uncommitted changes in the current Git clone, and the GitLens extension helps it do the same for showing past commit diffs.

IntelliJ IDEA handles both cases well by default.

### For those left behind

To make the most of Git, you'll want a fairly recent version, since new features are being added all the time. If you're working on a server using the popular but aging CentOS 7 which comes with the ancient Git 1.8.3, you can follow our [simple tutorial to upgrade to Git 2.34.1 or newer on CentOS 7](/blog/2021/12/installing-git-2-on-centos-7/).

Enjoy!

### Reference

* [diff](https://en.wikipedia.org/wiki/Diff) on Wikipedia, including history and samples of original, context, and unified context diff output
* [patch](https://en.wikipedia.org/wiki/Patch_(Unix)) on Wikipedia
* [git-diff](https://git-scm.com/docs/git-diff) man page
* [wdiff](https://www.gnu.org/software/wdiff/)
* [dwdiff](https://os.ghalkes.nl/dwdiff.html)
* [Pangrams](https://en.wikipedia.org/wiki/Pangram) on Wikipedia, the source of our sample prose here
