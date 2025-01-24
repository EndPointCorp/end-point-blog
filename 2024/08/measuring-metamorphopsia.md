---
author: Darius Clynes
title: "Measuring Metamorphopsia"
date: 2024-08-07
github_issue_number: 2067
description: Metamorphopsia is a visual condition causing deformation of the visual field. I created an app to measure my progress while healing from it.
featured:
  image_url: /blog/2024/08/measuring-metamorphopsia/banner.webp
tags:
- tools
---

![Two black circles are broken by irregularly shaped cutouts showing concentric circles beneath, some of which are labeled. There are geometric shapes in between the circles, showing some kind of diagram.](/blog/2024/08/measuring-metamorphopsia/banner.webp)<br>
[Photo](https://www.flickr.com/photos/internetarchivebookimages/14770211305) in public domain.

Metamorphopsia is an abnormal condition of vision that can cause deformation of the visual field. This condition, aside from having a wonderful name, has a real effect on my vision: Even after a successful operation to correct the macular hole which causes this, I still see circles as ellipses. Faces are elongated vertically like in a funhouse mirror, so I have an “ugly face” eye and a "normal face" eye.

My ophthalmologist assured me that with time — 6 weeks to 6 months — my vision should become normal and this distortion and visual alignment problem should disappear, or at least improve drastically. It occurred to me it would be nice to have an application to measure any progress in the restoration of my vision.

### What Causes Metamorphopsia?

The most common cause of metamorphopsia is an irregularity in the retinal surface of the eye. A typical irregularity of the retinal surface that can produce a noticeable distortion in the center of the visual field is referred to as a “macular” anomaly. Macular anomalies come in different varieties. One such anomaly, a macular hole, arises when the retina in the area of the fovea in the center of the eye is pulled off of its normal hyperbolic depression. The cause of the detachment or displacement can be the vitreous humour — the clear jelly-like filling of the eye — becoming viscous with age, attaching to the retina, and pulling on it. A term for this used by ophthalmologists is "friction".

| ![A close-up X-ray of a retina, side on. There is a subtle curve downward on the outer layer of material, which never fully breaks. This is labeled "Normal macula".](/blog/2024/08/measuring-metamorphopsia/normal-macula.webp) | ![A similar X-ray to the previous, but in place of the dip is a complete break in the outer layer, labeled "Macular hole".](/blog/2024/08/measuring-metamorphopsia/macular-hole.webp) |
| ------------------------------------------------------------- | ------------------------------------------------------------ |

Images © 2006–2024 Macula Retina Vitreous Center, Dr. Mehran Taban, Inc.

While there are operations to "repair" macular holes, the beautiful hyperbolic or parabolic shape of the original macular depression may not be physically reconstructed; it may be almost flat across. That means the light sensing elements rods and cones are all “bunched” together and the deformation of the image is what results. Instead of having increased information (think of this as higher density of “pixels”) for the same angle of view, now the rods and cones are fed image info from farther afield, resulting in distortion.

![Five images, labeled A through E, of various types of macular holes. Some pull up and away from the lower layer of material, some have a thin amount of material stretching the hole, and the bottom image, labeled "E", has a very slightly curved dip where the hole is in the other images.](/blog/2024/08/measuring-metamorphopsia/macular-holes-different-stages.webp)

Macular Holes at different stages, with E being a postoperative repaired macular hole. [Image source](https://www.reviewofophthalmology.com/article/revisiting-macular-holes).

### The Measuring Metamorphopsia Application

I decided to design and implement an application that had two features:

1. Correct the distortion where it is perceived so that the visual field would be much closer to normal.
2. In doing so, measure the subjectively experienced distortion, save it for future reference and for communicating it to others.

Although there may be other applications for this measuring technique, my personal motivation was to measure the progress of the restoration of normal vision in the affected eye by saving the correction parameters and comparing them later as they may change. In my case they haven't changed much in 9 months.

![A square grid with a blue circle in the center, and with regularly spaced blue boxes dotting the grid.](/blog/2024/08/measuring-metamorphopsia/empty-grid.webp)

Here is the link to access my application, Measuring Metamorphopsia: https://darius.endpointdev.com/examples/measuring_metamorphopsia.html

#### How to Use the Application

1. Look at the center of the blue circle with the eye needing correction. Close the other eye or wear an eyepatch.
2. Adjust any distortions by selecting and dragging the blue boxes in the appropriate direction to correct the distortion until the blue circle is perfectly round again. Repeat for any distortions you notice until you are satisfied.
3. Press save to keep your corrections.
4. You may load an image of your choice — a face you know well would be a good choice — to see the corrections in effect. Please be sure it is a square image; the width and height of the image should be equal.
5. You may reload your saved corrections at any time.
6. You may also invert your corrections to impose your measured distortions on an image to simulate what you see. With this, you can communicate to someone how your distortions affect your vision.

### Applications of the Saved Distortions Parameters

The saved deformation values can be used for a variety of purposes:

* Improving vision via digital image processing, by adjusting an image with the parameters to restore stereoscopic alignment and thereby merging vision from both eyes.

    For example, this can be done in VR sets where images can be processed separately for each eye. It could also be used by stereo displays like Samsung 3D televisions with synchronized polarized glasses, where separate images are given to each eye. The separate images could use the distortion parameters to correct differently for the right and left images.

* Contact lenses may be able to be made to correct some local anomalies using the distortion parameters.
* Measure and record the restoration progress or the deterioration of the perceived visual field in:

    * visual field measurements for preoperative subjective deterioration
    * visual field measurements for postoperative subjective restoration progress
    * self-healing or spontaneous macular hole repair (see references below).

In the following image, my normal face is on the left with the correct “undistorted” proportions. On the right is a corrected version using the saved distortion parameters to adjust my vision so the left eye can see things more “normally”. In my case, the image is compressed to account for the loss of acuity in the center.

![On the left, a man's face. On the right, the same face stretched slightly wider, with a more compressed image and a grid of blue dots across it.](/blog/2024/08/measuring-metamorphopsia/face-with-and-without-grid.webp)

By crossing my eyes, as if using a stereoscope, I can create a third image in the center that merges the two images and properly aligns my facial features again.

As seen below, we can also invert the saved distortion parameters to communicate to others how my uncorrected left eye now views the world.

![The same man's face, compressed and with blue dots, but now slightly vertically elongated.](/blog/2024/08/measuring-metamorphopsia/distorted-face-on-grid.webp)

### Additional Information

* [What is a macular hole?](https://macularetinavitreouscenter.com/macular-hole/)
* [Metamorphopsia and the typical Amsler grid](https://www.garciadeoteyza.es/en/metamorphopsia-test-amsler-grid)
* [More about Metamorphopsia](https://www.scottpautlermd.com/metamorphopsia-visual-distortion/)
* [Spontaneous Closure of Macular Holes](https://www.researchgate.net/figure/Spontaneous-closure-of-macular-holes-in-four-patients-A-Development-and-closure-of-a_fig1_336829530)
* <a href="https://www.thelancet.com/article/S0140-6736(24)00136-3/abstract">Prosopometamorphopsia</a>. Note that this is usually a cortical abnormality and not usually caused by retinal anomalies. It is also extra exciting to say: prosopometamorphopsia!

### Acknowledgements

I would like to thank the following people for their advice and support:

* [Ben Goldstein](/team/benjamin-goldstein/) for encouraging me to pursue this blog.
* [Bimal Gharti Magar](/team/bimal-gharti-magar/) for streamlining the presentation and JavaScript.
* Dr. Andy Burrows, retinal surgeon practicing in New Jersey, for his encouragement and enthusiastic support, including how it could help in his work.
* Dr. Fanny Nerinckx, retinal surgeon who operated on my left eye in October 2023 to repair my macular hole.
* Dr, Thierry Vandorselaer, the ophthalmologist who discovered my macular hole.
