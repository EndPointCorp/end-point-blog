---
author: Jon Jensen
title: 'API gaps: an Android MediaPlayer example'
github_issue_number: 422
tags:
- android
- java
- mobile
- api
date: 2011-03-02
---

Many programming library APIs come with several levels of functionality, including the low-level but flexible way, and the high-level and simpler but limited way. I recently came across a textbook case of this in Android’s Java audio API, in the [MediaPlayer class](https://developer.android.com/reference/android/media/MediaPlayer.html).

We needed to play one of several custom Ogg Vorbis audio files in the [Locate Express](https://web.archive.org/web/20110902084453/http://www.locateexpress.com/) Android app to alert the user to various situations.

Getting this going initially was fairly straightforward:

<script src="https://gist.github.com/850599.js?file=PlaySound.java"></script>

In this simplified version of our PlaySound class we pass in the app resource ID of the sound file, and using the [MediaPlayer.create()](https://developer.android.com/reference/android/media/MediaPlayer#create(android.content.Context,%20int)) method is about as simple as can be.

We keep a map of playing sound files so that external events can stop all playing sounds at once in a single call.

We set an OnCompletionListener to clean up after ourselves if the sound plays to its end without interruption.

Everything worked fine. Except for a pesky volume problem in real-world use. MediaPlayer uses Android’s default audio stream, which seemed to be [STREAM_MUSIC](https://developer.android.com/reference/android/media/AudioManager#STREAM_MUSIC). That plays the audio files fine, but has an interesting consequence during the actual playing: You can’t turn the volume down or up because the volume control outside of any specific media-playing contexts affects the [STREAM_RING](https://developer.android.com/reference/android/media/AudioManager#STREAM_RING) volume, not the one we’re playing on. Practically speaking, that’s a big problem because if the music stream was turned up all the way and the alert goes off at full volume in a public place, you have no way to turn it down! (Not a hypothetical situation, as you may guess ...)

Switching to STREAM_RING would be the obvious and hopefully simple thing to do, but calling the [MediaPlayer.setAudioStreamType() method](https://developer.android.com/reference/android/media/MediaPlayer.html#setAudioStreamType(int)) must be done before the MediaPlayer state machine enters the prepared state, which the MediaPlayer.create() does automatically. The convenience is our undoing!

Switching over to the low-level way of doing things turns out to be a bit of a pain because:

1. There’s no interface to pass an Android resource ID to one of the [setDataSource()](https://developer.android.com/reference/android/media/MediaPlayer.html#setDataSource(java.lang.String)) methods. Instead, we have to use a file path, file descriptor, or URI.

1. The easiest of those options seemed to be a URI, and doing a little research, the format comes to light: android.resource://package.name/resource_id

1. We have to handle IOException which wasn’t throwable using the higher-level MediaPlayer.create() invocation.

Putting it all together, we end up with:

<script src="https://gist.github.com/850599.js?file=PlaySound2.java"></script>

It’s not so hard, but it’s not the one-line addition of MediaPlayer.setAudioStreamType() that I expected. This is an example of how the API lacking a MediaPlayer.setDataSource(Context, int) for the resource ID makes a simple change a lot more painful than it really needs to be—​especially since the URI variation could easily be handled behind the scenes by MediaPlayer.

I later took a look at the [Android MediaPlayer class source](https://github.com/aosp-mirror/platform_frameworks_base/blob/gingerbread/media/java/android/media/MediaPlayer.java#L648) to see how the create() method does its work:

<script src="https://gist.github.com/850599.js?file=MediaPlayer-excerpt.java"></script>

Instead of creating a URI, the authors chose to go the file descriptor route, and they check for exceptions just like I had to. It seems more cumbersome to have to open the file, get the descriptor, and manually call getStartOffset() and getLength() in the call to setDataSource, but perhaps there’s some benefit there.

This gap between low-level and high-level interfaces is another small lesson I’ll remember both when using and creating APIs.

There’s one final unanswered question I had earlier: Was STREAM_MUSIC really the default output stream? Empirically that seemed to be the case, but I didn’t see it stated explicitly anywhere in the documentation. To find out for sure we have to delve into the native C++ code that backs MediaPlayer, in [libmedia/mediaplayer.cpp](https://github.com/aosp-mirror/platform_frameworks_base/blob/gingerbread/media/libmedia/mediaplayer.cpp#L48), and sure enough, in the constructor the default is set:

```plain
mStreamType = AudioSystem::MUSIC;
```

My experience with Android so far has been that it’s well documented, but it’s been very nice to be able to read the source and see how the core libraries are implemented when needed.
