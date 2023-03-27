---
author: "Trevor Slocum"
title: "How to use the caps lock key as a convenient escape key"
description: "A guide on how to use the caps lock key as an additional escape key."
date: 2023-03-29
tags:
- tips
github_issue_number: 0
---

<!-- TODO photo -->

On most keyboards, the escape key is distant from most of the keys. In order to
reach it, you likely need to lift your hand from the keyboard. This interrupts
the flow of typing and, over time, may cause repetitive strain injury.

When using modal applications which require frequent use of the escape key, such
as the text editor [Vim](https://www.vim.org), shortening the distance your
fingers travel to and from the escape key helps prevent injury and saves time.

After following the instructions below, you may need to restart your system in
order to finish applying the changes.

### Windows instructions

Download and install [PowerToys](https://github.com/microsoft/PowerToys/releases),
a set of utilities created by Microsoft.

Open PowerToys and browse to the **Keyboard Manager**. Enable the **Keyboard Manager**
and click **Remap a key**.  Choose **Caps lock -> Escape**.

### macOS instructions

Go to **Apple menu -> System preferences -> Keyboard**.  If you have multiple
keyboards, make sure your active keyboard is selected.

Click on the **Modifier keys** button to open a popup dialog.  Open the dropdown
next to **Caps lock** and select **Escape**.

### Linux instructions

There are separate instructions for Linux depending on whether you are using X11
or Wayland.  If you don't know what these are, you are likely using X11.

Note for Linux users: After following the instructions below, it is still
possible to toggle caps lock by holding shift before pressing the caps lock key.

#### X11

Open `~/.xprofile` in a text editor and add the following line:

```
setxkbmap -option "caps:escape_shifted_capslock"
```

#### Wayland

Each Wayland compositor uses its own unique configuration format. The
instructions below are for [Sway](https://swaywm.org). If you are using a
different Wayland compositor, you will need to research how to specify keyboard
options in the configuration file of your particular compositor.

Open `~/.config/sway/config` in a text editor and add the following line:

```
input * xkb_options "caps:escape_shifted_capslock"
```
