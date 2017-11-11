---
author: Jon Jensen
gh_issue_number: 400
tags: android, mobile
title: DROID 2 review
---

I got a [Motorola DROID 2](http://www.motorola.com/Consumers/US-EN/Consumer-Product-and-Services/Mobile-Phones/Motorola-DROID-2-US-EN) phone a couple of months ago and have assembled here my notes about how it's worked out so far. First, some background.

This is my second Android phone. My first was the [Google Ion](http://developer.htc.com/google-io-device.html), basically the same as the HTC Magic. That was running standard Android 1.5 (Cupcake), while the DROID 2 runs Android 2.2 (Froyo) tweaked somewhat by Motorola. I've used several other Android phones belonging to friends and relatives.

Overall I like the Android operating system fairly well. Like everything, it can be improved. It's been advancing at a fairly quick pace. It's mostly free software. Too many phones are locked down and have to be broken into to change the operating system, but Android's still a freer computing environment than most phones have and I hope the situation will improve over time.

I take for granted much of Android's feature set: The excellent system-wide notification bar that many apps hook into and which is always easy to get to. The solid multitasking. Automatic screen adjustment for using the phone in landscape vs. portrait mode. The ability to mount the normal filesystem on the SD card from another computer via USB or by removing the SD card. The freedom to run any applications I want, downloaded from wherever, not just the Android Market.

For one of our clients, I'm currently developing an Android application in Java that uses geolocation, JSON web services, and Urban Airship's [AirMail Push](http://urbanairship.com/products/push/) for push notifications. So I'm using the phone both as my main mobile phone and as an app developer.

### Keyboard

This is the first phone I've had with a full slide-out QWERTY keyboard. I wasn't sure if I'd use it often or just stick with the touchscreen keyboard. So far I use the real keyboard most of the time. But it's nice to be able to use either the hard keyboard or touchscreen keyboard, whichever's more convenient.

I like the keyboard a lot, especially that its rows are offset like a normal keyboard and not a straight aligned grid:

<img height="369" src="http://www.motorola.com/staticfiles/Consumers/Products/Mobile%20Phones/Motorola-DROID-2/_Images/_Staticfiles/Droid2_FrontOpen_email_alt.png" width="376"/>

The real keyboard makes using ssh (via the ConnectBot app) on the phone much easier than with the touchscreen keyboard, because the real keyboard doesn't use up any screen real estate.

The biggest annoyance for me has been the keyboard's microphone key which launches the voice commands function. I don't use voice commands, so this has never been what I've wanted and is highly annoying when accidentally pressed.

Third-party alternative touchscreen keyboards for European languages, Hebrew, Arabic, and others work pretty well too.

### Touchscreen

I really miss having physical buttons for menu, home, back, and search, as I had on the HTC Magic:

<img height="360" src="http://swappa.com/static/images/dynamic/htc-magic-google-ion-vertical_180x360.png" width="180"/>

On the DROID 2 they're touchscreen buttons and it's annoying and error-prone to have to look at the phone and carefully press one. Much better to have real buttons for those core functions used by all apps.

However, good riddance to the trackball.

The DROID 2 screen itself is higher resolution, bright, and responds well to touch, swipe, and multitouch, as you'd expect.

### Battery

Battery life on the DROID 2 is not great, especially when using GPS heavily. But that's a problem on most phones.

I later got the optional extended-life battery. It isn't much bigger or heavier, and does add a lot more life to the phone. It wouldn't be necessary if I weren't doing heavy GPS & web service interaction with my own Android app under development.

### Audio

The DROID 2 has a normal 1/8" stereo headphone jack, which is nice. The HTC Magic needed a special adapter to use normal headphones, which was a pain.

Audio playback is usually fine, though on a couple of occasions it's stuttered, presumably while contending with other apps for CPU. Audio playback when the screen is off doesn't drain the battery much at all.

### Calling and Contacts

There have been a few isolated incidents, perhaps involving switching off Bluetooth, where I couldn't turn down the call volume in the middle of the call. That could've been either a generic Android problem, or the Motorola Android build; I'm not sure.

I didn't much like the special Motorola apps that shipped on the phone, but simply not using them has made them no problem.

An exception to that is the Contacts app that integrates with Facebook and Twitter. That's a lot more helpful than I imagined it would be, though when you have many contacts it can sometime slow down on opening an individual contact, when I imagine it tries to fetch the latest details from social networks.

The in-call screen's "Mute" button is small and way too close to the "End call" button:

<a href="/blog/2011/01/24/droid-2-review/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565943804238104434" src="/blog/2011/01/24/droid-2-review/image-0.png" style="cursor:pointer; cursor:hand;width: 225px; height: 400px;"/></a>

That's led to me accidentally hanging up during conference calls a couple of times. The stock open source Android call screen is arguably less pretty, but equally-sized buttons makes it easier to use:

<a href="/blog/2011/01/24/droid-2-review/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5565944683885559442" src="/blog/2011/01/24/droid-2-review/image-1.png" style="cursor:pointer; cursor:hand;width: 270px; height: 400px;"/></a>

Because I'm using Verizon for the first time with this phone, I've been introduced to the sad problem of not being able to use voice and data at the same time on CDMA. I used to laugh about that when I was using AT&T because it seemed silly. Now I find it really does get in the way fairly often.

The normal Skype app doesn't allow using a Bluetooth headset or using the cell network for calls (in the US). The special Verizon Skype app burns voice minutes and won't let you use wifi for calling (in the US). The combination of proprietary software plus controlling phone carriers is bad for users! Because of the limitations I use Skype mostly for text chat on my phone.

### GPS

As I mentioned, the GPS uses a lot of battery. But it works well. The GPS on my HTC Magic sometimes took a very long time to get a location fix, but on the DROID 2 it's fast and works very well. Given the location-aware app I'm working on, I've had more opportunity to notice this than I otherwise might have.

There was one funny problem with the GPS, though. Once when the battery got down to 5% or so, the GPS started to report hilariously wrong data to my app, and thus to the web service it reported to. For example, it reported every second that my phone, which was sitting on my nightstand, was traveling at 121 m/s (270 mph), and the point in latitude and longitude moved quickly. This continued even after I'd plugged the phone back in. I haven't seen it happen since, but it was strange.

### Useful apps

I don't spend a lot of time trying out new apps, but I've found several to be very useful: K-9 Mail for multiple mail accounts (reviewed yesterday on [Ars Technica](http://arstechnica.com/open-source/reviews/2011/01/excellent-k-9-mail-app-for-android-keeps-your-messages-on-a-leash.ars)), Yaaic (an IRC client), 3G Watchdog (bandwidth monitor), TweetsRide (Twitter client), Google Sky Map, and My Tracks. I haven't found a great music player yet, but the built-in Android Music app and Winamp are both fine.

### Security

I've long used crypto filesystems on desktop and laptop computers, and feel the lack on Android. A phone needs a solid cryptofs option more than normal computers even, and I hope that'll be available soon.

### The end (for now)

I'm probably forgetting lots of things, but this is already longer than I'd expected, so I'll stop now and put any afterthoughts in the comments. In short, I like the phone, but it's hard to avoid looking forward to a brighter future when it comes to mobile devices.
