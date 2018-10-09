---
author: "Muhammad Najmi bin Ahmad Zabidi"
title: "Image Recognition Tools"
tags: opencv, machine learning, deep learning, tensorflow, python
gh_issue_number: 1456
---

I always impressed with the advancement of machine learning and recently deep learning (although I also 
came across to the academic paperwork on extreme learning). However since I am not expert in the field I decided to let
the interested researchers and scholars to elaborate more on them.

In this write up I will share the existing tools (and the associated libraries to make them work, at least in my case). 

The reason I explored these tools is simple, I plan to deploy a cheap, poor's man version of security camera in my home with some "sense" of intelligence. That is consider this case: Since I am working at home, I want to know who is actually knocking my door (since my door's bell was broken). So I decided that, what if I could use a web cam to monitor my door and let me know who actually standing at the door?


### Face Detection
I searched around for the existing works which regards to the face detection and I found [this work](https://github.com/shantnu/FaceDetect/blob/master/face_detect.py). It uses [Haarcascade](https://github.com/opencv/opencv/tree/master/data/haarcascades). So I was then able to detect faces, but then upon sharing the "findings" with a friend he then said this is just a "face detection", but how does the computer would be able to recognize who's who? Then I stumbled upon the phrase "face recognition" (in which I believe should be the next sequence).

You might noticed that if you use the image file that you import directly from your smartphone then the output will be displayed in a large file to the screen. You can use the ImageMagick program in Linux to resize the file to say, 640x480 format.

```bash
$ file makan.jpg
makan.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=15, height=3120, bps=0, width=4160], baseline, precision 8, 4160x3120, frames 3

$ convert makan.jpg -resize 640x480 makan-small.jpg

$ file makan-small.jpg 
makan-small.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=15, height=3120, bps=0, width=4160], baseline, precision 8, 640x480, frames 3
```

![](../image-recognition-tools/makan-small.jpg)

![](../image-recognition-tools/aufa-detect.jpg)

#### Machine Vision
Computer doesn't see the image directly as the humans are as we need to convert the images into the numerical values. For example in of the facial regcognition tools, the training file contains the following matrices:

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
I continued my search for the existing works on face recognition and found several works which could be tested right away (with some modifications from the original source codes). There is one [tutorial](https://www.youtube.com/watch?v=PmZ29Vta7Vc) in YouTube which explained clearly how we could get the face recognition worksfrom the web camera (real time). 
If the codes provided in the video  isn't working directly, you could use my small patches, in which I corrected out a typo and extend the filename extensions towards the source file from [here](https://github.com/codingforentrepreneurs/OpenCV-Python-Series/compare/master...raden:utk-github)


<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/aufa-im-process.mp4" type="video/mp4">
  </video>
<caption>My kid Aufa is joining me on the facial recognition session</caption>
</center>

 Apart from that there is also a forked work [in Github](https://github.com/nazmiasri95/Face-Recognition) in which could allow us to do the real time face recognition. For latter however, some manual works needeed to be done in order to add more datasets (person's face images) if you want to use the code right away. 


<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/tom-cruise.mp4" type="video/mp4">
  </video>
<caption>Obviously I am not Tom Cruise</caption>
</center>


### Object Recognition
I also searched more related works which could possibly provides an alternative to the face recognition. However turns out I found a quite interesing piece of work for objection detection by using Neural Network. The work is running on a framework called as [Darknet](https://pjreddie.com/darknet/). It allows us to do post-processing objection detection for still pictures and videos. It also able to do real time object recognition but requires GPUs to allow us to make it happened efficiently. I tried with the CPU only mode but I could not get a real time result (my computer almost freezed). 

#### Still images' samples
![](../image-recognition-tools/bot.jpg)


![](../image-recognition-tools/burung-zoo.jpg)


#### Video samples
<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/keteslow.mp4" type="video/mp4">
  </video>
<caption>This video was on Lebuhraya Utara Selatan (Freeway) in Malaysia</caption>
</center>

<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/keteslow2.mp4" type="video/mp4">
  </video>
<caption>This is another video which was on Lebuhraya Utara Selatan (Freeway) in Malaysia</caption>
</center>

<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/kids-bubble.mp4" type="video/mp4">
  </video>
<caption>Two kids in the playground playing water bubbles</caption>
</center>

<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/perhentian-swim-analyzed-slow.mp4" type="video/mp4">
  </video>
<caption>This video was taken a on a boat, with several people floating in the sea wearing their life jackets</caption>
</center>

<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/jalan-pantai.mp4" type="video/mp4">
  </video>
<caption>This is my kid and I, walking on the beach in Western Australia</caption>
</center>

<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/aufa-naik-kuda-slow.mp4" type="video/mp4">
  </video>
<caption>This is a video a kid, riding small horse</caption>
</center>

##### Vehicle Counting and Speed Measurement
I found a tool developed by [Ahmet Ozlu](https://github.com/ahmetozlu/vehicle_counting_tensorflow) which uses Tensorflow. In this case the use case are vechicle counting, vehicle type and color recoginition and speed detection.

You can see the following video on how it works.

<center>
  <video width="100%" controls poster="poster.png">
    <source src="../image-recognition-tools/ahmet-traffic.mp4" type="video/mp4">
  </video>
<caption>This is a video a kid, riding small horse</caption>
</center>

### Libraries

#### OpenCV
[OpenCV](https://opencv.org/) is an open source library for computer vision, in which it comes together with libraries which we could use for our detection and recognition work.

In my understanding, the face detection will come first and subsequently with the recognition. In the latest development of the digital cameras and smartphones the features of facial detection is quite common to be found. Socmed (Social Media) applications sometimes use facial recognition too in order to suggest the potential similar faces to be tagged in the photo albums (or for photo album reorganization). 

#### Tools based/making use of OpenCV

Apart from the custom-written Python codes which use OpenCV and Numpy, I also found out there are several works which use Tensorflow together with Neural Networks-related algorithm, called as Yolo (You Look Only Once). They are:

* [darknet](https://pjreddie.com/darknet/) (written in C language)
* [darkflow](https://github.com/thtrieu/darkflow) (written with Python and seems work as a wrapper for darknet)
** You need to install different depedencies as compared to darknet, for example Cython and Tensorflow. The good thing is that we could use this tool for a video post-processing (in which we do not need to
take in input directly from a webcam, rather from existing videos). However if you want to use the latest Yolo algorithm, then just stick to Darknet rather than using Darkflow. There is a fork in github which could allow Darknet to save the output of the processed video into a file as well. 

To rotate the video if it was taken from a smartphone but in a 180 degree position:

`ffmpeg -i sourcefile.mp4 -vf "transpose=4"  fileout.mp4`

The transpose value is depending on the nature of the rotation. If let us say it is 90 degrees - then the transpose value should be 2. In which it also depends on the nature of the rotation whether it is a clockwise or anti-clockwise.

To convert the video in a slow frame per second (FPS):

` ffmpeg -i sourcefile.avi -r 8 fileout.mp4`

(for the Darkflow tool, the default output is in AVI format, but ffmpeg allow us to convert it to MP4, you can also maintain the format to AVI if you want)


#### ImageAI
[ImageAI](https://github.com/OlafenwaMoses/ImageAI) is a Python based computer vision library which utilizes the use of Tensorflow, Keras, Matplotlib and several other dependencies which are commonly being used for machine learning. In term of the usage, it is similar as darkflow.

### Conclusion
The advancement of the field of Artificial Intelligence (AI) contributes a lot of useful automation to the human lives. Ranged from helping detecting tumor, search and rescue mission, reducing keystrokes with keyword predictions up to the use of anti spam. AI also accelerates the field of image processing and pattern recognition. A lot of the hard works of smart people and scholars produced many smart solutions to make people live a better life with the use of AI. As what I have shown from the existing tools, some of these tools could achieve better detection give a good amout of samples to be trained and the correct size of picture to be detected. 

In term of the usability, the provided tools above will work as is (and may need some tweaking/editing if you want to customize it, for example some of the codes works with their own demo, so you may need to pass an argument for e.g `sys.argv[]` inside the Python code if you want to process your own video). 
