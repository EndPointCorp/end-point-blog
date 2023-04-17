---
author: "Trevor Slocum"
title: "How to use the Caps Lock key as an Escape key on Windows, macOS, and Linux"
github_issue_number: 1955
date: 2023-04-17
tags:
- tips
---

![At sunset, the sky is a dark, fading orange above mountains which seen through layers of haze, making them appear blue. In the foreground, a lake with a large outcropping of land reflects the sky and mountains. At the bottom of the image much darker land is broken by a path of water travelling into the lake, reflecting orange, positioned directly into the center of the frame.](/blog/2023/04/use-caps-lock-as-escape/sunset-lake-mountains.webp)

<!-- Photo by Seth Jensen, 2022 -->

On most keyboards, the Escape key is distant from the most common keys. In order to
reach it, you likely need to lift your hand from the keyboard. This interrupts
the flow of typing and, over time, may cause repetitive strain injuries.

When using modal applications which require frequent use of the Escape key, such
as the text editor [Vim](https://www.vim.org), shortening the distance your
fingers travel to and from the Escape key helps prevent injury and saves time.

After following the instructions below, you may need to restart your system in
order to finish applying the changes.

### Windows instructions

Download and install [PowerToys](https://github.com/microsoft/PowerToys/releases),
a set of utilities created by Microsoft.

Open PowerToys and browse to the **Keyboard Manager**. Enable the **Keyboard Manager**
and click **Remap a key**. Choose **Caps Lock -> Escape**.

Note that this fix requires PowerToys to be running.

### macOS instructions

Go to **Apple menu -> System preferences -> Keyboard**. If you have multiple
keyboards, make sure your active keyboard is selected.

Click on the **Modifier keys** button to open a popup dialog. Open the dropdown
next to **Caps Lock** and select **Escape**.

### Linux instructions

There are separate instructions for Linux depending on whether you are using X11
or Wayland. If you don't know what these are, you are likely using X11.

On Linux, after following the instructions below, it is still
possible to toggle Caps Lock by holding Shift before pressing the Caps Lock key.

#### X11

Open `~/.xprofile` in a text editor and add the following line:

```plain
setxkbmap -option "caps:escape_shifted_capslock"
```

#### Wayland

Each Wayland compositor uses its own unique configuration format. The
instructions below are for [Sway](https://swaywm.org). If you are using a
different Wayland compositor, you will need to research how to specify keyboard
options in the configuration file of your particular compositor.

Open `~/.config/sway/config` in a text editor and add the following line:

```plain
input * xkb_options "caps:escape_shifted_capslock"
```

You can see more options for changing Caps Lock behavior in the XKB rules file:

```plain
grep -E "(ctrl|caps):" /usr/share/X11/xkb/rules/base.lst
```

Or, in the man page for XKB:

```plain
man xkeyboard-config
```

#### Conclusion

These aren't the only ways to make this swap. Furthermore, some prefer other key swaps, such as making Caps Lock an additional Control key. Let us know in the comments about your preferred fix!
