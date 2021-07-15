---
author: Muhammad Najmi bin Ahmad Zabidi
title: Image Recognition Tools
github_issue_number: 1463
tags:
- machine-learning
- python
date: 2018-10-10
---

<img src="/blog/2018/10/image-recognition-tools/image-1.jpg" alt="detecting 1 face" />

I’m always impressed with the advancement of machine learning, and, more recently, deep learning. However, since I am not an expert in the field I decided to let the researchers and scholars elaborate more on them.

In this post I will share the existing tools and the associated libraries to make them work, at least for me.

The reason I explored these tools is simple: I plan to deploy a poor man’s security camera in my home with some “sense” of intelligence. Since I am working at home, I want to know who is actually knocking my door. So I thought, what if I could use a web cam to monitor my door and let me know who’s actually standing at the door?

### Face Detection

I searched around for existing face detection software and found [this Python script](https://github.com/shantnu/FaceDetect/blob/master/face_detect.py) using [Haarcascade](https://github.com/opencv/opencv/tree/master/data/haarcascades). So I was able to detect faces, but upon sharing the “findings” with a friend he said this only detects faces. How would the computer be able to recognize who’s who? Then I stumbled upon the phrase “face recognition”.

You might have noticed that if you use the image file that you import directly from your smartphone, the output will be displayed in a large file to the screen. You can use ImageMagick to resize the file to say, 640x480 pixels.

```bash
$ file makan.jpg
makan.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=15, height=3120, bps=0, width=4160], baseline, precision 8, 4160x3120, frames 3

$ convert makan.jpg -resize 640x480 makan-small.jpg

$ file makan-small.jpg
makan-small.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=15, height=3120, bps=0, width=4160], baseline, precision 8, 640x480, frames 3
```

<img src="/blog/2018/10/image-recognition-tools/image-0.jpg" alt="detecting 2 faces" />

### Machine Vision

The computer doesn’t see the image directly as the humans seem to, so we need to convert the images into numerical values. For example, in the facial regcognition tools, the training file contains the following matrices:

```
opencv_lbphfaces:
   threshold: 1.7976931348623157e+308
   radius: 1
   neighbors: 8
   grid_x: 8
   grid_y: 8
   histograms:
      - !!opencv-matrix
         rows: 1
         cols: 16384
         dt: f
         data: [ 2.46913582e-02, 1.85185187e-02, 0., 3.08641978e-03,
             1.23456791e-02, 6.17283955e-03, 3.08641978e-03,
             2.46913582e-02, 0., 0., 0., 0., 0., 3.08641978e-03, 0.,
             9.25925933e-03, 1.85185187e-02, 9.25925933e-03, 0., 0.,
             3.08641978e-03, 0., 0., 0., 3.08641978e-03, 0., 0., 0.,
             2.46913582e-02, 3.08641978e-03, 0., 6.79012388e-02, 0., 0.,
		...................
             1.30385486e-02, 1.47392293e-02, 4.53514745e-03,
             1.13378686e-03, 7.93650839e-03, 5.66893432e-04,
             5.66893432e-04, 1.13378686e-03, 6.80272095e-03,
             2.26757373e-03, 0., 0., 5.66893443e-03, 2.83446722e-03,
             5.10204071e-03, 9.07029491e-03, 7.14285746e-02 ]
   labels: !!opencv-matrix
      rows: 26
      cols: 1
      dt: i
      data: [ 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 4, 4, 4, 4, 5, 5, 5, 5, 5,
          6, 6, 8, 8, 8, 8 ]
   labelsInfo:
      []
```

### Face Recognition

I continued my search for existing face recognition software and found several projects which could be tested right away, with some modifications from the original source. I found one [tutorial](https://www.youtube.com/watch?v=PmZ29Vta7Vc) which explained clearly how we could get the face recognition working from the web camera, in real time.

If the code provided in the video isn’t working directly, you could try my small patches, in which I corrected a typo and extended the filename extensions towards the source file from [here](https://github.com/codingforentrepreneurs/OpenCV-Python-Series/compare/master...raden:utk-github).

<center>
  <video width="100%" controls>
    <source src="/blog/2018/10/image-recognition-tools/aufa-im-process.webm" type="video/webm">
  </video>
<caption>My daughter Aufa is joining me in this facial recognition session.</caption>
</center>

Apart from that there is also a fork [on GitHub](https://github.com/nazmiasri95/Face-Recognition) which allows us to do the real-time face recognition. For now, however, some manual work needed to be done in order to add more datasets (images of faces) if you want to use the code right away.

<center>
  <video width="100%" controls>
    <source src="/blog/2018/10/image-recognition-tools/tom-cruise.webm" type="video/webm">
  </video>
<caption>Obviously I am not Tom Cruise.</caption>
</center>

### Object Recognition

I also searched for more related software which could possibly provide an alternative to the face recognition. I found quite an interesing piece of work for object detection by using Neural Networks. It runs on a framework called [Darknet](https://pjreddie.com/darknet/). It allows us to do post-​processing object detection for still pictures and videos. It can also do real-time object recognition but requires a GPU to do it efficiently. I tried with the CPU-​only mode but I could not get a real-time result (my computer almost crashed).

#### Still image samples

<img src="/blog/2018/10/image-recognition-tools/image-2.jpg" alt="detecting boats and people at the beach" />

<img src="/blog/2018/10/image-recognition-tools/image-3.jpg" alt="detecting birds at the zoo" />

#### Video samples

<center>
  <video width="40%" controls>
    <source src="/blog/2018/10/image-recognition-tools/keteslow.webm" type="video/webm">
  </video>
<br /><caption>This video was on Lebuhraya Utara Selatan (freeway) in Malaysia</caption>
</center>

<center>
  <video width="40%" controls>
    <source src="/blog/2018/10/image-recognition-tools/keteslow2.webm" type="video/webm">
  </video>
<br /><caption>Another from Lebuhraya Utara Selatan (freeway) in Malaysia</caption>
</center>

<center>
  <video width="100%" controls>
    <source src="/blog/2018/10/image-recognition-tools/kids-bubble.webm" type="video/webm">
  </video>
<caption>Two kids playing with bubbles</caption>
</center>

<center>
  <video width="40%" controls>
    <source src="/blog/2018/10/image-recognition-tools/perhentian-swim-analyzed.webm" type="video/webm">
  </video>
<br /><caption>This video was taken a on a boat, with several people floating in the sea wearing their life jackets</caption>
</center>

<center>
  <video width="100%" controls>
    <source src="/blog/2018/10/image-recognition-tools/jalan-pantai.webm" type="video/webm">
  </video>
<caption>My kid and I walking on the beach in western Australia</caption>
</center>

<center>
  <video width="100%" controls>
    <source src="/blog/2018/10/image-recognition-tools/aufa-naik-kida-slow.webm" type="video/webm">
  </video>
<caption>Here’s a kid riding a small horse</caption>
</center>

#### Vehicle Counting and Speed Measurement

I found a tool developed by [Ahmet Ozlu](https://github.com/ahmetozlu/vehicle_counting_tensorflow) which uses TensorFlow. The use case here is vechicle counting, vehicle type and color recoginition, and speed detection.

You can see the in following video how it works.

<center>
  <video width="100%" controls>
    <source src="/blog/2018/10/image-recognition-tools/ahmet-traffic.webm" type="video/webm">
  </video>
<caption></caption>
</center>

### Libraries

#### OpenCV

[OpenCV](https://opencv.org/) is an open source library for computer vision, which comes together with libraries which we can use for our detection and recognition work.

In my understanding, the face detection will come first and the recognition second. In newer digital cameras and smartphones facial detection is quite common. Social media applications sometimes use facial recognition to suggest similar faces to be tagged in photo albums, or for photo album reorganization.

#### Tools based on or making use of OpenCV

Apart from the custom-​written Python code which uses OpenCV and Numpy, I also found out there are several works which use TensorFlow together with neural networks, called YOLO (You Look Only Once). They are:

* [darknet](https://pjreddie.com/darknet/) (written in C)
* [darkflow](https://github.com/thtrieu/darkflow) (written with Python and seems to work as a wrapper for darknet) — You need to install different dependencies from darknet, for example Cython and TensorFlow. The good thing is that we could use this tool for a video post-​processing, where instead of taking input directly from a webcam, we take it from existing videos. However, if you want to use the latest YOLO algorithm, then just stick to Darknet rather than using Darkflow. There is a fork on GitHub which could allow Darknet to save the output of the processed video into a file as well.

To rotate the video if it was taken from a smartphone but in a 180 degree position:

`ffmpeg -i sourcefile.mp4 -vf "transpose=4"  fileout.mp4`

The transpose value depends on the nature of the rotation. If it’s 90 degrees, the transpose value should be 2. It also depends on whether the rotation is clockwise or counter-​clockwise.

To convert the video to a slower framerate:

`ffmpeg -i sourcefile.avi -r 8 fileout.mp4`

For the Darkflow tool, the default output is in AVI format, but ffmpeg allows us to convert it to MP4 if you want.

#### ImageAI

[ImageAI](https://github.com/OlafenwaMoses/ImageAI) is a Python-​based computer vision library which utilizes the use of TensorFlow, Keras, Matplotlib and several other dependencies which are commonly used for machine learning. In terms of usage, it is similar to darkflow.

### Conclusion

The advancement of AI field contributes a lot of useful automation to life. It can range from helping detect tumors, helping search and rescue missions, reducing keystrokes with keyword predictions, to spam filtering. AI also accelerates the field of image processing and pattern recognition.

A lot of the hard work of smart people and scholars have produced many smart solutions to make people live a better life with the use of AI. As I have shown, some of these tools could achieve better detection given a good amount of samples to be trained on and the correct size of picture to be detected.

The tools above will work as-is, but may need some tweaking/​editing if you want to customize it. For example, some of the code works with their own demos, so you may need to pass an argument such as `sys.argv[]` inside the Python code if you want to process your own video.
