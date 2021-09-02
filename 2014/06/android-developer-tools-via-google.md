---
author: Zed Jensen
title: Android Developer Tools via Google Chrome
github_issue_number: 995
tags:
- android
- browsers
- tools
date: 2014-06-11
---

Recently I was working on a website on my Android phone, and I found myself needing Chrome’s Developer Tools. However, Developer Tools are not included in the Android version of Chrome for many reasons, including lack of screen real estate.

So, I looked around, and I found a solution: using a USB cable and ADB ([Android Debug Bridge](https://developer.android.com/tools/help/adb.html)), you can do debugging on an Android device with Chrome’s Developer Tools *from your desktop.*

To show you exactly what I mean, here’s a short video demonstrating this:

<div class="separator" style="clear: both; text-align: center;">
<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/ut7NWQZVXEk?rel=0" frameborder="0" allowfullscreen></iframe>
</div>

So, how does one work this magic? There are several ways, but I’ll talk about the one that I used. For this method, you need to have Google Chrome version 31 or higher installed on both your Android device and your development machine.

First, you have to enable Android debugging on your device. From [android.com](https://developer.android.com/tools/device.html):

>- On most devices running Android 3.2 or older, you can find the option under **Settings > Applications > Development**.
>- On Android 4.0 and newer, it’s in **Settings > Developer options**.
>    - **Note:** On Android 4.2 and newer, **Developer options** is hidden by default. To make it available, go to **Settings > About phone** and tap **Build number** seven times. Return to the previous screen to find **Developer options**.

Next, connect your device with a USB cable and, on your development machine, go to **about:inspect** and check **Discover USB Devices**. After a second or two, your device should show up like this:

<a href="/blog/2014/06/android-developer-tools-via-google/image-0-big.jpeg" imageanchor="1"><img border="0" src="/blog/2014/06/android-developer-tools-via-google/image-0.jpeg"/></a>

To open Dev Tools for a tab, just click “inspect” below it. The buttons next to “inspect” only appear for tabs open in Chrome, but you can open Developer Tools for any app that uses WebView, whether it’s in Chrome or not.

And there you go! Fully featured Chrome Developer Tools for your Android device on your development machine. More information, including a way to do this with earlier versions of Chrome, can be found at the [Android Developer site](https://developer.chrome.com/devtools/docs/remote-debugging).
