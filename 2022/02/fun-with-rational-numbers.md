---
author: "Darius Clynes"
title: "Fun with Rational Numbers"
tags:
- programming
- javascript
- audio
- mathematics
- graphics
github_issue_number: 1831
date: 2022-02-11
---

![Rock hillside with trees](/blog/2022/02/fun-with-rational-numbers/20210428_210604-sm.webp)

<!-- Photo by Zed Jensen -->

So, you say you adored learning long division in elementary school? Well here we are revisiting that wonderful activity we have missed so much: fabulous magical moments like dividing 1.0 by 7. The especially tedious exercise of dragging over one more of the endless 0’s and seeing how many 7’s would fit into that woefully large remainder. Soon the delight mounts as you desperately hope the next digit will be the last and you discover that beautiful 1 as a remainder.

Undoubtedly you have wondered, like I have, what would happen if you divided 1.0 by 19? Would it repeat after only 8 digits? How many digits would it really take before it repeats?

That's exactly how I stumbled into the wonderful world of rational numbers. There I was, wondering and wandering along the gloomy Belgian beach — the tide way out as far as you could see — in the winter wind, and I couldn’t stop thinking how long it would take for that mantissa to repeat. I had actually already tried 1.0 over 19. Finally, on that miserable day, I got the courage to divide 1 by 23.

Fortunately for me, I wasn’t alone, and I was able to enlist, coax, oblige, implore the help of baffled little Susan, my daughter who was 7 years old at the time. Her job would be to write out the digits in the sand as I discovered them, yelling them out to her, getting farther and farther away from her as the calculation got longer and longer. Finally, shrieking in the wind with delight as I hit 1 as the remainder, Susan seemed confused but amused.

Well, it was so much fun I decided to share my excitement and enthusiasm while at the same time bringing attention to these often overlooked treasure chests of digits.

After my satisfaction in coming up with the answer, the pleasure of which clearly eluded my daughter who was overjoyed that this exercise was over, I decided to write a computer program to discover how these numbers might turn out as the values became larger.

### Numbers as music

As a composer, I thought it might be nice to portray the results in a sound representation. My first attempt was to use a fundamental sine wave and have each digit represent the number of overtones in the resulting sound. So the fundamental stayed constant, while the overtones quivered above not unlike Mongolian, Sardinian, or Tibetan Buddhist monk throat singing.

The digit 0 became the lonely fundamental, the digit 1 became the first harmonic an octave above, 2 was an octave and a fifth, and so on, until 9 the 10th harmonic. For timing I added varying amounts of delay between the sound events proportional to the digits calculated.

The first incarnation of my computer program was in 1999 in the programming language C, creating a sound wave file as an output. It created an interesting harmonic whistling kind of wind chime not unlike serrated plastic tubes that you swing around your head — the faster you swing, the higher the harmonics generated.

Later, I thought of applying the repeating nature of the calculated series of numbers to create a periodic waveform itself, instead of using sine waves. Seems like an obvious path to explore, doesn't it? I still have to try that sound experiment some day.

### Visualizing numbers

However, before continuing with sound, I did create a simple visual representation in JavaScript by making gradient-filled colored rectangles overlaid by arcs and line segments.

Let's look at my program showing results for some interesting numbers.

For example, here is a screenshot of what the reciprocal of 7 (1 divided by 7) looks like in my little program:

#### 1/7

![Visual representation of 1 divided by 7](/blog/2022/02/fun-with-rational-numbers/7.webp)

#### 1/13

![Visual representation of 1 divided by 13](/blog/2022/02/fun-with-rational-numbers/13.webp)

#### 1/523

![Visual representation of 1 divided by 523](/blog/2022/02/fun-with-rational-numbers/523.webp)

### A demo

<a href="/blog/2022/02/fun-with-rational-numbers/demo/" target="_blank">Click here to try it out for yourself!</a>

And make sure your sound is turned up a bit.

Two types of sounds are generated: one, by ‘subtractive’ synthesis, using filtered white noise, and the second, by just using a sampled plucked string sound. The first one, whistle-like, starts with white noise bandpass filtered with the center frequency set at the notes of a piano and the bandwidth or Q of each filter set at one semitone. This produces airy, whispery, wind-like flute sounds.

### Repeating digits

By the way, it turns out that:

* 1/19 produces 18 digits before repeating
* 1/23 produces 22
* 1/29 ⇒ 28
* 1/263 ⇒ 262 repeating digits, etc.

Nice pattern, right? Seems like you can safely say that a reciprocal will never have a mantissa with more digits than the number itself.

### Related resources

* The [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API#guides_and_tutorials) components allow you to construct ‘circuits’ like you would with wires on an analog synthesizer, plugging outputs of one component into another, by ‘connecting’ modules.
* Olivia Jack's work:
  * [PIXELSYNTH](https://ojack.xyz/PIXELSYNTH/) is a very nice version of this concept.
  * Her [main website](https://hydra.ojack.xyz/) has other very nice visual coding experiments.
