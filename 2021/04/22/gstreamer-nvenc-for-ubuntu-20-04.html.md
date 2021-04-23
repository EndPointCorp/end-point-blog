---
author: "Neil Elliott"
title: "Gstreamer Nvenc for Ubuntu 20.04"
tags: gstreamer, nvenc, nvcodec, H.264
---

Gstreamer is a library for creating media-handling components. Using gstreamer you can screencast your desktop, transcode a live stream, or write a media player application for your kiosk.

Video encoding is expensive, even with AMD's current lineup making it more palatable. Recent Nvidia Quadro and GeForce video cards include dedicated H.264 encoding and decoding hardware as a set of discrete components alongside the GPU. The hardware is used in the popular Shadowplay toolkit on Windows and available to developers through the Nvidia Video SDK on Linux.

Gstreamer includes elements as part of the “[Gstreamer Bad](https://gstreamer.freedesktop.org/modules/gst-plugins-bad.html)” plugin set that leverages the SDK without having to get your hands too dirty. The plugins are not included with gst-plugins-bad in apt, and must be compiled with supporting libs from Nvidia. Previously this required registering with Nvidia and downloading the Nvidia Video SDK, but Ubuntu recently added apt packages providing them, a big help for automation.

## Environment
* Ubuntu 20.04
* [Video card from GPU support matrix](https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new)
* [Install Gstreamer](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c#install-gstreamer-on-ubuntu-or-debian)

## CUDA
The nvenc and nvdec plugins depend on cuda 11. The apt version is too old. I’ve found the [runfile](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Debian&target_version=10&target_type=runfilelocal) to be the most reliable installation method.
Deselect the nvidia drivers when using the runfile if using the distro-maintained driver.

## Plugin
Install prerequisites from apt.

```
# apt install nvidia-driver-460 libnvidia-encode-460 libnvidia-decode-460 libdrm-dev
```

Clone gst-plugins-bad source matching distro version.

```
$ git clone --single-branch -b 1.16.2 git://anongit.freedesktop.org/gstreamer/gst-plugins-bad
$ cd gst-plugins-bad
```

Compile and install plugins.

```
$ ./autogen.sh --with-cuda-prefix="/usr/local/cuda"
$ cd sys/nvenc
$ make
# cp .libs/libgstnvenc.so /usr/lib/x86_64-linux-gnu/gstreamer-1.0/
$ cd ../nvdec
$ make
# cp .libs/libgstnvdec.so /usr/lib/x86_64-linux-gnu/gstreamer-1.0/
```

Clear Gstreamer cache and check for dependency issues using gst-inspect.

```
$ rm -r ~/.cache/gstreamer-1.0
$ gst-inspect-1.0 | grep 'nvenc\|nvdec'
nvenc:  nvh264enc: NVENC H.264 Video Encoder
nvenc:  nvh265enc: NVENC HEVC Video Encoder
nvdec:  nvdec: NVDEC video decoder
```

## Benchmark
Here is an example pipeline using the standard CPU based H.264 encoder to encode 10000 frames at 320x240.

```
$ gst-launch-1.0 videotestsrc num-buffers=10000 ! x264enc ! h264parse ! mp4mux ! filesink location=vid1.mp4
```
On my modest machine, this took around 9.6 seconds and 400% CPU.

Running the same pipeline with the nvenc element.

```
$ gst-launch-1.0 videotestsrc num-buffers=10000 ! nvh264enc ! h264parse ! mp4mux ! filesink location=vid2.mp4
```
About 2.3 seconds with 100% CPU.

## Alternatives
The apt supported version of these plugins are limited to H.264 and 4K pixels in either dimension. Features have been fleshed out upstream. Elements for the Nvidia Tegra line of MPUs provide more features, but the required hardware probably isn’t included with your workstation.

[Ffmpeg also provides hardware accelerated elements](https://trac.ffmpeg.org/wiki/HWAccelIntro), including nvcodec supported H.264 and HEVC encoders and decoders, out of the box on Ubuntu.

