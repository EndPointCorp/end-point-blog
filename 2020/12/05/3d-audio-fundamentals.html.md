---
author: "Matt Vollrath"
title: "3D Audio Fundamentals"
tags: audio
gh_issue_number: 1703
---

![Concert hall acoustics](/blog/2020/12/05/3d-audio-fundamentals/acoustics.jpg)
Photo by [PT Russell](https://unsplash.com/@pt_photos?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText) on [Unsplash](https://unsplash.com/?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText)</span>

It’s easy to prove to yourself that you need two eyes to perceive how far away things are in the world around you. Shut one eye and the world appears flat. This ability is called stereoscopic vision. A less known exercise is proving that you also need two ears to perceive which direction a sound is coming from. Shut one ear and the world outside your vision is harder to track. This ability is called binaural hearing.

As VR technology continues to push the boundaries of sight immersion with increasing accessibility, sound reproduction has not lagged behind. In fact, the consumer hardware needed for sound immersion has been accessible for decades. By leveraging 3D audio techniques, a pair of headphones can be turned into the aural equivalent of a VR headset.

The magic of stereophonic audio reproduction was first demonstrated in 1881 when French inventor Clément Ader connected microphones on the stage of the Paris Opera to listening rooms in the Palais de l’Industrie through telephone lines, where visitors experienced remote live performances on pairs of receivers. The exhibit was extremely popular and got [a glowing review in Scientific American](https://babel.hathitrust.org/cgi/pt?id=mdp.39015024538491;view=1up;seq=428).

The technology began to proliferate in the 1930s after British engineer Alan Blumlein patented binaural sound applications and applied them to cinema, producing sound that seemed to follow actors across the screen. The use of two (or more) audio channels for sound reproduction continued to develop. Today, stereophonic audio mastering and reproduction is the industry baseline.

Stereophonic alone is not the final word in spatial audio. Recording a symphony with two microphones and experiencing it with headphones or stereo speakers is much more immersive than a single microphone and speaker, but much like a 3D movie, it is a window into another world. Advanced 3D audio can deliver the same kind of immersion upgrade as a VR headset over a 3D movie, putting the user firmly inside another world.

### Putting Sound in Space

3D audio immersion is implemented by layering simple and advanced “psycho-acoustic” effects. Each effect adds a dimension or ambience to the experience. Stereo reproduction is described, but implementation with more speaker sources is possible. When setting up a 3D audio environment, a sound listener and any number of sound sources are positioned in virtual space. Effects such as the following are applied to create the illusion that the sound sources are in the space with the listener.

### Panning

Panning is the baseline for spatial audio. When a sound source is further to one side of the listening position, the sound it produces is louder in the corresponding speaker or earpiece. Alone, this gives you one dimension of spatialization: left to right.

### Distance Model

A distance model reduces the loudness of sounds when their source positions are further away. For example, an object 5 meters away from the listening position may be twice as loud as an object 10 meters away, depending on the distance model formula chosen.

### Doppler Effect

The doppler effect is caused by the compression and expansion of sound waves produced by sound sources moving towards or away from the listener. An example is the sound of a race car speed past, changing from higher pitch while approaching to lower pitch while receding. Changing the pitch of a sound’s playback depending on the source’s relative velocity simulates the physics of sound waves traveling through the air at the speed of sound. This effect is most desirable when rendering fast-moving objects.

### HRTF

You may notice that when listening to something in front of you it sounds “brighter” or more detailed. This is because the geometry of your outer ear directionally funnels those frequencies into your ear canals.

A Head-Related Transfer Function (HRTF) simulates the way the ear perceives sounds coming from different directions. Engineers have created physical models of human heads and ears with microphones inside the ears and recorded sounds coming from different directions to create a model of the effect, most effective when experienced with headphones. You can think of HRTF as a more advanced panning effect that does more than just change the relative volume on the left and right. This gives the impression of sounds coming from above, below, or behind.

### Reverb

A subtle but important physical property of any indoor or outdoor space is the reflection and diffusion of sound waves when they impact a surface. Consider the difference between clapping your hands in your bedroom and in a gymnasium. This reflection is simulated to make the 3D audio illusion even more believable.

### 3D Audio with OpenAL

[OpenAL](https://www.openal.org/) is a cross-platform 3D audio library created by Loki Software in 2000. It is now developed and maintained by a community of developers including Apple and Creative Technology. OpenAL support libraries are included with OS X and are freely available for Linux and Windows. The library interfaces are implemented in C with bindings available for other languages.

The OpenAL specification includes many of the spatial audio fundamentals such as panning, distance model, and doppler effect. The open source OpenAL-soft library extends the OpenAL spec with optional HRTF and reverb effects. This library is a good place to start when integrating 3D audio in desktop applications.

### 3D Audio with Web Audio API

Web browsers gained support for 3D audio with the proliferation of the Web Audio API, now implemented by most major browsers. This JavaScript API has many of the tools you need to create a 3D audio soundscape including panning, distance model, HRTF, and reverb. Doppler effect was removed from the API, but could probably still be simulated with some work. See the [MDN tutorial](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Web_audio_spatialization_basics) for a great walkthrough of Web Audio API usage. This library is your last stop for 3D audio in a browser.
