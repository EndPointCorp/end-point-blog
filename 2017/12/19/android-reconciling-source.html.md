---
author: "Zed Jensen"
title: "Reconciling Android source code"
tags: android
---

Recently, a client came to us with an interesting problem. They needed some changes made to an internal-use Android app that had been created for them by another
company, but they didn't have up-to-date source code for the app, and they had no way of getting it. They gave us an old archive of source code, a more recent
working build of the app, and asked us to figure it out.

The working version of the app they sent us was built in early 2016, and the app was compiled for Android SDK version 22, which is 5.1 Lollipop. It came out in March 2015, so it was a year old even when the app was created, and the code was using lots of features which have since been deprecated.

After putting this source code in a Git repository, I started by building the app from the source they'd sent and comparing it to the working version. It looked
mostly the same, but a couple of features were broken. At the suggestion of a coworker, I used BytecodeViewer (https://github.com/Konloch/bytecode-viewer/releases)
to decompile the APK and took a look around.

![BytecodeViewer screenshot](/2017/12/19/android-reconciling-source/bytecode-viewer.jpg)

It was a little while before I was able to find any differences between the source we had and this decompiled code,
but I did find a few. Combining those with a few tweaks (the source was using a few old APIs that needed to be updated), I soon had a working build of the app
that matched the functionality of the one we already had.

This wasn't the only thing wrong with the app. However, another hurdle in picking up this project from its previous developers showed up when I had to fix a few
oddball problems reported by our client. One reported issue I had to fix was found on an information screen listing attributes of items. An example:

![Details screen](/2017/12/19/android-reconciling-source/details.jpg)

The "Quantity" field worked just fine for any non-zero value, but if it was zero, then the app was displaying 0 instead. This turned out to be very simple to fix. Below is the snippet of code involved:

```java
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:textAppearance="?android:attr/textAppearanceMedium"
    android:text="16"
    android:textColor="@color/background_black"
    android:id="@+id/txt_info_quantity" />
```

The default text of that field was, likely as a placeholder, set to 16, and it wasn't being overwritten when the given value was 0. So, all I had to do was replace
it with 0, since it would be overwritten anytime there was a nonzero value. This was a good reminder to somehow keep track of placeholders like this (for example, putting a todo comment or something similar) so bugs like this don't happen.

Figuring out how to reconcile the source and binary of this app seemed like a daunting task, but it turned out to be very doable, and was a very interesting project.
